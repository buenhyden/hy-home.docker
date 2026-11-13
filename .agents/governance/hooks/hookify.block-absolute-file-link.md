---
title: "BLOCKED: absolute file:// link"
version: "1.0.5"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
action: "block"
conditions:
- "field": "file_path"
  operator: "regex_match"
  pattern: "\\.md$"
- "field": "new_text"
  operator: "regex_match"
  pattern: "\\]\\(file://|href=[\"']file://"
enabled: true
event: "file"
name: "block-absolute-file-link"
---

# BLOCKED: absolute file:// link

## Purpose

### Objective

Apply the declared `block` action for block-absolute-file-link.

### Authority

No governance policy states the file:// ban; this rule owns it.

## Scope

### Applies To

The `block-absolute-file-link` rule applies on the `file` event and matches file edits whose path and text meet every structured `conditions` entry ("BLOCKED: absolute file:// link"). The frontmatter owns the exact matcher.

### Exclusions

None.

## Rules

### Requirements

**Absolute `file://` link blocked (project rule)**

The document link contract and this hook require portable repository links.
Use a relative path instead of a machine-specific `file://` URL.

**Why this is forbidden:**

- `file://` links work only on one local machine.
- They break in CI, for other developers, and in GitHub rendering.
- They break SSoT traceability.

**Correct link format:**

```markdown
<!-- BLOCKED: absolute file URL -->
[document link](file:///home/hy/projects/hy-home.docker/docs/01.requirements/0001-gateway.md)

<!-- ALLOWED from inside docs/: relative link -->
[document link](../01.requirements/0001-gateway.md)

<!-- ALLOWED from outside docs/: entry point plus the path as text -->
[Documentation index](../../../docs/README.md) - `docs/01.requirements/0001-gateway.md`
```

Calculate relative paths from the current file location.

The declared action applies when the pattern matches.

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

None.
