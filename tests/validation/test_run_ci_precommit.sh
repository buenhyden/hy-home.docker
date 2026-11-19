#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
WRAPPER="$REPO_ROOT/scripts/validation/run-ci-precommit.sh"
TMP_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/test-ci-precommit.XXXXXX")"
FAKE_BIN="$TMP_ROOT/bin"
CALL_FILE="$TMP_ROOT/call"
CANDIDATE_REPO="$TMP_ROOT/candidate"
REAL_REPO="$TMP_ROOT/local-staged"

cleanup() {
  rm -rf "$TMP_ROOT"
}
trap cleanup EXIT HUP INT TERM

mkdir -p "$FAKE_BIN"
export PRE_COMMIT_HOME="$TMP_ROOT/pre-commit-home"

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

# The single-quoted entries are the literal body of the generated fake command.
# shellcheck disable=SC2016
printf '%s\n' \
  '#!/usr/bin/env bash' \
  'set -euo pipefail' \
  'if [[ "${1:-}" == "--version" ]]; then printf "pre-commit %s\n" "${FAKE_PRECOMMIT_VERSION:-4.6.2}"; exit 0; fi' \
  'readonly_config=""' \
  'previous=""' \
  'for argument in "$@"; do if [[ "$previous" == "--config" ]]; then readonly_config="$argument"; break; fi; previous="$argument"; done' \
  'test -n "$readonly_config"' \
  'scratch_root="$(dirname "$readonly_config")"' \
  'markdown_config="$scratch_root/markdownlint-check.yaml"' \
  'test -f "$readonly_config" && test -f "$markdown_config"' \
  'if [[ "$EXPECTED_STYLE_MODE" == "pr-merge" ]]; then' \
  '  test "$(git rev-parse HEAD)" = "${EXPECTED_MERGE_SHA:?}"' \
  '  grep -q "^  MD013: true$" "$markdown_config"' \
  '  grep -q "^base-side$" interaction.md' \
  '  grep -q "^feature-side$" interaction.md' \
  '  test "$(grep -o "id: [a-z0-9-]*" "$readonly_config" | tr "\n" " ")" = "${EXPECTED_PR_HOOKS:?}"' \
  'else' \
  '  test "$PWD" != "${EXPECTED_LOCAL_REPO:?}"' \
  '  grep -q "^  MD013: true$" "$markdown_config"' \
  '  test "$(git show :interaction.md)" = "staged-side"' \
  '  test "$(cat interaction.md)" = "staged-side"' \
  'fi' \
  'if [[ "$EXPECTED_STYLE_MODE" != "pr-merge" ]]; then test "$(grep -o "id: [a-z0-9-]*" .pre-commit-config.yaml)" = "$(grep -o "id: [a-z0-9-]*" "$readonly_config")"; grep -A8 "id: ruff-format" "$readonly_config" | grep -q -- "--check"; fi' \
  'grep -A8 "id: mixed-line-ending" "$readonly_config" | grep -q -- "--fix=no"' \
  'grep -A8 "id: markdownlint-cli2" "$readonly_config" | grep -q "$markdown_config"' \
  'grep -q "^fix: false$" "$markdown_config"' \
  'case "${FAKE_PRECOMMIT_MUTATION:-}" in worktree) printf "%s\n" changed >interaction.md ;; index) printf "%s\n" changed >interaction.md; git add interaction.md ;; source-index) printf "%s\n" concurrent >"$EXPECTED_LOCAL_REPO/interaction.md"; git -C "$EXPECTED_LOCAL_REPO" add interaction.md ;; esac' \
  'if [[ "${FAKE_PRECOMMIT_SIGNAL:-}" == TERM ]]; then kill -TERM "$PPID"; fi' \
  'if [[ "${FAKE_PRECOMMIT_SIGNAL:-}" == TERM_HANG ]]; then trap "" TERM; printf "%s\n" "$$" >"$FAKE_PRECOMMIT_CALL_FILE.pid"; kill -TERM "$PPID"; while :; do sleep 1; done; fi' \
  "printf \"%s\\n\" \"CALL\" \"PWD=\$PWD\" \"SKIP=\${SKIP-}\" \"\$@\" >>\"\${FAKE_PRECOMMIT_CALL_FILE:?}\"" \
  "exit \"\${FAKE_PRECOMMIT_EXIT:-0}\"" \
  >"$FAKE_BIN/pre-commit"
