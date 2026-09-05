---
title: "{{TITLE}}"
version: "0.1.0"
type: "sdlc/task"
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

# {{TITLE}}

## Objective

{{OBJECTIVE}}

## Inputs

{{INPUTS}}

## Work Log

{{WORK_LOG}}

## Verification Evidence

{{RED_GREEN_AND_GATE_EVIDENCE}}

<!-- Author prompt: Before completing the owning Spec, map every numbered acceptance criterion to a declared Plan W-number. Record PASS with observed evidence or SKIP with a reason, and link the durable owner or explain N/A. This is the sole promotion receipt. -->

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| {{CRITERION_NUMBER}} | {{WORK_UNIT}} | {{RESULT_AND_EVIDENCE}} | {{DURABLE_OWNER_OR_REASON}} |

## Review Evidence

{{REVIEW_EVIDENCE}}

## Commit Ledger

{{COMMIT_LEDGER}}

## Rulings

{{RULINGS}}

## Deferred Items

{{DEFERRED_ITEMS}}
