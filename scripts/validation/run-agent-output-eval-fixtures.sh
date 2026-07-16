#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
BASE_DIR="$(cd -- "$SCRIPT_DIR/../.." && pwd -P)"
cd "$BASE_DIR"

exec python3 "$BASE_DIR/scripts/validation/agent_output_eval.py" "$@"
