---
layer: common
title: 'Common Engineering Scope'
---

# Common Engineering Scope

**Universal engineering standards, naming conventions, and shared patterns across all layers.**

## 1. Context & Objective

- **Goal**: Ensure consistency, maintainability, and readability across the entire `hy-home.docker` codebase.
- **Standards**: Priority on Clean Code, SOLID principles, and `docs/00.agent-governance/rules/quality-standards.md`.

## 2. Requirements & Constraints

- **Language**: Use English for all code, comments, and internal documentation.
- **Naming**:
  - Variables/Functions: `camelCase`
  - Classes/Types: `PascalCase`
  - Constants: `SCREAMING_SNAKE_CASE`
  - Files: `kebab-case.ext`
- **Formatting**: Adhere to Prettier/ESLint defaults for the project.

## 3. Implementation Flow

1. **DRY Check**: Before implementing a new utility, check for existing logic in `common/` or shared libs.
2. **Type Safety**: Prefer strict typing and avoid `any` or loose types.
3. **Documentation**: Add JSDoc/Docstrings for all public APIs and complex logic.

## 4. Operational Procedures

- **Linting**: Run `npm run lint` before committing.
- **Formatting**: Run `npm run format` (if available) or ensure editor auto-format is on.

## 5. Maintenance & Safety

- **Refactoring**: Proactively extract shared logic into common utilities when spotted in multiple layers.
- **Legacy Code**: When touching legacy files, apply "Boy Scout Rule" (leave it cleaner than you found it).

## 6. File Ownership SSOT

| Path Pattern                 | Owner Agent     | Read-Only For                  |
| ---------------------------- | --------------- | ------------------------------ |
| `common/`, `lib/`, `shared/` | `code-reviewer` | read; changes by layer agent   |
| `docs/04.specs/`             | `code-reviewer` | `infra-implementer` (read)     |
| `.pre-commit-config.yaml`    | `code-reviewer` | all — never run hooks manually |

## 7. Subagent Bridge

```text
# code-reviewer agent preamble
@import docs/00.agent-governance/scopes/common.md
# H100:21 Review pattern — read → assess → report
# Clean Code · SOLID · no plaintext secrets
```

Spawn via Task tool. Do not embed common standards inline in agent files.
