#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
WRAPPER="$REPO_ROOT/scripts/validation/run-ci-precommit.sh"
TMP_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/test-ci-precommit.XXXXXX")"
FAKE_BIN="$TMP_ROOT/bin"
CALL_FILE="$TMP_ROOT/call"
CANDIDATE_REPO="$TMP_ROOT/candidate"

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

# The single-quoted entries are the literal body of the generated fake command.
# shellcheck disable=SC2016
printf '%s\n' \
  '#!/usr/bin/env bash' \
  'set -euo pipefail' \
  'scratch_root="$(cd "$PWD/.." && pwd)"' \
  'readonly_config="$scratch_root/pre-commit-check.yaml"' \
  'markdown_config="$scratch_root/markdownlint-check.yaml"' \
  'test -f "$readonly_config" && test -f "$markdown_config"' \
  'test "$(git rev-parse HEAD)" = "${EXPECTED_MERGE_SHA:?}"' \
  'grep -q "^  MD013: true$" "$markdown_config"' \
  'grep -q "^base-side$" interaction.md' \
  'grep -q "^feature-side$" interaction.md' \
  '! grep -q "id: end-of-file-fixer" "$readonly_config"' \
  '! grep -q "id: trailing-whitespace" "$readonly_config"' \
  'grep -A8 "id: mixed-line-ending" "$readonly_config" | grep -q -- "--fix=no"' \
  'grep -A8 "id: ruff-format" "$readonly_config" | grep -q -- "--check"' \
  'grep -A8 "id: markdownlint-cli2" "$readonly_config" | grep -q "$markdown_config"' \
  'grep -q "^fix: false$" "$markdown_config"' \
  "printf \"%s\\n\" \"CALL\" \"PWD=\$PWD\" \"SKIP=\${SKIP-}\" \"\$@\" >>\"\${FAKE_PRECOMMIT_CALL_FILE:?}\"" \
  "exit \"\${FAKE_PRECOMMIT_EXIT:-0}\"" \
  >"$FAKE_BIN/pre-commit"
chmod +x "$FAKE_BIN/pre-commit"

git init -q -b main "$CANDIDATE_REPO"
git -C "$CANDIDATE_REPO" config user.name "Diagnostic"
git -C "$CANDIDATE_REPO" config user.email "diagnostic@example.invalid"
cp "$REPO_ROOT/.pre-commit-config.yaml" "$CANDIDATE_REPO/.pre-commit-config.yaml"
cp "$REPO_ROOT/.markdownlint-cli2.yaml" "$CANDIDATE_REPO/.markdownlint-cli2.yaml"
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
git -C "$CANDIDATE_REPO" merge -q --no-ff feature -m "Merge candidate"
MERGE_SHA="$(git -C "$CANDIDATE_REPO" rev-parse HEAD)"

expect_rejected "missing GITHUB_ACTIONS" \
  env CI=true PR_BASE_SHA="$BASE_SHA" PR_HEAD_SHA="$HEAD_SHA" "$WRAPPER"
expect_rejected "missing CI" \
  env GITHUB_ACTIONS=true PR_BASE_SHA="$BASE_SHA" PR_HEAD_SHA="$HEAD_SHA" "$WRAPPER"
expect_rejected "false GITHUB_ACTIONS" \
  env GITHUB_ACTIONS=false CI=true PR_BASE_SHA="$BASE_SHA" PR_HEAD_SHA="$HEAD_SHA" "$WRAPPER"
expect_rejected "false CI" \
  env GITHUB_ACTIONS=true CI=false PR_BASE_SHA="$BASE_SHA" PR_HEAD_SHA="$HEAD_SHA" "$WRAPPER"
expect_rejected "missing PR_BASE_SHA" \
  env GITHUB_ACTIONS=true CI=true PR_HEAD_SHA="$HEAD_SHA" "$WRAPPER"
expect_rejected "abbreviated PR_BASE_SHA" \
  env GITHUB_ACTIONS=true CI=true PR_BASE_SHA=0123456 PR_HEAD_SHA="$HEAD_SHA" "$WRAPPER"
expect_rejected "missing PR_HEAD_SHA" \
  env GITHUB_ACTIONS=true CI=true PR_BASE_SHA="$BASE_SHA" "$WRAPPER"
