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
<!-- Author prompt: Before setting status to cancelled, supply cancellation frontmatter with a nonempty reason, an actual authorization_ref, and criteria_disposition entries containing an integer criterion plus exactly one successor Task identity or approved withdrawal_ref. A successor is another non-cancelled Task in the same package. authorization_ref and withdrawal_ref use unambiguous same-Task heading anchors to actual structural evidence; those records do not authenticate or grant approval. An empty criteria_disposition list states that this Task held no criterion; it does not waive Spec completion evidence. Never seed or infer cancellation approval. -->
<!-- Author prompt: Keep the Evidence header, separator, and every data row in one contiguous pipe-table block. Narrative may appear before or after that block; put other pipe tables outside the Evidence section. -->

# {{TITLE}}

## Objective

{{OBJECTIVE}}

## Inputs and Authorization

{{INPUTS_AND_AUTHORIZATION}}

## Work Log

{{WORK_LOG}}

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| {{EVIDENCE}} | {{CRITERIA}} | {{WORK_UNIT}} | {{CHECK}} | {{INPUT}} | {{RESULT}} | {{LOCATION}} | {{ACCEPTANCE}} |

## Review and Completion

{{REVIEW_AND_COMPLETION}}

## Related Documents

{{RELATED_DOCUMENTS}}
