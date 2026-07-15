---
layer: agentic
runtime: claude
---

# Claude Project Surface

## Scope

`.claude/` contains Claude-native project adapters. Shared governance remains
in Stage 00 and the root `CLAUDE.md` performs the executable imports.

## Structure

- `agents/`: Claude-native agent adapters.
- `skills/`: shared skill projections using canonical `SKILL.md` names.
- `hooks/`, `settings.json`: Claude-native event wiring.

## How to Work in This Area

Change canonical Stage 00 sources first and update this projection only through
the registered renderer. Canonical Hookify rules are tracked at
`docs/00.agent-governance/rules/hooks/hookify.*.md`; a Claude-local Hookify
projection is not tracked until the provider renderer owns it.

## Related Documents

- `../CLAUDE.md`
- `../docs/00.agent-governance/providers/claude.md`
- `../docs/00.agent-governance/rules/provider-capability-matrix.md`
