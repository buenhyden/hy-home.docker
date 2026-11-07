#!/usr/bin/env bash
# Executable evidence for scripts/lib/hardening-lib.sh.
#
# The library is sourced by scripts/hardening/check-all-hardening.sh, which is
# gate-registered, but nothing exercised the library itself: every match for
# `check-all-hardening.sh` under tests/ is a string marker inside a
# workflow-contract assertion, never a run. Its eight functions decide whether
# every tier hardening check passes or fails, so they are asserted here
# directly.

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
LIB="${REPO_ROOT}/scripts/lib/hardening-lib.sh"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

failures=0

expect() {
  local label="$1"
  local expected="$2"
  local actual="$3"
  if [[ "$expected" != "$actual" ]]; then
    printf 'FAIL %s\n  expected: %s\n  actual:   %s\n' "$label" "$expected" "$actual"
    failures=$((failures + 1))
  fi
}

# Run a snippet with the library sourced, printing its exit status last so a
# non-zero return from a library function is observable rather than fatal.
run_snippet() {
  local body="$1"
  # The library sets `-e` at the top, which would end the sourcing shell at the
  # first function that returns 1 — before the snippet could observe it. Its
  # own caller keeps every call inside a conditional for the same reason.
  bash -c "
    set -uo pipefail
    source '${LIB}'
    set +e
    ${body}
  " 2>&1
}

printf 'sourcing %s\n' "$LIB"

# --- fail / success -------------------------------------------------------

expect "fail prints the [FAIL] marker" \
  "  [FAIL] broken" \
  "$(run_snippet 'fail broken')"

expect "fail increments the counter" \
  "2" \
  "$(run_snippet 'fail a >/dev/null; fail b >/dev/null; echo "$FAILURES"')"

expect "success prints the [PASS] marker" \
  "  [PASS] fine" \
  "$(run_snippet 'success fine')"

expect "success leaves the counter alone" \
  "0" \
  "$(run_snippet 'success fine >/dev/null; echo "$FAILURES"')"

# --- check_file -----------------------------------------------------------

printf 'present\n' >"${WORK}/present.txt"

expect "check_file accepts an existing file" \
  "rc=0 failures=0" \
  "$(run_snippet "check_file '${WORK}/present.txt'; rc=\$?; echo \"rc=\$rc failures=\$FAILURES\"")"

expect "check_file rejects a missing file and counts it" \
  "rc=1 failures=1" \
  "$(run_snippet "check_file '${WORK}/absent.txt' >/dev/null; rc=\$?; echo \"rc=\$rc failures=\$FAILURES\"")"

expect "check_file rejects a directory" \
  "rc=1" \
  "$(run_snippet "check_file '${WORK}' >/dev/null; echo \"rc=\$?\"")"

# --- check_contains / check_not_contains ----------------------------------

printf 'alpha\nno-new-privileges:true\nbeta [literal]\n' >"${WORK}/subject.txt"

expect "check_contains accepts a present pattern" \
  "rc=0" \
  "$(run_snippet "check_contains '${WORK}/subject.txt' 'no-new-privileges:true' label; echo \"rc=\$?\"")"

expect "check_contains rejects an absent pattern and labels it" \
  "  [FAIL] label (Expected: gamma)" \
  "$(run_snippet "check_contains '${WORK}/subject.txt' gamma label || true")"

# The library greps with -F, so a bracket expression is matched literally and
# never as a character class. A regex-mode grep would report `beta [literal]`
# as a match for `[lit]`.
expect "check_contains matches literally, not as a regex" \
  "rc=1" \
  "$(run_snippet "check_contains '${WORK}/subject.txt' '[lit]' label >/dev/null; echo \"rc=\$?\"")"

expect "check_not_contains accepts an absent pattern" \
  "rc=0" \
  "$(run_snippet "check_not_contains '${WORK}/subject.txt' gamma label; echo \"rc=\$?\"")"

expect "check_not_contains rejects a present pattern and labels it" \
  "  [FAIL] label (Forbidden: alpha)" \
  "$(run_snippet "check_not_contains '${WORK}/subject.txt' alpha label || true")"

