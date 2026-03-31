#!/usr/bin/env bash
set -euo pipefail

failures=0

fail() {
  echo "FAIL: $1"
  failures=$((failures + 1))
}

check_file() {
  local file="$1"
  if [[ ! -f "$file" ]]; then
    fail "missing file: $file"
    return 1
  fi
  return 0
}

check_contains() {
  local file="$1"
  local pattern="$2"
  local label="$3"
  if ! grep -Fq -- "$pattern" "$file"; then
    fail "$label (file: $file, expected: $pattern)"
  fi
}

ollama_compose="infra/08-ai/ollama/docker-compose.yml"
webui_compose="infra/08-ai/open-webui/docker-compose.yml"

spec_file="docs/04.specs/08-ai/spec.md"
guide_file="docs/07.guides/08-ai/optimization-hardening.md"
ops_file="docs/08.operations/08-ai/optimization-hardening.md"
runbook_file="docs/09.runbooks/08-ai/optimization-hardening.md"
plan_file="docs/05.plans/2026-03-28-08-ai-optimization-hardening-plan.md"
task_file="docs/06.tasks/2026-03-28-08-ai-optimization-hardening-tasks.md"
prd_file="docs/01.prd/2026-03-28-08-ai-optimization-hardening.md"
ard_file="docs/02.ard/0023-ai-optimization-hardening-architecture.md"
adr_file="docs/03.adr/0023-ai-hardening-and-ha-expansion-strategy.md"

check_file "$ollama_compose" || true
check_file "$webui_compose" || true

check_file "$spec_file" || true
check_file "$guide_file" || true
check_file "$ops_file" || true
check_file "$runbook_file" || true
check_file "$plan_file" || true
check_file "$task_file" || true
check_file "$prd_file" || true
check_file "$ard_file" || true
check_file "$adr_file" || true

if [[ "$failures" -eq 0 ]]; then
  # Ollama gateway and runtime contracts.
  check_contains "$ollama_compose" "traefik.http.routers.ollama.middlewares: gateway-standard-chain@file,sso-errors@file,sso-auth@file" "ollama middleware chain mismatch"
  check_contains "$ollama_compose" "OLLAMA_NUM_PARALLEL=" "ollama parallel cap missing"
  check_contains "$ollama_compose" "OLLAMA_MAX_LOADED_MODELS=" "ollama loaded model cap missing"
  check_contains "$ollama_compose" "OLLAMA_MAX_QUEUE=" "ollama queue cap missing"
  check_contains "$ollama_compose" "depends_on:" "ollama-exporter dependency contract missing"
  check_contains "$ollama_compose" "condition: service_healthy" "ollama-exporter health dependency missing"
  check_contains "$ollama_compose" 'http://localhost:${OLLAMA_EXPORTER_PORT:-8000}/metrics' "ollama-exporter healthcheck missing"
  check_contains "$ollama_compose" "networks:" "ollama compose networks block missing"
  check_contains "$ollama_compose" "infra_net:" "ollama compose infra_net declaration missing"
  check_contains "$ollama_compose" "external: true" "ollama compose infra_net external contract missing"

  # Open WebUI gateway and persistence contracts.
  check_contains "$webui_compose" "service: template-stateful-med" "open-webui should use stateful template"
  check_contains "$webui_compose" "traefik.http.routers.open-webui.middlewares: gateway-standard-chain@file,sso-errors@file,sso-auth@file" "open-webui middleware chain mismatch"
  check_contains "$webui_compose" "depends_on:" "open-webui dependency contract missing"
  check_contains "$webui_compose" "condition: service_healthy" "open-webui ollama dependency should be health-gated"
  check_contains "$webui_compose" "networks:" "open-webui compose networks block missing"
  check_contains "$webui_compose" "infra_net:" "open-webui compose infra_net declaration missing"
  check_contains "$webui_compose" "external: true" "open-webui compose infra_net external contract missing"

  # Spec traceability checks for optimization-hardening set.
  check_contains "$spec_file" "../../01.prd/2026-03-28-08-ai-optimization-hardening.md" "spec missing PRD trace link"
  check_contains "$spec_file" "../../02.ard/0023-ai-optimization-hardening-architecture.md" "spec missing ARD trace link"
  check_contains "$spec_file" "../../03.adr/0023-ai-hardening-and-ha-expansion-strategy.md" "spec missing ADR trace link"
  check_contains "$spec_file" "../../05.plans/2026-03-28-08-ai-optimization-hardening-plan.md" "spec missing Plan trace link"
  check_contains "$spec_file" "../../06.tasks/2026-03-28-08-ai-optimization-hardening-tasks.md" "spec missing Task trace link"
  check_contains "$spec_file" "../../07.guides/08-ai/optimization-hardening.md" "spec missing Guide trace link"
  check_contains "$spec_file" "../../08.operations/08-ai/optimization-hardening.md" "spec missing Operations trace link"
  check_contains "$spec_file" "../../09.runbooks/08-ai/optimization-hardening.md" "spec missing Runbook trace link"
fi

echo "AI hardening check"
echo "failures=$failures"

if [[ "$failures" -gt 0 ]]; then
  exit 1
fi

echo "PASS: 08-ai hardening baseline enforced"
