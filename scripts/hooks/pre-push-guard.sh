#!/usr/bin/env bash
# pre-push-guard.sh - refuse any push that updates refs/heads/main.
#
# The native hook installed by install-pre-push-guard.sh passes every raw
# "<local ref> <local sha> <remote ref> <remote sha>" line, including deletions.
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
