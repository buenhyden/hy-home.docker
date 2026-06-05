#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

echo "==> Harness validation wrapper"
bash scripts/validation/run-local-qa-gates.sh --harness
