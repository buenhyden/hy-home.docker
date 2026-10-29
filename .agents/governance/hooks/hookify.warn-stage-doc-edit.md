---
title: "WARNING: Stage document edit"
version: "1.1.2"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-10-29"
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

## Overview

Apply the declared `warn` action for warn-stage-doc-edit.

## Scope

Applies to the `warn-stage-doc-edit` rule on the `file` event. The frontmatter of this document owns the exact matcher.

## Rules

**Stage document edit detected (project rule)**

`docs/01` through `docs/99` are **read-only by default**.

**Canonical environment policy:**
> `docs/01` to `docs/99` are read-only by default; modify only with explicit user instruction.

**Before editing, confirm:**

- [ ] The user explicitly authorized the stage document edit.
- [ ] The target is inside an active stage artifact directory (`docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/05.operations`, `docs/90.references`, `docs/99.templates`).
- [ ] The edit is in-place; no parallel replacement file is being created.
- [ ] This rule applies whether the path arrives as `docs/...` or `/.../docs/...`.

**After editing, inspect the selected plan:**

```bash
python3 scripts/validation/run-ci-gate.py --profile changed --explain
```

The plan inspection does not execute QA. Follow the current
[quality policy](../quality-standards.md#canonical-delivery-phase-matrix) for
focused authoring checks and remote PR candidate validation.

## Exceptions

No exception is declared by this rule.

## Verification

The declared `file` event and structured `conditions` define the matching scope; native event delivery remains a separate observation.

## Related Documents

- `.agents/README.md`
