---
trigger: model_decision
glob: ["**/*"]
description: "Git Standards: Enforces Conventional Commits, Atomic PRs, branching strategies, and repository hygiene."
---

# Git Standards & Workflows

- **Role**: Software Release Engineer
- **Purpose**: Enforce consistent history, atomic changes, and secure version control practices.
- **Activates When**: Committing code, creating branches, or opening Pull Requests.

**Trigger**: model_decision — Activate during version control interactions.

## 1. Standards

### Principles

- **[REQ-GIT-01] Conventional Commits**
  - Messages MUST follow the `type(scope): description` format.
- **[REQ-GIT-02] Atomic Changes**
  - Every Pull Request (PR) MUST represent exactly one logical change.
- **[REQ-GIT-03] Secret Hygiene**
  - No secrets, credentials, or `.env` files MUST ever be committed to the repository.

### Branching Strategy

| Type | Naming Pattern | Purpose |
| --- | --- | --- |
| Feature | `feat/short-description` | New functionality |
| Fix | `fix/short-description` | Bug repairs |
| Chore | `chore/short-description` | Maintenance / Dependencies |
| Release | `release/X.Y.Z` | Version staging |

### Must

- **[REQ-GIT-04] Imperative Mood**
  - Commit descriptions MUST use the imperative mood (e.g., "add", not "added").
- **[REQ-GIT-05] Squash and Merge**
  - Feature branches MUST be squashed and merged to maintain a clean main history.
- **[REQ-GIT-06] PR Documentation**
  - Every PR MUST include a context description, change list, and testing instructions.

### Must Not

- **[BAN-GIT-01] Vague Commits**
  - Commits MUST NOT use vague messages like "fix bug" or "WIP".
- **[BAN-GIT-02] Direct Main Commits**
  - Direct commits to the `main` or `protected` branches are FORBIDDEN.

### Failure Handling

- **Stop Condition**: Stop the commit process if a secret is detected in the diff.
- **Action**: Alert the user and request cleanup via `.gitignore` or `bfg`.

## 2. Procedures

- **[PROC-GIT-01] Commit Workflow**
  - IF preparing a commit THEN MUST verify the type matches `feat|fix|docs|style|refactor|perf|test|chore`.
- **[PROC-GIT-02] Branch Creation**
  - IF starting a new task THEN MUST create a branch from the latest `main`.

## 3. Examples

### Good Commit Message

- ✅ `feat(auth): add JWT token validation middleware`

### Good Branch Name

- ✅ `feat/login-page-redesign`

## 4. Validation Criteria

- **[VAL-GIT-01] Message Regex**
  - [ ] Commit header matches `^(feat|fix|docs|style|refactor|perf|test|chore)(\(.+\))?: .{1,72}$`.
- **[VAL-GIT-02] Secret Audit**
  - [ ] No `.env` or sensitive keys are present in the staged changes.
- **[VAL-GIT-03] PR Completeness**
  - [ ] PR contains Before/After visuals for UI changes.
