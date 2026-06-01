---
status: active
---
<!-- Target: docs/02.architecture/requirements/README.md -->

# Architecture Reference Documents (ARD)

> 시스템 경계, 참조 아키텍처, 품질 속성을 관리하는 ARD 문서 공간

## Overview

`docs/02.architecture/requirements`는 PRD의 요구사항을 아키텍처 관점으로 해석한 참조 문서를 보관한다. ARD는 시스템이 무엇을 소유하고, 무엇을 소비하며, 어떤 품질 속성을 만족해야 하는지 설명한다.

구현 파일, API 세부 계약, 실행 순서는 이 경로의 책임이 아니다. 그런 내용은 후속 Spec, Plan, Task, Operations 문서에서 관리한다.

## Audience

이 README의 주요 독자:

- System Architects
- Developers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 도메인별/시스템별 책임 경계
- 품질 속성(성능, 보안, 안정성, 확장성, 관측성, 운영성)
- 시스템 구성 요소 간 인터페이스와 데이터 흐름
- AI Agent 아키텍처 요구사항이 있는 경우의 tool, memory, guardrail boundary
- 관련 ADR, Spec, Plan, Task, Operations 문서로의 추적성

### Out of Scope

- 제품 요구사항 정의 (`docs/01.requirements` 담당)
- 기술 선택의 결정 기록 (`docs/02.architecture/decisions` 담당)
- 파일 단위 구현 상세와 계약 (`docs/03.specs` 담당)
- 실행 계획과 작업 증거 (`docs/04.execution` 담당)
- 운영 절차와 장애 대응 (`docs/05.operations` 담당)

## Structure

```text
docs/02.architecture/requirements/
├── 0001-gateway-architecture.md
├── 0002-auth-architecture.md
├── ...
├── 0026-standardize-infra-net.md        # Canonical infra_net ARD
├── 0027-agent-governance-canonical-adapter.md # Canonical agent governance adapter ARD
└── README.md                            # This file
```

## Current Inventory

- 24 ARD leaf documents are present.
- `0001` through `0014` cover the base service and tier architecture set.
- `0018` through `0026` cover hardening/HA and network architecture follow-up work.
- [`0026-standardize-infra-net.md`](./0026-standardize-infra-net.md) is the canonical `infra_net` ARD for this stage.
- [`0027-agent-governance-canonical-adapter.md`](./0027-agent-governance-canonical-adapter.md) is the canonical agent governance adapter ARD for this stage.

## How to Work in This Area

1. 상위 PRD는 [`../../01.requirements/`](../../01.requirements/README.md)에서 확인한다.
2. 같은 tier, system, architecture concern을 다루는 ARD가 이미 있는지 먼저 확인한다.
3. 새 ARD는 [`../../99.templates/ard.template.md`](../../99.templates/ard.template.md)에서 시작한다.
4. 모든 링크는 이 폴더 아래의 대상 ARD 위치 기준으로 다시 계산한다.
5. ARD가 중요한 trade-off를 기록하거나 변경하면 [`../decisions/`](../decisions/README.md)의 ADR과 연결한다.
6. 구현 상세는 [`../../03.specs/`](../../03.specs/README.md)에 둔다.

## Documentation Standards

- ARD는 implementation task가 아니라 architecture reference model을 설명한다.
- 하나의 ARD는 하나의 system, tier, 또는 architecture concern을 다룬다.
- 번호가 부여된 canonical ARD가 있으면 같은 목적의 dated duplicate를 만들지 않는다.
- 관련 산출물이 존재하면 `## Related Documents`에 PRD, ADR, Spec, Plan, Task, Operations 링크를 둔다.

## AI Agent Guidance

1. ARD를 수정하기 전에 이 README를 먼저 읽는다.
2. 대체 파일을 추가하지 말고 canonical ARD를 in-place로 수정한다.
3. `infra_net` architecture reference는 [`0026-standardize-infra-net.md`](./0026-standardize-infra-net.md)를 canonical로 본다.
4. 아키텍처 문서 작성 중 secret 값을 조회하거나 노출하지 않는다.

## Related Documents

- **Architecture Stage**: [Architecture index](../README.md)
- **PRD**: [Product requirements](../../01.requirements/README.md)
- **ADR**: [Architecture decisions](../decisions/README.md)
- **Agent Governance Adapter ARD**: [0027-agent-governance-canonical-adapter](./0027-agent-governance-canonical-adapter.md)
- **Spec**: [Technical specifications](../../03.specs/README.md)
- **Plan**: [Execution plans](../../04.execution/plans/README.md)
- **Task**: [Execution tasks](../../04.execution/tasks/README.md)
- **Template**: [ARD template](../../99.templates/ard.template.md)
