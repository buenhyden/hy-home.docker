---
title: "WARNING: non-Conventional Commit message"
version: "1.0.6"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
action: "warn"
enabled: true
event: "bash"
name: "warn-conventional-commit"
pattern: "git\\s+commit\\s+(?!.*--amend|.*-C[\\s=]).*-m\\s+(\"|\\')(?!(build|chore|ci|deps|docs|feat|fix|perf|refactor|release|revert|style|test)(\\([^)]*\\))?!?:[ \\t]|Merge\\s|Revert\\s|Initial commit)"
---

# WARNING: non-Conventional Commit message

## Purpose

### Objective

Apply the declared `warn` action for warn-conventional-commit.

### Authority

Owning policy: [Git workflow](../git-workflow.md).

## Scope

### Applies To

The `warn-conventional-commit` rule applies on the `bash` event and matches Bash commands that match its `pattern` ("WARNING: non-Conventional Commit message"). The frontmatter owns the exact matcher.

### Exclusions

**Exclusions:** `--amend`, `-C` (message reuse), `Merge`, `Revert`, `Initial commit`

## Rules

### Requirements

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

Reference issue IDs, ADR IDs, or plan/task IDs in the footer when applicable.

### Enforcement

Native event delivery is a separate observation from the frontmatter match.

## Exceptions

### Exception Conditions

No exception is declared by this rule.

### Approval and Review

None: this document states no separate approval or review step.

## Ownership

### Responsibilities

The rule owner is `@buenhyden`.

### Change and Adoption

Canonical governance navigation:

- `.agents/README.md`
