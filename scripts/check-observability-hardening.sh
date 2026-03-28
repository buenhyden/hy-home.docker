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

compose_file="infra/06-observability/docker-compose.yml"

spec_file="docs/04.specs/06-observability/spec.md"
guide_file="docs/07.guides/06-observability/optimization-hardening.md"
ops_file="docs/08.operations/06-observability/optimization-hardening.md"
runbook_file="docs/09.runbooks/06-observability/optimization-hardening.md"
plan_file="docs/05.plans/2026-03-28-06-observability-optimization-hardening-plan.md"
task_file="docs/06.tasks/2026-03-28-06-observability-optimization-hardening-tasks.md"
prd_file="docs/01.prd/2026-03-28-06-observability-optimization-hardening.md"
ard_file="docs/02.ard/0021-observability-optimization-hardening-architecture.md"
adr_file="docs/03.adr/0021-observability-hardening-and-ha-expansion-strategy.md"

check_file "$compose_file" || true
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
  # Gateway middleware standard + SSO enforcement.
  check_contains "$compose_file" "traefik.http.routers.prometheus.middlewares: gateway-standard-chain@file,sso-errors@file,sso-auth@file" "prometheus middleware chain mismatch"
  check_contains "$compose_file" "traefik.http.routers.alloy.middlewares: gateway-standard-chain@file,sso-errors@file,sso-auth@file" "alloy middleware chain mismatch"
  check_contains "$compose_file" "traefik.http.routers.grafana.middlewares: gateway-standard-chain@file,sso-errors@file,sso-auth@file" "grafana middleware chain mismatch"
  check_contains "$compose_file" "traefik.http.routers.alertmanager.middlewares: gateway-standard-chain@file,sso-errors@file,sso-auth@file" "alertmanager middleware chain mismatch"
  check_contains "$compose_file" "traefik.http.routers.pushgateway.middlewares: gateway-standard-chain@file,sso-errors@file,sso-auth@file" "pushgateway middleware chain mismatch"

  # Newly routed observability endpoints.
  check_contains "$compose_file" 'traefik.http.routers.loki.rule: Host(`loki.${DEFAULT_URL}`)' "loki router rule missing"
  check_contains "$compose_file" 'traefik.http.routers.tempo.rule: Host(`tempo.${DEFAULT_URL}`)' "tempo router rule missing"
  check_contains "$compose_file" 'traefik.http.routers.pyroscope.rule: Host(`pyroscope.${DEFAULT_URL}`)' "pyroscope router rule missing"

  # Health-based dependency and host-observer hardening.
  check_contains "$compose_file" "loki:" "compose missing loki block"
  check_contains "$compose_file" "tempo:" "compose missing tempo block"
  check_contains "$compose_file" "condition: service_healthy" "service_healthy dependency contract missing"
  check_contains "$compose_file" 'http://localhost:${CADVISOR_PORT:-8080}/healthz' "cadvisor healthcheck missing"

  # Container hardening checks for custom images.
  check_contains "infra/06-observability/loki/Dockerfile" "USER 10001:10001" "loki Dockerfile non-root user missing"
  check_contains "infra/06-observability/tempo/Dockerfile" "USER 10001:10001" "tempo Dockerfile non-root user missing"
  check_contains "infra/06-observability/loki/docker-entrypoint.sh" "missing secret: /run/secrets/minio_app_user_password" "loki entrypoint secret guard missing"
  check_contains "infra/06-observability/tempo/docker-entrypoint.sh" "missing secret: /run/secrets/minio_app_user_password" "tempo entrypoint secret guard missing"

  # Spec traceability checks for optimization-hardening set.
  check_contains "$spec_file" "../../01.prd/2026-03-28-06-observability-optimization-hardening.md" "spec missing PRD trace link"
  check_contains "$spec_file" "../../02.ard/0021-observability-optimization-hardening-architecture.md" "spec missing ARD trace link"
  check_contains "$spec_file" "../../03.adr/0021-observability-hardening-and-ha-expansion-strategy.md" "spec missing ADR trace link"
  check_contains "$spec_file" "../../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md" "spec missing Plan trace link"
  check_contains "$spec_file" "../../06.tasks/2026-03-28-06-observability-optimization-hardening-tasks.md" "spec missing Task trace link"
  check_contains "$spec_file" "../../07.guides/06-observability/optimization-hardening.md" "spec missing Guide trace link"
  check_contains "$spec_file" "../../08.operations/06-observability/optimization-hardening.md" "spec missing Operations trace link"
  check_contains "$spec_file" "../../09.runbooks/06-observability/optimization-hardening.md" "spec missing Runbook trace link"
fi

echo "Observability hardening check"
echo "failures=$failures"

if [[ "$failures" -gt 0 ]]; then
  exit 1
fi

echo "PASS: 06-observability hardening baseline enforced"
