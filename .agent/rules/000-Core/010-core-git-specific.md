---
trigger: always_on
glob: "**/*"
description: "Git: Conventional Commits, Branching Strategy, Atomic PRs, and Security."
---
# Git Standards

## 1. Conventional Commits

- **Structure**: `type(scope): description` (lowercase).
- **Types**:
  - `feat`: ✨ A new feature
  - `fix`: 🐛 A bug fix
  - `docs`: 📝 Documentation only changes
  - `style`: 🎨 Changes that do not affect the meaning of the code (white-space, formatting, etc)
  - `refactor`: ♻️ A code change that neither fixes a bug nor adds a feature
  - `perf`: ⚡️ A code change that improves performance
  - `test`: ✅ Adding missing tests or correcting existing tests
  - `chore`: 🧑‍💻 Changes to the build process or auxiliary tools and libraries
  - `security`: 🔒 Security improvements
- **Scope**: Mandatory for monorepos (e.g., `feat(auth):`).

### Example: Commits

**Good**

```text
feat(user): add login endpoint validation
fix(api): handle null response in get_profile
docs: update readme with setup instructions
```

**Bad**

```text
added login // No type
fixed bug // Vague
WIP // Not actionable
Feature/Login // Don't use caps or slash in message subject
```

## 2. Branching Strategy

- **Format**: `type/short-description`.
- **Main Branch**: Protected. Direct commits are blocked.
- **Delete**: Delete branches after merging.

### Example: Branches

**Good**

```text
feat/oauth-login
fix/memory-leak
docs/api-spec
chore/upgrade-deps
```

**Bad**

```text
my-branch
login
patch-1
```

## 3. Pull Requests & Workflow

- **Atomic**: One logical change per PR. If descriptions need bullet points for completely unrelated changes, split the PR.
- **Squash & Merge**: Default merge strategy to maintain a linear history on `main`.
- **Description**: REQUIRED. Fill out the PR Template. Explain "Why" and "How".

### Example: PR Description

**Good**

```markdown
## Why
The login endpoint crashed when upstream was down.

## What
- Added try/catch block in `AuthService`.
- Added 503 Service Unavailable test case.
- Updated API docs.

Closes #123
```

**Bad**

```text
fixes login
```

## 4. Git Security & hygiene

- **No Secrets**: NEVER commit `.env`, keys, or credentials. Use `.gitignore`.
- **Large Files**: Do not commit binaries (>10MB). Use LFS if absolutely necessary.
- **Force Push**: Never force push to shared branches (`main`, `develop`).

## 5. Fast Commit Workflow (Automation)

- **Process**: `git status` -> Generate Suggestions -> Select Best -> Commit.
- **Rules**:
  - **No Co-Author**: Exclude co-authorship footers for automated agents.
  - **Descriptive**: Ensure messages explain *why* and *what*.
- **Tools**: Use `fast-commit` scripts if available in the repo.
