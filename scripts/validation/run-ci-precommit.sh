#!/usr/bin/env bash
set -euo pipefail

# Read-only style/static controller for two distinct inputs: the local Git index
# immediately before commit, and the authenticated hosted PR merge candidate.

die() {
  echo "ERROR: $1" >&2
  exit 2
}

[[ "$#" -eq 2 && "$1" == "--mode" ]] || die "exactly --mode <mode> is required"
mode="$2"
[[ "$mode" == "local-staged" || "$mode" == "pr-merge" ]] || die "unknown mode"
[[ -z "${TASK_FILE+x}" ]] || die "Agent wrapper variable TASK_FILE is not accepted"
[[ -z "${ALLOW_PREFIXES+x}" ]] || die "Agent wrapper variable ALLOW_PREFIXES is not accepted"
[[ -z "${SKIP+x}" ]] || die "SKIP is not accepted"

repository_root="$(git rev-parse --show-toplevel)" || die "repository root unavailable"
scratch="$(mktemp -d "${TMPDIR:-/tmp}/ci-style.XXXXXX")"
checkout=""
checker_pid=""
cleanup() {
  if [[ -n "$checker_pid" ]]; then
    # The checker owns this process group; never signal the caller's group.
    kill -TERM -- "-$checker_pid" 2>/dev/null || true
    sleep 0.1
    kill -KILL -- "-$checker_pid" 2>/dev/null || true
    wait "$checker_pid" 2>/dev/null || true
  fi
  if [[ -n "$checkout" ]]; then
    git -C "$repository_root" worktree remove --force "$checkout" >/dev/null 2>&1 || true
  fi
  rm -rf -- "$scratch"
}
trap cleanup EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

run_pre_commit() {
  local child_exit
  # Job control gives only this background checker its own process group.
  set -m
  (
    cd "$checkout"
    exec pre-commit "$@"
  ) &
  checker_pid=$!
  set +m
  wait "$checker_pid"
  child_exit=$?
  checker_pid=""
  return "$child_exit"
}

render_readonly_config() {
  local source_config="$1"
  local markdown_source="$2"
  python3 - "$source_config" "$markdown_source" "$scratch" <<'PY'
import pathlib
import sys

import yaml

source_config = pathlib.Path(sys.argv[1])
markdown_source = pathlib.Path(sys.argv[2])
scratch = pathlib.Path(sys.argv[3])
config = yaml.safe_load(source_config.read_text(encoding="utf-8"))
markdown_output = scratch / "markdownlint-check.yaml"
repositories = []
for repository in config["repos"]:
    hooks = []
    for hook in repository["hooks"]:
        hook_id = hook["id"]
        # Every hook is kept. Fixers without a check mode run only on the
        # isolated checkout, where any change they make fails the run.
        arguments = {
            "mixed-line-ending": ["--fix=no"],
            "ruff-format": ["--check"],
            "markdownlint-cli2": ["--config", str(markdown_output)],
        }.get(hook_id)
        hooks.append({**hook, **({"args": arguments} if arguments else {})})
    repositories.append({**repository, "hooks": hooks})
(scratch / "pre-commit-check.yaml").write_text(
    yaml.safe_dump({**config, "repos": repositories}, sort_keys=False),
    encoding="utf-8",
)

markdown = yaml.safe_load(markdown_source.read_text(encoding="utf-8"))
markdown_output.write_text(
    yaml.safe_dump({**markdown, "fix": False}, sort_keys=False),
    encoding="utf-8",
)
PY
}

require_registered_pre_commit() {
  local root="$1"
  local expected actual
  expected="$(python3 - "$root/scripts/requirements-pre-commit.txt" <<'PY'
import pathlib
import re
import sys

lines = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()
matches = [
    match.group(1)
    for line in lines
    if (match := re.fullmatch(r"pre-commit==([0-9]+(?:\.[0-9]+)*)", line))
]
if len(matches) != 1:
    raise SystemExit(1)
print(matches[0])
PY
)" || die "registered pre-commit pin is invalid"
  actual="$(pre-commit --version)" || die "pre-commit version is unavailable"
  [[ "$actual" == "pre-commit $expected" ]] || die "pre-commit version does not match the registered pin"
  registered_pre_commit_version="$expected"
}

