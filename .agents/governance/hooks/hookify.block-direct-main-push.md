---
title: "BLOCKED: direct push to main"
version: "1.2.1"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-10-15"
action: "block"
enabled: true
event: "bash"
name: "block-direct-main-push"
pattern: "\\bgit(\\s+-C\\s+\\S+)*\\s+push\\b[^;&|\\n]*?(\\s|:|\\+)(refs/heads/)?main(\\s|$|[;&|])"
---

# BLOCKED: direct push to main

## Overview

Apply the declared `block` action for block-direct-main-push.

## Scope

`.agents/governance/github-governance.md` — Repository Protection Contract:

> "Agents must treat `main` as a protected branch: no direct pushes, no force pushes, no bypass of required checks."

> "\"No exceptions\" is mandatory agent behavior even when GitHub admin enforcement or repository rulesets do not fully enforce the same boundary."

The declared `bash` event and `pattern` match an explicit `main` destination
(`main`, `HEAD:main`, `HEAD:refs/heads/main`, `+main`, `-u`, `--force`,
`git -C <dir>`, compound commands). The dispatcher judges what the text cannot
show: `HEAD` and `@`, implicit refspecs, `heads/main`, wildcard refspecs,
`--all`, `--branches`, `--mirror`, `-c` push settings, and the repository a
push runs in (`cd`, `pushd`, `git -C`, `--git-dir`, `GIT_DIR`). A push from a
repository it cannot read is denied.

## Rules

```bash
# BLOCKED: direct push to main
git push origin main
git push origin HEAD:main

# ALLOWED: push a feature branch and open a PR
git push origin HEAD:refs/heads/feat/42-my-feature
# Create a GitHub PR, then review and merge through the governed flow.
```

**PR completion gate (`github-governance.md` — Completion Gate):**

1. All required status checks pass.
2. All required reviews are approved.
3. No BLOCK-severity findings remain.
4. CODEOWNERS reviewers are notified.
5. No secrets or unpinned actions were introduced.

The declared action applies when the pattern matches.

## Exceptions

No exception is declared by this rule.

## Verification

The native Git hook installed by `scripts/hooks/install-pre-push-guard.sh`
passes all raw refs to `scripts/hooks/pre-push-guard.sh`, including mixed-ref
pushes and deletions. It refuses every destination `refs/heads/main` before
any pre-commit ref selection. The installer preserves a recognized pre-commit
shim for recovery and refuses unknown hooks or a selected `core.hooksPath`;
it does not replace another host owner's chain. Hook bypass remains possible,
so only remote protection without bypass enforces the boundary. Installation,
synthetic pushes, provider delivery and editor sync are separate observations.

## Related Documents

- `.agents/README.md`
