#!/usr/bin/env bash
set -euo pipefail

TASK_FILE=""
ALLOW_PREFIXES=()

readonly EXIT_USAGE=2
readonly EXIT_WORKTREE=3
readonly EXIT_TASK=4
readonly EXIT_DIRTY=5
readonly EXIT_SNAPSHOT=6
readonly EXIT_UNEXPECTED_PATHS=20

usage() {
  echo "Usage: $0 --task <tracked-task-path> --allow-prefix <repo-relative-prefix> [--allow-prefix ...]" >&2
}

die() {
  local status="$1"
  shift
  echo "ERROR: $*" >&2
  exit "$status"
}

is_safe_relative_path() {
  local value="$1"

  [[ -n "$value" ]] || return 1
  [[ "$value" != /* ]] || return 1
  [[ "$value" != *$'\n'* && "$value" != *$'\r'* ]] || return 1
  [[ ! "$value" =~ (^|/)\.\.?(/|$) ]] || return 1
}

normalize_prefix() {
  local prefix="$1"

  while [[ "$prefix" == */ ]]; do
    prefix="${prefix%/}"
  done
  printf '%s' "$prefix"
}

path_has_symlink_component() {
  local path="$1"
  local current=""
  local component
  local -a components=()

  IFS='/' read -r -a components <<<"$path"
  for component in "${components[@]}"; do
    current="${current:+$current/}$component"
    if [[ -L "$current" ]]; then
      return 0
    fi
    if [[ ! -e "$current" ]]; then
      return 1
    fi
  done
  return 1
}

snapshot_changed_paths() {
  local raw_file="$1"
  local output_file="$2"
  local entry status path original
  local malformed=0

  : >"$output_file" || return 1
  if ! git status --porcelain=v1 -z --untracked-files=all >"$raw_file"; then
    return 1
  fi
  while IFS= read -r -d '' entry; do
    status="${entry:0:2}"
    path="${entry:3}"
    printf '%s\0' "$path" >>"$output_file" || return 1
    if [[ "$status" == *R* || "$status" == *C* ]]; then
      if ! IFS= read -r -d '' original; then
        malformed=1
        break
      fi
      printf '%s\0' "$original" >>"$output_file" || return 1
    fi
  done <"$raw_file"
  [[ "$malformed" -eq 0 ]] || return 1
  sort -zu "$output_file" -o "$output_file" || return 1
}

count_paths() {
  local input_file="$1"
  local count=0 path

  while IFS= read -r -d '' path; do
    count=$((count + 1))
  done <"$input_file"
  printf '%d' "$count"
}

print_paths() {
  local label="$1"
  local input_file="$2"
  local first=1 path

  printf '%s=' "$label"
  while IFS= read -r -d '' path; do
    if [[ "$first" -eq 0 ]]; then
      printf ','
    fi
    printf '%q' "$path"
    first=0
  done <"$input_file"
  if [[ "$first" -eq 1 ]]; then
    printf '(none)'
  fi
  printf '\n'
}

path_is_allowed() {
  local path="$1"
  local prefix

  for prefix in "${ALLOW_PREFIXES[@]}"; do
    if [[ "$path" == "$prefix" || "$path" == "$prefix/"* ]]; then
      return 0
    fi
  done
  return 1
}

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --task)
      [[ "$#" -ge 2 ]] || die "$EXIT_USAGE" "--task requires a value"
      [[ -z "$TASK_FILE" ]] || die "$EXIT_USAGE" "--task may be supplied only once"
      TASK_FILE="$2"
      shift 2
      ;;
    --allow-prefix)
      [[ "$#" -ge 2 ]] || die "$EXIT_USAGE" "--allow-prefix requires a value"
      ALLOW_PREFIXES+=("$2")
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      usage
      die "$EXIT_USAGE" "unknown argument: $1"
      ;;
  esac
done

