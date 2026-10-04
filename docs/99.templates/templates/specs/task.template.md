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
<!-- Author prompt: Write body prose in English; keep headings, paths, identifiers, and commands unchanged. -->
<!-- Author prompt: Before setting status to cancelled, supply cancellation frontmatter with a nonempty reason and approved_by, a valid approved_at date, and criteria entries containing an integer criterion plus exactly one reassigned_to Task identity or nonempty withdrawn reason. An empty criteria list states that this Task held no criterion; it does not waive Spec completion evidence. Never seed or infer cancellation approval. -->

# {{TITLE}}

## Objective

{{OBJECTIVE}}

## Inputs

{{INPUTS}}

## Work Log

{{WORK_LOG}}

<!-- Author prompt: For an observed direct registered transition in this package, add the optional `### Lifecycle Events` subsection here with the exact `Artifact | From | To | Evidence` table. Evidence must name a real same-Task anchor. Remove the whole optional subsection when no event is observed; do not seed approval or execution timestamps. -->

## Verification Evidence

{{RED_GREEN_AND_GATE_EVIDENCE}}

<!-- Author prompt: Fill the promotion receipt using .agents/governance/sdlc.md. Task result is exactly one of NOT_RUN, PASS, FAIL, DEFER, or NOT_APPLICABLE; link genuine evidence or record its reason in the durable-owner cell. -->
<!-- Author prompt: A single logical Task keeps the four-column receipt below, whose status source is frontmatter. For multiple acceptance-criterion/work-unit items, deliberately replace it with one five-column receipt: `| Acceptance criterion | Plan work unit | Status | Task result | Durable owner |`; its Status cells are the source and frontmatter stores the validated derived summary. Do not add another progress table. -->

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| {{CRITERION_NUMBER}} | {{WORK_UNIT}} | {{TASK_RESULT}} | {{DURABLE_OWNER_OR_REASON}} |

## Review Evidence

{{REVIEW_EVIDENCE}}

<!-- Author prompt: For every numbered acceptance criterion, add one row using the registered review table. `not-required` records a review disposition only; it never waives the Task's PASS completion evidence. -->

| Acceptance criterion | Acceptance | Evidence |
| --- | --- | --- |
| {{CRITERION_NUMBER}} | {{REVIEW_ACCEPTANCE}} | {{REVIEW_EVIDENCE}} |

## Commit Ledger

{{COMMIT_LEDGER}}

## Rulings

{{RULINGS}}

## Deferred Items

{{DEFERRED_ITEMS}}
