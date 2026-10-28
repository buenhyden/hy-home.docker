---
title: "Remaining Request Review Task"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0013"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-29"
---

# Remaining Request Review Task

## Overview

### Objective

Execute W29: review the request areas after Archive (Stage 99 lifecycle, Task
contract, templates, document language and links, timeboxes, CI/QA, and the
agent harness), apply the verified small corrections, and route the rest. This
Task owns criterion 24 only.

## Inputs and Authorization

On 2026-10-29 the owner asked to review the rest of the request and proceed.
The input is branch `docs/archive-disposition-dryrun` after TSK-0012. Two
read-only reviews traced each area against current source; their findings were
re-checked against the cited lines before any edit. The authorization covers
this branch, its pull request, and merge through the protected path. It does
not cover another active Task's writer scope or any runtime action.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0013 | draft | ready | #inputs-and-authorization |
| SPEC-0212-TSK-0013 | ready | in-progress | #applied |
| SPEC-0212-TSK-0013 | in-progress | completed | #evidence |

### Applied

| Area | Change | Location |
| --- | --- | --- |
| Lifecycle drift | ADR statuses now match the Registry `architecture-decision` lifecycle (`deprecated`, not `retired`). | `.agents/governance/sdlc.md` |
| Document language | The language rule is stated directly instead of only linked. | `.agents/governance/standards.md` |
| Document language | Generated provider READMEs are Korean, as the protocol requires; both were re-rendered. | `scripts/operations/provider_surface_renderer.py`, `.claude/README.md`, `.codex/README.md` |
| Provider neutrality | The Codex sandbox limit and each provider's native-memory setting moved from `.agents` into the provider adapters; `.agents` keeps one neutral line each. | `.agents/governance/environment-constraints.md`, `.claude/provider.md`, `.codex/provider.md` |
| Timeboxes | Postmortem corrective actions no longer require a due date. The published INC-0002 postmortem keeps the columns it was written with. | `docs/99.templates/templates/operations/postmortem.template.md`, `.agents/governance/documentation-protocol.md` |
| Workspace | The seven `_workspace` contract READMEs exist and are tracked through one ignore ladder each; only sanitized results may sit under `diagnostics/`. | `_workspace/`, `.gitignore`, `tests/lib/test_surface_ownership.py` |

### Kept

The Registry owns lifecycle names and transitions once, and all 39
template/profile pairs use a status from their lifecycle. Task-only execution
state, per-criterion acceptance, CI leaf de-duplication, check-only CI
formatting, the commit message contract, the single release producer, the
single shared memory store with no automatic deletion, native memory off, and
the local-settings ignore rules already match the request.

### Deferred and blocked

| Item | Decision | Owner | Reason |
| --- | --- | --- | --- |
| `###` subtopics in 12 templates and section guidance in `specs/spec.template.md` | BLOCKED | Stage 99 owner | Needs a per-profile subtopic set and may conflict with Registry section-order checks. |
| Remove the unused `cliff.toml` and its test and contract entries | BLOCKED | SPEC-0211 TSK-0001 | That in-progress Task's release writer owns `cliff`. |
| Tests that assert removed paths stay absent | DEFER | Each test's surface owner | Several guard current contracts (ADR-0047 InfluxDB absence, tier layout). Removal needs proof that the guarantee moved elsewhere. |
| `_workspace` producers | DEFER | Script owners | No script writes to the new directories yet; existing writers keep their paths until changed by their own Task. |
| Four-repository adoption, remote protection, runtime and native-loader acceptance | NOT_RUN | Owner | Outside this repository's local write scope. |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Provider render | 24 | W29 | `provider_surface_renderer.py --check` | This branch | PASS | providers=2 drift=0 | required | - |
| Metadata contracts | 24 | W29 | `check-document-metadata.py --mode check-contracts` | This branch | PASS | 0 violations | required | - |
| Changed documents | 24 | W29 | `check-document-metadata.py --mode check-changed`, including the INC-0002 postmortem | This branch | PASS | 0 violations | required | - |
| Affected tests | 24 | W29 | `python3 -m unittest` over `test_registry`, `test_ci_gate_contract`, `test_surface_ownership`, `test_agent_governance_ci_routing`, `test_spec_packages` | This branch; Python 3.12.3 | PASS | 327 tests | required | - |
| Workspace tracking | 24 | W29 | `git ls-files _workspace/` | This branch | PASS | Exactly the seven contract READMEs | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 24 | accepted | Provider render, Metadata contracts, Changed documents, Affected tests, Workspace tracking | Six corrections applied; two items blocked and three deferred or not run with named owners. | SPEC-0212 TSK-0013 |

## Review and Completion

This Task completes on the evidence above. Hosted checks and the merge are
observed on the pull request.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Archive removal Task](tsk-0012-archive-history-only-removal.md)
