---
profile_id: readme
status: active
---

# 03.specs

> 현재 capability 명세와 승인된 변경의 Plan/Task를 함께 관리하는 stage

## Overview

`docs/03.specs`는 요구사항과 아키텍처 결정을 구현 가능한 capability
계약으로 구체화합니다. 각 `<4-digit-id>-<capability>/` 디렉터리의
`spec.md`는 현재 동작의 durable source of truth이며, 승인된 변경이 진행
중일 때만 `plan.md`와 `tasks/tsk-<4-digit-id>-<slug>.md`가 함께 존재합니다.

Plan은 prospective strategy, Task는 실제 작업 상태와 검증 evidence를
담당합니다. 완료 시 구현된 동작을 `spec.md`에 반영한 뒤 Plan과 Task를
하나의 typed change packet으로 함께 보존합니다. capability child README는
두지 않으며 `spec.md`가 capability 설명을 소유합니다.

## Audience

- Developers
- System Architects
- QA Engineers
- Operators
- AI Agents

## Scope

### In Scope

- capability별 current technical specification
- 승인된 변경의 co-located Plan과 numbered Task records
- Registry가 승인한 OpenAPI, GraphQL schema, Proto executable contracts
- 구현 경계, interface/data contract, failure guardrail, 검증 기준
- Requirement, Architecture Description, ADR, Operations로의 traceability

### Out of Scope

- 제품 요구사항과 사용자 가치 정의 (`docs/01.requirements`)
- Architecture Description과 ADR (`docs/02.architecture`)
- 운영 가이드, 정책, 런북, incident (`docs/05.operations`)
- 완료된 Plan/Task 본문과 retired capability body (`docs/98.archive`)
- Docker Compose runtime 원문과 secret 값

## Structure

```text
docs/03.specs/
├── README.md
└── <4-digit-id>-<capability>/
    ├── spec.md              # mandatory current capability contract
    ├── plan.md              # optional/transient implementation sequence
    ├── tasks/               # optional numbered execution/evidence records
    │   └── tsk-<4-digit-id>-<slug>.md
    └── contracts/           # optional registered executable contracts
```

한 capability에는 `plan.md`가 최대 하나만 존재하며 Task는 numbered record로
관리합니다. `design.md`, `tests.md`, singular `task.md`는 package role이
아닙니다. 완료된 Spec은 `spec.md`로 남고, Plan/Task evidence는 durable capture와
승인된 recovery가 모두 존재할 때만 제거할 수 있습니다.

## Capability Index

