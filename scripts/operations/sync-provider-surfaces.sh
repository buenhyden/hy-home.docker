#!/usr/bin/env bash
# Compatibility entry point for the Stage 00 provider surface renderer.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

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