[[ -n "$TASK_FILE" ]] || die "$EXIT_USAGE" "--task is required"
[[ "${#ALLOW_PREFIXES[@]}" -gt 0 ]] || die "$EXIT_USAGE" "at least one --allow-prefix is required"
is_safe_relative_path "$TASK_FILE" || die "$EXIT_TASK" "task path must be repository-relative and non-traversing"

for index in "${!ALLOW_PREFIXES[@]}"; do
  prefix="${ALLOW_PREFIXES[$index]}"
  is_safe_relative_path "$prefix" || die "$EXIT_USAGE" "allow prefix must be non-empty, repository-relative, and non-traversing"
  prefix="$(normalize_prefix "$prefix")"
  [[ -n "$prefix" ]] || die "$EXIT_USAGE" "allow prefix must not resolve to an empty path"
  ALLOW_PREFIXES[index]="$prefix"
done

if ! REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"; then
  die "$EXIT_WORKTREE" "run this command inside a Git repository"
fi
cd "$REPO_ROOT"

GIT_DIR="$(git rev-parse --absolute-git-dir)"
GIT_COMMON_DIR="$(git rev-parse --path-format=absolute --git-common-dir)"
[[ "$GIT_DIR" != "$GIT_COMMON_DIR" ]] || die "$EXIT_WORKTREE" "an isolated linked worktree is required; primary checkout rejected"

