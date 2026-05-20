#!/usr/bin/env bash
# pre-compact.sh - Claude wrapper for PreCompact event dispatch.
set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
exec bash "$PROJECT_DIR/scripts/hooks/agent-event-hook.sh" PreCompact
