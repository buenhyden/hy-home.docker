---
status: active
---
<!-- Target: docs/02.architecture/README.md -->

# Architecture

> 아키텍처 참조 모델(ARD)과 아키텍처 결정 기록(ADR)을 라우팅하는 stage 문서 공간

## Overview

`docs/02.architecture`는 `docs/01.requirements`에서 정의한 요구사항을 시스템 구조와 결정 기록으로 연결하는 stage다. 이 경로는 구현 상세가 아니라 시스템 경계, 품질 속성, 데이터 흐름, 통합 구조, 그리고 중요한 기술 선택의 이유를 관리한다.

아키텍처 참조 모델은 `requirements/`에 둔다. 선택의 배경과 대안, 결과를 남기는 결정 기록은 `decisions/`에 둔다.

## Audience

이 README의 주요 독자:

- System Architects
- Developers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 아키텍처 요구사항과 품질 속성 정의
- 시스템 경계, 데이터 흐름, 통합 구조
- 기술 선택, 대안, 결과를 남기는 ADR
- 관련 PRD, Spec, Plan, Task, Operations 문서로의 추적성

### Out of Scope

- 제품 요구사항 정의 (`docs/01.requirements` 담당)
- 상세 기술 명세와 계약 (`docs/03.specs` 담당)
- 실행 계획과 작업 증거 (`docs/04.execution` 담당)
- 운영 가이드, 정책, 반복 절차 (`docs/05.operations` 담당)
- 안정 참고 자료와 용어집 (`docs/90.references` 담당)

## Structure

```text
docs/02.architecture/
├── requirements/  # ARD: architecture reference documents and quality attributes
├── decisions/     # ADR: architecture decision records and trade-offs
└── README.md      # This file
```

## Current Inventory

- `requirements/`: 24 ARD leaf documents plus `README.md`.
- `decisions/`: 24 ADR leaf documents plus `README.md`.
- `infra_net` canonical ARD: [`requirements/0026-standardize-infra-net.md`](requirements/0026-standardize-infra-net.md).
- `infra_net` canonical ADR: [`decisions/0026-standardize-infra-net.md`](decisions/0026-standardize-infra-net.md).
- Dated `infra_net` files remain in this stage as legacy duplicate candidates until cross-stage references are remediated with separate approval.

## How to Work in This Area

1. 상위 PRD는 [`../01.requirements/`](../01.requirements/README.md)에서 확인한다.
2. ARD 라우팅은 [`requirements/README.md`](requirements/README.md), ADR 라우팅은 [`decisions/README.md`](decisions/README.md)를 따른다.
3. 새 ARD는 [`../99.templates/ard.template.md`](../99.templates/ard.template.md)에서 시작한다.
4. 새 ADR은 [`../99.templates/adr.template.md`](../99.templates/adr.template.md)에서 시작한다.
5. 링크는 템플릿 위치가 아니라 복사된 대상 문서 위치 기준으로 계산한다.
6. 구현 상세는 [`../03.specs/`](../03.specs/README.md), 운영 절차는 [`../05.operations/`](../05.operations/README.md)에 둔다.

## Architecture Contract

| Artifact | Canonical Location | Responsibility |
| --- | --- | --- |
| ARD | `requirements/` | 시스템 경계, 품질 속성, 참조 아키텍처 |
| ADR | `decisions/` | 결정, 대안, consequence, supersession |

ARD와 ADR은 서로 대체하지 않습니다. ARD가 “시스템이 어떤 구조와 품질 속성을 가져야 하는지”를 설명하고, ADR은 “왜 특정 선택을 했는지”를 기록합니다. 구현 세부와 검증 명령은 Spec과 Execution stage로 내려보냅니다.

## Documentation Standards

- 새 stage 문서는 매핑된 템플릿에서 시작한다.
- ARD와 ADR은 각각 하나의 아키텍처 관심사를 다룬다.
- canonical 아키텍처 문서를 대체하는 병렬 파일을 만들지 않는다.
- PRD, ARD, ADR, Spec, Plan, Task, Operations 산출물이 존재하면 추적성을 유지한다.

## Related Documents

- **Requirements**: [Product requirements](../01.requirements/README.md)
- **Architecture Requirements**: [ARD index](requirements/README.md)
- **Architecture Decisions**: [ADR index](decisions/README.md)
- **Specs**: [Technical specifications](../03.specs/README.md)
- **Execution**: [Execution plans and tasks](../04.execution/README.md)
- **Operations**: [Operations knowledge base](../05.operations/README.md)
- **Templates**: [Documentation templates](../99.templates/README.md)
