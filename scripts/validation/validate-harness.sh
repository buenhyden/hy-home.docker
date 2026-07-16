#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

if [[ "$#" -ne 0 ]]; then
  echo "Usage: bash scripts/validation/validate-harness.sh" >&2
  exit 2
fi

echo "==> Harness validation wrapper (typed contracts, semantic eval, and repository gates)"
bash scripts/validation/run-local-qa-gates.sh --harness
