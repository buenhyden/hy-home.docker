---
layer: agentic
runtime: codex
---

# Codex Runtime Surface

This directory contains Codex-specific runtime support for `hy-home.docker`.
Shared policy remains in `AGENTS.md` and `docs/00.agent-governance/`.

## Files

- `hooks.json` — Codex-local hook configuration.

## Runtime Boundary

- Codex uses `AGENTS.md` plus `docs/00.agent-governance/providers/codex.md`
  as its repository entry contract.
- `.codex/hooks.json` provides Codex-local context and post-edit validation.
- The canonical delegated-agent catalog remains the `.claude` runtime mirror
  documented in `docs/00.agent-governance/agents/`.
- Do not create a parallel Codex agent catalog unless repository governance
  explicitly adopts one.

## Current Hook Contract

- `PreToolUse` emits graphify additional context when `graphify-out/graph.json` exists.
- `PostToolUse` runs `scripts/post-tool-validate.sh` after file edits when the hook payload includes changed paths.
- The hook is advisory and must not be treated as the policy source of truth.
- Agents still follow `AGENTS.md`, provider notes, scope rules, and active sandbox approvals.

## Safety Rules

- Do not store secrets, tokens, credentials, personal settings, shell history, or logs here.
- Do not add user-global Codex configuration under this repository.
- Keep tracked `.codex/` files minimal and auditable.

## Related Documents

- `../AGENTS.md`
- `../docs/00.agent-governance/providers/codex.md`
- `../docs/00.agent-governance/providers/agents-md.md`
- `../docs/00.agent-governance/agents/`
- `../docs/00.agent-governance/rules/bootstrap.md`
- `../.claude/CLAUDE.md`
- `../scripts/post-tool-validate.sh`