chmod +x "$FAKE_BIN/pre-commit"

git init -q -b main "$CANDIDATE_REPO"
git -C "$CANDIDATE_REPO" config user.name "Diagnostic"
git -C "$CANDIDATE_REPO" config user.email "diagnostic@example.invalid"
# Local hooks keep the pr-merge hook selection offline. Python and shell hooks
# match no changed file; always_run and commit-msg hooks stay.
cat >"$CANDIDATE_REPO/.pre-commit-config.yaml" <<'YAML'
exclude: '^graphify-out/'
repos:
  - repo: local
    hooks:
      - {id: mixed-line-ending, name: mixed, language: system, entry: 'true', types: [text]}
      - {id: markdownlint-cli2, name: markdown, language: system, entry: 'true', files: '\.md$'}
      - {id: ruff-format, name: ruff, language: system, entry: 'true', files: '\.pyi?$'}
      - {id: shellcheck, name: shell, language: system, entry: 'true', files: '\.sh$'}
      - {id: always-check, name: always, language: system, entry: 'true', files: '^never$', always_run: true}
      - {id: commitizen, name: message, language: system, entry: 'true', stages: [commit-msg]}
YAML
cp "$REPO_ROOT/.markdownlint-cli2.yaml" "$CANDIDATE_REPO/.markdownlint-cli2.yaml"
mkdir -p "$CANDIDATE_REPO/scripts"
cp "$REPO_ROOT/scripts/requirements-pre-commit.txt" \
  "$CANDIDATE_REPO/scripts/requirements-pre-commit.txt"
printf '%s\n' common-side two three four common-feature >"$CANDIDATE_REPO/interaction.md"
git -C "$CANDIDATE_REPO" add .
git -C "$CANDIDATE_REPO" commit -qm "chore: Establish common tree"
git -C "$CANDIDATE_REPO" switch -q -c feature
sed -i 's/common-feature/feature-side/' "$CANDIDATE_REPO/interaction.md"
git -C "$CANDIDATE_REPO" commit -qam "fix(ci): Change feature content"
HEAD_SHA="$(git -C "$CANDIDATE_REPO" rev-parse HEAD)"
git -C "$CANDIDATE_REPO" switch -q main
sed -i 's/MD013: false/MD013: true/' "$CANDIDATE_REPO/.markdownlint-cli2.yaml"
sed -i 's/common-side/base-side/' "$CANDIDATE_REPO/interaction.md"
git -C "$CANDIDATE_REPO" commit -qam "chore: Advance base configuration"
BASE_SHA="$(git -C "$CANDIDATE_REPO" rev-parse HEAD)"
git -C "$CANDIDATE_REPO" merge -q --no-ff --no-commit feature
printf '%s\n' '# Merge-only resolution' >"$CANDIDATE_REPO/merge-only.md"
git -C "$CANDIDATE_REPO" add merge-only.md
git -C "$CANDIDATE_REPO" commit -qm "Merge candidate"
MERGE_SHA="$(git -C "$CANDIDATE_REPO" rev-parse HEAD)"
EXPECTED_PR_HOOKS="id: mixed-line-ending id: markdownlint-cli2 id: always-check id: commitizen "

expect_rejected "missing GITHUB_ACTIONS" \
  env CI=true PR_BASE_SHA="$BASE_SHA" PR_HEAD_SHA="$HEAD_SHA" "$WRAPPER" --mode pr-merge
expect_rejected "missing CI" \
  env GITHUB_ACTIONS=true PR_BASE_SHA="$BASE_SHA" PR_HEAD_SHA="$HEAD_SHA" "$WRAPPER" --mode pr-merge
expect_rejected "false GITHUB_ACTIONS" \
  env GITHUB_ACTIONS=false CI=true PR_BASE_SHA="$BASE_SHA" PR_HEAD_SHA="$HEAD_SHA" "$WRAPPER" --mode pr-merge
