#!/usr/bin/env bash
# Local preflight for the two candidate-quality checks that the local-only
# gate otherwise leaves to CI (SPEC-0221): the changed-document metadata
# deltas and the tech-stack registry drift. The comparison base is the
# merge-base of HEAD with origin/main, so committed, staged and unstaged
# branch work are all compared, as CI compares PR_BASE_SHA...PR_HEAD_SHA.
set -euo pipefail

die() {
  echo "ERROR: $*" >&2
  exit 2
}

[[ "$#" -eq 0 ]] || die "no arguments are accepted"
root="$(git rev-parse --show-toplevel)" || die "repository root unavailable"
cd "$root"
base="$(git merge-base HEAD refs/remotes/origin/main 2>/dev/null)" ||
  die "no merge-base with origin/main; fetch it first (this check never passes without a base)"

echo "candidate preflight: base=$base"
python3 scripts/validation/check-document-metadata.py --mode check-changed --base-ref "$base"
bash scripts/operations/sync-tech-stack-versions.sh --check
