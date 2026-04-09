#!/usr/bin/env bash
# post-tool-validate.sh — PostToolUse hook: validate docker-compose after Write/Edit/MultiEdit
set -euo pipefail
bash "$CLAUDE_PROJECT_DIR/scripts/validate-docker-compose.sh"
