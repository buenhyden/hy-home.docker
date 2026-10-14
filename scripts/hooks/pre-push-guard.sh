#!/usr/bin/env bash
# pre-push-guard.sh - refuse any push that updates refs/heads/main.
#
# Runs as the `pre-push` stage of .pre-commit-config.yaml, so it also covers
# pushes an agent hook never sees, such as an editor's sync. pre-commit exposes
# the remote ref as PRE_COMMIT_REMOTE_BRANCH; a direct git hook passes
# "<local ref> <local sha> <remote ref> <remote sha>" lines on stdin. Both are read.
set -euo pipefail

refs=("${PRE_COMMIT_REMOTE_BRANCH:-}")
if [[ ! -t 0 ]]; then
  while read -r _ _ remote_ref _; do
    refs+=("$remote_ref")
  done
fi

for ref in "${refs[@]}"; do
  if [[ "$ref" == "refs/heads/main" ]]; then
    echo "pre-push-guard: direct push to main refused; push a feature branch and open a pull request." >&2
    exit 1
  fi
done
