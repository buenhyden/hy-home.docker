---
name: warn-conventional-commit
enabled: true
event: bash
pattern: git\s+commit\s+(?!.*--amend|.*-C[\s=]).*-m\s+("|\')(?!(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([^)]*\))?!?:[ \t]|Merge\s|Revert\s|Initial commit)
action: warn
---

<!-- markdownlint-disable MD041 MD040 -->

**Non-Conventional Commit message detected (project rule)**

The message does not follow Commit Standards in
`docs/00.agent-governance/rules/git-workflow.md`.

**Required format:**

```
<type>[(scope)][!]: <description>
```

**Allowed types:**

| type | Purpose |
| ---- | ------- |
| `feat` | new feature |
| `fix` | bug fix |
| `docs` | documentation change |
| `style` | formatting change with no behavior change |
| `refactor` | refactor with no feature or bug change |
| `perf` | performance improvement |
| `test` | test addition or change |
| `build` | build system change |
| `ci` | CI configuration change |
| `chore` | maintenance |
| `revert` | revert a commit |

**Correct examples:**

```bash
git commit -m "feat(nginx): add rate limiting config"
git commit -m "fix(compose): correct volume mount path"
git commit -m "docs(readme): update service list"
git commit -m "chore!: drop support for legacy volume names"
```

**This rule detects:**

- `"Update something"`, `"Fix the bug"`, `"Add feature"` — missing type prefix
- `"feat something"` — missing colon separator
- `"FEAT: something"` — uppercase type

**Exclusions:** `--amend`, `-C` (message reuse), `Merge`, `Revert`, `Initial commit`

Reference issue IDs, ADR IDs, or plan/task IDs in the footer when applicable.

## Related Documents

- `docs/00.agent-governance/README.md`
