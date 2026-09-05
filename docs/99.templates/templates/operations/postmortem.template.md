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

# {{TITLE}}

## Summary

{{SUMMARY}}

## Impact

{{IMPACT}}

## Timeline

<!-- Author prompt: Record factual events with ISO 8601 timestamps and explicit UTC offsets; distinguish hypotheses. -->

{{TIMELINE}}

## Root Cause

{{ROOT_CAUSE}}

## Contributing Factors

{{CONTRIBUTING_FACTORS}}

## Detection and Response

{{DETECTION_AND_RESPONSE}}

## Corrective Actions

<!-- Author prompt: Each action needs an owner, due date, tracking ID and verification; avoid blame. -->

| Action | Owner | Due date | Tracking ID | Verification |
| --- | --- | --- | --- | --- |
| {{ACTION}} | {{ACTION_OWNER}} | {{DUE_DATE}} | {{TRACKING_ID}} | {{VERIFICATION}} |

## Learning

{{LEARNING}}

## Traceability

{{INCIDENT_RUNBOOK_AND_TASK_LINKS}}

## Follow-up Review

{{FOLLOW_UP_REVIEW}}
