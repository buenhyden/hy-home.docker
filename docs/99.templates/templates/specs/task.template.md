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
<!-- Author prompt: Before setting status to cancelled, supply cancellation frontmatter with a nonempty reason and approved_by, a valid approved_at date, and criteria entries containing an integer criterion plus exactly one reassigned_to Task identity or nonempty withdrawn reason. An empty criteria list states that this Task held no criterion; it does not waive Spec completion evidence. Never seed or infer cancellation approval. -->

# {{TITLE}}

## Objective

{{OBJECTIVE}}

## Inputs

{{INPUTS}}

## Work Log

{{WORK_LOG}}

## Verification Evidence

{{RED_GREEN_AND_GATE_EVIDENCE}}

<!-- Author prompt: Fill the promotion receipt using .agents/governance/sdlc.md; record actual results and limits under the current approval and completion policies. -->

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
