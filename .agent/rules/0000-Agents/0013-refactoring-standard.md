---
trigger: model_decision
glob: ["**/*"]
description: "Refactoring Agent Standards: Enforces behavior-preserving code improvements, incremental modernization, and test-backed modernization logic."
---

# Refactoring Agent Standards

- **Role**: Code Modernization Specialist
- **Purpose**: Define standards for improving the internal structure of existing codebases without altering their external behavior, focusing on maintainability and pattern alignment.
- **Activates When**: The user requests code cleanup, deduplication, architectural alignment, or modernization of legacy modules.

**Trigger**: model_decision — Apply during all code cleanup, modernization, and structural refactoring phases.

## 1. Standards

### Principles

- **[REQ-REF-01] Mandatory behavior Preservation**
  - Refactoring MUST NOT change the runtime behavior or public contract of the module. Any functional modification MUST be treated as an Implementation task, not a Refactor.
- **[REQ-REF-02] Green-to-Green Test Cycle**
  - A refactor MUST begin with passing tests and end with passing tests. Modifying code without an existing test suite is PROHIBITED.
- **[REQ-REF-03] Atomic Incrementalism**
  - improvements MUST be applied in small, verifiable steps. Monolithic "rewrite-as-refactor" approaches are STRICTLY PROHIBITED.

### Modernization Matrix

| Pattern | Requirement ID | Critical Action |
| --- | --- | --- |
| Extraction | [REQ-REF-04] | extract complex logic to atomic functions |
| Naming | [REQ-REF-05] | align identifiers with intent and local style |
| DRY | [REQ-REF-06] | Consolidate duplicate logic into shared util |
| Pattern | [REQ-REF-07] | apply project-standard design patterns |

### Must

- **[REQ-REF-08] Prioritized Smell Resolution**
  - Identify and explicitly state the "Code Smell" being targeted (e.g., God Object, Long Method, Duplicated Code) before modification.
- **[REQ-REF-09] Explicit Diff Rationale**
  - Refactoring summaries MUST document not just *what* changed, but *why* the new structure is superior in terms of maintainability or performance.
- **[REQ-REF-10] Synchronized Documentation**
  - All associated documentation (JSDoc, README) MUST be updated immediately to reflect the new internal naming and structure.

### Must Not

- **[BAN-REF-01] Feature Creep Contamination**
  - DO NOT bundle bug fixes or new feature development within a refactoring task. Keep the two concerns strictly separated.
- **[BAN-REF-02] Opaque Global Side-Effects**
  - Avoid introducing new global dependencies or side-effects during structural cleanup.

### Failure Handling

- **Stop Condition**: Stop refactoring if a unit test fails at any point in the cycle. Revert to the last "Green" state before attempting the next incremental step.

## 2. Procedures

- **[PROC-REF-01] The Refactor Loop**
  - 1. Verify Baseline (Green) -> 2. Identify Smell -> 3. Apply Atomic Pattern -> 4. Verify Result (Green) -> 5. Document Change.
- **[PROC-REF-02] Pattern Audit**
  - IF applying a design pattern (e.g., Strategy, Factory) THEN MUST verify that it aligns with the project's broader architectural blueprint.

## 3. Examples

### Clean Extraction (Good)

```javascript
// Before: God Function
function process() { /* 50 lines of logic */ }

// After: Atomic Decompositon
function validate() { ... }
function transform() { ... }
function process() { validate(); transform(); }
```

## 4. Validation Criteria

- **[VAL-REF-01] Test Suite Integrity**
  - [ ] build logs confirm that 100% of existing tests pass before and after the refactoring operation.
- **[VAL-REF-02] Maintainability Metric**
  - [ ] Structural analysis confirms a reduction in Cyclomatic Complexity or duplicate code percentage.
- **[VAL-REF-03] Documentation Parity**
  - [ ] Verification confirms that internal JSDoc/types accurately reflect 100% of the structural changes.
