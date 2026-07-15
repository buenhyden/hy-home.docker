---
layer: agentic
runtime: codex
---

# Codex Project Surface

## Scope

`.codex/` contains Codex-native project configuration, agent TOML adapters,
and hook compatibility. It does not own shared agent policy.

## Structure

- `agents/*.toml`: Codex-native custom-agent adapters.
- `config.toml`: project-local Codex configuration.
- `hooks.json`: repository hook compatibility configuration.

## How to Work in This Area

Change canonical Stage 00 sources first and use the registered renderer for
agent adapters. Shared skills are discovered from `.agents/skills/`; do not
create a parallel `.codex/skills/` policy surface.

## Related Documents

- `../AGENTS.md`
- `../docs/00.agent-governance/providers/codex.md`
- `../docs/00.agent-governance/rules/provider-capability-matrix.md`
