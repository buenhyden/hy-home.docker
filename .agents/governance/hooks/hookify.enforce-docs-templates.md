---
title: "WARNING: template use required"
version: "1.1.5"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
action: "warn"
conditions:
- "field": "file_path"
  operator: "regex_match"
  pattern: "(^|/)docs/(0[1-5]|90)\\."
enabled: true
event: "file"
name: "enforce-docs-templates"
---

# WARNING: template use required

## Purpose

### Objective

Apply the declared `warn` action for enforce-docs-templates.

### Authority

Owning policies:

- [Documentation protocol](../documentation-protocol.md)
- [Stage authoring matrix](../stage-authoring-matrix.md)

## Scope

### Applies To

The `enforce-docs-templates` rule applies on the `file` event and matches file edits whose path meets its structured `conditions` entry ("WARNING: template use required"). The frontmatter owns the exact matcher.

### Exclusions

None.

## Rules

### Requirements

**Template use required (project rule)**

When creating or editing documents under `docs/01` through `docs/05` or
`docs/90`, follow the mapped template under `docs/99.templates/templates/`.

The canonical `.agents/governance/documentation-protocol.md` authoring rules
require selecting the Stage 99 profile and preserving its metadata, links, and
stage-specific contract. The Registry owns the mapped template for each profile.

**Required actions:**

1. Read the mapped template under `docs/99.templates/templates/` before editing.
2. Preserve required heading structure.
3. Remove all temporary placeholders before saving.
4. Keep related links in the section the template declares for them, such as
   `Traceability` or `References` for a role on the common form and
   `## Related Documents` for a role that has not moved.

After editing, inspect `python3 scripts/validation/run-ci-gate.py --profile changed --explain`.
This selects checks without executing or accepting template validation.

The plan inspection does not execute QA. Follow the current
[quality policy](../quality-standards.md#canonical-delivery-phase-matrix) for
focused authoring checks and remote PR candidate validation.

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
