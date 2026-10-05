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
<!-- Author prompt: Write body prose in Korean; keep headings, paths, identifiers, and commands unchanged. -->

# {{TITLE}}

## Overview

{{SUMMARY}}

## Impact

{{IMPACT}}

## Timeline

<!-- Author prompt: Record factual events with ISO 8601 timestamps and explicit UTC offsets; distinguish hypotheses. -->

{{TIMELINE}}

## Response

### Coordination

{{ROLES_AND_COORDINATION}}

### Mitigation

{{MITIGATION}}

### Communications

{{COMMUNICATIONS}}

## Resolution

### Current Status

<!-- Author prompt: Derive any current lifecycle label from frontmatter status. Describe observations with their actual timestamp and timezone; do not maintain a second independent current-state value or invent precision. -->
{{CURRENT_STATUS}}

### Corrective Actions

<!-- Author prompt: Record observed mitigation and tracked next actions; move causal analysis and durable follow-up to the postmortem after stabilization. -->

{{CORRECTIVE_ACTIONS}}

## Related Documents

{{RUNBOOK_AND_SYSTEM_LINKS}}
