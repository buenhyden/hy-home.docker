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
| POSTFLIGHT-CHECKLIST-R1 | Completion of a change | Required: record completion evidence in the co-located Stage 03 Task | none | co-located Stage 03 Task |
| POSTFLIGHT-CHECKLIST-R2 | Completion of a change | Required: treat Git history as the recovery boundary | none | none |
| POSTFLIGHT-CHECKLIST-R3 | Always | Forbidden: creating a second handoff or progress authority | none | none |
| POSTFLIGHT-CHECKLIST-R4 | Approved all-files gate | Required: leave direct pre-commit prohibition and every wrapper condition to `quality-standards.md#4-execution-boundary` | none | none |
| POSTFLIGHT-CHECKLIST-R5 | Approved all-files gate | Required: postflight records only the concise result and hook-managed fallout | none | none |

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

Postflight routes to other owners and ties no check to any rule in Requirements.

- Evidence placement and handoff authority (R1-R3): no check is named.
- All-files gate (R4-R5): no check is named.
- Rules stated under Enforcement (Mechanisms) are outside this table.

## Ownership

### Owner

`@buenhyden` approves changes; `rules-engineer` reviews them ([approval boundaries](approval-boundaries.md#authorization-source-and-records)).

### Review Triggers

Changes land in place with Task evidence; related documents:

- [Task checklists](task-checklists.md)
- [Quality standards](quality-standards.md#4-execution-boundary)
- [Documentation protocol](documentation-protocol.md)
- [Provider registry](providers/registry.yaml)
