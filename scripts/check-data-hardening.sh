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

check_not_contains() {
  local file="$1"
  local pattern="$2"
  local label="$3"
  if grep -Fq -- "$pattern" "$file"; then
    fail "$label (file: $file, forbidden: $pattern)"
  fi
}

check_service_healthcheck() {
  local compose_file="$1"
  local service_name="$2"

  local block
  block="$(
    awk -v svc="$service_name" '
      BEGIN { in_svc = 0; pat = "^  " svc ":" }
      $0 ~ pat { in_svc = 1; next }
      /^  [A-Za-z0-9_.-]+:/ && in_svc { in_svc = 0 }
      in_svc { print }
    ' "$compose_file"
  )"

  if [[ -z "$block" ]]; then
    fail "service block not found: $service_name (file: $compose_file)"
    return
  fi

  if ! grep -Fq "healthcheck:" <<<"$block"; then
    fail "healthcheck missing in service block: $service_name (file: $compose_file)"
  fi
}

supabase_compose="infra/04-data/operational/supabase/docker-compose.yml"
valkey_compose="infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml"
seaweed_compose="infra/04-data/lake-and-object/seaweedfs/docker-compose.yml"
ksql_compose="infra/04-data/analytics/ksql/docker-compose.yml"

spec_file="docs/04.specs/04-data/spec.md"
guide_file="docs/07.guides/04-data/optimization-hardening.md"
ops_file="docs/08.operations/04-data/optimization-hardening.md"
runbook_file="docs/09.runbooks/04-data/optimization-hardening.md"
plan_file="docs/05.plans/2026-03-28-04-data-optimization-hardening-plan.md"
task_file="docs/06.tasks/2026-03-28-04-data-optimization-hardening-tasks.md"
prd_file="docs/01.prd/2026-03-28-04-data-optimization-hardening.md"
ard_file="docs/02.ard/0019-data-optimization-hardening-architecture.md"
adr_file="docs/03.adr/0019-04-data-hardening-and-ha-expansion-strategy.md"

check_file "$supabase_compose" || true
check_file "$valkey_compose" || true
check_file "$seaweed_compose" || true
check_file "$ksql_compose" || true
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
  check_contains "$supabase_compose" "file: ../../../common-optimizations.yml" "supabase template inheritance missing"
  check_contains "$valkey_compose" "file: ../../../common-optimizations.yml" "valkey template inheritance missing"
  check_contains "$seaweed_compose" "file: ../../../common-optimizations.yml" "seaweedfs template inheritance missing"
  check_contains "$ksql_compose" "file: ../../../common-optimizations.yml" "ksql template inheritance missing"

  check_contains "$ksql_compose" "hy-home.tier: data" "ksql tier label not normalized to data"

  check_not_contains "$seaweed_compose" ":-19333}]" "seaweedfs master malformed expose token remains"
  check_not_contains "$seaweed_compose" ":-18085}]" "seaweedfs volume malformed expose token remains"
  check_not_contains "$seaweed_compose" ":-18888}]" "seaweedfs filer malformed expose token remains"

  check_not_contains "$valkey_compose" "/run/secrets/mng_valkey_password" "valkey exporter stale secret contract remains"
  check_contains "$valkey_compose" "/run/secrets/service_valkey_password" "valkey exporter secret contract missing"

  required_supabase_services=(
    studio
    kong
    auth
    rest
    realtime
    storage
    analytics
    db
    vector
    supavisor
  )
  for service in "${required_supabase_services[@]}"; do
    check_service_healthcheck "$supabase_compose" "$service"
  done

  # Traceability links in spec document
  check_contains "$spec_file" "../../01.prd/2026-03-28-04-data-optimization-hardening.md" "spec missing PRD trace link"
  check_contains "$spec_file" "../../02.ard/0019-data-optimization-hardening-architecture.md" "spec missing ARD trace link"
  check_contains "$spec_file" "../../03.adr/0019-04-data-hardening-and-ha-expansion-strategy.md" "spec missing ADR trace link"
  check_contains "$spec_file" "../../05.plans/2026-03-28-04-data-optimization-hardening-plan.md" "spec missing Plan trace link"
  check_contains "$spec_file" "../../06.tasks/2026-03-28-04-data-optimization-hardening-tasks.md" "spec missing Task trace link"
  check_contains "$spec_file" "../../07.guides/04-data/optimization-hardening.md" "spec missing Guide trace link"
  check_contains "$spec_file" "../../08.operations/04-data/optimization-hardening.md" "spec missing Operations trace link"
  check_contains "$spec_file" "../../09.runbooks/04-data/optimization-hardening.md" "spec missing Runbook trace link"
fi

echo "Data hardening check"
echo "failures=$failures"

if [[ "$failures" -gt 0 ]]; then
  exit 1
fi

echo "PASS: 04-data hardening baseline enforced"
