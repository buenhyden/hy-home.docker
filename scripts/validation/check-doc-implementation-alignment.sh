#!/usr/bin/env bash
set -euo pipefail

if [[ "$#" -ne 0 ]]; then
  printf '%s\n' 'Usage: bash scripts/validation/check-doc-implementation-alignment.sh' >&2
  exit 2
fi

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"
exec python3 scripts/validation/check-document-links.py --mode alignment