| ID | Capability | Current roles |
| :-- | :-- | :-- |
| `SPEC-0001` | [Gateway](./0001-gateway/spec.md) | Spec |
| `SPEC-0002` | [Auth](./0002-auth/spec.md) | Spec |
| `SPEC-0003` | [Security](./0003-security/spec.md) | Spec |
| `SPEC-0004` | [Data](./0004-data/spec.md) | Spec |
| `SPEC-0005` | [Data Analytics](./0005-data-analytics/spec.md) | Spec |
| `SPEC-0006` | [Messaging](./0006-messaging/spec.md) | Spec |
| `SPEC-0007` | [Observability](./0007-observability/spec.md) | Spec |
| `SPEC-0008` | [Workflow](./0008-workflow/spec.md) | Spec |
| `SPEC-0009` | [AI](./0009-ai/spec.md) | Spec |
| `SPEC-0010` | [Tooling](./0010-tooling/spec.md) | Spec |
| `SPEC-0011` | [Communication](./0011-communication/spec.md) | Spec |
| `SPEC-0012` | [Laboratory](./0012-laboratory/spec.md) | Spec |
| `SPEC-0093` | [Documentation Taxonomy Agent-first Migration](./0093-docs-taxonomy-agent-first-migration/spec.md) | Spec |
| `SPEC-0094` | [Harness Agent-first Engineering](./0094-harness-agent-first-engineering/spec.md) | Spec |
| `SPEC-0095` | [Infra, Secrets, and Docs Refresh](./0095-infra-secrets-docs-refresh/spec.md) | Spec |
| `SPEC-0096` | [LLM Wiki Agent-first Completion](./0096-llm-wiki-agent-first-completion/spec.md) | Spec |
| `SPEC-0097` | [Home Docker Revalidation Follow-up](./0097-home-docker-revalidation-deferred-follow-up/spec.md) | Spec |
| `SPEC-0098` | [infra_net Standardization](./0098-standardize-infra-net/spec.md) | Spec |
| `SPEC-0102` | [Workspace Document Contract Audit Pack](./0102-workspace-document-contract-audit-pack/spec.md) | Spec |
| `SPEC-0103` | [Document Restructure Audit and Archive](./0103-document-restructure-audit-contract-archive/spec.md) | Spec |
| `SPEC-0105` | [Agentic Engineering Implementation Audit Pack](./0105-agentic-engineering-implementation-audit-pack/spec.md) | Spec |
| `SPEC-0123` | [Agentic Engineering Audit Remediation](./0123-agentic-engineering-audit-remediation/spec.md) | Spec, [Task](./0123-agentic-engineering-audit-remediation/tasks/tsk-0001-research-pack-extension.md) |
| `SPEC-0131` | [Document Corpus Lifecycle Migration Foundation](./0131-document-corpus-lifecycle-migration-foundation/spec.md) | Spec |
| `SPEC-0132` | [Agent Governance Harness Convergence](./0132-agent-governance-harness-convergence/spec.md) | Spec |
| `SPEC-0133` | [Target Surface Contract Convergence](./0133-target-surface-contract-convergence/spec.md) | Spec |
| `SPEC-0134` | [Agent Governance Canonical Convergence](./0134-agent-governance-canonical-convergence/spec.md) | [Plan](./0134-agent-governance-canonical-convergence/plan.md), [Task](./0134-agent-governance-canonical-convergence/tasks/tsk-0001-canonical-convergence.md) |
| `SPEC-0135` | [Target Surface Delta Convergence](./0135-target-surface-delta-convergence/spec.md) | [Plan](./0135-target-surface-delta-convergence/plan.md), [Task](./0135-target-surface-delta-convergence/tasks/tsk-0001-delta-convergence.md) |
| `SPEC-0136` | [SDLC Taxonomy Convergence](./0136-sdlc-taxonomy-convergence/spec.md) | [Plan](./0136-sdlc-taxonomy-convergence/plan.md), [Task](./0136-sdlc-taxonomy-convergence/tasks/tsk-0001-taxonomy-convergence.md) |
| `SPEC-0137` | [Agentic Research Pack Rebuild](./0137-agentic-research-pack-rebuild/spec.md) | [Plan](./0137-agentic-research-pack-rebuild/plan.md), [Tasks](./0137-agentic-research-pack-rebuild/tasks/) |
| `SPEC-0152` | [Deleted Reference Leaf Disposition](./0152-deleted-reference-leaf-disposition/spec.md) | [Plan](./0152-deleted-reference-leaf-disposition/plan.md), [Task](./0152-deleted-reference-leaf-disposition/tasks/tsk-0001-reference-disposition.md) |
| `SPEC-0154` | [Governance Consistency Convergence](./0154-governance-consistency-convergence/spec.md) | [Plan](./0154-governance-consistency-convergence/plan.md), [Tasks](./0154-governance-consistency-convergence/tasks/) |
| `SPEC-0155` | [Validation Surface Reduction](./0155-validation-surface-reduction/spec.md) | [Plan](./0155-validation-surface-reduction/plan.md), [Tasks](./0155-validation-surface-reduction/tasks/) |
| `SPEC-0156` | [Compose Enablement Model Convergence](./0156-compose-enablement-model-convergence/spec.md) | Spec |
| `SPEC-0157` | [Script Surface Ownership Convergence](./0157-script-surface-ownership-convergence/spec.md) | [Plan](./0157-script-surface-ownership-convergence/plan.md), [Task](./0157-script-surface-ownership-convergence/tasks/tsk-0001-convergence.md) |
| `SPEC-0158` | [Document Governance Lifecycle Convergence](./0158-document-governance-lifecycle-convergence/spec.md) | [Plan](./0158-document-governance-lifecycle-convergence/plan.md), [Task](./0158-document-governance-lifecycle-convergence/tasks/tsk-0001-convergence.md) |

## Role Contract

| Role | Responsibility |
| :-- | :-- |
| Spec | 현재 구현 동작, interface/data contract, failure boundary, 검증 기준 |
| Plan | 승인된 한 변경의 prospective strategy, 순서, 위험, rollback, completion criteria |
| Task | 실제 work log, 명령, 결과, review, commit, deferral evidence |

Plan과 Task의 상태가 완료되면 먼저 구현된 동작을 Spec과 필요한 Operations
문서에 반영합니다. Durable evidence capture와 승인된 recovery가 모두 확인된
경우에만 package에서 제거하며, 별도 redirect 문서는 만들지 않습니다.

## How to Work in This Area

1. 관련 Requirement, Architecture Description, ADR을 확인합니다.
2. [Spec template](../99.templates/templates/specs/spec.template.md)으로
   `spec.md`를 작성하고 stable artifact ID를 사용합니다.
3. 승인된 변경에만 [Plan template](../99.templates/templates/specs/plan.template.md)과
   [Task template](../99.templates/templates/specs/task.template.md)을 사용해
   `plan.md`와 numbered Task records를 co-locate합니다.
4. Plan은 package당 하나로 제한하고 Task number와 artifact identity를
   package owner에 맞춥니다.
5. 실제 결과를 Task에 기록하고 current behavior를 Spec에 write-back합니다.
6. 운영자에게 보이는 변경은 `docs/05.operations`의 typed owner에 반영합니다.
7. 완료된 Plan/Task는 evidence capture와 승인된 recovery를 확인한 뒤에만
   현재 capability에서 제거합니다.
8. 변경 문서 metadata, lifecycle, traceability, implementation alignment를
   검증합니다.

## Related Documents

- [Requirements](../01.requirements/README.md)
- [Architecture](../02.architecture/README.md)
- [Operations](../05.operations/README.md)
- [Archive](../98.archive/README.md)
- [Stage authoring matrix](../00.agent-governance/policies/stage-authoring-matrix.md)
- [Document metadata profiles](../99.templates/registry.json)
- [Archive retention contract](../99.templates/README.md)
