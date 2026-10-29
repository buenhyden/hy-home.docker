---
title: "WARNING: branch naming rule violation"
version: "1.0.4"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-10-29"
action: "warn"
enabled: true
event: "bash"
name: "warn-branch-naming"
pattern: "git\\s+(checkout\\s+-b|switch\\s+-c)\\s+(?!(build|chore|ci|deps|docs|feat|fix|hotfix|perf|refactor|release|revert|style|test|dependabot|codex)/)"
---

# WARNING: branch naming rule violation

## Overview

Apply the declared `warn` action for warn-branch-naming.

## Scope

Applies to the `warn-branch-naming` rule on the `bash` event. The frontmatter of this document owns the exact matcher.

## Rules

**Branch naming rule violation detected (project rule)**

The branch name does not follow the Branching Strategy in
`.agents/governance/git-workflow.md`.

**Allowed prefixes:**

| prefix | Purpose |
| ------ | ------- |
| `feat/<issue-id>-<description>` | new feature |
| `fix/<issue-id>-<description>` | bug fix |
| `hotfix/<issue-id>-<description>` | urgent production fix |
| `<type>/<description>` | any other type admitted by `.cz.toml` |
| `dependabot/**`, `codex/**` | automation-owned branches |

**Correct examples:**

```bash
git checkout -b feat/42-add-nginx-service
git checkout -b fix/17-fix-volume-mount
git checkout -b hotfix/99-patch-secret-leak
git checkout -b deps/update-python-pins
git checkout -b release/publish-v1.0.0
```

Do not work directly on `main`. Start from a feature or fix branch.

## Exceptions

No exception is declared by this rule.

## Verification

The declared `bash` event and `pattern` define the matching scope; native event delivery remains a separate observation.

## Related Documents

- `.agents/README.md`
