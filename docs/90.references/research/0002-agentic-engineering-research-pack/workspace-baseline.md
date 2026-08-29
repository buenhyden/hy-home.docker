---
status: active
artifact_id: reference:agentic-engineering-research:workspace-baseline
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-28
review_cycle: on-source-change
---

# Workspace Baseline

## Overview

This leaf records only local, tracked foundation facts for the branch-only
draft pack. Its literal measurement baseline is
`264a6d1d64a41c329cd86b5978fb47f38503673f`.

## Purpose

Provide later draft leaves with a reproducible distinction between repository
configuration and observed execution, so neither is substituted for the other.

## Scope

The scope is tracked governance, templates, and the canonical destination
census at the stated baseline. It excludes Docker, environment values, remote
systems, provider probes, credentials, and Task 9 acceptance.

## Definitions / Facts

`tracked configuration` means a committed declaration of intended routing or
control. It does not prove that a hook ran, a provider accepted a model, or a
remote control is enforced. The cited `main` revision is a comparison snapshot
only; it is not accepted Task 9 evidence.

| Claim ID | Claim | Evidence class | State | Workspace target | Implication |
| --- | --- | --- | --- | --- | --- |
| `WB-001` | At baseline `264a6d1d64a41c329cd86b5978fb47f38503673f`, the approved draft destination is absent, so these three files are pre-acceptance draft content rather than a routed canonical pack. | tracked workspace configuration | VERIFIED | `docs/90.references/research/0002-agentic-engineering-research-pack/` | Do not infer Task 9 acceptance or parent-router ownership. |
| `WB-002` | Stage 00 assigns canonical governance to policies, roles, skills, and the provider registry; adapters are runtime mechanics, and configured surfaces do not prove execution. | tracked workspace configuration | VERIFIED | `docs/00.agent-governance/` | Later analysis must label configuration separately from runtime or remote evidence. |

## Sources

| Source ID | Claim IDs | Title / publisher | URL or path | Class | Revision / observed | Accessed at | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `WB-SRC-001` | `WB-001` | Git tree / local repository | `git ls-tree -r 264a6d1d64a41c329cd86b5978fb47f38503673f -- docs/90.references/research/0002-agentic-engineering-research-pack` | tracked workspace configuration | `264a6d1d64a41c329cd86b5978fb47f38503673f` | 2026-08-28 | Empty destination census proves neither migration acceptance nor future state. |
| `WB-SRC-002` | `WB-002` | Agent Bootstrap Policy / workspace | [bootstrap policy](../../../00.agent-governance/policies/bootstrap.md) | tracked workspace configuration | `264a6d1d64a41c329cd86b5978fb47f38503673f` | 2026-08-28 | Declares authority and verification routing; it is not execution evidence. |
| `WB-SRC-003` | `WB-002` | Agentic Engineering Policy and Approval Boundaries / workspace | [agentic policy](../../../00.agent-governance/policies/agentic.md); [approval boundaries](../../../00.agent-governance/policies/approval-boundaries.md); [provider registry](../../../00.agent-governance/providers/registry.yaml) | tracked workspace configuration | `264a6d1d64a41c329cd86b5978fb47f38503673f` | 2026-08-28 | Registry `runtime_acceptance: needs_revalidation` is configuration state, not provider proof. |

## Scope Application

| Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
| --- | --- | --- | --- | --- |
| agentic | applies | Use the Stage 00 authority sequence before agentic changes. | Read cited policy at the literal baseline. | No runtime activity observed. |
| architecture | applies | Before architecture use, compare a tracked architecture artifact with its canonical owner. | Confirm the artifact and scoped diff; seek separate approval for runtime observation. | Baseline evidence does not select an architecture. |
| common | applies | Preserve shared-worktree ownership and declared boundaries. | Inspect the scoped diff and Task ledger. | Shared rules are configuration, not enforcement proof. |
| docs | applies | Use the approved research profile and reference contract. | Check metadata and required sections. | Draft identity reconciliation remains deferred. |
| infra | applies | Inspect tracked infrastructure configuration only; seek separate approval for runtime observation. | Confirm the cited configuration revision and scoped diff. | Compose configuration is not runtime proof. |
| ops | applies | Route operational evidence to its owner and inspect tracked records before use. | Confirm the record path and scoped diff; seek separate approval for live operation. | No operational result is claimed. |
| qa | applies | Run only the scoped metadata, path, census, and whitespace checks. | Record exact commands and exits in Task 0004; seek separate approval for execution-environment checks. | Broad acceptance suites remain Not Run. |
| security | applies | Preserve the approval boundary and avoid secrets or credential access. | Confirm sources are tracked paths only; seek separate approval for control testing. | No security control effectiveness is claimed. |

## Maintenance

Remeasure this leaf when the source paths change or a later authorized baseline
is captured. Keep its literal revision and do not turn configuration evidence
into execution evidence.

## Related Documents

- [Research pack README](./README.md)
- [Scope application matrix](./scope-application-matrix.md)
- [Task 0004](../../../03.specs/0137-agentic-research-pack-rebuild/tasks/tsk-0004-canonical-research-refresh.md)
