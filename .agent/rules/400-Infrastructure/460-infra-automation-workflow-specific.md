---
trigger: always_on
glob: "**/*.{yml,yaml,json,sh}"
description: "Automation & Workflow: Semantic Release, Hooks, and Makefiles."
---
# Automation & Workflow Standards

## 1. Release Automation

- **Semantic Release**: Automate versioning based on commit messages.
- **Changelog**: Auto-generate `CHANGELOG.md`.

### Example: Commits

**Good**

```text
feat(auth): add login page
fix(api): handle timeout
```

**Bad**

```text
update code
fixed bug
```

## 2. Git Hooks (Husky/Pre-commit)

- **Local Checks**: Lint staged files before commit (`lint-staged`).
- **Safety**: Block commits with secrets or conflicts (`<<<< HEAD`).

### Example: Hook

**Good** (pre-commit logic)

```bash
npm run type-check && npm run lint
```

**Bad**

```bash
# No hooks: Bad code enters CI, wasting minutes
```

## 3. Scripts

- **Standardization**: Use `Makefile` or `Justfile` to standardize commands (`make build`, `make deploy`) across languages.
- **Idempotency**: Scripts should handle re-runs gracefully.