[[ "$TASK_FILE" == docs/04.execution/tasks/* ]] || die "$EXIT_TASK" "--task must be under docs/04.execution/tasks/"
[[ ! -L "$TASK_FILE" ]] || die "$EXIT_TASK" "--task must not be a symlink"
path_has_symlink_component "$TASK_FILE" && die "$EXIT_TASK" "--task path must not contain a symlink component"
[[ -f "$TASK_FILE" ]] || die "$EXIT_TASK" "tracked task file does not exist: $TASK_FILE"
if ! TASK_INDEX_ENTRY="$(git ls-files --stage -- "$TASK_FILE")"; then
  die "$EXIT_TASK" "unable to inspect tracked task index entry"
fi
[[ -n "$TASK_INDEX_ENTRY" && "$TASK_INDEX_ENTRY" != *$'\n'* ]] || die "$EXIT_TASK" "--task must name exactly one tracked task index entry"
TASK_INDEX_MODE="${TASK_INDEX_ENTRY%% *}"
[[ "$TASK_INDEX_MODE" == "100644" || "$TASK_INDEX_MODE" == "100755" ]] || die "$EXIT_TASK" "--task must be a regular Git blob (mode 100644 or 100755)"
TASK_INDEX_PATH="${TASK_INDEX_ENTRY#*$'\t'}"
[[ "$TASK_INDEX_PATH" == "$TASK_FILE" ]] || die "$EXIT_TASK" "--task path must match its canonical Git index path exactly"

for prefix in "${ALLOW_PREFIXES[@]}"; do
  path_has_symlink_component "$prefix" && die "$EXIT_USAGE" "allow prefix must not contain a symlink component: $prefix"
done

command -v pre-commit >/dev/null 2>&1 || die 127 "pre-commit is required on PATH"

TEMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/agent-precommit.XXXXXX")"
BEFORE_RAW_FILE="$TEMP_DIR/before.raw"
BEFORE_FILE="$TEMP_DIR/before.paths"
AFTER_RAW_FILE="$TEMP_DIR/after.raw"
AFTER_FILE="$TEMP_DIR/after.paths"
CHANGED_FILE="$TEMP_DIR/changed.paths"
UNEXPECTED_FILE="$TEMP_DIR/unexpected.paths"
HOOK_OUTPUT_FILE="$TEMP_DIR/hook.output"

# Invoked directly by the signal handler and indirectly by the EXIT trap.
# shellcheck disable=SC2329
cleanup() {
  rm -rf -- "$TEMP_DIR"
}

# Signal traps invoke this function indirectly. Cleanup is limited to the
# wrapper-owned mktemp directory, then the original signal is re-raised.
# shellcheck disable=SC2329
handle_signal() {
  local signal_name="$1"
  local conventional_status="$2"

  trap - EXIT HUP INT TERM
  cleanup
  kill -s "$signal_name" "$$"
  exit "$conventional_status"
}

trap cleanup EXIT
trap 'handle_signal HUP 129' HUP
trap 'handle_signal INT 130' INT
trap 'handle_signal TERM 143' TERM

if ! snapshot_changed_paths "$BEFORE_RAW_FILE" "$BEFORE_FILE"; then
  die "$EXIT_SNAPSHOT" "before-hook Git status snapshot failed; hook was not run"
fi
BEFORE_COUNT="$(count_paths "$BEFORE_FILE")"
[[ "$BEFORE_COUNT" -eq 0 ]] || die "$EXIT_DIRTY" "wrapper requires a clean linked worktree before hook execution"

if pre-commit run --all-files --show-diff-on-failure >"$HOOK_OUTPUT_FILE" 2>&1; then
  HOOK_EXIT=0
  HOOK_RESULT="passed"
else
  HOOK_EXIT=$?
  HOOK_RESULT="failed"
fi

if ! snapshot_changed_paths "$AFTER_RAW_FILE" "$AFTER_FILE"; then
  echo "agent_precommit_command=pre-commit run --all-files --show-diff-on-failure"
  printf 'task=%q\n' "$TASK_FILE"
  printf 'allow_prefixes='
  printf '%q,' "${ALLOW_PREFIXES[@]}"
  printf '\n'
  echo "hook_result=$HOOK_RESULT hook_exit=$HOOK_EXIT"
  echo "snapshot_result=failed-after-hook"
  echo "observation=git-visible-non-ignored-repository-status"
  exit "$EXIT_SNAPSHOT"
fi
if ! comm -z -13 "$BEFORE_FILE" "$AFTER_FILE" >"$CHANGED_FILE"; then
  echo "agent_precommit_command=pre-commit run --all-files --show-diff-on-failure"
  printf 'task=%q\n' "$TASK_FILE"
  printf 'allow_prefixes='
  printf '%q,' "${ALLOW_PREFIXES[@]}"
  printf '\n'
  echo "hook_result=$HOOK_RESULT hook_exit=$HOOK_EXIT"
  echo "snapshot_result=failed-after-hook"
  echo "observation=git-visible-non-ignored-repository-status"
  exit "$EXIT_SNAPSHOT"
fi
: >"$UNEXPECTED_FILE"
while IFS= read -r -d '' changed_path; do
  if ! path_is_allowed "$changed_path"; then
    printf '%s\0' "$changed_path" >>"$UNEXPECTED_FILE"
  fi
done <"$CHANGED_FILE"

AFTER_COUNT="$(count_paths "$AFTER_FILE")"
CHANGED_COUNT="$(count_paths "$CHANGED_FILE")"
UNEXPECTED_COUNT="$(count_paths "$UNEXPECTED_FILE")"

echo "agent_precommit_command=pre-commit run --all-files --show-diff-on-failure"
printf 'task=%q\n' "$TASK_FILE"
printf 'allow_prefixes='
for index in "${!ALLOW_PREFIXES[@]}"; do
  [[ "$index" -eq 0 ]] || printf ','
  printf '%q' "${ALLOW_PREFIXES[$index]}"
done
printf '\n'
echo "hook_result=$HOOK_RESULT hook_exit=$HOOK_EXIT"
echo "snapshot_result=passed"
echo "observation=git-visible-non-ignored-repository-status"
echo "before_count=$BEFORE_COUNT after_count=$AFTER_COUNT changed_count=$CHANGED_COUNT unexpected_count=$UNEXPECTED_COUNT"
print_paths "before_paths" "$BEFORE_FILE"
print_paths "after_paths" "$AFTER_FILE"
print_paths "changed_paths" "$CHANGED_FILE"
print_paths "unexpected_paths" "$UNEXPECTED_FILE"

if [[ "$UNEXPECTED_COUNT" -gt 0 ]]; then
  exit "$EXIT_UNEXPECTED_PATHS"
fi
exit "$HOOK_EXIT"
