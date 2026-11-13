---
title: "WARNING: canonical governance root authority edit"
version: "1.0.5"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
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

## Purpose

### Objective

Apply the declared `warn` action for warn-governance-memory-edit.

### Authority

Owning policy: `.agents/governance/sdlc.md`.

## Scope

### Applies To

The `warn-governance-memory-edit` rule applies on the `file` event and matches file edits whose path meets its structured `conditions` entry ("WARNING: canonical governance root authority edit"). The frontmatter owns the exact matcher.

### Exclusions

None: this document states no exclusion.

## Rules

### Requirements

**Canonical governance root authority edit detected**

Confirm that the change preserves the registered canonical governance inventory, routes
document shapes to Stage 99, records evidence in the co-located Task, and
regenerates provider projections when their inputs change.

### Enforcement

Native event delivery is a separate observation from the frontmatter match.

## Exceptions

### Exception Conditions

No exception is declared by this rule.

### Approval and Review

None: this document states no separate approval or review step.

## Ownership

### Responsibilities

The rule owner is `@buenhyden`.

### Change and Adoption

Canonical governance navigation:

- `.agents/README.md`
