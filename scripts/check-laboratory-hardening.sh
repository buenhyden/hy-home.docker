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

dashboard_compose="infra/11-laboratory/dashboard/docker-compose.yml"
dozzle_compose="infra/11-laboratory/dozzle/docker-compose.yml"
portainer_compose="infra/11-laboratory/portainer/docker-compose.yml"
redisinsight_compose="infra/11-laboratory/redisinsight/docker-compose.yml"

spec_file="docs/04.specs/11-laboratory/spec.md"
guide_file="docs/07.guides/11-laboratory/optimization-hardening.md"
ops_file="docs/08.operations/11-laboratory/optimization-hardening.md"
runbook_file="docs/09.runbooks/11-laboratory/optimization-hardening.md"
plan_file="docs/05.plans/2026-03-28-11-laboratory-optimization-hardening-plan.md"
task_file="docs/06.tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md"
prd_file="docs/01.prd/2026-03-28-11-laboratory-optimization-hardening.md"
ard_file="docs/02.ard/0025-laboratory-optimization-hardening-architecture.md"
adr_file="docs/03.adr/0025-laboratory-hardening-and-ha-expansion-strategy.md"

check_file "$dashboard_compose" || true
check_file "$dozzle_compose" || true
check_file "$portainer_compose" || true
check_file "$redisinsight_compose" || true

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
  # Gateway + SSO + IP allowlist chain enforcement.
  check_contains "$dashboard_compose" "traefik.http.routers.homer.middlewares: gateway-standard-chain@file,homer-admin-ip@docker,sso-errors@file,sso-auth@file" "homer middleware chain mismatch"
  check_contains "$dozzle_compose" "traefik.http.routers.dozzle.middlewares: gateway-standard-chain@file,dozzle-admin-ip@docker,sso-errors@file,sso-auth@file" "dozzle middleware chain mismatch"
  check_contains "$portainer_compose" "traefik.http.routers.portainer.middlewares: gateway-standard-chain@file,portainer-admin-ip@docker,sso-errors@file,sso-auth@file" "portainer middleware chain mismatch"
  check_contains "$redisinsight_compose" "traefik.http.routers.redisinsight.middlewares: gateway-standard-chain@file,redisinsight-admin-ip@docker,sso-errors@file,sso-auth@file" "redisinsight middleware chain mismatch"

  # Network boundary contract.
  check_contains "$dashboard_compose" "infra_net:" "dashboard infra_net declaration missing"
  check_contains "$dashboard_compose" "external: true" "dashboard infra_net external contract missing"
  check_contains "$dozzle_compose" "infra_net:" "dozzle infra_net declaration missing"
  check_contains "$dozzle_compose" "external: true" "dozzle infra_net external contract missing"
  check_contains "$portainer_compose" "infra_net:" "portainer infra_net declaration missing"
  check_contains "$portainer_compose" "external: true" "portainer infra_net external contract missing"
  check_contains "$redisinsight_compose" "infra_net:" "redisinsight infra_net declaration missing"
  check_contains "$redisinsight_compose" "external: true" "redisinsight infra_net external contract missing"

  # Laboratory-specific hardening contracts.
  check_contains "$dashboard_compose" "expose:" "dashboard should expose internal port only"
  check_contains "$dashboard_compose" "- \${HOMER_PORT:-8080}" "dashboard expose contract missing"
  if grep -Fq -- "ports:" "$dashboard_compose"; then
    fail "dashboard direct host ports exposure should be removed"
  fi
  check_contains "$dozzle_compose" "- /var/run/docker.sock:/var/run/docker.sock:ro" "dozzle docker.sock should be read-only"

  # Spec traceability checks for optimization-hardening set.
  check_contains "$spec_file" "../../01.prd/2026-03-28-11-laboratory-optimization-hardening.md" "spec missing PRD trace link"
  check_contains "$spec_file" "../../02.ard/0025-laboratory-optimization-hardening-architecture.md" "spec missing ARD trace link"
  check_contains "$spec_file" "../../03.adr/0025-laboratory-hardening-and-ha-expansion-strategy.md" "spec missing ADR trace link"
  check_contains "$spec_file" "../../05.plans/2026-03-28-11-laboratory-optimization-hardening-plan.md" "spec missing Plan trace link"
  check_contains "$spec_file" "../../06.tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md" "spec missing Task trace link"
  check_contains "$spec_file" "../../07.guides/11-laboratory/optimization-hardening.md" "spec missing Guide trace link"
  check_contains "$spec_file" "../../08.operations/11-laboratory/optimization-hardening.md" "spec missing Operations trace link"
  check_contains "$spec_file" "../../09.runbooks/11-laboratory/optimization-hardening.md" "spec missing Runbook trace link"
fi

echo "Laboratory hardening check"
echo "failures=$failures"

if [[ "$failures" -gt 0 ]]; then
  exit 1
fi

echo "PASS: 11-laboratory hardening baseline enforced"
