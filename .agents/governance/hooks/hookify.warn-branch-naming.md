---
title: "WARNING: branch naming rule violation"
version: "1.0.7"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
action: "warn"
enabled: true
event: "bash"
name: "warn-branch-naming"
pattern: "git\\s+(checkout\\s+-b|switch\\s+-c)\\s+(?!(build|chore|ci|deps|docs|feat|fix|hotfix|perf|refactor|release|revert|style|test|renovate|codex)/)"
---

# WARNING: branch naming rule violation

## Purpose

### Objective

Apply the declared `warn` action for warn-branch-naming.

### Authority

Owning policy: [Git workflow](../git-workflow.md).

## Scope

### Applies To

The `warn-branch-naming` rule applies on the `bash` event and matches Bash commands that match its `pattern` ("WARNING: branch naming rule violation"). The frontmatter owns the exact matcher.

### Exclusions

None.

## Rules

### Requirements

**Branch naming rule violation detected (project rule)**

The branch name does not follow the Branching Strategy in
`.agents/governance/git-workflow.md`.

**Allowed prefixes:**

| prefix | Purpose |
| ------ | ------- |
| `feat/[<issue-id>-]<description>` | new feature |
| `fix/[<issue-id>-]<description>` | bug fix |
| `hotfix/<description>` | urgent production fix |
| `<type>/<description>` | any other type admitted by `.cz.toml` |
| `renovate/**`, `codex/**` | automation-owned branches |

**Correct examples:**

```bash
git checkout -b feat/42-add-nginx-service
git checkout -b fix/17-fix-volume-mount
git checkout -b hotfix/patch-secret-leak
git checkout -b feat/add-nginx-service
git checkout -b deps/update-python-pins
git checkout -b release/publish-v1.0.0
```

Do not work directly on `main`. Start from a feature or fix branch.

### Enforcement

Native event delivery is a separate observation from the frontmatter match.

## Exceptions

### Exception Conditions

No exception is declared by this rule.

### Approval and Review

None.

## Ownership

### Responsibilities

`@buenhyden`.

### Change and Adoption

`.agents/README.md`.
