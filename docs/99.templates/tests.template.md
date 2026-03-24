<!-- Target: docs/04.specs/<feature-id>/tests.md -->

# [Feature Name] Test & Evaluation Strategy

> Use this template for `docs/04.specs/<feature-id>/tests.md`.
>
> Rules:
>
> - This document defines the verification strategy for the feature.
> - Core behavior defaults to TDD.
> - Agent functionality must include both software tests and eval coverage when applicable.
> - Execution-tracking remains in `06.tasks/`.
> - This document defines strategy and test inventory.

---

## Overview (KR)

단위, 통합, 계약, 성능 테스트 및 Agent Eval 기준을 정리한다.

## Parent Documents

- **Spec**: `[./spec.md]`
- **Agent Design**: `[./agent-design.md]`
- **API Spec**: `[./api-spec.md]`

## Verification Goals

- **What must be proven**:
- **What risks are targeted**:

## TDD Scope

- **Core behavior requiring test-first implementation**:
- **Exceptions and reason**:

## Test Matrix

| Test ID | Layer | Purpose | Input / Fixture | Expected Result | Automation |
| --- | --- | --- | --- | --- | --- |
| TEST-001 | unit | [Purpose] | [Input] | [Result] | yes |

## Contract & Integration Tests

- **API contract checks**:
- **Consumer compatibility checks**:
- **Dependency integration checks**:

## Non-Functional Tests

- **Performance / latency**:
- **Reliability / retry**:
- **Security / abuse**:

## Agent Evals (If Applicable)

| Eval ID | Type | Scenario | Dataset / Prompt Set | Metric | Threshold |
| --- | --- | --- | --- | --- | --- |
| EVAL-001 | offline | [Scenario] | [Dataset] | [Metric] | [Threshold] |

## Fixtures / Datasets

- **Test fixtures**:
- **Eval datasets**:
- **Golden outputs**:

## How to Run

```bash
pytest tests/
npm test
python evals/run_feature_eval.py
```

## Evidence & Reporting

- **Where results are stored**:
- **Failure triage rule**:
- **Linked execution tasks**: `[../../06.tasks/YYYY-MM-DD-<feature-or-stream>.md]`
