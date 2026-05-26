#!/usr/bin/env bash
  # User prompt event hook - Claude wrapper for provider-neutral event dispatch.
  set -euo pipefail

  PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
  EVENT="${1:-UserPromptSubmit}"
  exec bash "$PROJECT_DIR/scripts/hooks/agent-event-hook.sh" "$EVENT"
