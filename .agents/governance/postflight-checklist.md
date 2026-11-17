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
| POSTFLIGHT-CHECKLIST-R1 | Completion of any change | Required: record completion evidence in the co-located Stage 03 Task with Git history as recovery boundary; forbidden: creating a second handoff or progress authority | none | Stage 03 Task |
| POSTFLIGHT-CHECKLIST-R2 | An approved all-files gate | Required: record only the concise result and hook-managed fallout; the `quality-standards.md#4-execution-boundary` owns direct pre-commit prohibition and wrapper conditions | Controlled wrapper (exit 20 for unexpected paths) | Concise result and hook-managed fallout in the Task |

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

- Evidence placement in the Stage 03 Task and the ban on a second handoff or progress authority name no check.
- Selection of validators mapped to the changed surface rests on agent judgment; `task-checklists.md` is the completion authority.
- The all-files gate wrapper conditions live in `quality-standards.md#4-execution-boundary`; only its exit 20 report for unexpected paths is named here.
- Provider projection freshness is named through the agent governance contract and renderer check, not detailed here.

## Ownership

### Owner

`@buenhyden` approves changes; `rules-engineer` reviews them ([approval boundaries](approval-boundaries.md#authorization-source-and-records)).

### Review Triggers

Changes land in place with Task evidence; related documents:

- [Task checklists](task-checklists.md)
- [Quality standards](quality-standards.md#4-execution-boundary)
- [Documentation protocol](documentation-protocol.md)
- [Provider registry](providers/registry.yaml)
