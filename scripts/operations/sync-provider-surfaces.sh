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

agent_role_scope() {
  local src="$1"
  local scope
  scope="$(
    sed -n 's/.*Scope import: `docs\/00\.agent-governance\/scopes\/\([^`/]*\)\.md`.*/\1/p' "$src" | head -1
  )"
  if [ -z "$scope" ]; then
    scope="$(sed -n 's/^layer: *//p' "$src" | head -1)"
  fi
  if [ -z "$scope" ]; then
    scope="agentic"
  fi
  echo "$scope"
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
  local layer="$2"
  cat >"$TMP" <<EOF
---
layer: ${layer}
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
  case "$name" in
  style-validation | test-automator)
    cat >>"$TMP" <<'EOF'

Behavioral reminder: run `python3 scripts/validation/check-document-metadata.py --mode check-changed` with a safe base; approved all-files QA uses only `scripts/validation/run-agent-precommit-all-files.sh`.
EOF
    ;;
  ci-cd-patterns)
    cat >>"$TMP" <<'EOF'

Behavioral reminder: keep the `Check changed and new document metadata` step in the existing job and supply its safe event base through `TEMPLATE_GATE_BASE`.
EOF
    ;;
  esac
}

gen_gemini_readme() {
  cat >"$TMP" <<'EOF'
# Gemini Shared Runtime & Compatibility Surface

This directory is the native runtime surface for Gemini agents and a compatibility surface for agent tooling that reads `.agents/` paths. It is not the source of truth for repository policy.

## Scope

### In Scope

- Gemini reference index under `agents/` pointing to the governance agent catalog
- Gemini reference index under `skills/` pointing to the governance function catalog
- Gemini-native Workspace Rules in `rules/`
- Gemini-native Workflows in `workflows/`

Per the Provider Parity Model (`docs/00.agent-governance/providers/agents-md.md` §5),
both `agents/` and `skills/` are pointer-only reference indexes. However, `.agents/` natively supports defining workspace-specific behavior in `rules/` and `workflows/` to fully leverage the Antigravity IDE.

### Out of Scope

- Core global policy that belongs in `docs/00.agent-governance/`
- Parallel disconnected agent catalogs (must link to `docs/00.agent-governance/agents/`)
- Secrets, tokens, credentials, shell history, or logs

## Authority

- Policy source of truth: `docs/00.agent-governance/`
- Runtime agent/function source of truth: `docs/00.agent-governance/agents/`
- Claude runtime surface: `.claude/` (agents: `.claude/agents/`, skills: `.claude/skills/`)
- Codex hook/context surface: `.codex/`
- Gemini runtime surface: `.agents/` (this directory)

If a `.agents/skills/<name>/skill.md` file exists, it must stay functionally compatible with the corresponding provider-neutral governance function. It must not point to nonexistent runtime paths.

## Provider Behavior

Gemini CLI provider-native hooks and agents are provider facts, but this
repository does not track a `.gemini` hook or agent adapter. This surface is a
behavioral pointer/reminder, not a tracked native hook adapter.

- For changed or new target Markdown, run
  `python3 scripts/validation/check-document-metadata.py --mode check-changed`
  with a safe comparison base.
- Direct agent execution of all-files pre-commit is prohibited. At an approved
  final QA gate, use only
  `scripts/validation/run-agent-precommit-all-files.sh` and record reviewed
  Git-visible, non-ignored repository paths in Stage 04 evidence.

## How to Work in This Area

1. Update canonical governance and runtime files first.
2. Regenerate this surface with `bash scripts/operations/sync-provider-surfaces.sh --write`.
3. Verify no drift with `bash scripts/operations/sync-provider-surfaces.sh --check`.

## Related Documents

- [Agent governance hub](../docs/00.agent-governance/README.md)
- [Subagent protocol](../docs/00.agent-governance/subagent-protocol.md)
- [Claude runtime bootstrap](../.claude/CLAUDE.md)
- [Codex runtime surface](../.codex/README.md)
EOF
}

# Agents: Codex TOML adapter + Gemini pointer.
for src in docs/00.agent-governance/agents/agents/*.md; do
  name="$(basename "$src" .md)"
  layer="$(agent_role_scope "$src")"

  gen_codex_agent "$name" "$layer"
  sync_file ".codex/agents/${name}.toml"

  gen_gemini_agent "$name" "$layer"
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

gen_gemini_readme
sync_file ".agents/README.md"

if [ "$MODE" = "write" ]; then
  echo "sync-provider-surfaces: wrote Codex TOML adapters and Gemini reference index"
elif [ "$DRIFT" -ne 0 ]; then
  echo "sync-provider-surfaces: drift detected (run: scripts/operations/sync-provider-surfaces.sh --write)"
  exit 1
else
  echo "sync-provider-surfaces: no drift"
fi
