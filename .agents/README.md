# Shared Agent Compatibility Surface

## Scope

`.agents/` is the provider-neutral compatibility and shared-skill projection.
It is not the Gemini native agent or hook surface, and it does not own policy.

## Structure

- `agents/`: compatibility projections of the Stage 00 role catalog.
- `skills/`: shared `SKILL.md` projections used by compatible providers.
- `rules/` and `workflows/`: compatibility routing to Stage 00 governance.

## How to Work in This Area

Change the typed Stage 00 contracts and canonical role/function sources, then
use the registered provider renderer. Do not hand-author independent policy in
this directory.

## Related Documents

- [Agent governance hub](../docs/00.agent-governance/README.md)
- [Provider-neutral overlay](../docs/00.agent-governance/providers/agents-md.md)
- [Provider capability matrix](../docs/00.agent-governance/rules/provider-capability-matrix.md)
