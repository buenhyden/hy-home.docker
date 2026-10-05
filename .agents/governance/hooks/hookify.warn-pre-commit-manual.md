---
title: "WARNING: manual pre-commit execution"
version: "1.0.1"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
action: "warn"
enabled: true
event: "bash"
name: "warn-pre-commit-manual"
pattern: "pre-commit\\s+run"
---

**Manual `pre-commit run` detected (project rule)**

`.agents/governance/task-checklists.md` owns this boundary: agents never run
`pre-commit run` directly. An explicitly approved all-files gate uses only the
controlled wrapper under its Git-visible state and evidence requirements.

**Project pre-commit policy:**

- pre-commit hooks run **automatically** during `git commit`.
- Manual runs can create inconsistent evidence.
- CI performs separate lint and format validation.

**Correct approach:**

```bash
# WARNING: manual pre-commit execution

## Overview

Apply the declared `warn` action for warn-pre-commit-manual.

## Scope

The declared `bash` event and `pattern` define the matching scope; native event delivery remains a separate observation.

## Rules

pre-commit run --all-files
pre-commit run --files myfile.py

# ALLOWED: automatic execution during commit
git commit -m "feat(scope): my change"
# The pre-commit hook runs automatically.
```

If lint or format issues exist, fix the affected files directly before committing.

## Exceptions

No exception is declared by this rule.

## Related Documents

- `.agents/README.md`
