---
trigger: always_on
glob: ["**/*.js", "**/*.mjs"]
description: "JavaScript Standards: Enforces modern ES6+ syntax, functional patterns, and clean code practices."
---

# JavaScript Development Standards

- **Role**: Senior JavaScript Developer
- **Purpose**: Define standards for writing modern, maintainable, and performant JavaScript code when TypeScript is not applicable or for legacy interoperability.
- **Activates When**: Developing vanilla JavaScript modules, writing build scripts, or managing legacy JS assets.

**Trigger**: always_on — Apply during the design and implementation of JavaScript-based logic.

## 1. Standards

### Principles

- **[REQ-JS-01] Modern ES6+ Primacy**
  - All new code MUST utilize modern ES6+ features (Arrow functions, Template literals, Destructuring). The use of `var` is strictly PROHIBITED.
- **[REQ-JS-02] Immutable-First Patterns**
  - Favor `const` over `let`. Use non-mutating array methods (`map`, `filter`, `reduce`) over traditional `for` loops where applicable.
- **[REQ-JS-03] Decoupled Functionality**
  - Design functions to be pure and small, adhering to the Single Responsibility Principle (SRP).

### JavaScript Stack Baseline

| Category | Requirement ID | Mandatory Standard |
| --- | --- | --- |
| Syntax | [REQ-JS-04] | ES6 Modules (import/export) |
| Async | [REQ-JS-05] | `async/await` over callbacks |
| Errors | [REQ-JS-06] | Explicit `try-catch` with logging |
| Quality | [REQ-JS-07] | ESLint (Standard/Airbnb config) |

### Must

- **[REQ-JS-08] JSDoc Documentation**
  - Complex functions MUST include JSDoc comments to provide context and define expected parameter types for both humans and IDEs.
- **[REQ-JS-09] Modular Architecture**
  - Organize logic into discrete modules; use barrel exports to simplify high-level consumption.
- **[REQ-JS-10] Strict Formatter Adherence**
  - All code MUST be formatted using `Prettier` to maintain repository-wide visual consistency.

### Must Not

- **[BAN-JS-01] Global Namespace Pollution**
  - Do NOT attach variables or functions to the `window` or `global` object. Maintain all state within scoped modules.
- **[BAN-JS-02] Shadowing Variable Names**
  - Avoid naming local variables with the same names as variables in an outer scope to prevent developer confusion.

### Failure Handling

- **Stop Condition**: Stop feature execution if a JavaScript module identifies an unhandled promise rejection or a critical syntax error in the build pipe.

## 2. Procedures

- **[PROC-JS-01] Refactor Workflow**
  - IF identifying `var` usage in legacy code THEN MUST refactor to `const`/`let` during the next touch of that file.
- **[PROC-JS-02] Linter Integration**
  - Run `eslint --fix` as a pre-commit hook to automate the correction of style and logic violations.

## 3. Examples

### Modern Functional Pattern (Good)

```javascript
/**
 * Processes items by filtering and mapping.
 * @param {Array} items
 * @returns {Array}
 */
const processItems = (items) => items
  .filter(item => item.isActive)
  .map(item => ({ ...item, processed: true }));
```

## 4. Validation Criteria

- **[VAL-JS-01] ESLint Zero-Error Pass**
  - [ ] Automated checks confirm that all `.js` files pass the project's restrictive linting configuration.
- **[VAL-JS-02] Modernity Check**
  - [ ] Manual review confirms that no legacy patterns (e.g., `xmlhttprequest`) are used for new features.
- **[VAL-JS-03] Documentation Sufficiency**
  - [ ] Complexity audit confirms that 100% of exposed module functions include valid JSDoc.
