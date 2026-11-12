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

## Summary

### Incident Reference

{{INCIDENT_REFERENCE}}

### Review Scope

{{REVIEW_SCOPE}}

## Root Cause

### Causal Analysis

{{CAUSAL_ANALYSIS}}

### Contributing Factors

{{CONTRIBUTING_FACTORS}}

## Impact

### Observed Impact

{{OBSERVED_IMPACT}}

### Detection and Response

{{DETECTION_AND_RESPONSE}}

## Corrective Actions

### Actions

<!-- Author prompt: Each action needs an owner, tracking ID and verification; avoid blame. Do not set a completion deadline. -->

| Action | Owner | Tracking ID | Verification |
| --- | --- | --- | --- |
| {{ACTION}} | {{ACTION_OWNER}} | {{TRACKING_ID}} | {{VERIFICATION}} |

### Verification

{{FOLLOW_UP_REVIEW}}

## Evidence

### Source Records

{{SOURCE_RECORDS}}

### Review Decision

{{REVIEW_DECISION}}
