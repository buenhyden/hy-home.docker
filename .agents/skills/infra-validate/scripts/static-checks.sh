#!/usr/bin/env bash
# Run the static infrastructure checks and say plainly what was not run.
#
# The skill separates static checks from separately authorized runtime
# observation. That separation is only worth anything if the report says which
# side each result came from, so this reports SKIPPED for anything absent rather
# than omitting the line: an omitted check reads like a passing one.
set -euo pipefail

status=0
report() { printf '%-34s %s\n' "$1" "$2"; }

run() {
  local label="$1"; shift
  if ! command -v "$1" >/dev/null 2>&1; then
    report "$label" "SKIPPED (missing: $1)"
    return
  fi
  if "$@" >/dev/null 2>&1; then
    report "$label" "PASS"
  else
    report "$label" "FAIL"
    status=1
  fi
}

run "compose-config-render" docker compose config --quiet
run "compose-structure" bash scripts/validation/validate-docker-compose.sh
run "yaml-lint" yamllint -s infra
# Swallowing the exit code here would report a lint failure as a pass, which is
# the exact confusion this script exists to prevent.
mapfile -t infra_scripts < <(git ls-files 'infra/*.sh' 'infra/**/*.sh')
if [[ ${#infra_scripts[@]} -eq 0 ]]; then
  report "shell-lint" "NOT_APPLICABLE (no tracked infra shell scripts)"
elif ! command -v shellcheck >/dev/null 2>&1; then
  report "shell-lint" "SKIPPED (missing: shellcheck)"
else
  # `.pre-commit-config.yaml` owns the severity, and it says so in a comment
  # there because a `.shellcheckrc` key is silently ignored. Matching it keeps
  # this skill from reporting FAIL where the registered gate reports PASS.
  run "shell-lint" shellcheck --severity=warning "${infra_scripts[@]}"
fi

report "runtime-observation" "NOT_RUN (needs separate approval)"
report "secret-values" "NOT_RUN (out of scope by design)"

exit "$status"
