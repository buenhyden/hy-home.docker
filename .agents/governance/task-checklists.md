---
title: "Task Checklists"
version: "1.6.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
---

# Task Checklists

## Purpose and Scope

### Objective

Check scope, implementation evidence, and completion before changing repository state.

#### Authority

This policy is the canonical owner of the task checklists for editing, work, and completion under [bootstrap precedence](bootstrap.md#authority-and-precedence).

### Applies To

Approved repository edits, ongoing implementation, and completion evidence.

#### Exclusions

None: this document states no exclusion.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| TASK-CHECKLISTS-R1 | Before editing repository state | Required: confirm the approved objective, editable paths, protected surfaces and exclusions | none | none |
| TASK-CHECKLISTS-R2 | Before editing repository state | Required: load applicable Requirement, Architecture, Spec, Plan, Task, policy and skill sources | none | none |
| TASK-CHECKLISTS-R3 | Before editing repository state | Required: bind high-risk policy, runtime, CI, template, secret, remote, model and provider changes to explicit approval, validation and recovery | none | none |
| TASK-CHECKLISTS-R4 | Before editing repository state | Required: define acceptance checks | none | none |
| TASK-CHECKLISTS-R5 | Before editing repository state | Required: inspect the shared worktree | none | none |
| TASK-CHECKLISTS-R6 | During work | Required: keep changes traceable to the approved Plan Task | none | none |
| TASK-CHECKLISTS-R7 | During work | Required: keep canonical sources separate from generated provider projections | none | none |
| TASK-CHECKLISTS-R8 | During work | Required: preserve secrets and private state | none | none |
| TASK-CHECKLISTS-R9 | Secrets and private state | Required: record metadata only | none | none |
| TASK-CHECKLISTS-R10 | During work | Required: update affected links | none | none |
| TASK-CHECKLISTS-R11 | During work | Required: eliminate conflicting active guidance | none | none |
| TASK-CHECKLISTS-R12 | During work | Required: record actual evidence in the Task | none | the Task |
| TASK-CHECKLISTS-R13 | During work | Forbidden: recording evidence in a second progress or handoff document | none | none |
| TASK-CHECKLISTS-R14 | Missing authority, destructive ambiguity or unexpected scope | Required: stop | none | none |

#### Before Editing

- [ ] Confirm the approved objective, editable paths, protected surfaces, and exclusions.
- [ ] Load applicable Requirement, Architecture, Spec, Plan, Task, policy, and skill sources.
- [ ] Bind high-risk policy, runtime, CI, template, secret, remote, model, and
      provider changes to explicit approval, validation, and recovery.
- [ ] Define acceptance checks and inspect the shared worktree.

#### During Work

- [ ] Keep changes traceable to the approved Plan Task.
- [ ] Keep canonical sources separate from generated provider projections.
- [ ] Preserve secrets and private state; record metadata only.
- [ ] Update affected links and eliminate conflicting active guidance.
- [ ] Record actual evidence in the Task, not a second progress or handoff document.
- [ ] Stop on missing authority, destructive ambiguity, or unexpected scope.

### Exceptions

#### Exception Conditions

No exception is granted here; a separately authorized operation follows [Approval boundaries](approval-boundaries.md).

#### Approval and Review

None: no exception exists to approve.

## Enforcement

### Mechanisms

#### Before Completion

- [ ] Follow the [execution boundary](quality-standards.md#4-execution-boundary)
      for staged lint/format immediately before local commit, server PR final
      defense, direct pre-commit prohibition and the separate all-files route.
- [ ] Run focused tests and validators for each changed authority surface.
- [ ] For registered projections whose inputs changed, regenerate through the
      registered renderer and prove byte-for-byte freshness; do not write
      unaffected projections.
- [ ] Inspect `git diff --check`, status, and the exact task-owned diff.
- [ ] Record pass, fail, baseline debt, skipped checks, recovery, and review separately.
- [ ] Record final criterion acceptance before disposition. A Stage 03 package
      may wait once it is [ready for removal review](sdlc.md#sequence);
      cancelled criteria do not waive remaining Spec acceptance evidence, and
      closing a criterion follows the [SDLC](sdlc.md#sequence) decisions.
- [ ] Before removing a retired document, meet the
      [retirement preconditions](documentation-protocol.md#retirement-preconditions);
      delete a Stage 03 package only as the [SDLC](sdlc.md#sequence) allows.
- [ ] Distinguish the worktree, index, and commit a review examined, and report
      missing history or unsupported checkout conversion without claiming success.
- [ ] Create logical Conventional Commits after the review findings are resolved.

### Limits

No check, script or review is tied to any rule in Requirements.

- Before Editing (R1-R5): no check is named.
- During Work (R6-R14): no check is named.
- Rules stated under Enforcement (Mechanisms) are outside this table.

## Ownership

### Owner

`@buenhyden` approves changes; `rules-engineer` reviews them ([approval boundaries](approval-boundaries.md#authorization-source-and-records)).

### Review Triggers

Changes land in place with Task evidence; related documents:

- [Agentic policy](agentic.md)
- [Approval boundaries](approval-boundaries.md)
- [Git workflow](git-workflow.md)
- [Postflight checklist](postflight-checklist.md)
