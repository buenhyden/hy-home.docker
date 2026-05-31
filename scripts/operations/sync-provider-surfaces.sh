#!/usr/bin/env bash
#
# sync-provider-surfaces.sh
#
# Regenerate provider adapter surfaces from the Stage 00 canonical catalog, per
# the Stage 00 Canonical Adapter Model
# (docs/00.agent-governance/providers/agents-md.md, section 5) and the Model
# Policy (docs/00.agent-governance/subagent-protocol.md).
#
# Usage:
#   scripts/operations/sync-provider-surfaces.sh           # verify mode (default)
#   scripts/operations/sync-provider-surfaces.sh --write   # write generated surfaces
#
# Verify mode exits non-zero when any generated adapter surface drifts from
# Stage 00.

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

codex_model() {
  if [ "$1" = "$SUPERVISOR" ]; then
    echo "gpt-5.5"
  else
    echo "gpt-5.4-mini"
  fi
}

codex_reasoning_effort() {
  if [ "$1" = "$SUPERVISOR" ]; then
    echo "xhigh"
  else
    echo "medium"
  fi
}

# Map an agent name to its Gemini model tier.
gemini_model() {
  if [ "$1" = "$SUPERVISOR" ]; then
    echo "gemini-3.1-pro"
  else
    echo "gemini-3.5-flash"
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

gen_codex_agent() {
  local name="$1"
  local layer="$2"
  cat >"$TMP" <<EOF
name = "${name}"
layer = "${layer}"
model = "$(codex_model "$name")"
model_reasoning_effort = "$(codex_reasoning_effort "$name")"
source_catalog = "docs/00.agent-governance/agents/agents/${name}.md"
scope = "docs/00.agent-governance/scopes/${layer}.md"
legacy_markdown_adapter = ".codex/agents/${name}.md"
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

# Agents: Codex TOML adapter + Gemini pointer.
for src in docs/00.agent-governance/agents/agents/*.md; do
  name="$(basename "$src" .md)"
  layer="$(sed -n 's/^layer: *//p' "$src" | head -1)"
  if [ -z "$layer" ]; then
    layer="agentic"
  fi

  gen_codex_agent "$name" "$layer"
  sync_file ".codex/agents/${name}.toml"

  gen_gemini_agent "$name"
  sync_file ".agents/agents/${name}.md"
done

# Skills: Codex skill adapter (currently content-compatible with Claude) +
# Gemini pointer. Stage 00 remains the source of truth for the function set.
for src in .claude/skills/*/skill.md; do
  name="$(basename "$(dirname "$src")")"

  cp "$src" "$TMP"
  sync_file ".codex/skills/${name}/skill.md"

  gen_gemini_skill "$name"
  sync_file ".agents/skills/${name}/skill.md"
done

if [ "$MODE" = "write" ]; then
  echo "sync-provider-surfaces: wrote Codex TOML adapters and Gemini reference index"
elif [ "$DRIFT" -ne 0 ]; then
  echo "sync-provider-surfaces: drift detected (run: scripts/operations/sync-provider-surfaces.sh --write)"
  exit 1
else
  echo "sync-provider-surfaces: no drift"
fi
