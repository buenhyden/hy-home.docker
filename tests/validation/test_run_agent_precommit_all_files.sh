#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
WRAPPER="$REPO_ROOT/scripts/validation/run-agent-precommit-all-files.sh"
TMP_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/test-agent-precommit.XXXXXX")"
PASS_COUNT=0
FAIL_COUNT=0

cleanup() {
  rm -rf "$TMP_ROOT"
}
trap cleanup EXIT HUP INT TERM

if [[ ! -x "$WRAPPER" ]]; then
  echo "FAIL: wrapper does not exist or is not executable: $WRAPPER" >&2
  exit 1
fi

fail_test() {
  local name="$1"
  local detail="$2"
  echo "not ok - $name: $detail" >&2
  FAIL_COUNT=$((FAIL_COUNT + 1))
}

pass_test() {
  local name="$1"
  echo "ok - $name"
  PASS_COUNT=$((PASS_COUNT + 1))
}

assert_exit() {
  local expected="$1"
  local actual="$2"
  [[ "$actual" -eq "$expected" ]]
}

assert_contains() {
  local path="$1"
  local expected="$2"
  grep -Fq -- "$expected" "$path"
}

assert_not_contains() {
  local path="$1"
  local unexpected="$2"
  ! grep -Fq -- "$unexpected" "$path"
}

new_fixture() {
  local name="$1"
  local fixture="$TMP_ROOT/$name"
  local primary="$fixture/primary"
  local linked="$fixture/linked"
  local fake_bin="$fixture/fake-bin"

  mkdir -p "$primary" "$fake_bin"
  git -C "$primary" init -q
  git -C "$primary" config user.name "Wrapper Test"
  git -C "$primary" config user.email "wrapper-test@example.invalid"
  mkdir -p "$primary/docs/04.execution/tasks" "$primary/allowed" "$primary/outside"
  printf '%s\n' '# Task evidence' >"$primary/docs/04.execution/tasks/task.md"
  printf '%s\n' 'allowed baseline' >"$primary/allowed/tracked.txt"
  printf '%s\n' 'outside baseline' >"$primary/outside/tracked.txt"
  printf '%s\n' '# Repository' >"$primary/README.md"
  git -C "$primary" add .
  git -C "$primary" commit -qm "test fixture"
  git -C "$primary" worktree add -q --detach "$linked" HEAD

  cat >"$fake_bin/pre-commit" <<'FAKE'
#!/usr/bin/env bash
set -euo pipefail

printf '%s\0' "$@" >"${FAKE_PRECOMMIT_ARGS_FILE:?}"
printf '%s\n' 'hook log token=super-secret-output'

case "${FAKE_PRECOMMIT_ACTION:-pass}" in
  pass)
    ;;
  modify)
    printf '%s\n' 'hook edit' >>"${FAKE_PRECOMMIT_PATH:?}"
    ;;
  untracked)
    mkdir -p "$(dirname "${FAKE_PRECOMMIT_PATH:?}")"
    printf '%s\n' 'hook addition' >"${FAKE_PRECOMMIT_PATH:?}"
    ;;
  rename)
    mkdir -p "$(dirname "${FAKE_PRECOMMIT_PATH_TO:?}")"
    mv "${FAKE_PRECOMMIT_PATH_FROM:?}" "${FAKE_PRECOMMIT_PATH_TO:?}"
    ;;
  delete)
    rm "${FAKE_PRECOMMIT_PATH:?}"
    ;;
  *)
    printf '%s\n' "unsupported fake action" >&2
    exit 98
    ;;
esac

exit "${FAKE_PRECOMMIT_EXIT:-0}"
FAKE
  chmod +x "$fake_bin/pre-commit"

  FIXTURE="$fixture"
  PRIMARY="$primary"
  LINKED="$linked"
  FAKE_BIN="$fake_bin"
  OUTPUT="$fixture/output.txt"
  ARGS_FILE="$fixture/args.bin"
}