# pre-commit installs every hook of the stage before it skips a hook whose
# filters match no file. Remove exactly those hooks first, with pre-commit's own
# hook definitions, classifier and changed-file list, so their environments are
# never installed. Each remaining hook's outcome is unchanged.
drop_hooks_without_changed_files() {
  local from_ref="$1"
  local to_ref="$2"
  (
    cd "$checkout"
    python3 -P - "$scratch/pre-commit-check.yaml" "$from_ref" "$to_ref" \
      "$registered_pre_commit_version" <<'PY'
import sys

import yaml

config_path, from_ref, to_ref, registered = sys.argv[1:]
try:
    from pre_commit import constants
    from pre_commit.clientlib import load_config
    from pre_commit.commands.run import Classifier
    from pre_commit.git import get_changed_files
    from pre_commit.repository import all_hooks
    from pre_commit.store import Store
except ImportError as error:
    raise SystemExit(f"registered pre-commit module is unavailable: {error}")
if constants.VERSION != registered:
    raise SystemExit("pre-commit module version does not match the registered pin")

config = load_config(config_path)
classifier = Classifier.from_config(
    get_changed_files(from_ref, to_ref), config["files"], config["exclude"]
)
matched = set()
unmatched = set()
for hook in all_hooks(config, Store()):
    key = (hook.src, hook.id)
    if "pre-commit" not in hook.stages or hook.always_run:
        matched.add(key)
    elif any(True for _ in classifier.filenames_for_hook(hook)):
        matched.add(key)
    else:
        unmatched.add(key)
dropped = unmatched - matched

with open(config_path, encoding="utf-8") as handle:
    raw = yaml.safe_load(handle)
repositories = []
for repository in raw["repos"]:
    hooks = [
        hook
        for hook in repository["hooks"]
        if (repository["repo"], hook["id"]) not in dropped
    ]
    if hooks:
        repositories.append({**repository, "hooks": hooks})
with open(config_path, "w", encoding="utf-8") as handle:
    yaml.safe_dump({**raw, "repos": repositories}, handle, sort_keys=False)
if dropped:
    names = ", ".join(sorted(hook_id for _, hook_id in dropped))
    print(f"No changed file matches: {names}", file=sys.stderr)
PY
  ) || die "pre-commit module hook selection failed"
}

run_pr_merge() {
  [[ "${GITHUB_ACTIONS:-}" == "true" ]] || die "GITHUB_ACTIONS=true is required"
  [[ "${CI:-}" == "true" ]] || die "CI=true is required"
  [[ "${PR_BASE_SHA:-}" =~ ^[0-9a-f]{40}$ ]] || die "PR_BASE_SHA must be a full SHA"
  [[ "${PR_HEAD_SHA:-}" =~ ^[0-9a-f]{40}$ ]] || die "PR_HEAD_SHA must be a full SHA"
  [[ "$PR_BASE_SHA" != "$PR_HEAD_SHA" ]] || die "PR revisions must differ"

  local merge_record merge_sha merge_base merge_head merge_extra
  merge_record="$(git -C "$repository_root" rev-list --parents --max-count=1 HEAD)" || \
    die "candidate merge identity unavailable"
  read -r merge_sha merge_base merge_head merge_extra <<<"$merge_record"
  [[ "$merge_sha" =~ ^[0-9a-f]{40}$ ]] || die "candidate merge SHA is invalid"
  [[ "$merge_base" == "$PR_BASE_SHA" ]] || die "candidate base parent mismatch"
  [[ "$merge_head" == "$PR_HEAD_SHA" ]] || die "candidate head parent mismatch"
  [[ -z "$merge_extra" ]] || die "candidate checkout is not a two-parent merge"

  checkout="$scratch/repository"
  git -C "$repository_root" worktree add --quiet --detach "$checkout" "$merge_sha" || \
    die "isolated style checkout failed"
  render_readonly_config \
    "$checkout/.pre-commit-config.yaml" \
    "$checkout/.markdownlint-cli2.yaml"
  require_registered_pre_commit "$checkout"
  drop_hooks_without_changed_files "$merge_base" "$merge_sha"
  snapshot_candidate_state before

  set +e
  run_pre_commit run --config "$scratch/pre-commit-check.yaml" \
    --from-ref "$merge_base" --to-ref "$merge_sha" --show-diff-on-failure
  local child_exit=$?
  set -e

  require_unchanged_candidate "$child_exit" "PR style validation"
  return "$child_exit"
}

