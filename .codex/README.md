---
layer: agentic
runtime: codex
---

# Codex Runtime Surface

This directory contains Codex-specific runtime support for `hy-home.docker`.
Shared policy remains in `AGENTS.md` and `docs/00.agent-governance/`.

## Files

- `hooks.json` — Codex-local hook configuration.

## Current Hook Contract

- `PreToolUse` emits graphify additional context when `graphify-out/graph.json` exists.
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
- `../docs/00.agent-governance/rules/bootstrap.md`
