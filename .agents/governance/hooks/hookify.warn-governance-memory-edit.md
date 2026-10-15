---
title: "WARNING: canonical governance root authority edit"
version: "1.0.2"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-10-15"
action: "warn"
conditions:
- "field": "file_path"
  operator: "regex_match"
  pattern: "(^|/)\\.agents/(README\\.md|governance/sdlc\\.md)$"
enabled: true
event: "file"
name: "warn-stage00-root-edit"
---

# WARNING: canonical governance root authority edit

## Overview

Apply the declared `warn` action for warn-stage00-root-edit.

## Scope

`file` 이벤트의 `warn-stage00-root-edit` 규칙에 적용한다. 정확한 matcher는 이 문서의 frontmatter가 소유한다.

## Rules

**Canonical governance root authority edit detected**

Confirm that the change preserves the registered canonical governance inventory, routes
document shapes to Stage 99, records evidence in the co-located Task, and
regenerates provider projections when their inputs change.

## Exceptions

No exception is declared by this rule.

## Verification

The declared `file` event and structured `conditions` define the matching scope; native event delivery remains a separate observation.

## Related Documents

- `.agents/README.md`
- `.agents/governance/sdlc.md`
