---
layer: agentic
---

# Postflight Routing

This document is a compatibility pointer, not a second completion checklist.

## Completion Authority

Use `rules/task-checklists.md#3-completion-contract` for every completion
decision. Apply only the conditional gates relevant to the changed typed
authority, repository layer, and approved plan. A provider overlay, hook, or
runtime adapter may route a gate but may not redefine its pass criteria.

For agent, provider, or hook surfaces, the focused validators and registered
rollback are declared by
`contracts/agent-governance-artifacts.yaml`. Provider projection freshness is
checked through `scripts/operations/sync-provider-surfaces.sh --check`; mutation
uses only the registered renderer's explicit write mode.

## Related Documents

- `docs/00.agent-governance/rules/task-checklists.md`
- `docs/00.agent-governance/contracts/agent-governance-artifacts.yaml`
- `docs/00.agent-governance/rules/documentation-protocol.md`
- `docs/00.agent-governance/subagent-protocol.md`
