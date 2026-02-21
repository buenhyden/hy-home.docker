---
trigger: model_decision
glob: [".git/**","**/CONTRIBUTING.md","**/PULL_REQUEST_TEMPLATE.md"]
description: "Git Workflow Policy Standards: Enforces branch naming, commit message standards (Conventional), and PR quality gates."
---

# Git Workflow Policy Standard

- **Role**: Lead DevOps / Release Engineer
- **Purpose**: Define standards for maintaining a clean, traceable, and high-quality version history through rigorous Git operations and peer-review protocols.
- **Activates When**: Creating feature branches, drafting commit messages, or initiating Pull Request (PR) reviews.

**Trigger**: model_decision — Apply during every interaction with the project's version control system.

## 1. Standards

### Principles

- **[REQ-GIT-01] Sequential Branching Pattern**
  - Branches MUST follow a feature-scoped pattern: `<type>/<issue-number>-<short-description>`. Direct commits to the `main` or `production` branches are PROHIBITED.
- **[REQ-GIT-02] Atomic Traceability**
  - Each commit MUST represent a single, atomic change. Commits MUST be linked to an issue or task ID within the messaging template.
- **[REQ-GIT-03] Verified Release Integrity**
  - All merges to protected branches MUST pass automated CI/CD quality gates, including linting, testing, and security scans.

### Workflow Baseline

| Category | Requirement ID | Mandatory Standard |
| --- | --- | --- |
| Commits | [REQ-GIT-04] | Conventional Commits (feat, fix, docs, etc.) |
| Branching| [REQ-GIT-05] | `feat/`, `fix/`, `refactor/` prefixes |
| PR Size | [REQ-GIT-06] | Max 500 lines of code (LOC) per PR |
| History | [REQ-GIT-07] | Squash and merge preferred for features |

### Must

- **[REQ-GIT-08] Conventional Commit Headers**
  - Commit messages MUST utilize the header format: `<type>(<scope>): <subject>`.
- **[REQ-GIT-09] Peer Review Approval**
  - No code MUST be merged without at least one approved peer review from a designated code owner.
- **[REQ-GIT-10] Linear History Maintenance**
  - Feature branches MUST be regularly rebased against the target branch to ensure a clean, linear merge history.

### Must Not

- **[BAN-GIT-01] Forced Push on Protected Branches**
  - The use of `push --force` on `main`, `staging`, or `production` branches is STRICTLY PROHIBITED.
- **[BAN-GIT-02] Empty/Opaque PR Descriptions**
  - PRs MUST NOT be opened with empty descriptions. Every PR MUST utilize the project's standardized template.

### Failure Handling

- **Stop Condition**: Stop PR merge if the associated CI pipeline identifies a regression or if the PR size exceeds the review-quality threshold.

## 2. Procedures

- **[PROC-GIT-01] Branch Creation Sync**
  - IF starting a new task THEN MUST first create the branch using the `<type>/<id>-desc` convention before coding.
- **[PROC-GIT-02] Conflict Resolution Flow**
  - IF a merge conflict occurs THEN MUST resolve it in the feature branch and re-verify through local tests before resubmitting.

## 3. Examples

### Conventional Commit (Good)

```text
feat(auth): implement JWT token rotation logic
fix(ui): resolve layout shift on mobile search bar
```

## 4. Validation Criteria

- **[VAL-GIT-01] Message Compliance Audit**
  - [ ] Linting tools (commitlint) verify that 100% of commits follow the conventional format.
- **[VAL-GIT-02] Branch hygiene**
  - [ ] Audit confirms zero stale feature branches and zero unmerged direct-to-main commits.
- **[VAL-GIT-03] PR Template Completeness**
  - [ ] Lead check confirms that 100% of merged PRs contain valid "What", "Why", and "Testing" sections.
