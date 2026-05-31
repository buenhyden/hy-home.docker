---
name: warn-stage-doc-edit
enabled: true
event: file
conditions:
  - field: file_path
    operator: regex_match
    pattern: (^|/)docs/(0[1-9]|[1-9][0-9])\.
action: warn
---

<!-- markdownlint-disable MD041 MD040 -->

**Stage document edit detected (project rule)**

`docs/01` through `docs/99` are **read-only by default**.

**AGENTS.md policy:**
> `docs/01` to `docs/99` are read-only by default; modify only with explicit user instruction.

**Before editing, confirm:**

- [ ] The user explicitly authorized the stage document edit.
- [ ] The target is inside an active stage artifact directory (`docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations`, `docs/90.references`, `docs/99.templates`).
- [ ] The edit is in-place; no parallel replacement file is being created.
- [ ] This rule applies whether the path arrives as `docs/...` or `/.../docs/...`.

**After editing, verify:**

```bash
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-repo-contracts.sh
```

## Related Documents

- `docs/00.agent-governance/README.md`
