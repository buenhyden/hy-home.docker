#!/usr/bin/env bash
set -euo pipefail

# Enforces PLN-QW-001~005 baseline on the resolved root compose config.
# - QW-001: restart
# - QW-002: healthcheck (with approved one-shot init exceptions)
# - QW-003: no-new-privileges
# - QW-004: cpus + mem_limit
# - QW-005: secrets (with approved etcd auth-disabled exceptions)

if ! command -v jq >/dev/null 2>&1; then
  echo "ERROR: jq is required for baseline checks." >&2
  exit 2
fi

exceptions_file="infra/common-optimizations.exceptions.json"
if [[ ! -f "$exceptions_file" ]]; then
  echo "ERROR: exceptions registry not found: $exceptions_file" >&2
  exit 2
fi

tmp_json="$(mktemp)"
trap 'rm -f "$tmp_json"' EXIT

docker compose config --format json >"$tmp_json"

healthcheck_exceptions="$(
  jq -c '.quickwin_baseline.healthcheck_exceptions // [] | map(.service)' "$exceptions_file"
)"
secrets_exceptions="$(
  jq -c '.quickwin_baseline.secrets_exceptions // [] | map(.service)' "$exceptions_file"
)"

summary="$(
  jq -r \
    --argjson health_ex "$healthcheck_exceptions" \
    --argjson sec_ex "$secrets_exceptions" \
    '
      .services as $svc
      | ($svc | to_entries | length) as $total
      | {
          total: $total,
          restart_missing: ([$svc | to_entries[] | select(.value | has("restart") | not)] | length),
          healthcheck_missing: ([
            $svc | to_entries[]
            | .key as $name
            | select(.value | has("healthcheck") | not)
            | select(($health_ex | index($name)) | not)
          ] | length),
          nnp_missing: ([
            $svc | to_entries[]
            | select(((.value.security_opt // []) | map(tostring) | any(contains("no-new-privileges:true"))) | not)
          ] | length),
          cpus_missing: ([$svc | to_entries[] | select(.value | has("cpus") | not)] | length),
          mem_missing: ([$svc | to_entries[] | select(.value | has("mem_limit") | not)] | length),
          secrets_missing: ([
            $svc | to_entries[]
            | .key as $name
            | select(((.value.secrets // []) | length) == 0)
            | select(($sec_ex | index($name)) | not)
          ] | length)
        }
      | @json
    ' \
    "$tmp_json"
)"

echo "QuickWin baseline check (PLN-QW-001~005)"
echo "$summary" | jq .

violations="$(
  jq -r \
    --argjson health_ex "$healthcheck_exceptions" \
    --argjson sec_ex "$secrets_exceptions" \
    '
      .services
      | to_entries[]
      | .key as $name
      | .value as $s
      | [
          (if ($s | has("restart")) then empty else "restart" end),
          (if ($s | has("healthcheck") or ($health_ex | index($name))) then empty else "healthcheck" end),
          (if ((($s.security_opt // []) | map(tostring) | any(contains("no-new-privileges:true")))) then empty else "no-new-privileges" end),
          (if ($s | has("cpus")) then empty else "cpus" end),
          (if ($s | has("mem_limit")) then empty else "mem_limit" end),
          (if (((($s.secrets // []) | length) > 0) or ($sec_ex | index($name))) then empty else "secrets" end)
        ]
        | map(select(. != null))
        | select(length > 0)
        | "\($name): \(join(","))"
    ' \
    "$tmp_json"
)"

if [[ -n "$violations" ]]; then
  echo
  echo "FAILED: baseline violations detected"
  echo "$violations"
  exit 1
fi

echo
echo "PASS: baseline enforced (approved exceptions only)"
