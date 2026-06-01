---
layer: agentic
runtime: codex
---

# Codex Runtime Surface

> Codex-specific runtime hooks and provider notes for `hy-home.docker`.

## 1. Quick Reference

- **Governance Hub:** `../docs/00.agent-governance/`
- **Agent Catalog:** `../docs/00.agent-governance/agents/`
- **Hook Configuration:** `.codex/hooks.json`

## 2. Detailed Instructions

For specific Codex execution guidelines, including the Hook Parity Contract, QA/CI tooling, and runtime boundaries, see:

- [Codex Provider Notes](../docs/00.agent-governance/providers/codex.md)
- [Universal Entry Shim](../AGENTS.md)

## 3. Scope

- **In Scope:** `.codex/hooks.json`, `scripts/hooks/agent-event-hook.sh`, and the Codex-compatible runtime adapters (`.codex/agents/*.toml`, `.codex/skills/`).
- **Out of Scope:** User-global Codex settings or credentials. Shared policy remains in `docs/00.agent-governance/`.

Codex TOML files are the active agent adapter definitions. Legacy
`.codex/agents/*.md` files may remain as compatibility prompt context, but they
must not define separate governance, model policy, QA rules, or Template
Contract rules. When TOML and Markdown prompt context disagree, Stage 00 and
the validated TOML adapter surface win.

## 4. Hook Parity (Summary)

Hook event coverage should align with `.claude` settings where supported. Edit matchers cover `apply_patch` and `ApplyPatch`.

## Related Documents

- `../AGENTS.md`
- `../docs/00.agent-governance/providers/codex.md`
- `../docs/00.agent-governance/agents/`
