---
name: warn-parallel-doc-file
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: docs/.*(-new|-v\d+|-updated|-revised|-backup|-copy|-old|-draft|-temp|-tmp)\.md$
action: warn
---

<!-- markdownlint-disable MD041 MD040 -->

**Parallel replacement document file detected (project rule)**

`AGENTS.md` — Hard Constraints violation:

> "Use in-place refactors only; do not create parallel replacement files for canonical docs."

**Forbidden file patterns:**

- `*-new.md`, `*-v2.md`, `*-updated.md`
- `*-revised.md`, `*-backup.md`, `*-copy.md`
- `*-old.md`, `*-draft.md`, `*-temp.md`

**Correct approach:**

Edit the existing canonical file in place.

```bash
# BLOCKED
docs/03.specs/service-spec-new.md

# ALLOWED
docs/03.specs/service-spec.md
```

Before creating a file, check whether a canonical document already exists and
edit that file directly. Git history preserves the change record.

## Related Documents

- `docs/00.agent-governance/README.md`
