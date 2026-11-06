---
title: "WARNING: canonical governance root authority edit"
version: "1.0.4"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-11-06"
action: "warn"
conditions:
- "field": "file_path"
  operator: "regex_match"
  pattern: "(^|/)\\.agents/(README\\.md|governance/sdlc\\.md)$"
enabled: true
event: "file"
name: "warn-governance-memory-edit"
---

# WARNING: canonical governance root authority edit

## Overview

Apply the declared `warn` action for warn-governance-memory-edit.

## Scope

The `warn-governance-memory-edit` rule applies on the `file` event and matches file edits whose path meets its structured `conditions` entry ("WARNING: canonical governance root authority edit"). The frontmatter owns the exact matcher.

## Rules

**Canonical governance root authority edit detected**

Confirm that the change preserves the registered canonical governance inventory, routes
document shapes to Stage 99, records evidence in the co-located Task, and
regenerates provider projections when their inputs change.

## Exceptions

No exception is declared by this rule.

## Verification

Native event delivery is a separate observation from the frontmatter match.

## Related Documents

- `.agents/README.md`
- `.agents/governance/sdlc.md`
