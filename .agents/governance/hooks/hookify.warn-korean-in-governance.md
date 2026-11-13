---
title: "WARNING: Korean text in governance documentation"
version: "1.1.4"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
action: "warn"
conditions:
- "field": "file_path"
  operator: "regex_match"
  pattern: "(^|/)(\\.agents/(?:[^/]+/)*(?!README\\.md$)[^/]+\\.md|\\.(claude|codex)/provider\\.md)$"
- "field": "new_text"
  operator: "regex_match"
  pattern: "[\\uac00-\\ud7a3\\u3131-\\u318e]"
enabled: true
event: "file"
name: "warn-korean-in-governance"
---

# WARNING: Korean text in governance documentation

## Purpose

### Objective

Apply the declared `warn` action for warn-korean-in-governance.

### Authority

Owning policy: `.agents/governance/documentation-protocol.md`.

## Scope

### Applies To

The `warn-korean-in-governance` rule applies on the `file` event and matches file edits whose path and text meet every structured `conditions` entry ("WARNING: Korean text in governance documentation"). The frontmatter owns the exact matcher.

### Exclusions

It skips `README.md` files, whose language the documentation protocol owns; the negative lookahead in the path pattern is what excludes them, so keep it when editing the pattern.

## Rules

### Requirements

**Korean text detected in governance documentation (project rule)**

This hook is an advisory detector. Resolve the file's language through the sole
document-role authority at
`.agents/governance/documentation-protocol.md#document-language`;
the hook does not publish a second language table or exception rule.

### Enforcement

Native event delivery is a separate observation from the frontmatter match.

## Exceptions

### Exception Conditions

No exception is declared by this rule.

### Approval and Review

None.

## Ownership

### Responsibilities

`@buenhyden`.

### Change and Adoption

`.agents/README.md`.
