---
name: block-git-no-verify
enabled: true
event: bash
pattern: git\s+commit\s+.*(--no-verify|-n\s+-m|-n\s+['"]|-n$)
action: block
---

<!-- markdownlint-disable MD041 MD040 -->

**`git commit --no-verify` blocked (project rule)**

Global Claude Code policy and `docs/00.agent-governance/rules/git-workflow.md` — Enforcement:

> "Changes that bypass checks or violate secret safety must not be merged."

`AGENTS.md` — Verification:

> "Lint and format are managed by `.pre-commit-config.yaml`; do not run `pre-commit` manually."

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
# BLOCKED
git commit --no-verify -m "fix: something"
git commit -n -m "fix: something"

# If hooks fail, fix the root cause.
# Lint error: edit the affected file directly.
# Format error: apply the formatter, then stage the result.
git add -p
git commit -m "fix(scope): actual fix"
```

## Related Documents

- `docs/00.agent-governance/README.md`
