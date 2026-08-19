---
status: active
---

# 03.specs

> 현재 capability 명세와 승인된 변경의 Plan/Task를 함께 관리하는 stage

## Overview

`docs/03.specs`는 요구사항과 아키텍처 결정을 구현 가능한 capability
계약으로 구체화합니다. 각 `spec-<id>-<capability>/` 디렉터리의 `spec.md`는
현재 동작의 durable source of truth이며, 승인된 변경이 진행 중일 때만
`plan.md`와 `task.md`가 같은 디렉터리에 존재합니다.

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
- 승인된 단일 변경의 co-located Plan과 Task
- API, schema, protocol, data model, tests, agent design 같은 child contract
- 구현 경계, interface/data contract, failure guardrail, 검증 기준
- Requirement, Architecture Description, ADR, Operations로의 traceability

### Out of Scope

- 제품 요구사항과 사용자 가치 정의 (`docs/01.requirements`)
- Architecture Description과 ADR (`docs/02.architecture`)
- 운영 가이드, 정책, 런북, incident, release (`docs/05.operations`)
- 완료된 Plan/Task 본문과 retired capability body (`docs/98.archive`)
- Docker Compose runtime 원문과 secret 값

## Structure

```text
docs/03.specs/
├── README.md
└── spec-<id>-<capability>/
    ├── spec.md              # mandatory current capability contract
    ├── plan.md              # optional; one active approved change
    ├── task.md              # optional; one active evidence ledger
    └── contracts/           # optional machine-readable contracts
```

한 capability에는 `plan.md`와 `task.md` 역할이 각각 최대 하나만 존재합니다.
완료된 실행 evidence는 이 stage에 남기지 않습니다.

## Capability Index

| ID | Capability | Current roles |
| :-- | :-- | :-- |
| `spec-0001` | [Gateway](./spec-0001-gateway/spec.md) | Spec |
| `spec-0002` | [Auth](./spec-0002-auth/spec.md) | Spec |
| `spec-0003` | [Security](./spec-0003-security/spec.md) | Spec |
| `spec-0004` | [Data](./spec-0004-data/spec.md) | Spec |
| `spec-0005` | [Data Analytics](./spec-0005-data-analytics/spec.md) | Spec |
| `spec-0006` | [Messaging](./spec-0006-messaging/spec.md) | Spec |
| `spec-0007` | [Observability](./spec-0007-observability/spec.md) | Spec |
| `spec-0008` | [Workflow](./spec-0008-workflow/spec.md) | Spec, merged agent contract |
| `spec-0009` | [AI](./spec-0009-ai/spec.md) | Spec, merged Open WebUI contract |
| `spec-0010` | [Tooling](./spec-0010-tooling/spec.md) | Spec |
| `spec-0011` | [Communication](./spec-0011-communication/spec.md) | Spec |
| `spec-0012` | [Laboratory](./spec-0012-laboratory/spec.md) | Spec |
| `spec-0090` | [Workspace Audit 2026-05](./spec-0090-workspace-audit-2026-05/spec.md) | Spec |
| `spec-0091` | [Workspace Document Consistency](./spec-0091-workspace-doc-consistency-2026-05/spec.md) | Spec |
| `spec-0092` | [Workspace Consistency Follow-up](./spec-0092-workspace-consistency-2026-05b/spec.md) | Spec |
| `spec-0093` | [Documentation Taxonomy Agent-first Migration](./spec-0093-docs-taxonomy-agent-first-migration/spec.md) | Spec |
| `spec-0094` | [Harness Agent-first Engineering](./spec-0094-harness-agent-first-engineering/spec.md) | Spec |
| `spec-0095` | [Infra, Secrets, and Docs Refresh](./spec-0095-infra-secrets-docs-refresh/spec.md) | Spec |
| `spec-0096` | [LLM Wiki Agent-first Completion](./spec-0096-llm-wiki-agent-first-completion/spec.md) | Spec |
| `spec-0097` | [Home Docker Revalidation Follow-up](./spec-0097-home-docker-revalidation-deferred-follow-up/spec.md) | Spec |
| `spec-0098` | [infra_net Standardization](./spec-0098-standardize-infra-net/spec.md) | Spec |
| `spec-0102` | [Workspace Document Contract Audit Pack](./spec-0102-workspace-document-contract-audit-pack/spec.md) | Spec |
| `spec-0103` | [Document Restructure Audit and Archive](./spec-0103-document-restructure-audit-contract-archive/spec.md) | Spec |
| `spec-0105` | [Agentic Engineering Implementation Audit Pack](./spec-0105-agentic-engineering-implementation-audit-pack/spec.md) | Spec |
| `spec-0123` | [Agentic Engineering Audit Remediation](./spec-0123-agentic-engineering-audit-remediation/spec.md) | Spec, [Task](./spec-0123-agentic-engineering-audit-remediation/task.md) |
| `spec-0131` | [Document Corpus Lifecycle Migration Foundation](./spec-0131-document-corpus-lifecycle-migration-foundation/spec.md) | Spec |
| `spec-0132` | [Agent Governance Harness Convergence](./spec-0132-agent-governance-harness-convergence/spec.md) | Spec |
| `spec-0133` | [Target Surface Contract Convergence](./spec-0133-target-surface-contract-convergence/spec.md) | Spec |
| `spec-0134` | [Agent Governance Canonical Convergence](./spec-0134-agent-governance-canonical-convergence/spec.md) | [Plan](./spec-0134-agent-governance-canonical-convergence/plan.md), [Task](./spec-0134-agent-governance-canonical-convergence/task.md) |
| `spec-0135` | [Target Surface Delta Convergence](./spec-0135-target-surface-delta-convergence/spec.md) | [Plan](./spec-0135-target-surface-delta-convergence/plan.md), [Task](./spec-0135-target-surface-delta-convergence/task.md) |
| `spec-0136` | [SDLC Taxonomy Convergence](./spec-0136-sdlc-taxonomy-convergence/spec.md) | [Plan](./spec-0136-sdlc-taxonomy-convergence/plan.md), [Task](./spec-0136-sdlc-taxonomy-convergence/task.md) |
| `spec-0152` | [Deleted Reference Leaf Disposition](./spec-0152-deleted-reference-leaf-disposition/spec.md) | [Plan](./spec-0152-deleted-reference-leaf-disposition/plan.md), [Task](./spec-0152-deleted-reference-leaf-disposition/task.md) |