expect_rejected "false CI" \
  env GITHUB_ACTIONS=true CI=false PR_BASE_SHA="$BASE_SHA" PR_HEAD_SHA="$HEAD_SHA" "$WRAPPER" --mode pr-merge
expect_rejected "missing PR_BASE_SHA" \
  env GITHUB_ACTIONS=true CI=true PR_HEAD_SHA="$HEAD_SHA" "$WRAPPER" --mode pr-merge
expect_rejected "abbreviated PR_BASE_SHA" \
  env GITHUB_ACTIONS=true CI=true PR_BASE_SHA=0123456 PR_HEAD_SHA="$HEAD_SHA" "$WRAPPER" --mode pr-merge
expect_rejected "missing PR_HEAD_SHA" \
  env GITHUB_ACTIONS=true CI=true PR_BASE_SHA="$BASE_SHA" "$WRAPPER" --mode pr-merge
expect_rejected "abbreviated PR_HEAD_SHA" \
  env GITHUB_ACTIONS=true CI=true PR_BASE_SHA="$BASE_SHA" PR_HEAD_SHA=abcdef "$WRAPPER" --mode pr-merge
expect_rejected "identical PR revisions" \
  env GITHUB_ACTIONS=true CI=true PR_BASE_SHA="$BASE_SHA" PR_HEAD_SHA="$BASE_SHA" "$WRAPPER" --mode pr-merge
expect_rejected "caller-supplied SKIP" \
  env GITHUB_ACTIONS=true CI=true PR_BASE_SHA="$BASE_SHA" PR_HEAD_SHA="$HEAD_SHA" SKIP=public-validation-changed "$WRAPPER" --mode pr-merge
expect_rejected "empty caller-supplied SKIP" \
  env GITHUB_ACTIONS=true CI=true PR_BASE_SHA="$BASE_SHA" PR_HEAD_SHA="$HEAD_SHA" SKIP= "$WRAPPER" --mode pr-merge
expect_rejected "missing mode" "$WRAPPER"
expect_rejected "unknown mode" "$WRAPPER" --mode unknown
expect_rejected "extra positional argument" \
  env GITHUB_ACTIONS=true CI=true PR_BASE_SHA="$BASE_SHA" PR_HEAD_SHA="$HEAD_SHA" "$WRAPPER" --mode pr-merge --all-files
expect_rejected "TASK_FILE Agent-wrapper variable" \
  env GITHUB_ACTIONS=true CI=true PR_BASE_SHA="$BASE_SHA" PR_HEAD_SHA="$HEAD_SHA" TASK_FILE=task.md "$WRAPPER" --mode pr-merge
expect_rejected "ALLOW_PREFIXES Agent-wrapper variable" \
  env GITHUB_ACTIONS=true CI=true PR_BASE_SHA="$BASE_SHA" PR_HEAD_SHA="$HEAD_SHA" ALLOW_PREFIXES=scripts "$WRAPPER" --mode pr-merge

# Hook selection needs the registered pre-commit module; a different version
# or a missing module fails closed before any hook runs.
FAKE_MODULE="$TMP_ROOT/fake-module"
mkdir -p "$FAKE_MODULE/pre_commit"
printf '%s\n' "VERSION = '0.0.0'" >"$FAKE_MODULE/pre_commit/constants.py"
: >"$FAKE_MODULE/pre_commit/__init__.py"
BROKEN_MODULE="$TMP_ROOT/broken-module"
mkdir -p "$BROKEN_MODULE/pre_commit"
: >"$BROKEN_MODULE/pre_commit/__init__.py"
for module_case in mismatched missing; do
  rm -f "$CALL_FILE"
  set +e
  module_error="$(
    cd "$CANDIDATE_REPO"
    if [[ "$module_case" == mismatched ]]; then module_path="$FAKE_MODULE"; else module_path="$BROKEN_MODULE"; fi
    env \
      PATH="$FAKE_BIN:$PATH" \
      PYTHONPATH="$module_path" \
      PYTHONNOUSERSITE=1 \
      FAKE_PRECOMMIT_CALL_FILE="$CALL_FILE" \
      EXPECTED_STYLE_MODE=pr-merge \
      EXPECTED_PR_HOOKS="$EXPECTED_PR_HOOKS" \
      EXPECTED_MERGE_SHA="$MERGE_SHA" \
      GITHUB_ACTIONS=true \
      CI=true \
      PR_BASE_SHA="$BASE_SHA" \
      PR_HEAD_SHA="$HEAD_SHA" \
      "$WRAPPER" --mode pr-merge 2>&1
  )"
  module_exit=$?
  set -e
  [[ "$module_exit" -eq 2 ]] || fail "$module_case pre-commit module returned $module_exit"
  grep -q "pre-commit module" <<<"$module_error" || fail "$module_case pre-commit module was misclassified"
  [[ ! -e "$CALL_FILE" ]] || fail "$module_case pre-commit module invoked hooks"
