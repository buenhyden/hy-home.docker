---
title: "WARNING: non-Conventional Commit message"
version: "1.0.2"
type: "governance/hook-policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-08"
action: "warn"
enabled: true
event: "bash"
name: "warn-conventional-commit"
pattern: "git\\s+commit\\s+(?!.*--amend|.*-C[\\s=]).*-m\\s+(\"|\\')(?!(build|chore|ci|deps|docs|feat|fix|perf|refactor|release|revert|style|test)(\\([^)]*\\))?!?:[ \\t]|Merge\\s|Revert\\s|Initial commit)"
---

<!-- markdownlint-disable MD041 MD040 -->

**Non-Conventional Commit message detected (project rule)**

The message does not follow Commit Standards in
`.agents/governance/git-workflow.md`.

**Required format:**

```
<type>[(scope)][!]: <description>
```

Allowed types are the keys in `.cz.toml`'s `change_type_map`. This warning's
pattern is a lightweight translation of that map; the `commit-msg` hook applies
the complete executable grammar.

**Correct examples:**

```bash
git commit -m "feat(nginx): Add rate limiting config"
git commit -m "fix(compose): Correct volume mount path"
git commit -m "docs(readme): Update service list"
git commit -m "chore!: Drop support for legacy volume names"
git commit -m "deps(pre-commit): Update Commitizen hook"
git commit -m "release: Publish v1.0.0"
```

**This rule detects:**

- `"Update something"`, `"Fix the bug"`, `"Add feature"` — missing type prefix
- `"feat something"` — missing colon separator
- `"FEAT: something"` — uppercase type

**Exclusions:** `--amend`, `-C` (message reuse), `Merge`, `Revert`, `Initial commit`

Reference issue IDs, ADR IDs, or plan/task IDs in the footer when applicable.

## Related Documents

- `.agents/README.md`
