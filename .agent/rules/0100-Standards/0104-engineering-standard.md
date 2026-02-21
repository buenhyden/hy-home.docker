---
trigger: model_decision
glob: ["**/*.{ts,js,py,go,rs,java,sql}", "**/*"]
description: "Engineering Standards: Unified usage of Clean Code, SOLID, Naming, and Debugging principles."
---

# 0100-Engineering-Standards

- **Role**: Staff Engineer
- **Purpose**: Enforce universal standards for code quality, strict maintainability, and systematic debugging.
- **Activates When**: Writing code, refactoring, code reviewing, or debugging.

## 1. Standards

### 1.1 Principles

- **[REQ-ENG-CLN-01] Intent-Revealing**: Names MUST describe *what* a variable holds or *what* a function does.
- **[REQ-ENG-CLN-02] Single Responsibility**: Functions and classes MUST have one reason to change.
- **[REQ-ENG-CLN-03] DRY**: Logic MUST NOT be duplicated. Abstract repeated patterns.
- **[REQ-ENG-CLN-04] KISS**: Simple code MUST be preferred over clever code.
- **[REQ-ENG-CLN-05] YAGNI**: Implement ONLY what is needed today.

### 1.2 Scope

- **In-Scope**: General coding style, Naming, Architecture layering, Debugging methodology.
- **Out-of-Scope**: Language-specific syntax (see 1100-1600), Git workflows (see 0110).

### 1.3 Inputs & Outputs

- **Inputs**: User requirements, Legacy code.
- **Outputs**: Clean, maintainable, tested code.

### 1.4 Must / Must Not

- **[REQ-ENG-NAM-01] Casing**:
  - TS/JS/Go: `camelCase` for vars/funcs, `PascalCase` for classes.
  - Python/Rust: `snake_case` for vars/funcs.
  - Constants: `SCREAMING_SNAKE_CASE`.
- **[REQ-ENG-NAM-02] Booleans**: Boolean variables MUST use prefixes: `is`, `has`, `should`, `can`.
- **[BAN-ENG-STY-01] No Magic Numbers**: Replace numeric literals with named constants.
- **[BAN-ENG-STY-02] No Nested Else**: Use Guard Clauses (early returns) to flatten nesting.

## 2. Procedures

### 2.1 Object Calisthenics (Strict Mode)

1. **One Level of Indentation**: Extract methods to flatten logic.
2. **Tell, Don't Ask**: Encapsulate logic with data; don't just expose getters.
3. **Wrap Primitives**: Use Value Objects (e.g., `Email`) instead of raw strings where validatable.

### 2.2 Systematic Debugging

1. **Context**: Read valid logs and error messages.
2. **Reproduce**: Create a minimal reproduction case.
3. **Hypothesis**: Formulate a "Because of X, Y happens" theory.
4. **Fix**: Apply minimal fix + Regression Test.

### 2.3 Code Review Checklist

1. **Correctness**: Does it meet requirements over edge cases?
2. **Security**: Inputs validated? No secrets?
3. **Readability**: Is naming clear?
4. **Performance**: No N+1 queries?

## 3. Examples

### 3.1 Clean Code (Guard Clauses)

```typescript
// BAD: Deep nesting
function processUser(user) {
  if (user) {
    if (user.isActive) {
      if (user.hasCredit) {
        charge(user);
      }
    }
  }
}

// GOOD: Guard Clauses
function processUser(user) {
  if (!user) return;
  if (!user.isActive) return;
  if (!user.hasCredit) return;

  charge(user);
}
```

### 3.2 Naming (Intent)

```python
# BAD
d = 0 # elapsed time in days

# GOOD
elapsed_days_since_creation = 0
```

## 4. Validation Criteria

- [ ] **[VAL-ENG-NAM-01]** Naming follows language conventions.
- [ ] **[VAL-ENG-STY-01]** No deep nesting (>3 levels).
- [ ] **[VAL-ENG-STY-02]** No magic numbers/strings without constants.
- [ ] **[VAL-ENG-TST-01]** Fixes include regression tests.

## 5. References

- Related: [0110-git-standards.md](./0110-git-standards.md)