done

rm -f "$CALL_FILE"
if (
  cd "$CANDIDATE_REPO"
  env \
    PATH="$FAKE_BIN:$PATH" \
    FAKE_PRECOMMIT_CALL_FILE="$CALL_FILE" \
    EXPECTED_STYLE_MODE=pr-merge \
    EXPECTED_PR_HOOKS="$EXPECTED_PR_HOOKS" \
    EXPECTED_MERGE_SHA="$MERGE_SHA" \
    GITHUB_ACTIONS=true \
    CI=true \
    PR_BASE_SHA="$HEAD_SHA" \
    PR_HEAD_SHA="$BASE_SHA" \
    "$WRAPPER" --mode pr-merge
); then
  fail "swapped authenticated parents were accepted"
fi
[[ ! -e "$CALL_FILE" ]] || fail "parent mismatch invoked pre-commit"

(
  cd "$CANDIDATE_REPO"
  env \
    PATH="$FAKE_BIN:$PATH" \
    FAKE_PRECOMMIT_CALL_FILE="$CALL_FILE" \
    EXPECTED_STYLE_MODE=pr-merge \
    EXPECTED_PR_HOOKS="$EXPECTED_PR_HOOKS" \
    EXPECTED_MERGE_SHA="$MERGE_SHA" \
    GITHUB_ACTIONS=true \
    CI=true \
    PR_BASE_SHA="$BASE_SHA" \
    PR_HEAD_SHA="$HEAD_SHA" \
    "$WRAPPER" --mode pr-merge
)

[[ "$(grep -c '^CALL$' "$CALL_FILE")" -eq 1 ]] || fail "unexpected hook invocation count"
! grep -qx -- '--all-files' "$CALL_FILE" || fail "all-files mode was used"
[[ "$(grep -c '^--from-ref$' "$CALL_FILE")" -eq 1 ]] || fail "changed range was not used"
[[ "$(grep -c "^$BASE_SHA$" "$CALL_FILE")" -eq 1 ]] || fail "base SHA drifted"
[[ "$(grep -A1 -x -- '--to-ref' "$CALL_FILE" | tail -1)" == "$MERGE_SHA" ]] || fail "merge candidate was not selected"
! grep -qx "PWD=$CANDIDATE_REPO" "$CALL_FILE" || fail "style checks ran in the source worktree"

set +e
(
  cd "$CANDIDATE_REPO"
  env \
    PATH="$FAKE_BIN:$PATH" \
    FAKE_PRECOMMIT_CALL_FILE="$CALL_FILE" \
    FAKE_PRECOMMIT_EXIT=37 \
    EXPECTED_STYLE_MODE=pr-merge \
    EXPECTED_PR_HOOKS="$EXPECTED_PR_HOOKS" \
    EXPECTED_MERGE_SHA="$MERGE_SHA" \
    GITHUB_ACTIONS=true \
    CI=true \
    PR_BASE_SHA="$BASE_SHA" \
    PR_HEAD_SHA="$HEAD_SHA" \
    "$WRAPPER" --mode pr-merge
)
child_exit=$?
set -e
[[ "$child_exit" -eq 37 ]] || fail "child exit was not propagated"

