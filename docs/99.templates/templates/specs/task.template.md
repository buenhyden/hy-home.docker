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
<!-- Author prompt: Before setting status to cancelled, supply cancellation frontmatter with a nonempty reason, an actual authorization_ref, and criteria_disposition entries containing an integer criterion plus exactly one successor Task identity or approved withdrawal_ref. A successor is another non-cancelled Task in the same package. authorization_ref and withdrawal_ref use unambiguous same-Task heading anchors to actual structural evidence; those records do not authenticate or grant approval. An empty criteria_disposition list states that this Task held no criterion; it does not close any Spec criterion. Never seed or infer cancellation approval. -->
<!-- Author prompt: Keep the Evidence header, separator, and every data row in one contiguous pipe-table block. Narrative may appear before or after that block; put other pipe tables outside the Evidence section. -->
<!-- Author prompt: Evidence records observations only. Required is required or optional. Result is PASS, FAIL, ERROR, NOT_RUN, CANCELLED or NOT_APPLICABLE; every required non-PASS observation remains open until an equivalent PASS explicitly resolves it. Name each row uniquely. In Resolves, write `-` or the names of earlier non-PASS rows with the same Check and Work Unit in this Task that this PASS row resolves for a shared criterion. -->
<!-- Author prompt: Criterion Acceptance holds one row for each Spec criterion this Task owns. A criterion the Plan assigns to a current, non-cancelled Task has exactly one row, in one such Task; a criterion whose assigned Tasks are all historical or cancelled has none. Acceptance is pending, accepted, rejected or not-required; accepted needs a PASS row for the criterion and no unresolved required observation; not-required and rejected need a Decision. Current Owner names the durable owner or a reasoned N/A disposition. The Evidence cell is `-` or names of this Task's Evidence rows. -->
<!-- Author prompt: For several independently tracked items, add a `### Execution Items` table under Work Log with `Item | Work Unit | Scope | Owner | Status | Blocker` and at least two rows, and remove the frontmatter `status`; each row then owns its status, each Work Unit belongs to one item, and a blocked or cancelled item names its Blocker. -->

# {{TITLE}}

## Overview

### Objective

{{OBJECTIVE}}

## Inputs and Authorization

{{INPUTS_AND_AUTHORIZATION}}

## Work Log

{{WORK_LOG}}

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| {{EVIDENCE}} | {{CRITERIA}} | {{WORK_UNIT}} | {{CHECK}} | {{INPUT}} | {{RESULT}} | {{LOCATION}} | {{REQUIRED}} | {{RESOLVES}} |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| {{CRITERION}} | {{ACCEPTANCE}} | {{ACCEPTANCE_EVIDENCE}} | {{DECISION}} | {{CURRENT_OWNER}} |

## Review and Completion

{{REVIEW_AND_COMPLETION}}

## Related Documents

{{RELATED_DOCUMENTS}}
