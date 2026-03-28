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

airflow_compose="infra/07-workflow/airflow/docker-compose.yml"
n8n_compose="infra/07-workflow/n8n/docker-compose.yml"
n8n_dockerfile="infra/07-workflow/n8n/Dockerfile"
n8n_entrypoint="infra/07-workflow/n8n/docker-entrypoint.sh"

spec_file="docs/04.specs/07-workflow/spec.md"
guide_file="docs/07.guides/07-workflow/optimization-hardening.md"
ops_file="docs/08.operations/07-workflow/optimization-hardening.md"
runbook_file="docs/09.runbooks/07-workflow/optimization-hardening.md"
plan_file="docs/05.plans/2026-03-28-07-workflow-optimization-hardening-plan.md"
task_file="docs/06.tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md"
prd_file="docs/01.prd/2026-03-28-07-workflow-optimization-hardening.md"
ard_file="docs/02.ard/0022-workflow-optimization-hardening-architecture.md"
adr_file="docs/03.adr/0022-workflow-hardening-and-ha-expansion-strategy.md"

check_file "$airflow_compose" || true
check_file "$n8n_compose" || true
check_file "$n8n_dockerfile" || true
check_file "$n8n_entrypoint" || true

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
  # Airflow gateway/SSO contract.
  check_contains "$airflow_compose" "traefik.http.routers.airflow.middlewares: gateway-standard-chain@file,sso-errors@file,sso-auth@file" "airflow middleware chain mismatch"
  check_contains "$airflow_compose" "traefik.http.routers.flower.middlewares: gateway-standard-chain@file,sso-errors@file,sso-auth@file" "flower middleware chain mismatch"

  # Airflow health-gated startup contract.
  check_contains "$airflow_compose" "airflow-valkey:" "airflow valkey service missing"
  check_contains "$airflow_compose" "airflow-valkey:" "airflow valkey dependency contract missing"
  check_contains "$airflow_compose" "condition: service_healthy" "airflow health-gated dependency contract missing"

  # n8n gateway/SSO + runtime hardening contract.
  check_contains "$n8n_compose" "traefik.http.routers.n8n.middlewares: gateway-standard-chain@file,sso-errors@file,sso-auth@file" "n8n middleware chain mismatch"
  check_contains "$n8n_compose" "image: hyhome/n8n:2.12.3-local" "n8n custom image pin missing"
  check_contains "$n8n_compose" "test: ['CMD-SHELL', 'ps -ef | grep -q \"[n]8n worker\"']" "n8n-worker healthcheck missing"
  check_contains "$n8n_compose" "n8n-task-runner" "n8n-task-runner service missing"
  check_contains "$n8n_compose" "test: ['CMD-SHELL', 'ps -ef | grep -q \"[n]ode\" && test -s /run/secrets/n8n_runner_auth_token']" "n8n-task-runner healthcheck missing"
  check_contains "$n8n_compose" "n8n: { condition: service_healthy }" "n8n-task-runner dependency on n8n health missing"
  check_contains "$n8n_compose" "n8n-valkey: { condition: service_healthy }" "n8n-task-runner dependency on valkey health missing"

  # n8n image and entrypoint contract.
  check_contains "$n8n_dockerfile" "FROM alpine:3.21 AS font-builder" "n8n multi-stage builder missing"
  check_contains "$n8n_dockerfile" "USER node" "n8n Dockerfile non-root runtime missing"
  check_contains "$n8n_dockerfile" "ENTRYPOINT [\"./docker-entrypoint.sh\"]" "n8n custom entrypoint not configured"
  check_contains "$n8n_entrypoint" "require_secret /run/secrets/n8n_db_password" "n8n entrypoint db secret guard missing"
  check_contains "$n8n_entrypoint" "require_secret /run/secrets/n8n_valkey_password" "n8n entrypoint valkey secret guard missing"
  check_contains "$n8n_entrypoint" "require_secret /run/secrets/n8n_encryption_key" "n8n entrypoint encryption secret guard missing"
  check_contains "$n8n_entrypoint" "require_secret /run/secrets/n8n_runner_auth_token" "n8n entrypoint runner secret guard missing"

  # Spec traceability checks for optimization-hardening set.
  check_contains "$spec_file" "../../01.prd/2026-03-28-07-workflow-optimization-hardening.md" "spec missing PRD trace link"
  check_contains "$spec_file" "../../02.ard/0022-workflow-optimization-hardening-architecture.md" "spec missing ARD trace link"
  check_contains "$spec_file" "../../03.adr/0022-workflow-hardening-and-ha-expansion-strategy.md" "spec missing ADR trace link"
  check_contains "$spec_file" "../../05.plans/2026-03-28-07-workflow-optimization-hardening-plan.md" "spec missing Plan trace link"
  check_contains "$spec_file" "../../06.tasks/2026-03-28-07-workflow-optimization-hardening-tasks.md" "spec missing Task trace link"
  check_contains "$spec_file" "../../07.guides/07-workflow/optimization-hardening.md" "spec missing Guide trace link"
  check_contains "$spec_file" "../../08.operations/07-workflow/optimization-hardening.md" "spec missing Operations trace link"
  check_contains "$spec_file" "../../09.runbooks/07-workflow/optimization-hardening.md" "spec missing Runbook trace link"
fi

echo "Workflow hardening check"
echo "failures=$failures"

if [[ "$failures" -gt 0 ]]; then
  exit 1
fi

echo "PASS: 07-workflow hardening baseline enforced"