# A hook that changes the isolated candidate yet reports success is a hidden
# mutator; one that changes it and fails reports its own failure.
for case_exit in 0 1; do
  set +e
  (
    cd "$CANDIDATE_REPO"
    env \
      PATH="$FAKE_BIN:$PATH" \
      FAKE_PRECOMMIT_CALL_FILE="$CALL_FILE" \
      FAKE_PRECOMMIT_MUTATION=worktree \
      FAKE_PRECOMMIT_EXIT="$case_exit" \
      EXPECTED_STYLE_MODE=pr-merge \
      EXPECTED_PR_HOOKS="$EXPECTED_PR_HOOKS" \
    EXPECTED_PR_HOOKS="$EXPECTED_PR_HOOKS" \
      EXPECTED_MERGE_SHA="$MERGE_SHA" \
      GITHUB_ACTIONS=true \
      CI=true \
      PR_BASE_SHA="$BASE_SHA" \
      PR_HEAD_SHA="$HEAD_SHA" \
      "$WRAPPER" --mode pr-merge
  )
  pr_mutation_exit=$?
  set -e
  expected=$([[ "$case_exit" -eq 0 ]] && echo 2 || echo 1)
  [[ "$pr_mutation_exit" -eq "$expected" ]] || fail "pr-merge mutation with hook exit $case_exit returned $pr_mutation_exit"
done

# Local mode must derive its check configuration from the index while leaving
# both the index and the tracked working tree untouched.
git -C "$CANDIDATE_REPO" switch -q --detach "$BASE_SHA"
printf '%s\n' staged-side >"$CANDIDATE_REPO/interaction.md"
sed -i 's/MD013: false/MD013: true/' "$CANDIDATE_REPO/.markdownlint-cli2.yaml"
git -C "$CANDIDATE_REPO" add interaction.md .markdownlint-cli2.yaml
printf '%s\n' unstaged-side >"$CANDIDATE_REPO/interaction.md"
sed -i 's/MD013: true/MD013: false/' "$CANDIDATE_REPO/.markdownlint-cli2.yaml"
printf '%s\n' untracked >"$CANDIDATE_REPO/untracked.txt"
index_before="$(git -C "$CANDIDATE_REPO" diff --cached --binary HEAD)"
worktree_before="$(git -C "$CANDIDATE_REPO" diff --binary)"

expect_rejected "local mode with CI identity" \
  env CI=true "$WRAPPER" --mode local-staged
expect_rejected "local mode with PR identity" \
  env PR_BASE_SHA="$BASE_SHA" "$WRAPPER" --mode local-staged

rm -f "$CALL_FILE"
(
  cd "$CANDIDATE_REPO"
  env \
    PATH="$FAKE_BIN:$PATH" \
    FAKE_PRECOMMIT_CALL_FILE="$CALL_FILE" \
    EXPECTED_STYLE_MODE=local-staged \
    EXPECTED_LOCAL_REPO="$CANDIDATE_REPO" \
    "$WRAPPER" --mode local-staged
)
[[ "$(grep -c '^CALL$' "$CALL_FILE")" -eq 1 ]] || fail "local hook count drifted"
grep -qx -- '--hook-stage' "$CALL_FILE" || fail "local pre-commit stage was not explicit"
grep -qx -- 'pre-commit' "$CALL_FILE" || fail "local hook stage value drifted"
! grep -qx -- '--from-ref' "$CALL_FILE" || fail "local mode used a ref range"
! grep -qx -- '--to-ref' "$CALL_FILE" || fail "local mode used a ref range"
! grep -qx -- '--files' "$CALL_FILE" || fail "local mode supplied caller file paths"
! grep -qx -- '--all-files' "$CALL_FILE" || fail "local mode used all-files"
! grep -qx "PWD=$CANDIDATE_REPO" "$CALL_FILE" || fail "local hooks ran in the source worktree"
[[ "$index_before" == "$(git -C "$CANDIDATE_REPO" diff --cached --binary HEAD)" ]] || fail "local mode changed the index"
[[ "$worktree_before" == "$(git -C "$CANDIDATE_REPO" diff --binary)" ]] || fail "local mode changed tracked working bytes"
[[ "$(cat "$CANDIDATE_REPO/untracked.txt")" == "untracked" ]] || fail "local mode changed untracked bytes"

