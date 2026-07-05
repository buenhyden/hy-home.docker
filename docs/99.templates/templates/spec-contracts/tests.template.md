---
status: draft
---
<!-- Target: docs/03.specs/NNN-<feature-id>/tests.md -->

# [Feature Name] Test & Evaluation Strategy

> Use this template for `docs/03.specs/NNN-<feature-id>/tests.md`.
>
> Rules:
>
> - This document defines the verification strategy and test inventory for the feature.
> - Core behavior defaults to TDD.
> - Agent functionality must include both software tests and eval coverage when applicable.
> - Execution-tracking remains in `04.execution/tasks/`.
> - Write this document in English. Preserve code identifiers, command names,
>   service names, environment variables, and quoted upstream terms exactly.
> - Target-relative links in `## Related Documents` are calculated from the copied target path, not from `docs/99.templates/`.

---

## Overview

This document defines unit, integration, contract, performance, and Agent Eval
criteria for the feature.

## Parent Documents

- **Spec**: [./spec.md](./spec.md)
- **Agent Design**: [./agent-design.md](./agent-design.md)
- **API Spec**: [./api-spec.md](./api-spec.md)

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
- **Linked execution tasks**: [../../04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md](../../04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md)

## Related Documents

- **Spec**: [./spec.md](./spec.md)
- **Agent Design**: [./agent-design.md](./agent-design.md)
- **Execution Task**: [../../04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md](../../04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md)
