---
name: warn-force-push
enabled: true
event: bash
pattern: git\s+push\s+.*(--force\b|--force-with-lease\b|-f\s|-f$)
action: warn
---

<!-- markdownlint-disable MD041 MD040 -->

**Force push detected (project rule)**

`docs/00.agent-governance/rules/github-governance.md` — Repository Protection Contract:

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

## Related Documents

- `docs/00.agent-governance/README.md`
