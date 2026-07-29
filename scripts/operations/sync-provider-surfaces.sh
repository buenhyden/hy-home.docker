#!/usr/bin/env bash
# Compatibility entry point for the Stage 00 provider surface renderer.

set -euo pipefail

_verified_repository_root() {
  local direct_root candidate direct_identity candidate_identity
  direct_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
  if [[ -z "${HYHOME_CI_GATE_ROOT+x}" ]]; then
    printf '%s\n' "$direct_root"
    return 0
  fi
  candidate="$HYHOME_CI_GATE_ROOT"
  if [[ ! "$candidate" =~ ^/proc/self/fd/(0|[1-9][0-9]*)$ ]]; then
    printf '%s\n' "FAIL: invalid HYHOME_CI_GATE_ROOT" >&2
    return 2
  fi
  direct_identity="$(stat -Lc '%d:%i' -- "$direct_root" 2>/dev/null || true)"
  candidate_identity="$(stat -Lc '%d:%i' -- "$candidate" 2>/dev/null || true)"
  if [[ -z "$direct_identity" || "$candidate_identity" != "$direct_identity" || ! -d "$candidate" ]]; then
    printf '%s\n' "FAIL: invalid HYHOME_CI_GATE_ROOT" >&2
    return 2
  fi
  printf '%s\n' "$candidate"
}

REPO_ROOT="$(_verified_repository_root)"
cd "$REPO_ROOT"

if (( $# > 1 )); then
  printf 'Usage: %s [--check|--write]\n' "$0" >&2
  exit 2
fi

case "${1:---check}" in
  --check)
    exec python3 scripts/operations/provider_surface_renderer.py --check
    ;;
  --write)
    exec python3 scripts/operations/provider_surface_renderer.py --write
    ;;
  *)
    printf 'Usage: %s [--check|--write]\n' "$0" >&2
    exit 2
    ;;
esac
