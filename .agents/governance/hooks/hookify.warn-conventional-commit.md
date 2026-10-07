---
title: "WARNING: non-Conventional Commit message"
version: "1.0.2"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
action: "warn"
enabled: true
event: "bash"
name: "warn-conventional-commit"
pattern: "git\\s+commit\\s+(?!.*--amend|.*-C[\\s=]).*-m\\s+(\"|\\')(?!(build|chore|ci|deps|docs|feat|fix|perf|refactor|release|revert|style|test)(\\([^)]*\\))?!?:[ \\t]|Merge\\s|Revert\\s|Initial commit)"
---

# WARNING: non-Conventional Commit message

## Overview

Apply the declared `warn` action for warn-conventional-commit.

## Scope

The declared `bash` event and `pattern` define the matching scope; native event delivery remains a separate observation.

## Rules

**Non-Conventional Commit message detected (project rule)**

The message does not follow Commit Standards in
`.agents/governance/git-workflow.md`.

**Required format:**

```text
<type>[(scope)][!]: <description>
```

Allowed types are the keys in `.cz.toml`'s `change_type_map`. This warning's
pattern is a lightweight translation of that map. Explicit Commitizen checks
the complete grammar before commit, and the remote candidate checks its
authenticated contributor range. A `commit-msg` hook enforces that grammar only
when its installation and delivery are actually observed.

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

## Exceptions

No exception is declared by this rule.

## Related Documents

- `.agents/README.md`
