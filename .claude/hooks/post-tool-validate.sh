#!/usr/bin/env bash
# post-tool-validate.sh — Claude wrapper for provider-neutral validation.
set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
exec bash "$PROJECT_DIR/scripts/post-tool-validate.sh"
