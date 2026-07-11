#!/usr/bin/env bash
set -euo pipefail

TASK_FILE=""
ALLOW_PREFIXES=()

readonly EXIT_USAGE=2
readonly EXIT_WORKTREE=3
readonly EXIT_TASK=4
readonly EXIT_DIRTY=5
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

snapshot_changed_paths() {
  local output_file="$1"
  local entry status path original

  : >"$output_file"
  while IFS= read -r -d '' entry; do
    status="${entry:0:2}"
    path="${entry:3}"
    printf '%s\0' "$path" >>"$output_file"
    if [[ "$status" == *R* || "$status" == *C* ]]; then
      IFS= read -r -d '' original || die "$EXIT_WORKTREE" "malformed Git rename/copy status"
      printf '%s\0' "$original" >>"$output_file"
    fi
  done < <(git status --porcelain=v1 -z --untracked-files=all)
  sort -zu "$output_file" -o "$output_file"
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
[[ -f "$TASK_FILE" ]] || die "$EXIT_TASK" "tracked task file does not exist: $TASK_FILE"
git ls-files --error-unmatch -- "$TASK_FILE" >/dev/null 2>&1 || die "$EXIT_TASK" "--task must name a tracked task file"

command -v pre-commit >/dev/null 2>&1 || die 127 "pre-commit is required on PATH"

BEFORE_FILE="$(mktemp "${TMPDIR:-/tmp}/agent-precommit-before.XXXXXX")"
AFTER_FILE="$(mktemp "${TMPDIR:-/tmp}/agent-precommit-after.XXXXXX")"
CHANGED_FILE="$(mktemp "${TMPDIR:-/tmp}/agent-precommit-changed.XXXXXX")"
UNEXPECTED_FILE="$(mktemp "${TMPDIR:-/tmp}/agent-precommit-unexpected.XXXXXX")"
HOOK_OUTPUT_FILE="$(mktemp "${TMPDIR:-/tmp}/agent-precommit-hook.XXXXXX")"

trap 'rm -f "$BEFORE_FILE" "$AFTER_FILE" "$CHANGED_FILE" "$UNEXPECTED_FILE" "$HOOK_OUTPUT_FILE"' EXIT HUP INT TERM

snapshot_changed_paths "$BEFORE_FILE"
BEFORE_COUNT="$(count_paths "$BEFORE_FILE")"
[[ "$BEFORE_COUNT" -eq 0 ]] || die "$EXIT_DIRTY" "wrapper requires a clean linked worktree before hook execution"

if pre-commit run --all-files --show-diff-on-failure >"$HOOK_OUTPUT_FILE" 2>&1; then
  HOOK_EXIT=0
  HOOK_RESULT="passed"
else
  HOOK_EXIT=$?
  HOOK_RESULT="failed"
fi

snapshot_changed_paths "$AFTER_FILE"
comm -z -13 "$BEFORE_FILE" "$AFTER_FILE" >"$CHANGED_FILE"
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
echo "before_count=$BEFORE_COUNT after_count=$AFTER_COUNT changed_count=$CHANGED_COUNT unexpected_count=$UNEXPECTED_COUNT"
print_paths "before_paths" "$BEFORE_FILE"
print_paths "after_paths" "$AFTER_FILE"
print_paths "changed_paths" "$CHANGED_FILE"
print_paths "unexpected_paths" "$UNEXPECTED_FILE"

if [[ "$UNEXPECTED_COUNT" -gt 0 ]]; then
  exit "$EXIT_UNEXPECTED_PATHS"
fi
exit "$HOOK_EXIT"
