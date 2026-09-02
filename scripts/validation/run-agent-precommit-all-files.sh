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
readonly MAX_DIAGNOSTIC_OUTPUT_BYTES=1048576

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

load_tracked_hook_ids() {
  local config_path="$1"
  local output_file="$2"
  local config_index_entry config_index_mode config_index_path
  local line hook_id previous_id=""
  local malformed=0
  local id_line_re='^[[:space:]]*-[[:space:]]+id:'
  local valid_id_line_re='^[[:space:]]*-[[:space:]]+id:[[:space:]]*([A-Za-z0-9][A-Za-z0-9._-]{0,63})[[:space:]]*$'

  : >"$output_file" || return 1
  [[ -f "$config_path" && ! -L "$config_path" ]] || return 1
  path_has_symlink_component "$config_path" && return 1

  if ! config_index_entry="$(git ls-files --stage -- "$config_path")"; then
    return 1
  fi
  [[ -n "$config_index_entry" && "$config_index_entry" != *$'\n'* ]] || return 1
  config_index_mode="${config_index_entry%% *}"
  [[ "$config_index_mode" == "100644" || "$config_index_mode" == "100755" ]] || return 1
  config_index_path="${config_index_entry#*$'\t'}"
  [[ "$config_index_path" == "$config_path" ]] || return 1

  while IFS= read -r line || [[ -n "$line" ]]; do
    if [[ "$line" =~ $id_line_re ]]; then
      if [[ "$line" =~ $valid_id_line_re ]]; then
        hook_id="${BASH_REMATCH[1]}"
        printf '%s\n' "$hook_id" >>"$output_file" || return 1
      else
        malformed=1
      fi
    fi
  done <"$config_path"
  [[ "$malformed" -eq 0 && -s "$output_file" ]] || return 1

  sort "$output_file" -o "$output_file" || return 1
  while IFS= read -r hook_id; do
    if [[ -n "$previous_id" && "$hook_id" == "$previous_id" ]]; then
      return 1
    fi
    previous_id="$hook_id"
  done <"$output_file"
}

