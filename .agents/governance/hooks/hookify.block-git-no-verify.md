---
title: "BLOCKED: git commit --no-verify"
version: "1.0.1"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
action: "block"
enabled: true
event: "bash"
name: "block-git-no-verify"
pattern: "git\\s+commit\\s+.*(--no-verify|-n\\s+-m|-n\\s+['\"]|-n$)"
---

**`git commit --no-verify` blocked (project rule)**

`.agents/governance/git-workflow.md` — Enforcement:

> "Changes that bypass checks or violate secret safety must not be merged."

`.agents/governance/task-checklists.md` owns completion checks and prohibits
direct `pre-commit run`; only its explicitly approved controlled wrapper is an
agent all-files route.

**Project pre-commit hooks perform:**

- lint and format checks
- plaintext secret detection
- file type and size checks

**Why this is BLOCK-severity:**

- Bypassing pre-commit skips quality and security gates.
- Accidental secret commits become more likely.
- CI may block the PR on lint failures.

**Correct approach:**

```bash
# BLOCKED: git commit --no-verify

## Overview

Apply the declared `block` action for block-git-no-verify.

## Scope

The declared `bash` event and `pattern` define the matching scope; native event delivery remains a separate observation.

## Rules

git commit --no-verify -m "fix: something"
git commit -n -m "fix: something"

# If hooks fail, fix the root cause.
# Lint error: edit the affected file directly.
# Format error: apply the formatter, then stage the result.
git add -p
git commit -m "fix(scope): actual fix"
```

The declared action applies when the pattern matches.

## Exceptions

No exception is declared by this rule.

## Related Documents

- `.agents/README.md`
