---
name: warn-branch-naming
enabled: true
event: bash
pattern: git\s+(checkout\s+-b|switch\s+-c)\s+(?!(feat|fix|hotfix|docs|style|refactor|perf|test|build|ci|chore|revert|dependabot|codex)/)
action: warn
---

<!-- markdownlint-disable MD041 MD040 -->

**Branch naming rule violation detected (project rule)**

The branch name does not follow the Branching Strategy in
`docs/00.agent-governance/rules/git-workflow.md`.

**Allowed prefixes:**

| prefix | Purpose |
| ------ | ------- |
| `feat/<issue-id>-<description>` | new feature |
| `fix/<issue-id>-<description>` | bug fix |
| `hotfix/<issue-id>-<description>` | urgent production fix |
| `docs/`, `style/`, `refactor/` | documentation, style, or refactor work |
| `perf/`, `test/`, `build/`, `ci/`, `chore/`, `revert/` | other Conventional Commit types |
| `dependabot/**`, `codex/**` | automation-owned branches |

**Correct examples:**

```bash
git checkout -b feat/42-add-nginx-service
git checkout -b fix/17-fix-volume-mount
git checkout -b hotfix/99-patch-secret-leak
```

Do not work directly on `main`. Start from a feature or fix branch.

## Related Documents

- `docs/00.agent-governance/README.md`