snapshot_candidate_state() {
  local suffix="$1"
  git -C "$checkout" diff --cached --binary --full-index HEAD -- \
    >"$scratch/index.$suffix" || die "local index snapshot failed"
  git -C "$checkout" diff --binary --full-index -- \
    >"$scratch/worktree.$suffix" || die "local worktree snapshot failed"
  git -C "$checkout" status --porcelain=v2 -z --untracked-files=all \
    >"$scratch/status.$suffix" || die "local status snapshot failed"
}

# A hook that changed the isolated candidate and failed has reported its own
# defect; one that changed it and still passed is a hidden mutator.
require_unchanged_candidate() {
  local child_exit="$1"
  local label="$2"
  snapshot_candidate_state after
  if ! cmp -s "$scratch/index.before" "$scratch/index.after" || \
    ! cmp -s "$scratch/worktree.before" "$scratch/worktree.after" || \
    ! cmp -s "$scratch/status.before" "$scratch/status.after"; then
    [[ "$child_exit" -ne 0 ]] || die "$label changed repository state"
    echo "$label: a hook changed the isolated candidate; fix the reported files explicitly" >&2
  fi
}

run_local_staged() {
  [[ -z "${GITHUB_ACTIONS+x}" ]] || die "GITHUB_ACTIONS is not accepted locally"
  [[ -z "${CI+x}" ]] || die "CI is not accepted locally"
  [[ -z "${PR_BASE_SHA+x}" ]] || die "PR_BASE_SHA is not accepted locally"
  [[ -z "${PR_HEAD_SHA+x}" ]] || die "PR_HEAD_SHA is not accepted locally"
  local candidate_tree source_index source_head base_ref empty_tree current_head current_tree
  source_head="$(git -C "$repository_root" rev-parse --verify HEAD 2>/dev/null)" || source_head=""
  set +e
  git -C "$repository_root" diff --cached --quiet --
  local staged_exit=$?
  set -e
  case "$staged_exit" in
    0) echo 'NOT_APPLICABLE: local staged input is empty'; return 0 ;;
    1) ;;
    *) die "local staged input could not be inspected" ;;
  esac

  candidate_tree="$(git -C "$repository_root" write-tree)" || \
    die "local staged tree is unavailable"
  source_index="$(git -C "$repository_root" rev-parse --path-format=absolute --git-path index)" || \
    die "local index path is unavailable"
  base_ref="$source_head"
  if [[ -z "$base_ref" ]]; then
    git -C "$repository_root" symbolic-ref --quiet HEAD >/dev/null || \
      die "local HEAD is unavailable"
    empty_tree="$(git -C "$repository_root" hash-object -w -t tree --stdin </dev/null)" || \
      die "empty base tree is unavailable"
    # No branch is created or advanced; only the temporary worktree uses this base.
    base_ref="$(printf '%s\n' 'Local style empty base' | git -C "$repository_root" \
      -c user.name='Local style snapshot' -c user.email=local-style@example.invalid \
      commit-tree "$empty_tree")" || die "empty base commit is unavailable"
  fi
  # A caller-selected index belongs to the source, never the isolated worktree.
  unset GIT_INDEX_FILE
  checkout="$scratch/repository"
  git -C "$repository_root" worktree add --quiet --detach "$checkout" "$base_ref" || \
    die "isolated local style checkout failed"
  git -C "$checkout" read-tree --reset -u "$candidate_tree" || \
    die "isolated staged tree checkout failed"
  render_readonly_config \
    "$checkout/.pre-commit-config.yaml" \
    "$checkout/.markdownlint-cli2.yaml"
  require_registered_pre_commit "$checkout"
  snapshot_candidate_state before

  set +e
  run_pre_commit run --config "$scratch/pre-commit-check.yaml" \
    --hook-stage pre-commit --show-diff-on-failure
  local child_exit=$?
  set -e

  require_unchanged_candidate "$child_exit" "local style validation"
  current_tree="$(GIT_INDEX_FILE="$source_index" git -C "$repository_root" write-tree)" || \
    die "local source index could not be rechecked"
  current_head="$(git -C "$repository_root" rev-parse --verify HEAD 2>/dev/null)" || current_head=""
  [[ "$candidate_tree" == "$current_tree" && "$source_head" == "$current_head" ]] || \
    die "local source index or HEAD changed; rerun validation on the current candidate"
  return "$child_exit"
}

case "$mode" in
  local-staged) run_local_staged ;;
  pr-merge) run_pr_merge ;;
esac
