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

## Overview

{{SUMMARY}}

## Impact

{{IMPACT}}

## Causes

### Root Cause

{{ROOT_CAUSE}}

### Contributing Factors

{{CONTRIBUTING_FACTORS}}

### Timeline

<!-- Author prompt: Record factual events with ISO 8601 timestamps and explicit UTC offsets; distinguish hypotheses. -->

{{TIMELINE}}

## Lessons

### Learning

{{LEARNING}}

### Detection and Response

{{DETECTION_AND_RESPONSE}}

## Corrective Actions

<!-- Author prompt: Each action needs an owner, due date, tracking ID and verification; avoid blame. -->

| Action | Owner | Due date | Tracking ID | Verification |
| --- | --- | --- | --- | --- |
| {{ACTION}} | {{ACTION_OWNER}} | {{DUE_DATE}} | {{TRACKING_ID}} | {{VERIFICATION}} |

### Follow-up Review

{{FOLLOW_UP_REVIEW}}

## Related Documents

{{INCIDENT_RUNBOOK_AND_TASK_LINKS}}
