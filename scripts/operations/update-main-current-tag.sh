#!/usr/bin/env bash
set -euo pipefail

# Advance only the mutable channel tag for the audited, current main commit.
[[ ${GITHUB_REF:-} == refs/heads/main ]] || { echo 'main ref required' >&2; exit 1; }
[[ ${GITHUB_SHA:-} =~ ^[0-9a-f]{40}$ ]] || { echo 'full commit SHA required' >&2; exit 1; }
[[ $(git cat-file -t "$GITHUB_SHA" 2>/dev/null) == commit ]] || {
  echo 'local commit unavailable' >&2; exit 1;
}

remote_main=$(git ls-remote origin refs/heads/main)
[[ $remote_main == "$GITHUB_SHA"$'\t'refs/heads/main ]] || {
  echo 'audited commit is no longer remote main' >&2; exit 1;
}

remote_tag=$(git ls-remote origin refs/tags/main-current 'refs/tags/main-current^{}')
expected=''
while IFS=$'\t' read -r sha ref; do
  [[ -n $sha ]] || continue
  [[ $sha =~ ^[0-9a-f]{40}$ ]] || { echo 'invalid remote tag' >&2; exit 1; }
  [[ $ref == refs/tags/main-current ]] || {
    echo 'annotated or ambiguous channel tag refused' >&2; exit 1;
  }
  [[ -z $expected ]] || { echo 'duplicate channel tag refused' >&2; exit 1; }
  expected=$sha
done <<< "$remote_tag"

if [[ -n $expected ]]; then
  [[ $(git cat-file -t "$expected" 2>/dev/null) == commit ]] || {
    # A remote lightweight tag may not be in this checkout; fetch only that ref.
    git fetch --no-tags -q origin refs/tags/main-current
    [[ $(git cat-file -t "$expected" 2>/dev/null) == commit ]] || {
      echo 'non-commit channel tag refused' >&2; exit 1;
    }
  }
  [[ $expected != "$GITHUB_SHA" ]] || exit 0
fi

[[ $(git ls-remote origin refs/heads/main) == "$GITHUB_SHA"$'\t'refs/heads/main ]] || {
  echo 'remote main advanced before channel update' >&2; exit 1;
}
git push --porcelain --force-with-lease="refs/tags/main-current:$expected" \
  origin "$GITHUB_SHA:refs/tags/main-current"
