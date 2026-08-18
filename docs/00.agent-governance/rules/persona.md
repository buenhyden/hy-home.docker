---
layer: agentic
---

# AI Agent Identity Routing

Provider-neutral identity routing for task execution.

## 1. Activation Protocol

Before mutation:

1. Resolve exactly one active `agent_id` from
   `contracts/agent-catalog.yaml`.
2. Use that entry's `scope`, permission profile, work profile, functions, and
   provider projections without inventing a provider-local role.
3. Load the matching canonical role document and one registered primary scope.
4. State the active role, scope, and governing rule set in the task handoff.

Provider-native adapters preserve this identity and role intent. They do not
own separate persona names, scope mappings, permissions, or model policy.

## 2. Authority Boundary

- `contracts/agent-catalog.yaml` owns active role IDs and their typed routing.
- `agents/agents/<agent-id>.md` owns the canonical human-readable role intent.
- `contracts/agent-governance-artifacts.yaml` owns path authority and review
  obligations.
- `contracts/provider-models.yaml` owns work-profile model and reasoning
  selection.
- `rules/bootstrap.md#3-canonical-load-order` owns loading order.

If no catalog role matches, or multiple roles appear authoritative, stop and
route the ambiguity to `workflow-supervisor`; do not revive an unregistered
persona or scope file.

## 3. Collaboration

Multi-role work retains one supervising owner and explicit worker/reviewer
boundaries from `subagent-protocol.md`. Independent review must remain separate
from implementation where the typed authority or workflow requires it.

## Related Documents

- `docs/00.agent-governance/contracts/agent-catalog.yaml`
- `docs/00.agent-governance/contracts/agent-governance-artifacts.yaml`
- `docs/00.agent-governance/rules/bootstrap.md`
- `docs/00.agent-governance/rules/workflows.md`
- `docs/00.agent-governance/subagent-protocol.md`
