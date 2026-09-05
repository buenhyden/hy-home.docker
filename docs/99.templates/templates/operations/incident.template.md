---
title: "{{TITLE}}"
version: "0.1.0"
type: "operation/incident"
status: "detected"
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

# {{TITLE}}

## Summary

{{SUMMARY}}

## Impact

{{IMPACT}}

## Coordination

{{ROLES_AND_COORDINATION}}

## Timeline

<!-- Author prompt: Record factual events with ISO 8601 timestamps and explicit UTC offsets; distinguish hypotheses. -->

{{TIMELINE}}

## Mitigation

{{MITIGATION}}

## Current Status

{{CURRENT_STATUS}}

## Corrective Actions

<!-- Author prompt: Record observed mitigation and tracked next actions; move causal analysis and durable follow-up to the postmortem after stabilization. -->

{{CORRECTIVE_ACTIONS}}

## Traceability

{{RUNBOOK_AND_SYSTEM_LINKS}}

## Communications

{{COMMUNICATIONS}}
