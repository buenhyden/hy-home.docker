---
title: "Prefer --force-with-lease over --force."
version: "1.0.1"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
action: "warn"
enabled: true
event: "bash"
name: "warn-force-push"
pattern: "git\\s+push\\s+.*(--force\\b|--force-with-lease\\b|-f\\s|-f$)"
---

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

## Overview

Apply the declared `warn` action for warn-force-push.

## Scope

The declared `bash` event and `pattern` define the matching scope; native event delivery remains a separate observation.

## Rules

git push --force-with-lease origin feat/42-my-feature
```

## Exceptions

No exception is declared by this rule.

## Related Documents

- `.agents/README.md`
