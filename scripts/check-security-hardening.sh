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

compose_file="infra/03-security/vault/docker-compose.yml"
agent_hcl="infra/03-security/vault/config/vault-agent.hcl"
spec_file="docs/04.specs/03-security/spec.md"
guide_file="docs/07.guides/03-security/vault.md"
ops_file="docs/08.operations/03-security/vault.md"
runbook_file="docs/09.runbooks/03-security/vault.md"
plan_file="docs/05.plans/2026-03-28-03-security-optimization-hardening-plan.md"
task_file="docs/06.tasks/2026-03-28-03-security-optimization-hardening-tasks.md"
prd_file="docs/01.prd/2026-03-28-03-security-optimization-hardening.md"
ard_file="docs/02.ard/0018-security-optimization-hardening-architecture.md"
adr_file="docs/03.adr/0018-vault-hardening-and-ha-expansion-strategy.md"

check_file "$compose_file" || true
check_file "$agent_hcl" || true
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
  check_contains "$compose_file" "service: template-stateful-med" "vault compose template inheritance missing"
  check_contains "$compose_file" "vault-agent-out" "vault-agent output volume missing"
  check_contains "$compose_file" "/vault/out" "vault-agent output mount missing"
  check_contains "$compose_file" "vault-agent:" "vault-agent service missing"
  check_contains "$compose_file" "healthcheck:" "healthcheck block missing"
  check_contains "$compose_file" "pgrep -f" "vault-agent pid healthcheck contract missing"
  check_contains "$compose_file" "exit 1" "vault-agent process liveness check missing"

  if ! awk '
    /^  vault-agent:/ {in_agent=1; next}
    /^  [a-zA-Z0-9_-]+:/ && in_agent {in_agent=0}
    in_agent {print}
  ' "$compose_file" | grep -Fq "healthcheck:"; then
    fail "vault-agent healthcheck missing in vault-agent service block"
  fi

  mapfile -t sources < <(grep -E '^\s*source\s*=' "$agent_hcl" | awk -F'"' '{print $2}')
  mapfile -t destinations < <(grep -E '^\s*destination\s*=' "$agent_hcl" | awk -F'"' '{print $2}')

  if [[ "${#sources[@]}" -eq 0 ]]; then
    fail "vault-agent template source entries missing"
  fi

  if [[ "${#sources[@]}" -ne "${#destinations[@]}" ]]; then
    fail "vault-agent template source/destination count mismatch"
  fi

  for src in "${sources[@]}"; do
    if [[ "$src" != /vault/config/templates/* ]]; then
      fail "invalid vault-agent template source path: $src"
      continue
    fi
    src_file="infra/03-security/vault/config/templates/$(basename "$src")"
    if [[ ! -f "$src_file" ]]; then
      fail "template source file not found: $src_file"
    fi
  done

  for dst in "${destinations[@]}"; do
    if [[ "$dst" != /vault/out/* ]]; then
      fail "invalid vault-agent template destination path: $dst"
    fi
  done

  for ctmpl in infra/03-security/vault/config/templates/*.ctmpl; do
    if grep -Fq 'secret/data/example' "$ctmpl"; then
      fail "placeholder secret path still exists: $ctmpl"
    fi
  done

  # Traceability links in spec document
  check_contains "$spec_file" "../../01.prd/2026-03-28-03-security-optimization-hardening.md" "spec missing PRD trace link"
  check_contains "$spec_file" "../../02.ard/0018-security-optimization-hardening-architecture.md" "spec missing ARD trace link"
  check_contains "$spec_file" "../../03.adr/0018-vault-hardening-and-ha-expansion-strategy.md" "spec missing ADR trace link"
  check_contains "$spec_file" "../../05.plans/2026-03-28-03-security-optimization-hardening-plan.md" "spec missing Plan trace link"
  check_contains "$spec_file" "../../06.tasks/2026-03-28-03-security-optimization-hardening-tasks.md" "spec missing Task trace link"
  check_contains "$spec_file" "../../07.guides/03-security/vault.md" "spec missing Guide trace link"
  check_contains "$spec_file" "../../08.operations/03-security/vault.md" "spec missing Operations trace link"
  check_contains "$spec_file" "../../09.runbooks/03-security/vault.md" "spec missing Runbook trace link"
fi

echo "Security hardening check"
echo "failures=$failures"

if [[ "$failures" -gt 0 ]]; then
  exit 1
fi

echo "PASS: 03-security hardening baseline enforced"
