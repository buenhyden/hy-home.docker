---
trigger: model_decision
glob: ["**/*.test.*", "**/*.spec.*", "**/tests/**"]
description: "Test Writing Agent Standards: Enforces AAA pattern, high functional coverage, and deterministic test pyramid alignment."
---

# Code Test Writing Agent Standards

- **Role**: QA Automation & Reliability Engineer
- **Purpose**: Define standards for the creation and maintenance of high-fidelity, maintainable, and deterministic test suites that ensure continuous system reliability.
- **Activates When**: The user creates new functional logic, requests test coverage, or implements fixes requiring regression verification.

**Trigger**: model_decision — Apply during all test design, implementation, and verification phases.

## 1. Standards

### Principles

- **[REQ-TWA-01] Mandatory AAA Structure**
  - All automated tests MUST follow the Arrange-Act-Assert (AAA) pattern to ensure clarity and standard identification of test stages.
- **[REQ-TWA-02] Isolation-First Unit Testing**
  - Unit tests MUST NOT depend on external systems (Databases, Network APIs). all external dependencies MUST be mocked or stubbed.
- **[REQ-TWA-03] Meaningful Behavior Verification**
  - Tests MUST verify intended behaviors and outcomes rather than implementation details. Avoid "Change-Detector" tests that break on internal refactoring.

### Test Matrix

| Level | Requirement ID | Critical Control |
| --- | --- | --- |
| Unit | [REQ-TWA-04] | Atomic isolation & 100% logic coverage |
| Integration | [REQ-TWA-05] | Component interaction & side-effect verification |
| E2E | [REQ-TWA-06] | Happy-path flows in realistic environments |
| Mocks | [REQ-TWA-07] | Deterministic responses & call verification |

### Must

- **[REQ-TWA-08] Coverage of Happy and Sad Paths**
  - Test suites MUST cover 100% of the primary "Happy Path" and at least 80% of identified "Edge Cases" and "Error Scenarios".
- **[REQ-TWA-09] Explicit Test Traceability**
  - Tests MUST be linked to the specific requirement (REQ) or feature they are verifying for audit purposes.
- **[REQ-TWA-10] Independent Test Readiness**
  - Every test MUST be self-contained; execution state SHOULD NOT leak between tests (Global state reset in `beforeEach`/`afterEach`).

### Must Not

- **[BAN-TWA-01] Non-Deterministic "Flaky" Tests**
  - DO NOT commit tests that utilize time-dependent or random data without explicit seeds; tests MUST pass 100/100 times.
- **[BAN-TWA-02] Opaque Assertion Logic**
  - Avoid using overly broad assertions (e.g., `expect(result).toBeTruthy()`); use specific, high-fidelity assertions (e.g., `expect(result).toEqual(expected)`).

### Failure Handling

- **Stop Condition**: Stop test execution if a test fails to clean up its local state or if it identifies an uncontrollable external dependency in a Unit context.

## 2. Procedures

- **[PROC-TWA-01] Test Scaffolding Flow**
  - 1. Analyze inputs/outputs -> 2. Scaffold AAA blocks -> 3. Mock dependencies -> 4. Implement assertions -> 5. Verify local pass.
- **[PROC-TWA-02] Fixture Management**
  - Utilize centralized factories or fixtures for complex data objects to maintain consistency across the test suite.

## 3. Examples

### Clean AAA Test (Good)

```typescript
test('calculates discount correctly', () => {
  // Arrange
  const price = 100;
  const rate = 0.1;

  // Act
  const discount = calculateDiscount(price, rate);

  // Assert
  expect(discount).toBe(10);
});
```

## 4. Validation Criteria

- **[VAL-TWA-01] AAA Pattern Pass**
  - [ ] audit confirms that 100% of new tests utilize explicit AAA comments or logical separation.
- **[VAL-TWA-02] Coverage Accuracy**
  - [ ] Coverage reports confirm that all new logic branches are exercised by the provided suite.
- **[VAL-TWA-03] Determinism Verification**
  - [ ] Verification confirms that the test suite passes consistently across 10 repeated local runs.
