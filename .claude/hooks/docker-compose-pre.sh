#!/usr/bin/env bash
# PreToolUse Hook - Claude wrapper for provider-neutral event dispatch.
set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
exec bash "$PROJECT_DIR/scripts/agent-event-hook.sh" PreToolUse
