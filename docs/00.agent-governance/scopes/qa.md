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
  - **Target**: 90% coverage for changed domain logic when the repository has a measurable suite for that layer.
  - **E2E**: Critical paths verified via **Playwright**.
  - **Load**: API performance verified via **k6** or **Locust**.
- **Automation**: Mandatory CI/CD gate for all PRs.
- **Applicability**: Mark coverage N/A for docs-only, policy-only, infrastructure configuration, and validation-script changes when no domain-code coverage signal applies.

## 3. Implementation Flow

1. **Red**: Write failing tests based on the spec (`docs/03.specs/`).
2. **Green**: Implement minimal code to pass.
3. **Refactor**: Clean code patterns without changing behavior.
4. **Finalize**: Run all repository-available test and validation commands relevant to the touched area.

## 4. Operational Procedures

- **Regression**: Add regression tests for every bug fix.
- **Refactor evidence**: For behavior-preserving refactors, run checks that cover the touched behavior and state that no behavior change is intended.
- **Reporting**: Publish test results to the session summary or `docs/04.execution/tasks/`.

## 5. Maintenance & Safety

- **Flakiness**: Immediately isolate and fix flaky E2E tests.
- **Audit**: Conduct monthly quality audits of test infrastructure.

## Related Documents

- [Agent governance hub](../README.md)
- [Bootstrap rule](../rules/bootstrap.md)
- [Persona protocol](../rules/persona.md)
- [Task checklists](../rules/task-checklists.md)
- [Agentic rule](../rules/agentic.md)
