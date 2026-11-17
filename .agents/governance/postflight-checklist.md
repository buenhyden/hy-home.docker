---
title: "Postflight Routing"
version: "1.2.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
---

# Postflight Routing

## Purpose and Scope

### Objective

Route completion verification to the actual changed authority surface.

#### Authority

This policy is the canonical owner of completion verification routing for changed authority surfaces under [bootstrap precedence](bootstrap.md#authority-and-precedence).

### Applies To

Completion verification selected for the changed canonical and protected surfaces.

#### Exclusions

None: this document states no exclusion.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POSTFLIGHT-CHECKLIST-R1 | Completion of any change | Required: record completion evidence in the co-located Stage 03 Task | none | Stage 03 Task |
| POSTFLIGHT-CHECKLIST-R2 | Completion of any change | Required: treat Git history as the recovery boundary | none | none |
| POSTFLIGHT-CHECKLIST-R3 | Completion of any change | Forbidden: creating a second handoff or progress authority | none | none |
| POSTFLIGHT-CHECKLIST-R4 | An approved all-files gate | Required: record only the concise result and hook-managed fallout | none | Concise result and hook-managed fallout in the Task |
| POSTFLIGHT-CHECKLIST-R5 | An approved all-files gate | Required: leave direct pre-commit prohibition and wrapper conditions to `quality-standards.md#4-execution-boundary` | none | none |
| POSTFLIGHT-CHECKLIST-R6 | Always | Required: treat `task-checklists.md` as the completion authority | none | none |
| POSTFLIGHT-CHECKLIST-R7 | Always | Required: apply only validators mapped to the changed canonical source and protected surface | none | none |
| POSTFLIGHT-CHECKLIST-R8 | Provider projections | Required: run the agent governance contract and renderer check | agent governance contract and renderer check | none |
| POSTFLIGHT-CHECKLIST-R9 | Provider projections | Required: use write mode only through the registered renderer | none | none |

Completion evidence belongs in the co-located Stage 03 Task. Git history is the
recovery boundary. Do not create a second handoff or progress authority.

For an approved all-files gate, the
[execution boundary](quality-standards.md#4-execution-boundary) owns direct
pre-commit prohibition and every wrapper condition. Postflight records only
the concise result and hook-managed fallout; the controlled wrapper reports
exit 20 for unexpected paths.

### Exceptions

#### Exception Conditions

No exception is granted here; a separately authorized operation follows [Approval boundaries](approval-boundaries.md).

#### Approval and Review

None: no exception exists to approve.

## Enforcement

### Mechanisms

`task-checklists.md` is the completion authority. Apply only validators mapped
to the changed canonical source and protected surface. For provider projections,
run the agent governance contract and renderer check; write mode is used only through
the registered renderer.

### Limits

Postflight routes to other checks and names few of its own:

- Evidence placement and the ban on a second handoff or progress authority (R1-R3): no check is named.
- Selection of validators (R6-R7) rests on agent judgment; `task-checklists.md` is the completion authority.
- All-files gate recording and wrapper conditions (R4-R5): wrapper conditions live in `quality-standards.md#4-execution-boundary`; no check is tied to the recording rule.
- Registered-renderer-only write mode (R9): no check is named.

## Ownership

### Owner

`@buenhyden` approves changes; `rules-engineer` reviews them ([approval boundaries](approval-boundaries.md#authorization-source-and-records)).

### Review Triggers

Changes land in place with Task evidence; related documents:

- [Task checklists](task-checklists.md)
- [Quality standards](quality-standards.md#4-execution-boundary)
- [Documentation protocol](documentation-protocol.md)
- [Provider registry](providers/registry.yaml)
