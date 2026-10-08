#!/usr/bin/env bash
# Effective Compose controls for every root and LAB service (SPEC-0218):
# template adoption, security defaults, lifecycle, resources and the exact
# exceptions in infra/common-optimizations.exceptions.json.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
exec python3 scripts/validation/compose_controls.py "$@"
