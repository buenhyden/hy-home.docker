---
title: "WARNING: parallel replacement document file"
version: "1.0.5"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-11-06"
action: "warn"
conditions:
- "field": "file_path"
  operator: "regex_match"
  pattern: "(^|/)(docs|\\.agents)/.*(-new|-v\\d+|-updated|-revised|-backup|-copy|-old|-draft|-temp|-tmp)\\.md$"
enabled: true
event: "file"
name: "warn-parallel-doc-file"
---

# WARNING: parallel replacement document file

## Overview

Apply the declared `warn` action for warn-parallel-doc-file.

## Scope

The `warn-parallel-doc-file` rule applies on the `file` event and matches file edits whose path meets its structured `conditions` entry ("WARNING: parallel replacement document file"). The frontmatter owns the exact matcher.

## Rules

**Parallel replacement document file detected (project rule)**

`.agents/governance/bootstrap.md#hard-constraints`:

> "Use in-place canonical edits; do not create legacy redirects or parallel
> authority copies."

**Forbidden file patterns:**

- `*-new.md`, `*-v2.md`, `*-updated.md`
- `*-revised.md`, `*-backup.md`, `*-copy.md`
- `*-old.md`, `*-draft.md`, `*-temp.md`

**Correct approach:**

Edit the existing canonical file in place.

```bash
# doc-paths: illustrative

# WARNING: parallel replacement document file
docs/03.specs/0158-example/spec-new.md

# ALLOWED
docs/03.specs/0158-example/spec.md
```

Before creating a file, check whether a canonical document already exists and
edit that file directly. Record sequencing and execution evidence only in the
same Spec Package's `plan.md` and `tasks/tsk-####-*.md`; do not create a
parallel Plan, Task, progress, or handoff authority. Git history preserves the
change record.

## Exceptions

No exception is declared by this rule.

## Verification

Native event delivery is a separate observation from the frontmatter match.

## Related Documents

- `.agents/README.md`
