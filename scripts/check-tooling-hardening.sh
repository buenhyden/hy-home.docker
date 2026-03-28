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

registry_compose="infra/09-tooling/registry/docker-compose.yml"
sonarqube_compose="infra/09-tooling/sonarqube/docker-compose.yml"
terrakube_compose="infra/09-tooling/terrakube/docker-compose.yml"
syncthing_compose="infra/09-tooling/syncthing/docker-compose.yml"
locust_compose="infra/09-tooling/locust/docker-compose.yml"
k6_compose="infra/09-tooling/k6/docker-compose.yml"
terraform_compose="infra/09-tooling/terraform/docker-compose.yml"

spec_file="docs/04.specs/09-tooling/spec.md"
guide_file="docs/07.guides/09-tooling/optimization-hardening.md"
ops_file="docs/08.operations/09-tooling/optimization-hardening.md"
runbook_file="docs/09.runbooks/09-tooling/optimization-hardening.md"
plan_file="docs/05.plans/2026-03-28-09-tooling-optimization-hardening-plan.md"
task_file="docs/06.tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md"
prd_file="docs/01.prd/2026-03-28-09-tooling-optimization-hardening.md"
ard_file="docs/02.ard/0024-tooling-optimization-hardening-architecture.md"
adr_file="docs/03.adr/0024-tooling-hardening-and-ha-expansion-strategy.md"

check_file "$registry_compose" || true
check_file "$sonarqube_compose" || true
check_file "$terrakube_compose" || true
check_file "$syncthing_compose" || true
check_file "$locust_compose" || true
check_file "$k6_compose" || true
check_file "$terraform_compose" || true

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
  # Gateway + SSO chain enforcement on exposed tooling UIs.
  check_contains "$sonarqube_compose" "traefik.http.routers.sonarqube.middlewares: gateway-standard-chain@file,sso-errors@file,sso-auth@file" "sonarqube middleware chain mismatch"
  check_contains "$terrakube_compose" "traefik.http.routers.terrakube-api.middlewares: gateway-standard-chain@file,sso-errors@file,sso-auth@file" "terrakube-api middleware chain mismatch"
  check_contains "$terrakube_compose" "traefik.http.routers.terrakube-ui.middlewares: gateway-standard-chain@file,sso-errors@file,sso-auth@file" "terrakube-ui middleware chain mismatch"
  check_contains "$terrakube_compose" "traefik.http.routers.terrakube-executor.middlewares: gateway-standard-chain@file,sso-errors@file,sso-auth@file" "terrakube-executor middleware chain mismatch"
  check_contains "$syncthing_compose" "traefik.http.routers.syncthing.middlewares: gateway-standard-chain@file,sso-errors@file,sso-auth@file" "syncthing middleware chain mismatch"

  # Network isolation contract.
  check_contains "$registry_compose" "networks:" "registry networks block missing"
  check_contains "$registry_compose" "infra_net:" "registry infra_net declaration missing"
  check_contains "$registry_compose" "external: true" "registry infra_net external contract missing"
  check_contains "$sonarqube_compose" "infra_net:" "sonarqube infra_net declaration missing"
  check_contains "$terrakube_compose" "infra_net:" "terrakube infra_net declaration missing"
  check_contains "$syncthing_compose" "infra_net:" "syncthing infra_net declaration missing"
  check_contains "$locust_compose" "infra_net:" "locust infra_net declaration missing"
  check_contains "$k6_compose" "infra_net:" "k6 infra_net declaration missing"
  check_contains "$terraform_compose" "infra_net:" "terraform infra_net declaration missing"

  # Health/runtime hardening contracts.
  check_contains "$locust_compose" "pgrep -f \\\"locust.*--worker\\\"" "locust-worker healthcheck contract missing"
  check_contains "$k6_compose" "- k6-data:/mnt/locust:rw" "k6 volume contract mismatch"

  # Spec traceability checks for optimization-hardening set.
  check_contains "$spec_file" "../../01.prd/2026-03-28-09-tooling-optimization-hardening.md" "spec missing PRD trace link"
  check_contains "$spec_file" "../../02.ard/0024-tooling-optimization-hardening-architecture.md" "spec missing ARD trace link"
  check_contains "$spec_file" "../../03.adr/0024-tooling-hardening-and-ha-expansion-strategy.md" "spec missing ADR trace link"
  check_contains "$spec_file" "../../05.plans/2026-03-28-09-tooling-optimization-hardening-plan.md" "spec missing Plan trace link"
  check_contains "$spec_file" "../../06.tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md" "spec missing Task trace link"
  check_contains "$spec_file" "../../07.guides/09-tooling/optimization-hardening.md" "spec missing Guide trace link"
  check_contains "$spec_file" "../../08.operations/09-tooling/optimization-hardening.md" "spec missing Operations trace link"
  check_contains "$spec_file" "../../09.runbooks/09-tooling/optimization-hardening.md" "spec missing Runbook trace link"
fi

echo "Tooling hardening check"
echo "failures=$failures"

if [[ "$failures" -gt 0 ]]; then
  exit 1
fi

echo "PASS: 09-tooling hardening baseline enforced"
