---
name: block-direct-main-push
enabled: true
event: bash
pattern: git\s+push\s+\w[\w.-]*\s+(HEAD:)?main\s*$
action: block
---

<!-- markdownlint-disable MD041 MD040 -->

**Direct push to `main` blocked (project rule)**

`docs/00.agent-governance/rules/github-governance.md` — Repository Protection Contract:

> "Agents must treat `main` as a protected branch: no direct pushes, no force pushes, no bypass of required checks."

> "No exceptions is mandatory agent behavior even when GitHub admin enforcement does not fully enforce the same boundary."

**Correct workflow:**

```bash
# BLOCKED: direct push to main
git push origin main
git push origin HEAD:main

# ALLOWED: push a feature branch and open a PR
git push origin feat/42-my-feature
git push origin fix/17-bug-fix
# Create a GitHub PR, then review and merge through the governed flow.
```

**PR completion gate (`github-governance.md` — Completion Gate):**

1. All required status checks pass.
2. All required reviews are approved.
3. No BLOCK-severity findings remain.
4. CODEOWNERS reviewers are notified.
5. No secrets or unpinned actions were introduced.

## Related Documents

- `docs/00.agent-governance/README.md`
