---
layer: agentic
---

# Git Workflow Governance

This rule defines the mandatory git workflow for all contributors and agents.

## 1. Commit Standards

Use Conventional Commits with explicit scopes where possible.

- Format: `<type>(<scope>): <description>`
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

## 2. Branching Strategy

- Protected baseline: `main`
- Feature branch naming: `feat/<issue-id>-<short-description>`
- Fix branch naming: `fix/<issue-id>-<short-description>`
- Docs/refactor/chore branch naming may use matching prefixes.

## 3. Pull Request Protocol

1. Self-review changes before opening or updating a PR.
2. Run relevant programmatic checks before requesting review.
3. For governance work, ensure linked stage docs remain accurate.
4. Apply the GitHub completion gate from `rules/github-governance.md` §6 before declaring the PR done.

## 4. Operational Best Practices

- Keep commits atomic.
- Never commit plaintext secrets.
- Reference issue IDs, ADR IDs, or plan/task IDs when applicable.

## 5. Enforcement

Changes that bypass checks or violate secret safety must not be merged.
GitHub-specific enforcement rules (branch protection, required checks, CODEOWNERS, Actions security) are governed by `rules/github-governance.md`.

## Related Documents

- `docs/00.agent-governance/rules/github-governance.md`
- `docs/00.agent-governance/rules/quality-standards.md`
