---
title: "WARNING: Stage document edit"
version: "1.1.4"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
action: "warn"
conditions:
- "field": "file_path"
  operator: "regex_match"
  pattern: "(^|/)docs/(0[1-9]|[1-9][0-9])\\."
enabled: true
event: "file"
name: "warn-stage-doc-edit"
---

# WARNING: Stage document edit

## Purpose

### Objective

Apply the declared `warn` action for warn-stage-doc-edit.

### Authority

Owning policy: [Agent Bootstrap Policy](../bootstrap.md#hard-constraints).

## Scope

### Applies To

The `warn-stage-doc-edit` rule applies on the `file` event and matches file edits whose path meets its structured `conditions` entry ("WARNING: Stage document edit"). The frontmatter owns the exact matcher.

### Exclusions

None: this document states no exclusion.

## Rules

### Requirements

**Stage document edit detected (project rule)**

`docs/01` through `docs/99` are **read-only by default**.

**Canonical bootstrap policy (`bootstrap.md#hard-constraints`):**
> "Stage documents are read-only unless the request authorizes change."

**Before editing, confirm:**

- [ ] The user explicitly authorized the stage document edit.
- [ ] The target is inside an active stage artifact directory (the stages listed in [stage-authoring-matrix.md](../stage-authoring-matrix.md)).
- [ ] The edit is in-place; no parallel replacement file is being created.
- [ ] This rule applies whether the path arrives as `docs/...` or `/.../docs/...`.

**After editing, inspect the selected plan:**

```bash
python3 scripts/validation/run-ci-gate.py --profile changed --explain
```

The plan inspection does not execute QA. Follow the current
[quality policy](../quality-standards.md#canonical-delivery-phase-matrix) for
focused authoring checks and remote PR candidate validation.

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
