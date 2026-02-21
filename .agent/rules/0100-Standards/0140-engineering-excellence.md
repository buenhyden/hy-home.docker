---
trigger: model_decision
glob: ["**/*"]
description: "Engineering Excellence Standards: Enforces Clean Code, SOLID principles, and defensive debugging methodologies."
---

# Engineering Excellence Standards

- **Role**: Senior Software Engineer
- **Purpose**: Define standards for writing high-quality, maintainable, and "AI-optimizable" code through rigorous engineering discipline.
- **Activates When**: Writing new features, refactoring existing logic, or performing deep debugging sessions.

**Trigger**: model_decision — Apply during all coding and refactoring activities.

## 1. Standards

### Principles

- **[REQ-ENG-01] Intent-Revealing Declarativity**
  - Code MUST explain "why" through naming and structure, not just "what". Favor descriptive variable names with auxiliary verbs (e.g., `isUserAuthenticated`).
- **[REQ-ENG-02] Single Responsibility Purity (SRP)**
  - Every function and class MUST have one, and only one, reason to change. Functions SHOULD remain under 20 lines where possible.
- **[REQ-ENG-03] Defensive Failure**
  - Logic MUST "Fail Fast" by validating preconditions early using guard clauses and explicit error types.

### Quality Core

| Concept | Requirement ID | Application Target |
| --- | --- | --- |
| SOLID | [REQ-ENG-04] | Class & Module structure |
| DRY / KISS | [REQ-ENG-05] | Logic simplification |
| AI-Optimization | [REQ-ENG-06] | Type hints & Rich context |
| Definition of Done | [REQ-ENG-07] | Readiness verification |

### Must

- **[REQ-ENG-08] Mandatory Type Annotations**
  - Every public function signature and complex data structure MUST have explicit type definitions (TypeScript, Python hints, etc.).
- **[REQ-ENG-09] Narrative Code Structure**
  - Code MUST read like a story: high-level orchestrators at the top, detailed implementation helpers at the bottom.
- **[REQ-ENG-10] Traceable Debugging**
  - Debugging MUST follow a structured Assessment -> Investigation -> Resolution -> QA phase loop.

### Must Not

- **[BAN-ENG-01] Magic Variable Adoption**
  - Avoid literal "magic numbers" or strings; use well-named constants or enums for all configuration and threshold values.
- **[BAN-ENG-02] Nested Indentation Hell**
  - Avoid deeply nested `if/else` blocks (> 3 levels); refactor using early returns or strategy patterns.

### Failure Handling

- **Stop Condition**: Stop feature commit if the code fails to pass the "Self-Documentation" test (can a peer understand it in < 2 minutes?).

## 2. Procedures

- **[PROC-ENG-01] RCA Protocol**
  - IF a recurring bug is identified THEN MUST perform a formal Root Cause Analysis (RCA) and document the "5 Whys".
- **[PROC-ENG-02] Refactoring Sprint**
  - Allocate 10% of every development cycle for proactive refactoring of identified high-complexity components.

## 3. Examples

### Guard Clause Pattern (Good)

```typescript
function processUser(user: User | null) {
  if (!user) return; // Fail fast
  if (!user.isActive) throw new Error("User inactive");
  // ... process
}
```

## 4. Validation Criteria

- **[VAL-ENG-01] Lint & Format Pass**
  - [ ] Every modified file passes the project's automated linting and formatting gates.
- **[VAL-ENG-02] Test Coverage Check**
  - [ ] Complex logic units demonstrate > 80% code coverage.
- **[VAL-ENG-03] Peer Review Approval**
  - [ ] Code review confirms that variable naming and function size adhere to the SRP and Clean Code standards.
