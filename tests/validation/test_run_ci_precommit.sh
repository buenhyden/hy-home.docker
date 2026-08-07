#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
WRAPPER="$REPO_ROOT/scripts/validation/run-ci-precommit.sh"
TMP_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/test-ci-precommit.XXXXXX")"
FAKE_BIN="$TMP_ROOT/bin"
CALL_FILE="$TMP_ROOT/call"

cleanup() {
  rm -rf "$TMP_ROOT"
}
trap cleanup EXIT HUP INT TERM

mkdir -p "$FAKE_BIN"

if [[ ! -x "$WRAPPER" ]]; then
  echo "RED: CI pre-commit wrapper is not implemented: $WRAPPER" >&2
  exit 1
fi

fail() {
  echo "not ok - $1" >&2
  exit 1
}

expect_rejected() {
  local name="$1"
  shift
  rm -f "$CALL_FILE"
  if env PATH="$FAKE_BIN:$PATH" FAKE_PRECOMMIT_CALL_FILE="$CALL_FILE" "$@"; then
    fail "$name was accepted"
  fi
  [[ ! -e "$CALL_FILE" ]] || fail "$name invoked pre-commit"
}

printf '%s\n' \
  '#!/usr/bin/env bash' \
  'set -euo pipefail' \
  "printf \"%s\\n\" \"SKIP=\${SKIP-}\" \"\$@\" >\"\${FAKE_PRECOMMIT_CALL_FILE:?}\"" \
  "exit \"\${FAKE_PRECOMMIT_EXIT:-0}\"" \
  >"$FAKE_BIN/pre-commit"
chmod +x "$FAKE_BIN/pre-commit"

expect_rejected "missing GITHUB_ACTIONS" \
  env CI=true "$WRAPPER"
expect_rejected "missing CI" \
  env GITHUB_ACTIONS=true "$WRAPPER"
expect_rejected "false GITHUB_ACTIONS" \
  env GITHUB_ACTIONS=false CI=true "$WRAPPER"
expect_rejected "false CI" \
  env GITHUB_ACTIONS=true CI=false "$WRAPPER"
expect_rejected "missing SKIP" \
  env GITHUB_ACTIONS=true CI=true "$WRAPPER"
expect_rejected "wrong SKIP" \
  env GITHUB_ACTIONS=true CI=true SKIP=eslint "$WRAPPER"
expect_rejected "positional argument" \
  env GITHUB_ACTIONS=true CI=true "$WRAPPER" --all-files
expect_rejected "TASK_FILE Agent-wrapper variable" \
  env GITHUB_ACTIONS=true CI=true TASK_FILE=task.md "$WRAPPER"
expect_rejected "ALLOW_PREFIXES Agent-wrapper variable" \
  env GITHUB_ACTIONS=true CI=true ALLOW_PREFIXES=scripts "$WRAPPER"

env \
  PATH="$FAKE_BIN:$PATH" \
  FAKE_PRECOMMIT_CALL_FILE="$CALL_FILE" \
  GITHUB_ACTIONS=true \
  CI=true \
  SKIP=eslint-nextjs \
  "$WRAPPER"

expected_call=$'SKIP=eslint-nextjs\nrun\n--all-files\n--show-diff-on-failure'
actual_call="$(<"$CALL_FILE")"
[[ "$actual_call" == "$expected_call" ]] || fail "command or SKIP differs from the contract"

set +e
env \
  PATH="$FAKE_BIN:$PATH" \
  FAKE_PRECOMMIT_CALL_FILE="$CALL_FILE" \
  FAKE_PRECOMMIT_EXIT=37 \
  GITHUB_ACTIONS=true \
  CI=true \
  SKIP=eslint-nextjs \
  "$WRAPPER"
child_exit=$?
set -e
[[ "$child_exit" -eq 37 ]] || fail "child exit was not propagated"

echo "PASS: CI pre-commit wrapper contract"
