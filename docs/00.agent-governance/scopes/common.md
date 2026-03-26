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
