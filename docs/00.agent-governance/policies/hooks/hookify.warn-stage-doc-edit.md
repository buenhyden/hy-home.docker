---
title: "WARNING: Stage document edit"
version: "1.0.0"
type: "governance/hook-policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-04"
action: "warn"
conditions:
- field: "file_path"
  operator: "regex_match"
  pattern: "(^|/)docs/(0[1-9]|[1-9][0-9])\\."
enabled: true
event: "file"
name: "warn-stage-doc-edit"
---

<!-- markdownlint-disable MD041 MD040 -->

**Stage document edit detected (project rule)**

`docs/01` through `docs/99` are **read-only by default**.

**AGENTS.md policy:**
> `docs/01` to `docs/99` are read-only by default; modify only with explicit user instruction.

**Before editing, confirm:**

- [ ] The user explicitly authorized the stage document edit.
- [ ] The target is inside an active stage artifact directory (`docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/05.operations`, `docs/90.references`, `docs/99.templates`).
- [ ] The edit is in-place; no parallel replacement file is being created.
- [ ] This rule applies whether the path arrives as `docs/...` or `/.../docs/...`.

**After editing, verify:**

```bash
python3 scripts/validation/run-ci-gate.py --profile changed
```

## Related Documents

- `docs/00.agent-governance/README.md`