expect_rejected "abbreviated PR_HEAD_SHA" \
  env GITHUB_ACTIONS=true CI=true PR_BASE_SHA="$BASE_SHA" PR_HEAD_SHA=abcdef "$WRAPPER"
expect_rejected "identical PR revisions" \
  env GITHUB_ACTIONS=true CI=true PR_BASE_SHA="$BASE_SHA" PR_HEAD_SHA="$BASE_SHA" "$WRAPPER"
expect_rejected "caller-supplied SKIP" \
  env GITHUB_ACTIONS=true CI=true PR_BASE_SHA="$BASE_SHA" PR_HEAD_SHA="$HEAD_SHA" SKIP=public-validation-changed "$WRAPPER"
expect_rejected "empty caller-supplied SKIP" \
  env GITHUB_ACTIONS=true CI=true PR_BASE_SHA="$BASE_SHA" PR_HEAD_SHA="$HEAD_SHA" SKIP= "$WRAPPER"
expect_rejected "positional argument" \
  env GITHUB_ACTIONS=true CI=true PR_BASE_SHA="$BASE_SHA" PR_HEAD_SHA="$HEAD_SHA" "$WRAPPER" --all-files
expect_rejected "TASK_FILE Agent-wrapper variable" \
  env GITHUB_ACTIONS=true CI=true PR_BASE_SHA="$BASE_SHA" PR_HEAD_SHA="$HEAD_SHA" TASK_FILE=task.md "$WRAPPER"
expect_rejected "ALLOW_PREFIXES Agent-wrapper variable" \
  env GITHUB_ACTIONS=true CI=true PR_BASE_SHA="$BASE_SHA" PR_HEAD_SHA="$HEAD_SHA" ALLOW_PREFIXES=scripts "$WRAPPER"

rm -f "$CALL_FILE"
if (
  cd "$CANDIDATE_REPO"
  env \
    PATH="$FAKE_BIN:$PATH" \
    FAKE_PRECOMMIT_CALL_FILE="$CALL_FILE" \
    EXPECTED_MERGE_SHA="$MERGE_SHA" \
    GITHUB_ACTIONS=true \
    CI=true \
    PR_BASE_SHA="$HEAD_SHA" \
    PR_HEAD_SHA="$BASE_SHA" \
    "$WRAPPER"
); then
  fail "swapped authenticated parents were accepted"
fi
[[ ! -e "$CALL_FILE" ]] || fail "parent mismatch invoked pre-commit"

(
  cd "$CANDIDATE_REPO"
  env \
    PATH="$FAKE_BIN:$PATH" \
    FAKE_PRECOMMIT_CALL_FILE="$CALL_FILE" \
    EXPECTED_MERGE_SHA="$MERGE_SHA" \
    GITHUB_ACTIONS=true \
    CI=true \
    PR_BASE_SHA="$BASE_SHA" \
    PR_HEAD_SHA="$HEAD_SHA" \
    "$WRAPPER"
)

[[ "$(grep -c '^CALL$' "$CALL_FILE")" -eq 1 ]] || fail "unexpected hook invocation count"
! grep -qx -- '--all-files' "$CALL_FILE" || fail "all-files mode was used"
[[ "$(grep -c '^--from-ref$' "$CALL_FILE")" -eq 1 ]] || fail "changed range was not used"
[[ "$(grep -c "^$BASE_SHA$" "$CALL_FILE")" -eq 1 ]] || fail "base SHA drifted"
[[ "$(grep -c "^$HEAD_SHA$" "$CALL_FILE")" -eq 1 ]] || fail "head SHA drifted"
! grep -qx "PWD=$CANDIDATE_REPO" "$CALL_FILE" || fail "style checks ran in the source worktree"

set +e
(
  cd "$CANDIDATE_REPO"
  env \
    PATH="$FAKE_BIN:$PATH" \
    FAKE_PRECOMMIT_CALL_FILE="$CALL_FILE" \
    FAKE_PRECOMMIT_EXIT=37 \
    EXPECTED_MERGE_SHA="$MERGE_SHA" \
    GITHUB_ACTIONS=true \
    CI=true \
    PR_BASE_SHA="$BASE_SHA" \
    PR_HEAD_SHA="$HEAD_SHA" \
    "$WRAPPER"
)
child_exit=$?
set -e
[[ "$child_exit" -eq 37 ]] || fail "child exit was not propagated"

echo "PASS: CI pre-commit wrapper contract"
