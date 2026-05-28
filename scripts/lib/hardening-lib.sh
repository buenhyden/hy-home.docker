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

# Check if a service block in compose has a healthcheck
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
    fail "Service block not found: $service_name (file: $compose_file)"
    return 1
  fi

  if ! grep -Fq "healthcheck:" <<<"$block"; then
    fail "Healthcheck missing in service block: $service_name (file: $compose_file)"
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