## Role Contract

| Role | Responsibility |
| :-- | :-- |
| Spec | 현재 구현 동작, interface/data contract, failure boundary, 검증 기준 |
| Plan | 승인된 한 변경의 prospective strategy, 순서, 위험, rollback, completion criteria |
| Task | 실제 work log, 명령, 결과, review, commit, deferral evidence |

Plan과 Task의 상태가 완료되면 먼저 구현된 동작을 Spec과 필요한 Operations
문서에 반영합니다. 그 다음 두 문서를 동일한 `chg-<id>-<slug>/` packet으로
이동하고 capability에서는 제거합니다. 별도 redirect 문서는 만들지 않습니다.

## How to Work in This Area

1. 관련 Requirement, Architecture Description, ADR을 확인합니다.
2. [Spec template](../99.templates/templates/sdlc/spec.template.md)으로
   `spec.md`를 작성하고 stable artifact ID를 사용합니다.
3. 승인된 변경에만 [Plan template](../99.templates/templates/sdlc/plan.template.md)과
   [Task template](../99.templates/templates/sdlc/task.template.md)을 co-locate합니다.
4. 한 capability의 active change packet을 하나로 제한합니다.
5. 실제 결과를 Task에 기록하고 current behavior를 Spec에 write-back합니다.
6. 운영자에게 보이는 변경은 `docs/05.operations`의 typed owner에 반영합니다.
7. 완료된 Plan/Task는 [Stage 98 change packet](../98.archive/README.md)으로
   함께 이동하고 현재 capability에서 제거합니다.
8. 변경 문서 metadata, lifecycle, traceability, implementation alignment를
   검증합니다.

## Related Documents

- [Requirements](../01.requirements/README.md)
- [Architecture](../02.architecture/README.md)
- [Operations](../05.operations/README.md)
- [Archive](../98.archive/README.md)
- [Stage authoring matrix](../00.agent-governance/rules/stage-authoring-matrix.md)
- [Document metadata profiles](../99.templates/support/document-metadata-profiles.yaml)
- [Archive retention contract](../99.templates/support/archive-retention-contract.md)
