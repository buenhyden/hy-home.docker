---
title: "WARNING: manual pre-commit execution"
version: "1.1.0"
type: "governance/hook-policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-04"
action: "warn"
enabled: true
event: "bash"
name: "warn-pre-commit-manual"
pattern: "pre-commit\\s+run"
---

<!-- markdownlint-disable MD041 MD040 -->

**Manual `pre-commit run` detected (project rule)**

`.agents/governance/quality-standards.md#4-execution-boundary` owns this
boundary: agents never run `pre-commit run` directly. An explicitly approved
all-files gate uses only its controlled route and conditions.

**Project pre-commit policy:**

- Manual runs can create inconsistent evidence.
- Installed commit-hook delivery must be observed separately; this warning does
  not claim it ran automatically for a particular commit.
- CI has its separate pinned pre-commit route and validation responsibilities.

**Detected forms and normal commit path:**

```bash
# WARNING: manual pre-commit execution is prohibited for agents
pre-commit run --all-files
pre-commit run --files myfile.py

# A normal commit does not bypass configured checks.
git commit -m "feat(scope): My change"
```

If lint or format issues exist, fix the affected files directly before committing.

## Related Documents

- `.agents/governance/quality-standards.md#4-execution-boundary`