rm -f "$CALL_FILE"
if (
  cd "$CANDIDATE_REPO"
  env \
    PATH="$FAKE_BIN:$PATH" \
    FAKE_PRECOMMIT_CALL_FILE="$CALL_FILE" \
    FAKE_PRECOMMIT_VERSION=9.9.9 \
    EXPECTED_STYLE_MODE=local-staged \
    EXPECTED_LOCAL_REPO="$CANDIDATE_REPO" \
    "$WRAPPER" --mode local-staged
); then
  fail "unregistered pre-commit version was accepted"
fi
[[ ! -e "$CALL_FILE" ]] || fail "version mismatch invoked pre-commit hooks"

set +e
(
  cd "$CANDIDATE_REPO"
  env \
    PATH="$FAKE_BIN:$PATH" \
    FAKE_PRECOMMIT_CALL_FILE="$CALL_FILE" \
    FAKE_PRECOMMIT_EXIT=37 \
    EXPECTED_STYLE_MODE=local-staged \
    EXPECTED_LOCAL_REPO="$CANDIDATE_REPO" \
    "$WRAPPER" --mode local-staged
)
local_child_exit=$?
set -e
[[ "$local_child_exit" -eq 37 ]] || fail "local child exit was not propagated"

for mutation in worktree index; do
  set +e
  (
    cd "$CANDIDATE_REPO"
    env \
      PATH="$FAKE_BIN:$PATH" \
      FAKE_PRECOMMIT_CALL_FILE="$CALL_FILE" \
      FAKE_PRECOMMIT_MUTATION="$mutation" \
      EXPECTED_STYLE_MODE=local-staged \
      EXPECTED_LOCAL_REPO="$CANDIDATE_REPO" \
      "$WRAPPER" --mode local-staged
  )
  mutation_exit=$?
  set -e
  [[ "$mutation_exit" -eq 2 ]] || fail "$mutation mutation was not rejected"
  set +e
  (
    cd "$CANDIDATE_REPO"
    env \
      PATH="$FAKE_BIN:$PATH" \
      FAKE_PRECOMMIT_CALL_FILE="$CALL_FILE" \
      FAKE_PRECOMMIT_MUTATION="$mutation" \
      FAKE_PRECOMMIT_EXIT=1 \
      EXPECTED_STYLE_MODE=local-staged \
      EXPECTED_LOCAL_REPO="$CANDIDATE_REPO" \
      "$WRAPPER" --mode local-staged
  )
  failed_mutation_exit=$?
  set -e
  [[ "$failed_mutation_exit" -eq 1 ]] || fail "$mutation mutation by a failing hook returned $failed_mutation_exit"
  [[ "$index_before" == "$(git -C "$CANDIDATE_REPO" diff --cached --binary HEAD)" ]] || fail "$mutation mutation escaped into the source index"
  [[ "$worktree_before" == "$(git -C "$CANDIDATE_REPO" diff --binary)" ]] || fail "$mutation mutation escaped into tracked source bytes"
  [[ "$(cat "$CANDIDATE_REPO/untracked.txt")" == "untracked" ]] || fail "$mutation mutation escaped into untracked source bytes"
done

# Cancellation retains a distinct exit and removes the owned temporary worktree.
worktrees_before="$(git -C "$CANDIDATE_REPO" worktree list --porcelain)"
set +e
(
  cd "$CANDIDATE_REPO"
  env PATH="$FAKE_BIN:$PATH" FAKE_PRECOMMIT_CALL_FILE="$CALL_FILE" \
    FAKE_PRECOMMIT_SIGNAL=TERM EXPECTED_STYLE_MODE=local-staged \
    EXPECTED_LOCAL_REPO="$CANDIDATE_REPO" "$WRAPPER" --mode local-staged
)
cancelled_exit=$?
set -e
[[ "$cancelled_exit" -eq 143 ]] || fail "cancellation was not reported as signal exit 143"
[[ "$(git -C "$CANDIDATE_REPO" worktree list --porcelain)" == "$worktrees_before" ]] || \
  fail "cancelled run left an owned worktree"

