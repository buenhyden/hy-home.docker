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

Codex TOML files are the only active agent adapter definitions. The former
`.codex/agents/*.md` compatibility prompt surface is retired; do not recreate
Markdown agent prompts under `.codex/agents/`.

## 4. Harness Alignment Gates

- Clarification duty is blocking before Codex changes planning, implementation,
  model/reasoning values, hook/config state, or completion status when the
  answer cannot be discovered from repository evidence.
- `.codex/agents/*.toml` must use only model and `model_reasoning_effort`
  values permitted by Stage 00 policy, provider sync, and validators.
- `.codex/agents/*.md` is disallowed. Stage 00 and validated TOML adapters are
  the Codex agent source of truth.
- `.codex/skills/**/skill.md` is a provider skill adapter surface. Use the
  Stage 00 lifecycle terms: discovery -> applicability -> provider loading ->
  canonical artifact -> validation evidence.
- QA/CI completion evidence must distinguish local checks, CI-only gates,
  hook/script output, and skipped-check rationale.

## 5. Hook Parity (Summary)

Hook event coverage should align with `.claude` settings where supported. Edit matchers cover `apply_patch` and `ApplyPatch`.

## Related Documents

- `../AGENTS.md`
- `../docs/00.agent-governance/providers/codex.md`
- `../docs/01.requirements/024-agent-governance-standardization.md`
- `../docs/02.architecture/requirements/0027-agent-governance-canonical-adapter.md`
- `../docs/02.architecture/decisions/0027-stage-00-canonical-adapter-model.md`
- `../docs/00.agent-governance/agents/`
