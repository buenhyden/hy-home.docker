---
title: "{{TITLE}}"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
layer: "specs"
artifact_id: "{{ARTIFACT_ID}}"
parent_ids:
- "{{PARENT_ID}}"
created: "{{CREATED}}"
---

<!-- Author prompt: Replace every {{UPPER_SNAKE_CASE}} value and remove this comment before publishing. -->
<!-- Author prompt: Write body prose in English; keep headings, paths, identifiers, and commands unchanged. -->
<!-- Author prompt: Map each stable W-number to one or more numbered acceptance criteria without creating a second lifecycle or approval record. -->
<!-- Author prompt: Keep the Work Breakdown header, separator, and every data row in one contiguous pipe-table block. Narrative may appear before or after that block; put other pipe tables outside the Work Breakdown subsection. -->
<!-- Author prompt: A Plan holds strategy only. Execution state and check results live in the Task; link to it instead of copying them. -->

# {{TITLE}}

## Overview

### Goal and Boundary

{{PARENT_SPEC_AND_PLAN_BOUNDARY}}

### Assumptions

<!-- Author prompt: Separate facts from assumptions, and name the constraints and the authority this Plan works under. -->

{{ASSUMPTIONS_CONSTRAINTS_AND_AUTHORITY}}

## Dependencies

### Prerequisites

{{EXISTING_CONTRACTS_CONSUMERS_PERMISSIONS_AND_ENVIRONMENT}}

### Dependency Order

{{WORK_UNIT_INPUTS_OUTPUTS_AND_ORDER}}

## Implementation Strategy

### Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| {{WORK_UNIT}} | {{CRITERIA}} | {{WORK}} | {{DEPENDENCIES}} | {{TASK}} | {{VERIFICATION}} |

### Change and Rollback

{{CHANGE_METHOD_AND_ROLLBACK_ORDER}}

## Verification Plan

### Verification Matrix

<!-- Author prompt: For each criterion, name the normal, violating and regression cases, their inputs and who produces the evidence. -->

{{VERIFICATION_MATRIX}}

### Stage Placement

<!-- Author prompt: Say which checks run at commit, push, pull request and merge, without running the same check twice. -->

{{CHECK_STAGE_PLACEMENT}}

## Risks

### Risks and Mitigations

{{RISKS_DETECTION_MITIGATION_AND_OWNERS}}

### Escalation

{{BLOCKING_CONDITIONS_QUESTIONS_AND_RESUME_CONDITIONS}}

## Promotion Map

### Durable Meaning

<!-- Author prompt: Name the contract or operating meaning that outlives this package and the current document that will hold it. -->

{{DURABLE_CONTRACT_AND_OPERATING_MEANING}}

### Owner and Receipt

<!-- Author prompt: For each durable meaning, name the target owner document, the intended change and the handoff condition, and the Task whose Promotion Receipt will record it. Do not copy the receipt or any Task result here. -->

{{CURRENT_OWNER_VERIFICATION_AND_TASK_RECEIPT}}
