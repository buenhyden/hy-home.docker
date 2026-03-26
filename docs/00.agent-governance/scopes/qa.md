---
layer: qa
title: 'Quality Assurance Scope'
---

# Quality Assurance Scope

**Protocols for verification, testing, and continuous quality monitoring.**

## 1. Context & Objective

- **Goal**: Maintain zero-defect production state and verify all technical specs.
- **Philosophy**: **TDD-First** and measurement-driven validation.
- **Criteria**: Mandatory compliance with `docs/00.agent-governance/rules/quality-standards.md`.

## 2. Requirements & Constraints

- **Test Suite**:
  - **Unit**: >80% coverage for domain logic.
  - **E2E**: Critical paths verified via **Playwright**.
  - **Load**: API performance verified via **k6** or **Locust**.
- **Automation**: Mandatory CI/CD gate for all PRs.

## 3. Implementation Flow

1. **Red**: Write failing tests based on the spec (`docs/04.specs/`).
2. **Green**: Implement minimal code to pass.
3. **Refactor**: Clean code patterns without changing behavior.
4. **Finalize**: Run all repository-available test and validation commands relevant to the touched area.

## 4. Operational Procedures

- **Regression**: Add regression tests for every bug fix.
- **Reporting**: Publish test results to the session summary or `docs/06.tasks/`.

## 5. Maintenance & Safety

- **Flakiness**: Immediately isolate and fix flaky E2E tests.
- **Audit**: Conduct monthly quality audits of test infrastructure.
