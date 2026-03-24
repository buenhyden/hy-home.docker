<!-- Target: docs/04.specs/<feature-id>/spec.md -->
# [Feature Name] Specification

> Use this template for `docs/04.specs/<feature-id>/spec.md`.
>
> Rules:
>
> - Every active spec must declare PRD and ARD references or make the absence explicit.
> - Verification is mandatory.
> - If this feature exposes an external API, link a dedicated API Spec.
> - Keep one `Overview (KR)` summary near the top.
> - This document is the parent design doc; API contracts live in `api-spec.md` under the same feature directory.

---

# [Feature Name] Specification

## Overview (KR)

이 문서는 [기능명]의 기술 설계와 구현 계약을 정의하는 명세서다. PRD 요구를 기술적으로 구체화하고, 구현과 검증의 직접 기준이 된다.

## Strategic Boundaries & Non-goals

[What this spec owns, and what it does not.]

## Related Inputs

- **PRD**: `[../../01.prd/YYYY-MM-DD-<feature-or-system>.md]`
- **ARD**: `[../../02.ard/####-<system-or-domain-name>.md]`
- **Related ADRs**: `[../../03.adr/####-<short-title>.md]`

## Contracts

- **Config Contract**:
- **Data / Interface Contract**:
- **Governance Contract**:

## Core Design

- **Component Boundary**:
- **Key Dependencies**:
- **Tech Stack**:

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**:
- **Migration / Transition Plan**:

## Interfaces & Data Structures

### Core Interfaces

```typescript
interface ExampleContract {
  id: string;
  name: string;
}
```

## API Contract (If Applicable)

Contract-first 원칙: 이 기능이 외부 API를 제공하는 경우, 상세 API 계약은 별도 API Spec 문서에서 정의한다.

- **API Spec**: `[./api-spec.md]`
- **Policy**: API Spec은 `docs/api/` 같은 별도 최상위 경로가 아니라 현재 feature 디렉터리 아래에 둔다.
- **Machine-readable Contract**:
  - `./contracts/openapi.yaml`
  - `./contracts/service.proto`
  - `./contracts/schema.graphql`

## Agent Role & IO Contract (If Applicable)

- **Agent Role**:
- **Inputs**:
- **Outputs**:
- **Success Definition**:

## Tools & Tool Contract (If Applicable)

- **Tool List**:
- **Permission Boundary**:
- **Failure Handling**:

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**:
- **Policy Constraints**:
- **Versioning Rule**:

## Memory & Context Strategy (If Applicable)

- **Short-term Context**:
- **Long-term Memory**:
- **Retrieval Boundary**:

## Guardrails (If Applicable)

- **Input Guardrails**:
- **Output Guardrails**:
- **Blocked Conditions**:
- **Escalation Rule**:

## Evaluation (If Applicable)

- **Eval Types**:
- **Metrics**:
- **Datasets / Fixtures**:
- **How to Run**:

## Edge Cases & Error Handling

- **Error 1**:
- **Error 2**:

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**:
- **Fallback**:
- **Human Escalation**:

## Verification

List the required commands, manual checks, or evidence capture steps.

```bash
[command 1]
[command 2]
pytest tests/[feature]_test.py
python evals/run_[feature]_eval.py
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**:
- **VAL-SPC-002**:

## Related Documents

- **Plan**: `[../../05.plans/YYYY-MM-DD-<feature>.md]`
- **Tasks**: `[../../06.tasks/YYYY-MM-DD-<feature-or-stream>.md]`
- **Runbook**: `[../../09.runbooks/<topic>.md]`
