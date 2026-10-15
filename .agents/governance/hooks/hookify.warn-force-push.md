---
title: "Prefer --force-with-lease over --force."
version: "1.0.2"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-10-15"
action: "warn"
enabled: true
event: "bash"
name: "warn-force-push"
pattern: "git\\s+push\\s+.*(--force\\b|--force-with-lease\\b|-f\\s|-f$)"
---

# Prefer --force-with-lease over --force

## Overview

Apply the declared `warn` action for warn-force-push.

## Scope

`bash` 이벤트의 `warn-force-push` 규칙에 적용한다. 정확한 matcher는 이 문서의 frontmatter가 소유한다.

## Rules

**Force push detected (project rule)**

`.agents/governance/github-governance.md` — Repository Protection Contract:

> "no direct pushes, no force pushes, no bypass of required checks"

**When a force push may be justified:**

- Rewriting history after a rebase on your own feature branch.
- Using `--force-with-lease` to protect against overwriting remote changes.

**Never allowed:**

- Force pushing to `main`.
- Force pushing another agent's or developer's in-progress branch.
- Force pushing commits that have already been merged.

**Confirmation checklist:**

- [ ] This is your own branch, not `main`.
- [ ] The command uses `--force-with-lease`, not plain `--force`.
- [ ] No teammate or agent is working on the same branch.

```bash
# Prefer --force-with-lease over --force.

git push --force-with-lease origin feat/42-my-feature
```

## Exceptions

No exception is declared by this rule.

## Verification

The declared `bash` event and `pattern` define the matching scope; native event delivery remains a separate observation.

## Related Documents

- `.agents/README.md`
