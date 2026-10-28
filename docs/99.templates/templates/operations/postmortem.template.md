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
<!-- Author prompt: Write body prose in Korean; keep headings, paths, identifiers, and commands unchanged. -->

# {{TITLE}}

## Summary

{{SUMMARY}}

## Impact

{{IMPACT}}

## Timeline

<!-- Author prompt: Record factual events with ISO 8601 timestamps and explicit UTC offsets; distinguish hypotheses. -->

{{TIMELINE}}

## Analysis

### Root Cause

{{ROOT_CAUSE}}

### Contributing Factors

{{CONTRIBUTING_FACTORS}}

## Corrective Actions

<!-- Author prompt: Each action needs an owner, tracking ID and verification; avoid blame. Do not set a completion deadline. -->

| Action | Owner | Tracking ID | Verification |
| --- | --- | --- | --- |
| {{ACTION}} | {{ACTION_OWNER}} | {{TRACKING_ID}} | {{VERIFICATION}} |

### Follow-up Review

{{FOLLOW_UP_REVIEW}}

## Lessons

### Learning

{{LEARNING}}

### Detection and Response

{{DETECTION_AND_RESPONSE}}

## Related Documents

{{INCIDENT_RUNBOOK_AND_TASK_LINKS}}