# --- check_service_healthcheck --------------------------------------------

cat >"${WORK}/compose.yml" <<'YAML'
services:
  healthy:
    image: example
    healthcheck:
      test: ["CMD", "true"]
  unhealthy:
    image: example
    restart: unless-stopped
YAML

expect "check_service_healthcheck accepts a service that declares one" \
  "rc=0" \
  "$(run_snippet "check_service_healthcheck '${WORK}/compose.yml' healthy; echo \"rc=\$?\"")"

expect "check_service_healthcheck rejects a service without one" \
  "rc=1" \
  "$(run_snippet "check_service_healthcheck '${WORK}/compose.yml' unhealthy >/dev/null; echo \"rc=\$?\"")"

expect "check_service_healthcheck rejects an unknown service" \
  "  [FAIL] Service block not found: absent (file: ${WORK}/compose.yml)" \
  "$(run_snippet "check_service_healthcheck '${WORK}/compose.yml' absent || true")"

# The block ends at the next service key, so a later service's healthcheck is
# never credited to an earlier one.
expect "check_service_healthcheck does not read past the service block" \
  "  [FAIL] Healthcheck missing in service block: unhealthy (file: ${WORK}/compose.yml)" \
  "$(run_snippet "check_service_healthcheck '${WORK}/compose.yml' unhealthy || true")"

# --- check_service_contains / check_service_not_contains -------------------

cat >"${WORK}/scoped.yml" <<'YAML'
services:
  job:
    extends:
      service: template-job-med
  engine:
    extends:
      service: template-job-med
    ports:
      - '127.0.0.1:18090:8080'
YAML

expect "check_service_not_contains accepts a block without the text" \
  "rc=0" \
  "$(run_snippet "check_service_not_contains '${WORK}/scoped.yml' job 'ports:' 'job must not publish'; echo \"rc=\$?\"")"

# A later service's ports are never charged to an earlier one, and an earlier
# service's template is never credited to a later one.
expect "check_service_not_contains reads only its own block" \
  "  [FAIL] engine must not publish (Forbidden in engine: ports:)" \
  "$(run_snippet "check_service_not_contains '${WORK}/scoped.yml' engine 'ports:' 'engine must not publish' || true")"

expect "check_service_contains accepts text inside the block" \
  "rc=0" \
  "$(run_snippet "check_service_contains '${WORK}/scoped.yml' job 'service: template-job-med' 'job uses template'; echo \"rc=\$?\"")"

expect "check_service_contains rejects text only in another block" \
  "  [FAIL] job publishes (Expected in job: 127.0.0.1:18090)" \
  "$(run_snippet "check_service_contains '${WORK}/scoped.yml' job '127.0.0.1:18090' 'job publishes' || true")"

expect "check_service_contains rejects an unknown service" \
  "  [FAIL] Service block not found: absent (file: ${WORK}/scoped.yml)" \
  "$(run_snippet "check_service_contains '${WORK}/scoped.yml' absent 'x' 'y' || true")"

expect "a scoped failure is counted in the caller's shell" \
  "1" \
  "$(run_snippet "check_service_not_contains '${WORK}/scoped.yml' engine 'ports:' x >/dev/null; echo \"\$FAILURES\"")"

# --- start_tier / report_status -------------------------------------------

expect "start_tier announces the tier" \
  "==> Checking Gateway Hardening Baseline..." \
  "$(run_snippet 'start_tier Gateway')"

expect "report_status passes on a clean counter" \
  "Summary: ALL checks passed successfully.
rc=0" \
  "$(run_snippet 'report_status; echo "rc=$?"')"

expect "report_status fails once anything failed" \
  "Summary: 1 check(s) FAILED.
rc=1" \
  "$(run_snippet 'fail x >/dev/null; report_status; echo "rc=$?"')"

if ((failures > 0)); then
  printf 'FAIL: %d hardening library assertion(s) failed\n' "$failures"
  exit 1
fi

printf 'PASS: hardening library contract holds\n'
