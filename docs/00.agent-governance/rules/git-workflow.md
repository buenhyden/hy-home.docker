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
- Hotfix branch naming: `hotfix/<issue-id>-<short-description>` for emergency production fixes; follows the same issue-ID requirement as `feat/` and `fix/`.
- Other human-authored branch naming may use a matching Conventional Commit
  type prefix: `docs/`, `style/`, `refactor/`, `perf/`, `test/`, `build/`,
  `ci/`, `chore/`, or `revert/`.
- Automation branch exceptions: `dependabot/**` and `codex/**` are allowed for
  tool-generated PR branches only. They must still merge through the PR
  protocol and required checks.

## 3. Pull Request Protocol

1. Self-review changes before opening or updating a PR.
2. Run relevant programmatic checks before requesting review.
3. For governance work, ensure linked stage docs remain accurate.
4. Apply the Completion Gate from `rules/github-governance.md` before declaring the PR done.
5. Mark incomplete work as Draft/WIP and list remaining work in the PR template; do not request final review until the PR is ready.
6. Keep commits atomic and reviewable. If cleanup is needed, use the PR description to explain the intended squash/rebase strategy instead of hiding mixed concerns.

## 4. Operational Best Practices

- Keep commits atomic.
- Use `fix` for user-visible or operational defect corrections and include regression evidence.
- Use `refactor` only for behavior-preserving structure changes and list checks that demonstrate unchanged behavior.
- Never commit plaintext secrets.
- Reference issue IDs, ADR IDs, or plan/task IDs when applicable.
- For release tag creation, follow the `docs/05.operations/runbooks/release-management.md` procedure.

## 5. Agent Completion Commit Discipline

- For repository-modifying agent work, the completion default is to create
  logical Conventional Commits after verification and before declaring the task
  done.
- Split commits by reviewable concern: documentation evidence, runtime hook
  behavior, validators, generated graph outputs, and similar units should not be
  mixed unless they are inseparable.
- Stage only files or hunks owned by the current task. Leave unrelated untracked
  files and user changes untouched.
- Do not commit when the user explicitly asks not to commit, the work is
  exploratory or incomplete, required checks/approvals are missing, or committing
  would include secrets or unrelated changes. In that case, report the reason and
  remaining state.

## 6. Enforcement

Changes that bypass checks or violate secret safety must not be merged.
GitHub-specific enforcement rules (branch protection, required checks, CODEOWNERS, Actions security) are governed by `rules/github-governance.md`.

## Related Documents

- `docs/00.agent-governance/rules/github-governance.md`
- `docs/00.agent-governance/rules/quality-standards.md`
- `docs/05.operations/runbooks/release-management.md`
