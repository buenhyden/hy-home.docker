#!/usr/bin/env bash
# Common library for infrastructure hardening checks

set -euo pipefail

# Global failure counter
FAILURES=0

# Log a failure message
fail() {
  local msg="$1"
  echo "  [FAIL] $msg"
  FAILURES=$((FAILURES + 1))
}

# Log a success message
success() {
  local msg="$1"
  echo "  [PASS] $msg"
}

# Check if a file exists
check_file() {
  local file="$1"
  if [[ ! -f "$file" ]]; then
    fail "Missing file: $file"
    return 1
  fi
  return 0
}

# Check if a file contains a pattern
check_contains() {
  local file="$1"
  local pattern="$2"
  local label="$3"
  if ! grep -Fq -- "$pattern" "$file"; then
    fail "$label (Expected: $pattern)"
    return 1
  fi
  return 0
}

# Check if a file does NOT contain a pattern
check_not_contains() {
  local file="$1"
  local pattern="$2"
  local label="$3"
  if grep -Fq -- "$pattern" "$file"; then
    fail "$label (Forbidden: $pattern)"
    return 1
  fi
  return 0
}

# Print one top-level service block: the lines after "  <service>:" up to the
# next two-space key. Prints nothing when the service is absent; callers fail
# in their own shell so the FAILURES counter is not lost in a subshell.
_service_block() {
  awk -v svc="$2" '
    BEGIN { in_svc = 0; pat = "^  " svc ":" }
    $0 ~ pat { in_svc = 1; next }
    /^  [A-Za-z0-9_.-]+:/ && in_svc { in_svc = 0 }
    in_svc { print }
  ' "$1"
}

# Check that one service block contains (mode=contains) or does not contain
# (mode=not_contains) a fixed string
_check_service_text() {
  local mode="$1" compose_file="$2" service_name="$3" pattern="$4" label="$5"
  local block
  block="$(_service_block "$compose_file" "$service_name")"
  if [[ -z "$block" ]]; then
    fail "Service block not found: $service_name (file: $compose_file)"
    return 1
  fi
  if grep -Fq -- "$pattern" <<<"$block"; then
    [[ "$mode" == contains ]] && return 0
    fail "$label (Forbidden in $service_name: $pattern)"
    return 1
  fi
  [[ "$mode" == not_contains ]] && return 0
  fail "$label (Expected in $service_name: $pattern)"
  return 1
}

check_service_contains() { _check_service_text contains "$@"; }
check_service_not_contains() { _check_service_text not_contains "$@"; }

# Check if a service block in compose has a healthcheck
check_service_healthcheck() {
  local compose_file="$1"
  local service_name="$2"

  local block
  block="$(_service_block "$compose_file" "$service_name")"

  if [[ -z "$block" ]]; then
    fail "Service block not found: $service_name (file: $compose_file)"
    return 1
  fi

  if ! grep -Fq "healthcheck:" <<<"$block"; then
    fail "Healthcheck missing in service block: $service_name (file: $compose_file)"
    return 1
  fi
  return 0
}

# Check that a service block declares a network
check_service_network() {
  local compose_file="$1"
  local service_name="$2"
  local network_name="$3"

  local block
  block="$(_service_block "$compose_file" "$service_name")"

  if [[ -z "$block" ]]; then
    fail "Service block not found: $service_name (file: $compose_file)"
    return 1
  fi

  if ! grep -Eq "^      ${network_name}:" <<<"$block"; then
    fail "Network $network_name missing in service block: $service_name (file: $compose_file)"
    return 1
  fi
  return 0
}

# Start a new tier check
start_tier() {
  local tier_name="$1"
  echo "==> Checking $tier_name Hardening Baseline..."
}

# Final report
report_status() {
  if [[ "$FAILURES" -eq 0 ]]; then
    echo "Summary: ALL checks passed successfully."
    return 0
  else
    echo "Summary: $FAILURES check(s) FAILED."
    return 1
  fi
}
