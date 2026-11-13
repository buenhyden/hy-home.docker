---
title: "BLOCKED: git commit --no-verify"
version: "1.1.3"
type: "governance/rule"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
action: "block"
enabled: true
event: "bash"
name: "block-git-no-verify"
pattern: "git\\s+commit\\s+.*(--no-verify|-n\\s+-m|-n\\s+['\"]|-n$)"
---

# Git Commit Check Bypass Rule

## Purpose

### Objective

**`git commit --no-verify` blocked (project rule)**

### Authority

Owning policies:

- [Git workflow](../git-workflow.md)
- [Quality standards execution boundary](../quality-standards.md#4-execution-boundary)

## Scope

### Applies To

The `block-git-no-verify` rule applies on the `bash` event. `.agents/governance/git-workflow.md` — Enforcement:

> "Changes that bypass checks or violate secret safety must not be merged."

The [execution boundary](../quality-standards.md#4-execution-boundary) owns the
direct pre-commit prohibition and the sole approved all-files route. This hook
retains the separate block on bypassing configured commit checks.

### Exclusions

None: this document states no exclusion.

## Rules

### Requirements

**Project pre-commit hooks perform:**

- lint and format checks
- plaintext secret detection
- file type and size checks

**Why this rule blocks:**

- Bypassing pre-commit skips quality and security gates.
- Accidental secret commits become more likely.
- CI may block the PR on lint failures.

**Correct approach:**

```bash
# BLOCKED: git commit --no-verify
git commit --no-verify -m "fix: Something"
git commit -n -m "fix: Something"

# If hooks fail, fix the root cause.
# Lint error: edit the affected file directly.
# Format error: apply the formatter, then stage the result.
git add -p
git commit -m "fix(scope): Actual fix"
```

### Enforcement

The declared Bash event and unchanged native pattern identify matching commands.

## Exceptions

### Exception Conditions

No exception is declared by this rule.

### Approval and Review

None: this document states no separate approval or review step.

## Ownership

### Responsibilities

The rule owner is `@buenhyden`.

### Change and Adoption

None: this document states no separate change or adoption step.
