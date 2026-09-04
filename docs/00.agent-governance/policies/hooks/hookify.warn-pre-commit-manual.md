---
title: "WARNING: manual pre-commit execution"
version: "1.0.0"
type: "governance/hook-policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-04"
action: "warn"
enabled: true
event: "bash"
name: "warn-pre-commit-manual"
pattern: "pre-commit\\s+run"
---

<!-- markdownlint-disable MD041 MD040 -->

**Manual `pre-commit run` detected (project rule)**

`docs/00.agent-governance/policies/postflight-checklist.md` — Lint Gate violation:

> "`.pre-commit-config.yaml` hooks will pass (never run manually)"

**Project pre-commit policy:**

- pre-commit hooks run **automatically** during `git commit`.
- Manual runs can create inconsistent evidence.
- CI performs separate lint and format validation.

**Correct approach:**

```bash
# WARNING: manual pre-commit execution
pre-commit run --all-files
pre-commit run --files myfile.py

# ALLOWED: automatic execution during commit
git commit -m "feat(scope): my change"
# The pre-commit hook runs automatically.
```

If lint or format issues exist, fix the affected files directly before committing.

## Related Documents

- `docs/00.agent-governance/README.md`