invoke() {
  local cwd="$1"
  shift
  local status
  local wrapper_tmpdir="${WRAPPER_TMPDIR:-$FIXTURE/wrapper-tmp}"

  mkdir -p "$wrapper_tmpdir"

  set +e
  (
    cd "$cwd"
    PATH="$FAKE_BIN:$PATH" \
      FAKE_PRECOMMIT_ARGS_FILE="$ARGS_FILE" \
      FAKE_PRECOMMIT_ACTION="${FAKE_PRECOMMIT_ACTION:-pass}" \
      FAKE_PRECOMMIT_EXIT="${FAKE_PRECOMMIT_EXIT:-0}" \
      FAKE_PRECOMMIT_PATH="${FAKE_PRECOMMIT_PATH:-}" \
      FAKE_PRECOMMIT_PATH_FROM="${FAKE_PRECOMMIT_PATH_FROM:-}" \
      FAKE_PRECOMMIT_PATH_TO="${FAKE_PRECOMMIT_PATH_TO:-}" \
      TMPDIR="$wrapper_tmpdir" \
      bash "$WRAPPER" "$@"
  ) >"$OUTPUT" 2>&1
  status=$?
  set -e
  INVOKE_STATUS="$status"
}

test_missing_task_argument() {
  local name="missing --task is rejected"
  new_fixture "missing-task"
  invoke "$LINKED" --allow-prefix allowed
  if assert_exit 2 "$INVOKE_STATUS" && assert_contains "$OUTPUT" "--task is required"; then
    pass_test "$name"
  else
    fail_test "$name" "status=$INVOKE_STATUS"
  fi
}

test_non_task_path() {
  local name="tracked non-task path is rejected"
  new_fixture "non-task"
  invoke "$LINKED" --task README.md --allow-prefix allowed
  if assert_exit 4 "$INVOKE_STATUS" && assert_contains "$OUTPUT" "docs/04.execution/tasks"; then
    pass_test "$name"
  else
    fail_test "$name" "status=$INVOKE_STATUS"
  fi
}

test_untracked_task_path() {
  local name="untracked task path is rejected"
  new_fixture "untracked-task"
  printf '%s\n' '# Untracked task' >"$LINKED/docs/04.execution/tasks/untracked.md"
  invoke "$LINKED" --task docs/04.execution/tasks/untracked.md --allow-prefix allowed
  if assert_exit 4 "$INVOKE_STATUS" && assert_contains "$OUTPUT" "tracked task"; then
    pass_test "$name"
  else
    fail_test "$name" "status=$INVOKE_STATUS"
  fi
}

test_primary_checkout_rejected() {
  local name="primary checkout is rejected"
  new_fixture "primary-checkout"
  invoke "$PRIMARY" --task docs/04.execution/tasks/task.md --allow-prefix allowed
  if assert_exit 3 "$INVOKE_STATUS" && assert_contains "$OUTPUT" "linked worktree" && [[ ! -e "$ARGS_FILE" ]]; then
    pass_test "$name"
  else
    fail_test "$name" "status=$INVOKE_STATUS"
  fi
}

test_linked_worktree_accepts_exact_command() {
  local name="clean linked worktree runs the exact command"
  local -a actual_args=()
  new_fixture "linked-accept"
  mkdir -p "$FIXTURE/wrapper-tmp"
  invoke "$LINKED" --task docs/04.execution/tasks/task.md --allow-prefix allowed
  while IFS= read -r -d '' arg; do
    actual_args+=("$arg")
  done <"$ARGS_FILE"
  if assert_exit 0 "$INVOKE_STATUS" \
    && [[ "${actual_args[*]}" == "run --all-files --show-diff-on-failure" ]] \
    && assert_contains "$OUTPUT" "hook_exit=0" \
    && assert_contains "$OUTPUT" "unexpected_count=0" \
    && assert_not_contains "$OUTPUT" "super-secret-output" \
    && [[ -z "$(find "$FIXTURE/wrapper-tmp" -mindepth 1 -print -quit)" ]]; then
    pass_test "$name"
  else
    fail_test "$name" "status=$INVOKE_STATUS args=${actual_args[*]}"
  fi
}

