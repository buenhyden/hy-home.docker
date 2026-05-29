#!/usr/bin/env bash
#
# sync-provider-surfaces.sh
#
# Regenerate the Codex mirror (.codex/) and the Gemini reference index (.agents/)
# from the canonical Claude runtime (.claude/), per the Provider Parity Model
# (docs/00.agent-governance/providers/agents-md.md, section 5) and the Model Policy
# (docs/00.agent-governance/subagent-protocol.md).
#
# Usage:
#   scripts/operations/sync-provider-surfaces.sh           # verify mode (default)
#   scripts/operations/sync-provider-surfaces.sh --write   # write generated surfaces
#
# Verify mode exits non-zero when any generated surface drifts from canonical.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

MODE="verify"
if [ "${1:-}" = "--write" ]; then
  MODE="write"
fi

SUPERVISOR="workflow-supervisor"
DRIFT=0

TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

# Map a Claude worker/supervisor model to its Codex (GPT) equivalent.
codex_model() {
  case "$1" in
  opus) echo "gpt-5.1-codex" ;;
  sonnet) echo "gpt-5.1-codex-mini" ;;
  *) echo "$1" ;;
  esac
}

# Map an agent name to its Gemini model tier.
gemini_model() {
  if [ "$1" = "$SUPERVISOR" ]; then
    echo "gemini-3-pro"
  else
    echo "gemini-3-flash"
  fi
}

# Reconcile $TMP against the target file: copy in write mode, report drift otherwise.
sync_file() {
  local target="$1"
  if [ "$MODE" = "write" ]; then
    mkdir -p "$(dirname "$target")"
    cp "$TMP" "$target"
  elif [ ! -f "$target" ] || ! cmp -s "$TMP" "$target"; then
    echo "DRIFT: $target"
    DRIFT=1
  fi
}

gen_gemini_agent() {
  local name="$1"
  cat >"$TMP" <<EOF
---
layer: agentic
model: $(gemini_model "$name")
---

# ${name}.md

@docs/00.agent-governance/agents/agents/${name}.md

This file is a Gemini reference index. The source of truth for this agent is \`docs/00.agent-governance/agents/agents/${name}.md\`.
EOF
}

gen_gemini_skill() {
  local name="$1"
  cat >"$TMP" <<EOF
---
layer: agentic
---

# ${name}/skill.md

@docs/00.agent-governance/agents/functions/${name}.md

This file is a Gemini reference index. The source of truth for this skill is \`docs/00.agent-governance/agents/functions/${name}.md\`.
EOF
}

# Agents: Codex mirror (model line remapped) + Gemini pointer.
for src in .claude/agents/*.md; do
  name="$(basename "$src" .md)"

  claude_m="$(sed -n 's/^model: *//p' "$src" | head -1)"
  sed "s/^model: .*/model: $(codex_model "$claude_m")/" "$src" >"$TMP"
  sync_file ".codex/agents/${name}.md"

  gen_gemini_agent "$name"
  sync_file ".agents/agents/${name}.md"
done

# Skills: Codex mirror (verbatim) + Gemini pointer.
for src in .claude/skills/*/skill.md; do
  name="$(basename "$(dirname "$src")")"

  cp "$src" "$TMP"
  sync_file ".codex/skills/${name}/skill.md"

  gen_gemini_skill "$name"
  sync_file ".agents/skills/${name}/skill.md"
done

if [ "$MODE" = "write" ]; then
  echo "sync-provider-surfaces: wrote Codex mirror and Gemini reference index"
elif [ "$DRIFT" -ne 0 ]; then
  echo "sync-provider-surfaces: drift detected (run: scripts/operations/sync-provider-surfaces.sh --write)"
  exit 1
else
  echo "sync-provider-surfaces: no drift"
fi
