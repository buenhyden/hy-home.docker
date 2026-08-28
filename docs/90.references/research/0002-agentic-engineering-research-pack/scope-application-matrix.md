---
status: draft
artifact_id: reference:agentic-engineering-research-draft:scope-application-matrix
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-28
review_cycle: on-source-change
---

# Scope Application Matrix

## Overview

This leaf provides the closed eight-scope routing model for the current draft.
It is general routing only; the architecture-practice composition matrix and
`SCOPE-COMP-001` are deferred to D4.

## Purpose

Make each authored foundation claim explicit about applicability, adoption
conditions, verification, and limits without adding scope values or policy.

## Scope

The closed axis is `agentic`, `architecture`, `common`, `docs`, `infra`, `ops`,
`qa`, and `security`. Named agents are owners or consumers, not additional
scope values.

## Definitions / Facts

| Claim ID | Claim | Evidence class | State | Workspace target | Implication |
| --- | --- | --- | --- | --- | --- |
| `SAM-001` | SPEC-0137 defines exactly eight general Stage 00 role scopes for this draft. | tracked workspace configuration | VERIFIED | `docs/03.specs/0137-agentic-research-pack-rebuild/spec.md` | Every leaf must supply exactly one row for each scope. |
| `SAM-002` | Stage 00 separates policy, role, skill, and provider-registry ownership; provider adapters translate rather than own shared behavior. | tracked workspace configuration | VERIFIED | `docs/00.agent-governance/` | Route gaps to the canonical owner instead of extending this advisory pack. |

## Sources

| Source ID | Claim IDs | Title / publisher | URL or path | Class | Revision / observed | Accessed at | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SAM-SRC-001` | `SAM-001` | Agentic Engineering Research Pack Rebuild Specification / workspace | [SPEC-0137](../../../03.specs/0137-agentic-research-pack-rebuild/spec.md) | tracked workspace configuration | `264a6d1d64a41c329cd86b5978fb47f38503673f` | 2026-08-28 | The axis constrains this draft; it does not establish final acceptance. |
| `SAM-SRC-002` | `SAM-002` | Agentic Engineering Policy and Provider Adapters / workspace | [agentic policy](../../../00.agent-governance/policies/agentic.md); [provider adapters](../../../00.agent-governance/providers/README.md); [provider registry](../../../00.agent-governance/providers/registry.yaml) | tracked workspace configuration | `264a6d1d64a41c329cd86b5978fb47f38503673f` | 2026-08-28 | Provider runtime acceptance remains `needs_revalidation`; no provider probe occurred. |

## Scope Application

| Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
| --- | --- | --- | --- | --- |
| agentic | applies | Follow the approved Spec, Plan, and Task before agentic work. | Read governing paths at the literal baseline. | This is routing, not agent execution proof. |
| architecture | applies | Route architecture decisions to their canonical artifacts and owners. | Confirm the tracked artifact and scoped diff; seek separate approval for runtime observation. | No architecture-practice composition is asserted before D4. |
| common | applies | Apply shared-worktree and approval-boundary constraints. | Inspect only the exact owned-path diff. | A shared rule is not observed enforcement. |
| docs | applies | Apply the research and generic-reference document contracts. | Check frontmatter, headings, and local destinations. | The draft pack has no parent router. |
| infra | applies | Inspect tracked infrastructure configuration; seek separate approval for runtime observation. | Confirm the cited configuration path and scoped diff. | Configuration cannot demonstrate deployment. |
| ops | applies | Route an operational need to its owner and inspect tracked records before use. | Confirm the record path and scoped diff; seek separate approval for live operation. | No run or incident is inferred. |
| qa | applies | Perform scoped document and path checks after the unit is final. | Record actual commands and results in Task 0004; seek separate approval for execution-environment checks. | Full acceptance checks remain deferred. |
| security | applies | Keep sources local and avoid secret, credential, or remote-state access. | Confirm cited sources are tracked documentation; seek separate approval for control testing. | No control effectiveness is evaluated. |

## Maintenance

Update the general routing only when the Spec's closed axis or the cited Stage
00 ownership changes. Add D4 composition rows only with the authorized
cross-practice evidence and sibling files present.

## Related Documents

- [Research pack README](./README.md)
- [Workspace baseline](./workspace-baseline.md)
- [SPEC-0137](../../../03.specs/0137-agentic-research-pack-rebuild/spec.md)
