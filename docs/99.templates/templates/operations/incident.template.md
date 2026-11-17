---
title: "{{TITLE}}"
version: "0.1.0"
type: "operation/incident"
status: "open"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
layer: "operations"
artifact_id: "{{ARTIFACT_ID}}"
parent_ids:
- "{{PARENT_ID}}"
created: "{{CREATED}}"
occurred_at: "{{OCCURRED_AT}}"
---

<!-- Author prompt: Replace every {{UPPER_SNAKE_CASE}} value and remove this comment before publishing. -->
<!-- Author prompt: When status becomes `resolved`, add `resolved_at` (ISO 8601 with UTC offset) after `occurred_at`; the status requires it. -->
<!-- Author prompt: Write body prose in Korean; keep headings, paths, identifiers, and commands unchanged. -->

# {{TITLE}}

## Impact

### Affected Users

{{AFFECTED_USERS}}

### Observed Scope

<!-- Author prompt: Record the affected targets and when the impact was observed, with actual timestamps and their timezone. Derive any current lifecycle label from frontmatter status; do not keep a second current-state value or invent precision. -->

{{OBSERVED_SCOPE}}

## Response

### Timeline

<!-- Author prompt: Record factual events with ISO 8601 timestamps and explicit UTC offsets; distinguish hypotheses. -->

{{TIMELINE}}

### Actions

<!-- Author prompt: Add one row per action actually taken and keep the table without rows until one is. Owner names who acted or says it is unrecorded; Evidence names a record or `none`. -->

| Action | Owner | Condition | Evidence |
| --- | --- | --- | --- |
| {{ACTION}} | {{ACTION_OWNER}} | {{CONDITION}} | {{EVIDENCE}} |

## Resolution

### Verified State

{{VERIFIED_STATE}}

### Remaining Work

<!-- Author prompt: Record tracked next actions and their owners; move causal analysis and durable follow-up to the postmortem after stabilization. -->

{{REMAINING_WORK}}
