---
trigger: always_on
glob: ["**/*.{test,spec}.{ts,js,py}", "**/tests/**/*", "**/qa/**/*"]
description: "Testing & QA Standards: Enforces the Testing Pyramid, risk-based strategies, and CI/CD quality gates using ISTQB/ISO 25010 frameworks."
---

# Testing & Quality Assurance Standards

- **Role**: Lead QA Automation Engineer / SDET
- **Purpose**: Define standards for ensuring software reliability, performance, and security through a multi-layered, risk-based testing strategy.
- **Activates When**: Developing test suites (Unit, Integration, E2E), configuring CI/CD quality gates, or performing quality audits.

**Trigger**: always_on — Apply during the design, implementation, and execution of all testing activities.

## 1. Standards

### Principles

- **[REQ-TST-01] Testing Pyramid Adherence**
  - Test suites MUST follow the pyramid distribution: Many Unit Tests (70%), some Integration/API tests (20%), and few E2E tests (10%).
- **[REQ-TST-02] Shift-Left Logic**
  - Testing activities MUST begin as early as possible in the lifecycle. Unit tests MUST be developed alongside or before implementation (TDD).
- **[REQ-TST-03] Risk-Based Prioritization**
  - Testing effort MUST be prioritized based on the business impact and failure probability of the target feature.

### Quality Baseline (ISO 25010)

| Tier | Requirement ID | Critical Gate |
| --- | --- | --- |
| Unit | [REQ-TST-04] | > 80% line coverage |
| Integration | [REQ-TST-05] | 100% of API endpoints covered |
| E2E | [REQ-TST-06] | Primary user journeys pass in CI |
| Security | [REQ-TST-07] | Zero High/Critical vulnerabilities |

### Must

- **[REQ-TST-08] Mandatory Teardown (Isolation)**
  - All tests MUST be isolated and independent. Implement robust setup and teardown logic to ensure shared state does not leak between runs.
- **[REQ-TST-09] Explicit Failure Assertions**
  - Tests MUST have clear, descriptive assertions. Avoid "blind" tests that only verify the absence of a crash; verify specific expected outcomes.
- **[REQ-TST-10] CI/CD Gate Enforcement**
  - No code MUST be merged to the main branch unless all representative test suites (Unit + Integration) pass with 100% success.
- **[REQ-TST-11] Global Coverage Gate**
  - Total project coverage MUST be >= 80% to ensure long-term stability. CI MUST fail on regression.
- **[REQ-TST-12] Load Verification**
  - High-traffic or critical paths MUST undergo Load Testing (K6/Locust) to verify NFR compliance.

### Must Not

- **[BAN-TST-01] Flaky Test Tolerance**
  - Testing suites MUST NOT tolerate "flaky" results. Flaky tests MUST be quarantined and fixed immediately or removed from the CI gate.
- **[BAN-TST-02] Hardcoded Test Data**
  - Avoid hardcoding PII or production-sensitive data in tests; utilize data generators or anonymized fixtures.

### Failure Handling

- **Stop Condition**: Stop commit/merge if the code coverage drops below the project's established baseline or if a regression is identified in a core feature.

## 2. Procedures

- **[PROC-TST-01] TDD Cycle**
  - IF implementing a new feature THEN MUST follow the Red-Green-Refactor cycle: Write failing test -> Implement -> Verify & Clean.
- **[PROC-TST-02] Regression Mapping**
  - For every bug fix, MUST add at least one unit or integration test that specifically targets the resolved defect to prevent regressions.

## 3. Examples

### Clean Unit Test (Python/Pytest)

```python
def test_calc_add():
    assert calc.add(2, 3) == 5, "Addition logic failed"
```

## 4. Validation Criteria

- **[VAL-TST-01] Coverage Threshold**
  - [ ] `Istanbul` / `Coverage.py` confirms > 80% coverage across the core business domain.
- **[VAL-TST-02] CI Integrity**
  - [ ] GitHub Actions confirm that 100% of PRs are blocked until testing suites pass correctly.
- **[VAL-TST-03] Defect detection**
  - [ ] Audit confirms that 95% of regressions were identified by automated suites before reaching the staging environment.