# A controller-only signal must also stop a checker that stays alive.
set +e
env PATH="$FAKE_BIN:$PATH" FAKE_PRECOMMIT_CALL_FILE="$CALL_FILE" \
  FAKE_PRECOMMIT_SIGNAL=TERM_HANG EXPECTED_STYLE_MODE=local-staged \
  EXPECTED_LOCAL_REPO="$CANDIDATE_REPO" \
  python3 - "$WRAPPER" "$CANDIDATE_REPO" <<'PY'
import os
import pathlib
import signal
import subprocess
import sys

child = subprocess.Popen(
    [sys.argv[1], "--mode", "local-staged"], cwd=sys.argv[2], start_new_session=True
)
try:
    code = child.wait(timeout=5)
except subprocess.TimeoutExpired:
    # The checker may own a different group within this fixture's session.
    marker = pathlib.Path(os.environ["FAKE_PRECOMMIT_CALL_FILE"] + ".pid")
    try:
        checker = int(marker.read_text())
        if os.getsid(checker) == child.pid:
            os.killpg(os.getpgid(checker), signal.SIGKILL)
    except (OSError, ValueError):
        pass
    try:
        os.killpg(child.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    child.wait()
    raise SystemExit(124) from None
raise SystemExit(code)
PY
hanging_exit=$?
set -e
[[ "$hanging_exit" -eq 143 ]] || fail "cancellation waited for a hanging checker"
checker_pid="$(cat "$CALL_FILE.pid")"
! kill -0 "$checker_pid" 2>/dev/null || fail "cancelled checker remains alive"
[[ "$(git -C "$CANDIDATE_REPO" worktree list --porcelain)" == "$worktrees_before" ]] || \
  fail "hanging checker cancellation left an owned worktree"

# An external source-index change invalidates a successful snapshot verdict.
source_tree="$(git -C "$CANDIDATE_REPO" write-tree)"
set +e
(
  cd "$CANDIDATE_REPO"
  env PATH="$FAKE_BIN:$PATH" FAKE_PRECOMMIT_CALL_FILE="$CALL_FILE" \
    FAKE_PRECOMMIT_MUTATION=source-index EXPECTED_STYLE_MODE=local-staged \
    EXPECTED_LOCAL_REPO="$CANDIDATE_REPO" "$WRAPPER" --mode local-staged
)
source_race_exit=$?
set -e
[[ "$source_race_exit" -eq 2 ]] || fail "concurrent source index change reused snapshot PASS"
[[ "$(git -C "$CANDIDATE_REPO" show :interaction.md)" == concurrent ]] || fail "controller overwrote concurrent staged bytes"
git -C "$CANDIDATE_REPO" read-tree "$source_tree"
printf '%s\n' unstaged-side >"$CANDIDATE_REPO/interaction.md"

# Exercise real pre-commit staged semantics with a local, network-free hook.
git init -q -b main "$REAL_REPO"
git -C "$REAL_REPO" config user.name Diagnostic
git -C "$REAL_REPO" config user.email diagnostic@example.invalid
cat >"$REAL_REPO/.pre-commit-config.yaml" <<EOF
repos:
  - repo: local
    hooks:
      - id: staged-content
        name: staged content
        language: system
        entry: python3 verify.py
        files: ^candidate.txt$
EOF
printf '%s\n' 'fix: true' 'config:' '  MD013: false' >"$REAL_REPO/.markdownlint-cli2.yaml"
mkdir -p "$REAL_REPO/scripts"
cp "$REPO_ROOT/scripts/requirements-pre-commit.txt" \
  "$REAL_REPO/scripts/requirements-pre-commit.txt"
cat >"$REAL_REPO/verify.py" <<'PY'
import pathlib
import sys

if pathlib.Path(sys.argv[1]).read_text(encoding="utf-8") != "staged\n":
    raise SystemExit(41)
PY
printf '%s\n' baseline >"$REAL_REPO/candidate.txt"
git -C "$REAL_REPO" add .
git -C "$REAL_REPO" commit -qm "chore: Establish local fixture"
printf '%s\n' staged >"$REAL_REPO/candidate.txt"
git -C "$REAL_REPO" add candidate.txt
printf '%s\n' unstaged >"$REAL_REPO/candidate.txt"
(
  cd "$REAL_REPO"
  "$WRAPPER" --mode local-staged
)
[[ "$(cat "$REAL_REPO/candidate.txt")" == "unstaged" ]] || fail "pre-commit did not restore unstaged bytes"
[[ "$(git -C "$REAL_REPO" show :candidate.txt)" == "staged" ]] || fail "pre-commit changed staged bytes"

# An alternate source index must never become the isolated worktree's index.
alternate_index="$TMP_ROOT/alternate-index"
cp "$REAL_REPO/.git/index" "$alternate_index"
source_tree="$(git -C "$REAL_REPO" write-tree)"
(
  cd "$REAL_REPO"
  env GIT_INDEX_FILE="$alternate_index" "$WRAPPER" --mode local-staged
)
[[ "$(git -C "$REAL_REPO" write-tree)" == "$source_tree" ]] || fail "alternate run changed the default source index"
[[ "$(GIT_INDEX_FILE="$alternate_index" git -C "$REAL_REPO" write-tree)" == "$source_tree" ]] || fail "alternate run changed its source index"
[[ "$(cat "$REAL_REPO/candidate.txt")" == unstaged ]] || fail "alternate run changed source working bytes"

# Characterization: a bad staged version stays rejected when the worktree copy
# was fixed afterwards, because the hook sees the index, not the worktree.
printf '%s\n' bad >"$REAL_REPO/candidate.txt"
git -C "$REAL_REPO" add candidate.txt
printf '%s\n' staged >"$REAL_REPO/candidate.txt"
set +e
(
  cd "$REAL_REPO"
  "$WRAPPER" --mode local-staged >/dev/null 2>&1
)
fixed_worktree_exit=$?
set -e
[[ "$fixed_worktree_exit" -ne 0 ]] || fail "bad staged bytes passed because the worktree was fixed"
[[ "$(git -C "$REAL_REPO" show :candidate.txt)" == "bad" ]] || fail "rejected run changed staged bytes"
[[ "$(cat "$REAL_REPO/candidate.txt")" == "staged" ]] || fail "rejected run changed the fixed worktree bytes"

git -C "$REAL_REPO" reset -q --hard HEAD
rm -f "$CALL_FILE"
empty_output="$(env -C "$REAL_REPO" "$WRAPPER" --mode local-staged)"
grep -q 'NOT_APPLICABLE: local staged input is empty' <<<"$empty_output" || \
  fail "valid empty index was not explicitly not applicable"
[[ ! -e "$CALL_FILE" ]] || fail "empty index invoked pre-commit"
printf '%s\n' invalid-index >"$REAL_REPO/corrupt-index"
set +e
inspection_error="$(
  (
  cd "$REAL_REPO"
  env GIT_INDEX_FILE="$REAL_REPO/corrupt-index" \
    "$WRAPPER" --mode local-staged
  ) 2>&1
)"
inspection_exit=$?
set -e
[[ "$inspection_exit" -eq 2 ]] || fail "index inspection error did not fail closed"
grep -q "local staged input could not be inspected" <<<"$inspection_error" || \
  fail "index inspection error was misclassified"

unborn="$TMP_ROOT/unborn"
mkdir -p "$unborn/scripts"
git init -q -b main "$unborn"
cp "$REAL_REPO/.pre-commit-config.yaml" "$REAL_REPO/.markdownlint-cli2.yaml" \
  "$REAL_REPO/verify.py" "$unborn/"
cp "$REPO_ROOT/scripts/requirements-pre-commit.txt" "$unborn/scripts/"
printf '%s\n' staged >"$unborn/candidate.txt"
git -C "$unborn" add .
unborn_tree="$(git -C "$unborn" write-tree)"
(
  cd "$unborn"
  "$WRAPPER" --mode local-staged
)
[[ "$(git -C "$unborn" write-tree)" == "$unborn_tree" ]] || fail "unborn source index changed"
! git -C "$unborn" rev-parse --verify HEAD >/dev/null 2>&1 || fail "controller created an unborn source commit"

echo "PASS: CI pre-commit wrapper contract"
