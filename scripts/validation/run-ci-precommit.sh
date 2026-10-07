#!/usr/bin/env bash
set -euo pipefail

# Read-only PR route for changed-file style and static checks. Authoring hooks
# may repair staged files locally; the hosted candidate must only report drift.

die() {
  echo "ERROR: $1" >&2
  exit 2
}

[[ "$#" -eq 0 ]] || die "arguments are not accepted"
[[ "${GITHUB_ACTIONS:-}" == "true" ]] || die "GITHUB_ACTIONS=true is required"
[[ "${CI:-}" == "true" ]] || die "CI=true is required"
[[ "${PR_BASE_SHA:-}" =~ ^[0-9a-f]{40}$ ]] || die "PR_BASE_SHA must be a full SHA"
[[ "${PR_HEAD_SHA:-}" =~ ^[0-9a-f]{40}$ ]] || die "PR_HEAD_SHA must be a full SHA"
[[ "$PR_BASE_SHA" != "$PR_HEAD_SHA" ]] || die "PR revisions must differ"
[[ -z "${TASK_FILE+x}" ]] || die "Agent wrapper variable TASK_FILE is not accepted"
[[ -z "${ALLOW_PREFIXES+x}" ]] || die "Agent wrapper variable ALLOW_PREFIXES is not accepted"
[[ -z "${SKIP+x}" ]] || die "SKIP is not accepted"

repository_root="$(git rev-parse --show-toplevel)" || die "repository root unavailable"
merge_record="$(git -C "$repository_root" rev-list --parents --max-count=1 HEAD)" || \
  die "candidate merge identity unavailable"
read -r merge_sha merge_base merge_head merge_extra <<<"$merge_record"
[[ "$merge_sha" =~ ^[0-9a-f]{40}$ ]] || die "candidate merge SHA is invalid"
[[ "$merge_base" == "$PR_BASE_SHA" ]] || die "candidate base parent mismatch"
[[ "$merge_head" == "$PR_HEAD_SHA" ]] || die "candidate head parent mismatch"
[[ -z "$merge_extra" ]] || die "candidate checkout is not a two-parent merge"
scratch="$(mktemp -d "${TMPDIR:-/tmp}/ci-style.XXXXXX")"
checkout="$scratch/repository"
cleanup() {
  git -C "$repository_root" worktree remove --force "$checkout" >/dev/null 2>&1 || true
  rm -f -- "$scratch/pre-commit-check.yaml" "$scratch/markdownlint-check.yaml"
  rmdir "$scratch" >/dev/null 2>&1 || true
}
trap cleanup EXIT HUP INT TERM

git -C "$repository_root" worktree add --quiet --detach "$checkout" "$merge_sha" || \
  die "isolated style checkout failed"
python3 - "$checkout" <<'PY'
import pathlib
import sys

import yaml

root = pathlib.Path(sys.argv[1])
scratch = root.parent
source_config = root / ".pre-commit-config.yaml"
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
output_config = scratch / "pre-commit-check.yaml"
output_config.write_text(
    yaml.safe_dump({**config, "repos": repositories}, sort_keys=False),
    encoding="utf-8",
)

markdown_source = root / ".markdownlint-cli2.yaml"
markdown = yaml.safe_load(markdown_source.read_text(encoding="utf-8"))
markdown_output.write_text(
    yaml.safe_dump({**markdown, "fix": False}, sort_keys=False),
    encoding="utf-8",
)
PY
cd "$checkout"
pre-commit run --config "$scratch/pre-commit-check.yaml" \
  --from-ref "$PR_BASE_SHA" --to-ref "$PR_HEAD_SHA" --show-diff-on-failure