test_missing_precommit() {
  local name="missing pre-commit is rejected"
  new_fixture "missing-precommit"
  local empty_bin="$FIXTURE/empty-bin"
  mkdir -p "$empty_bin"
  ln -s "$(command -v git)" "$empty_bin/git"
  set +e
  (
    cd "$LINKED"
    PATH="$empty_bin" TMPDIR="$FIXTURE/wrapper-tmp" \
      /usr/bin/bash "$WRAPPER" --task docs/04.execution/tasks/task.md --allow-prefix allowed
  ) >"$OUTPUT" 2>&1
  INVOKE_STATUS=$?
  set -e
  if assert_exit 127 "$INVOKE_STATUS" && assert_contains "$OUTPUT" "pre-commit is required"; then
    pass_test "$name"
  else
    fail_test "$name" "status=$INVOKE_STATUS"
  fi
}

test_invalid_prefixes() {
  local name="absolute traversal and empty prefixes are rejected"
  local prefix status_ok=1
  new_fixture "invalid-prefixes"
  for prefix in "/tmp/allowed" "../allowed" "allowed/../../outside" ""; do
    invoke "$LINKED" --task docs/04.execution/tasks/task.md --allow-prefix "$prefix"
    if ! assert_exit 2 "$INVOKE_STATUS"; then
      status_ok=0
    fi
  done
  if [[ "$status_ok" -eq 1 ]] && [[ ! -e "$ARGS_FILE" ]]; then
    pass_test "$name"
  else
    fail_test "$name" "one or more invalid prefixes were accepted"
  fi
}

test_dirty_start_rejected() {
  local name="pre-existing dirty paths cannot mask hook changes"
  new_fixture "dirty-start"
  printf '%s\n' 'pre-existing edit' >>"$LINKED/allowed/tracked.txt"
  invoke "$LINKED" --task docs/04.execution/tasks/task.md --allow-prefix allowed
  if assert_exit 5 "$INVOKE_STATUS" && assert_contains "$OUTPUT" "clean linked worktree" && [[ ! -e "$ARGS_FILE" ]]; then
    pass_test "$name"
  else
    fail_test "$name" "status=$INVOKE_STATUS"
  fi
}

test_hook_exit_propagation() {
  local name="fake pre-commit exit status is propagated"
  new_fixture "exit-propagation"
  FAKE_PRECOMMIT_EXIT=37 invoke "$LINKED" --task docs/04.execution/tasks/task.md --allow-prefix allowed
  if assert_exit 37 "$INVOKE_STATUS" && assert_contains "$OUTPUT" "hook_exit=37" && assert_not_contains "$OUTPUT" "super-secret-output"; then
    pass_test "$name"
  else
    fail_test "$name" "status=$INVOKE_STATUS"
  fi
}

test_expected_edit() {
  local name="expected modified path is accepted"
  new_fixture "expected-edit"
  FAKE_PRECOMMIT_ACTION=modify FAKE_PRECOMMIT_PATH="$LINKED/allowed/tracked.txt" \
    invoke "$LINKED" --task docs/04.execution/tasks/task.md --allow-prefix allowed
  if assert_exit 0 "$INVOKE_STATUS" && assert_contains "$OUTPUT" "changed_count=1" && assert_contains "$OUTPUT" "allowed/tracked.txt"; then
    pass_test "$name"
  else
    fail_test "$name" "status=$INVOKE_STATUS"
  fi
}

run_unexpected_path_case() {
  local name="$1"
  local fixture_name="$2"
  local expected_count="$3"
  shift 3
  new_fixture "$fixture_name"
  "$@"
  if assert_exit 20 "$INVOKE_STATUS" \
    && assert_contains "$OUTPUT" "unexpected_count=$expected_count" \
    && assert_contains "$OUTPUT" "unexpected_paths=" \
    && assert_not_contains "$OUTPUT" "super-secret-output"; then
    pass_test "$name"
  else
    fail_test "$name" "status=$INVOKE_STATUS"
  fi
}

unexpected_modified() {
  FAKE_PRECOMMIT_ACTION=modify FAKE_PRECOMMIT_PATH="$LINKED/outside/tracked.txt" \
    invoke "$LINKED" --task docs/04.execution/tasks/task.md --allow-prefix allowed
}