derive_first_failure() {
  local output_file="$1"
  local hook_ids_file="$2"
  local nul_free_file="$3"
  local output_size line hook_id registered_id raw_exit
  local candidate_id="" candidate_detail="" expected=""
  local failure_headers=0 hook_metadata_lines=0 detail_metadata_lines=0
  local valid_blocks=0 malformed=0 registered_matches=0
  local failure_header_re='^.*\.{3,}Failed$'
  local hook_id_re='^- hook id: ([A-Za-z0-9][A-Za-z0-9._-]{0,63})$'
  local numeric_exit_re='^- exit code: ([0-9]{1,3})$'

  if ! output_size="$(wc -c <"$output_file")"; then
    return 1
  fi
  [[ "$output_size" =~ ^[0-9]+$ ]] || return 1
  [[ "$output_size" -le "$MAX_DIAGNOSTIC_OUTPUT_BYTES" ]] || return 1

  if ! LC_ALL=C tr -d '\000' <"$output_file" >"$nul_free_file"; then
    return 1
  fi
  cmp -s -- "$output_file" "$nul_free_file" || return 1

  while IFS= read -r line || [[ -n "$line" ]]; do
    if [[ "$expected" == "hook_id" ]]; then
      if [[ "$line" =~ $hook_id_re ]]; then
        hook_metadata_lines=$((hook_metadata_lines + 1))
        candidate_id="${BASH_REMATCH[1]}"
        expected="detail"
        continue
      fi
      malformed=1
      expected=""
    elif [[ "$expected" == "detail" ]]; then
      if [[ "$line" =~ $numeric_exit_re ]]; then
        detail_metadata_lines=$((detail_metadata_lines + 1))
        raw_exit="${BASH_REMATCH[1]}"
        if [[ $((10#$raw_exit)) -le 255 ]]; then
          candidate_detail="exit_$((10#$raw_exit))"
          valid_blocks=$((valid_blocks + 1))
        else
          malformed=1
        fi
        expected=""
        continue
      fi
      if [[ "$line" == "- files were modified by this hook" ]]; then
        detail_metadata_lines=$((detail_metadata_lines + 1))
        candidate_detail="files_modified"
        valid_blocks=$((valid_blocks + 1))
        expected=""
        continue
      fi
      malformed=1
      expected=""
    fi

    if [[ "$line" =~ $failure_header_re ]]; then
      failure_headers=$((failure_headers + 1))
      expected="hook_id"
    elif [[ "$line" == "- hook id:"* ]]; then
      hook_metadata_lines=$((hook_metadata_lines + 1))
      malformed=1
    elif [[ "$line" == "- exit code:"* || "$line" == "- files were modified by this hook"* ]]; then
      detail_metadata_lines=$((detail_metadata_lines + 1))
      malformed=1
    fi
  done <"$output_file"

  [[ -z "$expected" ]] || malformed=1
  [[ "$malformed" -eq 0 ]] || return 1
  [[ "$failure_headers" -eq 1 ]] || return 1
  [[ "$hook_metadata_lines" -eq 1 ]] || return 1
  [[ "$detail_metadata_lines" -eq 1 ]] || return 1
  [[ "$valid_blocks" -eq 1 ]] || return 1

  while IFS= read -r registered_id; do
    if [[ "$registered_id" == "$candidate_id" ]]; then
      registered_matches=$((registered_matches + 1))
    fi
  done <"$hook_ids_file"
  [[ "$registered_matches" -eq 1 ]] || return 1

  printf '(hook_id=%s,detail=%s)' "$candidate_id" "$candidate_detail"
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

[[ "$TASK_FILE" =~ ^docs/03\.specs/[0-9]{4}-[a-z0-9]([a-z0-9-]*[a-z0-9])?/tasks/tsk-[0-9]{4}-[a-z0-9]([a-z0-9-]*[a-z0-9])?\.md$ ]] || die "$EXIT_TASK" "--task must name a canonical numbered Task under docs/03.specs/####-<slug>/tasks/"
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
HOOK_OUTPUT_NUL_FREE_FILE="$TEMP_DIR/hook-output.nul-free"
HOOK_IDS_FILE="$TEMP_DIR/hook-ids"

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

HOOK_ID_REGISTRY_READY=0
if load_tracked_hook_ids ".pre-commit-config.yaml" "$HOOK_IDS_FILE"; then
  HOOK_ID_REGISTRY_READY=1
fi

if pre-commit run --all-files --show-diff-on-failure >"$HOOK_OUTPUT_FILE" 2>&1; then
  HOOK_EXIT=0
  HOOK_RESULT="passed"
else
  HOOK_EXIT=$?
  HOOK_RESULT="failed"
fi

if [[ "$HOOK_EXIT" -eq 0 ]]; then
  FIRST_FAILURE="not_applicable"
else
  FIRST_FAILURE="unavailable"
  if [[ "$HOOK_ID_REGISTRY_READY" -eq 1 ]]; then
    if SAFE_FAILURE="$(
      derive_first_failure "$HOOK_OUTPUT_FILE" "$HOOK_IDS_FILE" "$HOOK_OUTPUT_NUL_FREE_FILE"
    )"; then
      FIRST_FAILURE="$SAFE_FAILURE"
    fi
  fi
fi

if ! snapshot_changed_paths "$AFTER_RAW_FILE" "$AFTER_FILE"; then
  echo "agent_precommit_command=pre-commit run --all-files --show-diff-on-failure"
  printf 'task=%q\n' "$TASK_FILE"
  printf 'allow_prefixes='
  printf '%q,' "${ALLOW_PREFIXES[@]}"
  printf '\n'
  echo "hook_result=$HOOK_RESULT hook_exit=$HOOK_EXIT"
  printf 'first_failure=%s\n' "$FIRST_FAILURE"
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
  printf 'first_failure=%s\n' "$FIRST_FAILURE"
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
printf 'first_failure=%s\n' "$FIRST_FAILURE"
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
