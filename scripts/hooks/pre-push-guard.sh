#!/usr/bin/env bash
# pre-push-guard.sh - refuse any push that updates refs/heads/main.
#
# The native hook installed by install-pre-push-guard.sh passes every raw
# "<local ref> <local sha> <remote ref> <remote sha>" line, including deletions.
set -euo pipefail

refs=("${PRE_COMMIT_REMOTE_BRANCH:-}")
if [[ ! -t 0 ]]; then
  while IFS= read -r record || [[ -n "$record" ]]; do
    read -r local_ref local_oid remote_ref remote_oid extra <<<"$record"
    if [[ -z "$local_ref" || "$remote_ref" != refs/* || -n "$extra" \
      || ! "$local_oid" =~ ^([0-9a-f]{40}|[0-9a-f]{64})$ \
      || ! "$remote_oid" =~ ^([0-9a-f]{40}|[0-9a-f]{64})$ \
      || "${#local_oid}" -ne "${#remote_oid}" ]]; then
      echo 'pre-push-guard: malformed ref update input; push refused.' >&2
      exit 2
    fi
    if ! git check-ref-format "$remote_ref" >/dev/null 2>&1; then
      echo 'pre-push-guard: remote ref validation failed; check Git and input.' >&2
      exit 2
    fi
    refs+=("$remote_ref")
  done
fi

for ref in "${refs[@]}"; do
  if [[ "$ref" == "refs/heads/main" ]]; then
    echo "pre-push-guard: direct push to main refused; push a feature branch and open a pull request." >&2
    exit 1
  fi
done