unexpected_untracked() {
  FAKE_PRECOMMIT_ACTION=untracked FAKE_PRECOMMIT_PATH="$LINKED/outside/new file.txt" \
    invoke "$LINKED" --task docs/04.execution/tasks/task.md --allow-prefix allowed
}

unexpected_renamed() {
  FAKE_PRECOMMIT_ACTION=rename \
    FAKE_PRECOMMIT_PATH_FROM="$LINKED/outside/tracked.txt" \
    FAKE_PRECOMMIT_PATH_TO="$LINKED/outside/renamed file.txt" \
    invoke "$LINKED" --task docs/04.execution/tasks/task.md --allow-prefix allowed
}

unexpected_deleted() {
  FAKE_PRECOMMIT_ACTION=delete FAKE_PRECOMMIT_PATH="$LINKED/outside/tracked.txt" \
    invoke "$LINKED" --task docs/04.execution/tasks/task.md --allow-prefix allowed
}

test_prefix_boundary() {
  local name="allowed prefix does not admit a lexical sibling"
  new_fixture "prefix-boundary"
  mkdir -p "$LINKED/allowed-sibling"
  printf '%s\n' 'tracked sibling' >"$LINKED/allowed-sibling/tracked.txt"
  git -C "$LINKED" add allowed-sibling/tracked.txt
  git -C "$LINKED" commit -qm "add sibling"
  FAKE_PRECOMMIT_ACTION=modify FAKE_PRECOMMIT_PATH="$LINKED/allowed-sibling/tracked.txt" \
    invoke "$LINKED" --task docs/04.execution/tasks/task.md --allow-prefix allowed
  if assert_exit 20 "$INVOKE_STATUS" && assert_contains "$OUTPUT" "allowed-sibling/tracked.txt"; then
    pass_test "$name"
  else
    fail_test "$name" "status=$INVOKE_STATUS"
  fi
}

test_nul_safe_path() {
  local name="NUL-aware parsing handles control characters in paths"
  local odd_path
  new_fixture "nul-safe-path"
  odd_path="$LINKED/outside/line
break.txt"
  FAKE_PRECOMMIT_ACTION=untracked FAKE_PRECOMMIT_PATH="$odd_path" \
    invoke "$LINKED" --task docs/04.execution/tasks/task.md --allow-prefix allowed
  if assert_exit 20 "$INVOKE_STATUS" && assert_contains "$OUTPUT" "unexpected_count=1"; then
    pass_test "$name"
  else
    fail_test "$name" "status=$INVOKE_STATUS"
  fi
}

test_unexpected_overrides_hook_exit() {
  local name="unexpected-path status remains distinct from hook failure"
  new_fixture "unexpected-and-hook-failure"
  FAKE_PRECOMMIT_ACTION=modify FAKE_PRECOMMIT_PATH="$LINKED/outside/tracked.txt" FAKE_PRECOMMIT_EXIT=41 \
    invoke "$LINKED" --task docs/04.execution/tasks/task.md --allow-prefix allowed
  if assert_exit 20 "$INVOKE_STATUS" && assert_contains "$OUTPUT" "hook_exit=41"; then
    pass_test "$name"
  else
    fail_test "$name" "status=$INVOKE_STATUS"
  fi
}

test_missing_task_argument
test_non_task_path
test_untracked_task_path
test_primary_checkout_rejected
test_linked_worktree_accepts_exact_command
test_missing_precommit
test_invalid_prefixes
test_dirty_start_rejected
test_hook_exit_propagation
test_expected_edit
run_unexpected_path_case "unexpected modified path is rejected" "unexpected-modified" 1 unexpected_modified
run_unexpected_path_case "unexpected untracked path is rejected" "unexpected-untracked" 1 unexpected_untracked
run_unexpected_path_case "unexpected renamed paths are rejected" "unexpected-renamed" 2 unexpected_renamed
run_unexpected_path_case "unexpected deleted path is rejected" "unexpected-deleted" 1 unexpected_deleted
test_prefix_boundary
test_nul_safe_path
test_unexpected_overrides_hook_exit

echo
echo "Agent pre-commit wrapper tests"
echo "passed=$PASS_COUNT failed=$FAIL_COUNT"

if [[ "$FAIL_COUNT" -ne 0 ]]; then
  exit 1
fi
