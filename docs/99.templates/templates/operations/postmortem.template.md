---
title: "{{TITLE}}"
version: "0.1.0"
type: "operation/postmortem"
status: "draft"
owner: "{{OWNER}}"
updated: "{{UPDATED}}"
layer: "operations"
artifact_id: "{{ARTIFACT_ID}}"
parent_ids:
- "{{PARENT_ID}}"
created: "{{CREATED}}"
---

<!-- Author prompt: Replace every {{UPPER_SNAKE_CASE}} value and remove this comment before publishing. -->
<!-- Author prompt: When the postmortem is reviewed, add optional `reviewed_at` after `created`. -->
<!-- Author prompt: Write body prose in Korean; keep headings, paths, identifiers, and commands unchanged. -->

# {{TITLE}}

## Facts

### Timeline

<!-- Author prompt: Name the incident and the reviewed period, then the events with their recorded timestamps. -->

{{TIMELINE}}

### Impact

{{IMPACT}}

## Causes

### Contributing Factors

<!-- Author prompt: Record only verified causes and the conditions that let them act; avoid blame. -->

{{CONTRIBUTING_FACTORS}}

### Uncertainty

{{UNCERTAINTY}}

## Actions

### Prevention

{{PREVENTION}}

### Owners and Checks

<!-- Author prompt: Each action needs an owner, the condition that completes it and the evidence that checks it; Evidence names the tracking record or link and the check; `none` only for a lesson row with no corrective action. Do not set a completion deadline. -->

| Action | Owner | Condition | Evidence |
| --- | --- | --- | --- |
| {{ACTION}} | {{ACTION_OWNER}} | {{CONDITION}} | {{EVIDENCE}} |
