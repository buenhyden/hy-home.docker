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
- `hooks/`, `hookify.*.md`, `settings.json`: Claude-native event wiring.

## How to Work in This Area

Change canonical Stage 00 sources first and update this projection only through
the registered renderer. Use `.claude/hookify.*.md` for tracked Hookify rules.

## Related Documents

- `../CLAUDE.md`
- `../docs/00.agent-governance/providers/claude.md`
- `../docs/00.agent-governance/rules/provider-capability-matrix.md`
