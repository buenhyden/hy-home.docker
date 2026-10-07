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
cleanup() {
  if [[ -n "$checkout" ]]; then
    git -C "$repository_root" worktree remove --force "$checkout" >/dev/null 2>&1 || true
  fi
  rm -rf -- "$scratch"
}
trap cleanup EXIT HUP INT TERM

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
        if hook_id in {"end-of-file-fixer", "trailing-whitespace"}:
            continue
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
  (
    cd "$checkout"
    pre-commit run --config "$scratch/pre-commit-check.yaml" \
      --from-ref "$PR_BASE_SHA" --to-ref "$PR_HEAD_SHA" --show-diff-on-failure
  )
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

run_local_staged() {
  [[ -z "${GITHUB_ACTIONS+x}" ]] || die "GITHUB_ACTIONS is not accepted locally"
  [[ -z "${CI+x}" ]] || die "CI is not accepted locally"
  [[ -z "${PR_BASE_SHA+x}" ]] || die "PR_BASE_SHA is not accepted locally"
  [[ -z "${PR_HEAD_SHA+x}" ]] || die "PR_HEAD_SHA is not accepted locally"
  git -C "$repository_root" rev-parse --verify HEAD >/dev/null 2>&1 || \
    die "local HEAD is unavailable"
  set +e
  git -C "$repository_root" diff --cached --quiet HEAD --
  local staged_exit=$?
  set -e
  case "$staged_exit" in
    0) die "local staged input is empty" ;;
    1) ;;
    *) die "local staged input could not be inspected" ;;
  esac

  local candidate_tree
  candidate_tree="$(git -C "$repository_root" write-tree)" || \
    die "local staged tree is unavailable"
  checkout="$scratch/repository"
  git -C "$repository_root" worktree add --quiet --detach "$checkout" HEAD || \
    die "isolated local style checkout failed"
  git -C "$checkout" read-tree --reset -u "$candidate_tree" || \
    die "isolated staged tree checkout failed"
  render_readonly_config \
    "$checkout/.pre-commit-config.yaml" \
    "$checkout/.markdownlint-cli2.yaml"
  require_registered_pre_commit "$checkout"
  snapshot_candidate_state before

  set +e
  (
    cd "$checkout"
    pre-commit run --config "$scratch/pre-commit-check.yaml" \
      --hook-stage pre-commit --show-diff-on-failure
  )
  local child_exit=$?
  set -e

  snapshot_candidate_state after
  if ! cmp -s "$scratch/index.before" "$scratch/index.after" || \
    ! cmp -s "$scratch/worktree.before" "$scratch/worktree.after" || \
    ! cmp -s "$scratch/status.before" "$scratch/status.after"; then
    die "local style validation changed repository state"
  fi
  return "$child_exit"
}

case "$mode" in
  local-staged) run_local_staged ;;
  pr-merge) run_pr_merge ;;
esac
