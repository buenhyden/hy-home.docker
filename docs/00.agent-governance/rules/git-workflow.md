---
layer: agentic
---

# Git Workflow Governance

This rule defines the mandatory git workflow for all AI Agents and human contributors in `hy-home.docker`.

## 1. Commit Standards (March 2026)

All commits MUST follow the **Conventional Commits** standard with a focus on project-specific scopes.

- **Types**: `feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert`
- **Format**: `<type>(<scope>): <description>`
- **Example**: `feat(auth): add OIDC provider for Keycloak`

## 2. Branching Strategy

- **Main Branch**: `main` (Protected. No direct pushes allowed).
- **Feature Branches**: `feat/<issue-id>-<short-description>`
- **Fix Branches**: `fix/<issue-id>-<short-description>`

## 3. Pull Request Protocol

1. **Self-Review**: Agents must perform a self-review of changes before PR creation.
2. **Validation**: All PRs must pass `scripts/validate-docker-compose.sh`.
3. **Documentation**: Update [docs/05.plans/](../../05.plans/README.md) and [docs/06.tasks/](../../06.tasks/README.md) to reflect completion.

## 4. Operational Best Practices

- **Atomic Commits**: Keep commits small and focused on a single logical change.
- **No Secrets**: Never commit `.env` files or hardcoded credentials. Use Docker Secrets.
- **Traceability**: Reference Issue IDs or ADRs in commit messages when applicable.

## 5. Enforcement

AI Agents found violating this workflow will have their PRs rejected. Consistently clean history is a project-wide quality attribute.
