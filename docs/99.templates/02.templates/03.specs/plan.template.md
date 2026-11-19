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
<!-- Author prompt: A Plan holds strategy only. Execution state and check results live in the Task; link to it instead of copying them. -->

# {{TITLE}}

## Overview

### Outcome

<!-- Author prompt: Name the parent Spec and what this Plan delivers. -->

{{PARENT_SPEC_AND_OUTCOME}}

### Constraints

<!-- Author prompt: Separate facts from assumptions, and name the constraints and the authority this Plan works under. -->

{{ASSUMPTIONS_CONSTRAINTS_AND_AUTHORITY}}

## Dependencies

### Prerequisites

{{EXISTING_CONTRACTS_CONSUMERS_PERMISSIONS_AND_ENVIRONMENT}}

### Shared Resources

<!-- Author prompt: Name the files, services and environments more than one work unit or Task touches, and how their use is ordered. -->

{{SHARED_RESOURCES_AND_THEIR_ORDER}}

## Work Breakdown

### Work Units

<!-- Author prompt: Keep the Work Units header, separator, and every data row in one contiguous pipe-table block, and put no other pipe table under Work Breakdown. Work Unit is a stable W-number; Outcome what it delivers; Depends On `None` or earlier W-numbers; Owner the same-package Task or Tasks that execute it; Write Scope the paths it may change; Acceptance the numbered Spec criteria it serves; Checks the Check IDs it selects. -->

| Work Unit | Outcome | Depends On | Owner | Write Scope | Acceptance | Checks |
| --- | --- | --- | --- | --- | --- | --- |
| {{WORK_UNIT}} | {{OUTCOME}} | {{DEPENDS_ON}} | {{OWNER_TASK}} | {{WRITE_SCOPE}} | {{ACCEPTANCE}} | {{CHECKS}} |

### Dependency Edges

<!-- Author prompt: State each work unit's inputs and outputs, the order the Depends On column implies, the change method and the rollback order. -->

{{WORK_UNIT_ORDER_CHANGE_AND_ROLLBACK}}

## Verification Plan

### Selected Checks

<!-- Author prompt: List each check the work units select: Check ID is a stable identifier in this Plan, Guarantee what only that check proves, Input what it reads, Trust Boundary what it does not prove, Required When the condition that selects it, and Evidence the kind of observation it must produce. -->

| Check ID | Guarantee | Input | Trust Boundary | Required When | Evidence |
| --- | --- | --- | --- | --- | --- |
| {{CHECK_ID}} | {{GUARANTEE}} | {{INPUT}} | {{TRUST_BOUNDARY}} | {{REQUIRED_WHEN}} | {{EVIDENCE}} |

### Evidence Plan

<!-- Author prompt: Say which checks run at commit, push, pull request and merge without running the same check twice, who produces the evidence, and what stops the work. -->

{{CHECK_STAGES_EVIDENCE_PRODUCERS_AND_STOP_CONDITIONS}}

## Promotion Map

### Durable Owners

<!-- Author prompt: Name the contract or operating meaning that outlives this package and the current document that will hold it. -->

{{DURABLE_MEANING_AND_OWNER_DOCUMENTS}}

### Consumer Updates

<!-- Author prompt: For each durable meaning, name the intended change, the consumers to update, the handoff condition and the Task whose Promotion Receipt will record it. Do not copy the receipt or any Task result here. -->

{{CONSUMER_UPDATES_AND_TASK_RECEIPT}}
