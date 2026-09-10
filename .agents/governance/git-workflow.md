---
title: "Git Workflow Governance"
version: "1.1.1"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-11"
---

# Git Workflow Governance

This rule defines the mandatory git workflow for all contributors and agents.

## 1. Commit Standards

Use Conventional Commits with explicit scopes where possible.

- Format: `<type>[(<scope>)][!]: <Description>`; brackets denote optional
  parts and are not literal characters.
- Types: the keys in `.cz.toml`'s `change_type_map`. That map is the executable
  type vocabulary.
- The description starts with a capital letter and does not end with a
  period. The body, when present, is one block with no blank line inside
  it, and no body line starts with a word followed by a colon and a space,
  because the grammar cannot tell such a line from a trailer and stops
  reading the body there. Rewrap the sentence rather than reaching for
  `--no-verify`. Trailers come last, after a single blank line. `.cz.toml`
  is the sole executable authority for the allowed types, message grammar,
  and header length. Its interactive type choices explain each type; this
  policy governs commit usage and workflow.
- Validate a draft with
  `cz check --message-length-limit 75 --message "feat(auth): Add login guard"`
  before starting the commit. The `commit-msg` hook remains the final local
  enforcement point.

## 2. Branching Strategy

- Protected baseline: `main`
- Feature branch naming: `feat/<issue-id>-<short-description>`
- Fix branch naming: `fix/<issue-id>-<short-description>`
- Hotfix branch naming: `hotfix/<issue-id>-<short-description>` for emergency production fixes; follows the same issue-ID requirement as `feat/` and `fix/`.
- Other human-authored branches use `<type>/<short-description>`, where `type`
  is an admitted `.cz.toml` change type other than `feat` or `fix`.
- Automation branch exceptions: `dependabot/**` and `codex/**` are allowed for
  tool-generated PR branches only. They must still merge through the PR
  protocol and required checks.

## 3. Pull Request Protocol

1. Self-review changes before opening or updating a PR.
2. Run relevant programmatic checks before requesting review.
3. For governance work, ensure linked stage docs remain accurate.
4. Apply the Completion Gate from `.agents/governance/github-governance.md` before declaring the PR done.
5. Mark incomplete work as Draft/WIP and do not request final review until the PR is ready. Merge readiness and branch lifecycle belong to `.agents/governance/github-governance.md` section 3.
6. Keep commits atomic and reviewable. Document any cleanup proposal in the PR;
   the recovery-commit and history-rewrite rules it must satisfy are owned by
   `.agents/governance/github-governance.md` section 3.
7. Request review only after self-review and programmatic checks pass. Summarize scope, risk, and how to verify so reviewers can act efficiently.
8. Incorporate review feedback explicitly: resolve or reply to each finding, re-run affected checks, and record what changed before re-requesting review.

## 4. Operational Best Practices

- Keep commits atomic.
- Use `fix` for user-visible or operational defect corrections and include regression evidence.
- Use `refactor` only for behavior-preserving structure changes and list checks that demonstrate unchanged behavior.
- Never commit plaintext secrets.
- Reference issue IDs, ADR IDs, or plan/task IDs when applicable.
- For release tag creation, follow the stable Release Management Operations
  subject's sibling `runbook.md` procedure.

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
GitHub-specific enforcement rules (branch protection, required checks, CODEOWNERS, Actions security) are governed by `.agents/governance/github-governance.md`.

## Related Documents

- `.agents/governance/github-governance.md`
- `.agents/governance/quality-standards.md`
- `docs/05.operations/catalog/00-workspace/0009-release-management/runbook.md`
