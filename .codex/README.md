---
layer: agentic
runtime: codex
---

# Codex Runtime Surface

> Codex-specific runtime hooks and provider notes for `hy-home.docker`.

## Overview

This directory contains the Codex runtime surface for the repository. Shared
policy remains in `AGENTS.md` and `docs/00.agent-governance/`; `.codex/`
contains only Codex-local hook configuration and routing notes.

## Audience

This README is for:

- AI Agents
- Documentation Writers
- Repository Maintainers

## Scope

### In Scope

- Codex-local hook configuration
- Provider-specific runtime boundary notes
- References back to the shared governance hub

### Out of Scope

- User-global Codex settings
- Secrets, tokens, credentials, shell history, or logs
- A parallel Codex agent catalog

## Structure

```text
.codex/
├── hooks.json  # Codex-local hook configuration
└── README.md   # This file
```

## Runtime Boundary

- Codex uses `AGENTS.md` plus `docs/00.agent-governance/providers/codex.md`
  as its repository entry contract.
- `.codex/hooks.json` provides Codex-local context and post-edit validation.
- The canonical delegated-agent catalog remains the `.claude` runtime mirror
  documented in `docs/00.agent-governance/agents/`.
- Do not create a parallel Codex agent catalog unless repository governance
  explicitly adopts one.

## Current Hook Contract

- `SessionStart` uses `scripts/agent-event-hook.sh` to emit project context when the event is supported.
- `PreToolUse` uses `scripts/agent-event-hook.sh` to emit Graphify advisory context when relevant and Docker Compose guardrail context before matching edits.
- `PostToolUse` uses `scripts/agent-event-hook.sh`, which delegates to `scripts/post-tool-validate.sh` after file edits when the hook payload includes changed paths.
- `SessionEnd`, `Stop`, and `PreCompact` route through `scripts/agent-event-hook.sh` for lifecycle-safe advisory context when the runtime supports those events.
- The hook is advisory and must not be treated as the policy source of truth.
- Agents still follow `AGENTS.md`, provider notes, scope rules, and active sandbox approvals.

## Safety Rules

- Do not store secrets, tokens, credentials, personal settings, shell history, or logs here.
- Do not add user-global Codex configuration under this repository.
- Keep tracked `.codex/` files minimal and auditable.

## How to Work in This Area

1. Read `AGENTS.md` and the Codex provider overlay before changing Codex behavior.
2. Keep shared policy in `docs/00.agent-governance/` instead of duplicating it here.
3. Update this README when `hooks.json` gains or loses a repository-level behavior.
4. Run the repository contract checks after changing tracked runtime files.

## Related Documents

- `../AGENTS.md`
- `../docs/00.agent-governance/providers/codex.md`
- `../docs/00.agent-governance/providers/agents-md.md`
- `../docs/00.agent-governance/agents/`
- `../docs/00.agent-governance/rules/bootstrap.md`
- `../.claude/CLAUDE.md`
- `../scripts/agent-event-hook.sh`
- `../scripts/post-tool-validate.sh`
