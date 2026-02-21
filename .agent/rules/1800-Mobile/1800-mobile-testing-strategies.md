---
trigger: always_on
glob: "**/*.{kt,swift,tsx,js}"
description: "Mobile Testing Strategies: Enforces the testing pyramid, real-device verification, and automated regression standards."
---

# Mobile Testing Strategies

- **Role**: Mobile Quality Assurance Lead
- **Purpose**: Define standards for ensuring mobile application reliability through a balanced strategy of unit, integration, and E2E testing.
- **Activates When**: Writing test suites, configuring CI/CD pipelines, or performing manual exploratory testing.

**Trigger**: always_on — Apply during the testing and verification phases of mobile development.

## 1. Standards

### Principles

- **[REQ-MOBT-01] Balanced Testing Pyramid**
  - Verification MUST follow the testing pyramid: many unit tests, several integration tests, and focused E2E user-flow tests.
- **[REQ-MOBT-02] Real-Device Verification**
  - Final acceptance testing MUST be performed on physical devices, not exclusively on simulators or emulators.
- **[REQ-MOBT-03] Automated Regression Flow**
  - Critical user journeys MUST have automated regression tests that run on every pull request.

### Testing Stack

| Level | Requirement ID | Standard Tooling |
| --- | --- | --- |
| Unit | [REQ-MOBT-04] | JUnit / XCTest / Jest |
| Integration | [REQ-MOBT-05] | Robolectric / Detox |
| UI / E2E | [REQ-MOBT-06] | Espresso / XCUITest / Maestro |
| Snapshots | [REQ-MOBT-07] | React Native Snapshot / SwiftSnapshot |

### Must

- **[REQ-MOBT-08] Mock External Dependencies**
  - Unit tests MUST mock or fake network and database dependencies to ensure isolation and speed.
- **[REQ-MOBT-09] Flakiness Mitigation**
  - UI tests MUST utilize explicit wait mechanisms instead of arbitrary sleep timers to minimize flakiness.
- **[REQ-MOBT-10] Multi-Configuration Testing**
  - Tests MUST cover a baseline of varied screen sizes, OS versions, and network conditions (e.g., offline mode).

### Must Not

- **[BAN-MOBT-01] Simulator-Only Verification**
  - DO NOT approve a major release if it has only been verified on a simulator without physical device testing.
- **[BAN-MOBT-02] Deep UI-Only Suites**
  - Avoid creating monolithic UI tests for business logic that could be verified faster and more reliably at the unit level.

### Failure Handling

- **Stop Condition**: Stop the release pipeline if the automated E2E test suite pass rate falls below 100% on critical paths.

## 2. Procedures

- **[PROC-MOBT-01] Regression Run**
  - IF modifying a core data model THEN MUST re-run all snapshot and integration tests to detect unintended UI shifts.
- **[PROC-MOBT-02] Exploratory Audit**
  - Perform a manual "Chaos Test" (e.g., backgrounding, interrupts during load) before every major platform update.

## 3. Examples

### Widget Test (Flutter/React Native style)

```typescript
// Good: testing a specific component interaction
it('increments count on button press', () => {
  const { getByText, fireEvent } = render(<Counter />);
  fireEvent.press(getByText('Increment'));
  expect(getByText('Count: 1')).toBeTruthy();
});
```

## 4. Validation Criteria

- **[VAL-MOBT-01] coverage Threshold**
  - [ ] Business logic modules maintain a minimum of 80% unit test coverage.
- **[VAL-MOBT-02] Device Diversity**
  - [ ] Test logs verify successful execution on both the latest OS version and the project's minimum supported version.
- **[VAL-MOBT-03] Flakiness Report**
  - [ ] CI analytics show that UI tests have a stability rate > 98% over the last 30 runs.
