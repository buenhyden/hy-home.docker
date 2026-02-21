---
trigger: model_decision
glob: ["**/*.{js,ts,py,go,rs}"]
description: "Engineering Excellence Standards: Enforces Clean Code, SOLID principles, debugging methodology, and peer review quality gates."
---

# Engineering Excellence Standards

- **Role**: Quality & Excellence Architect
- **Purpose**: Define standards for writing high-quality, maintainable, and ethically sound code through rigorous attention to naming, structure, and debugging patterns.
- **Activates When**: Writing code, refactoring existing modules, implementing error handling, or performing code reviews.

**Trigger**: model_decision — Apply during every code modification or verification task.

## 1. Standards

### Principles

- **[REQ-EXC-01] Intent-Revealing Clean Code**
  - Code MUST be written with an emphasis on readability and story-telling. Identifiers MUST reveal intent, and functions MUST adhere to the Single Responsibility Principle (SRP).
- **[REQ-EXC-02] Fail-Safe Debugging Workflow**
  - Every technical investigation MUST follow a systematic 4-phase methodology: Assessment -> Investigation -> Resolution -> QA.
- **[REQ-EXC-03] Rigorous Definition of Done (DoD)**
  - No code is "Done" until it meets the project's quality gates: Readability, Testability, Performance, and robust Error Handling.

### Excellence Matrix

| Category | Requirement ID | Mandatory Standard |
| --- | --- | --- |
| Principles | [REQ-EXC-04] | SOLID, DRY, KISS |
| Naming | [REQ-EXC-05] | Language-appropriate casing (Camel/Snake) |
| Quality | [REQ-EXC-06] | 100% coverage for mission-critical logic |
| Review | [REQ-EXC-07] | Constructive, requirements-focused feedback |

### Must

- **[REQ-EXC-08] Explicit Error Normalization**
  - All caught exceptions MUST be normalized and logged with sufficient context (stack trace, input params) to allow for zero-repro debugging.
- **[REQ-EXC-09] Language-Specific Naming Conformity**
  - Identifiers MUST conform to the language's native standard (e.g., `camelCase` for TS/Go, `snake_case` for Python/Rust).
- **[REQ-EXC-10] Defensive Parameter Validation**
  - Every public function boundary MUST perform defensive validation on its input arguments to prevent runtime crashes.

### Must Not

- **[BAN-EXC-01] Silent Error Swallowing**
  - The use of empty `catch` blocks or `try...except pass` is STRICTLY PROHIBITED. All errors MUST be either handled or re-thrown.
- **[BAN-EXC-02] Monolithic Logic Sprawl**
  - Avoid creating functions or methods that exceed 50 lines of logical code. Decompose into atomic, testable sub-units.

### Failure Handling

- **Stop Condition**: Stop feature development if a code review identifies a violation of the Single Responsibility Principle that makes unit testing impossible.

## 2. Procedures

- **[PROC-EXC-01] Refactoring Baseline**
  - IF a new feature requires significant modification to legacy code THEN MUST first refactor the surrounding code to meet the current "Clean Code" standards.
- **[PROC-EXC-02] Post-Debug Regression**
  - UPON resolving a bug THEN MUST add a representative test case that specifically identifies and prevents the recurrence of that defect.

## 3. Examples

### Clean Function Anatomy (Good)

```typescript
function calculateOrderTotal(items: Item[]): number {
  validateItems(items);
  return items.reduce((total, item) => total + item.price, 0);
}
```

## 4. Validation Criteria

- **[VAL-EXC-01] Readability Review**
  - [ ] Peer reviewer confirms that the code "story" is clear without excessive inline comments.
- **[VAL-EXC-02] Static Analysis Pass**
  - [ ] Linter tools (ESLint, Pylint) confirm zero violations of the project's complexity and naming rules.
- **[VAL-EXC-03] Test Coverage Integrity**
  - [ ] Coverage reports verify that new logic meets the > 80% project-wide threshold.
