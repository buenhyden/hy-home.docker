#!/usr/bin/env bash
# Authored thin wrapper; Claude SessionStart adapter (session-start.sh) routes to scripts/hooks/agent-event-hook.sh.
set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
exec bash "$PROJECT_DIR/scripts/hooks/agent-event-hook.sh" SessionStart
