---
title: "BLOCKED: git commit --no-verify"
version: "1.1.0"
type: "governance/hook-policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-04"
action: "block"
enabled: true
event: "bash"
name: "block-git-no-verify"
pattern: "git\\s+commit\\s+.*(--no-verify|-n\\s+-m|-n\\s+['\"]|-n$)"
---

<!-- markdownlint-disable MD041 MD040 -->

**`git commit --no-verify` blocked (project rule)**

`.agents/governance/git-workflow.md` — Enforcement:

> "Changes that bypass checks or violate secret safety must not be merged."

The [execution boundary](../quality-standards.md#4-execution-boundary) owns the
direct pre-commit prohibition and the sole approved all-files route. This hook
retains the separate block on bypassing configured commit checks.

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
git commit --no-verify -m "fix: Something"
git commit -n -m "fix: Something"

# If hooks fail, fix the root cause.
# Lint error: edit the affected file directly.
# Format error: apply the formatter, then stage the result.
git add -p
git commit -m "fix(scope): Actual fix"
```

## Related Documents

- `.agents/governance/git-workflow.md`
- `.agents/governance/quality-standards.md#4-execution-boundary`
