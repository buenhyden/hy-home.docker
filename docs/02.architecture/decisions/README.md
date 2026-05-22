---
status: active
---
<!-- Target: docs/02.architecture/decisions/README.md -->

# Architecture Decision Records (ADR)

> 중요한 아키텍처 선택의 배경, 대안, 결과를 남기는 ADR 문서 공간

## Overview

`docs/02.architecture/decisions`는 프로젝트 전반의 아키텍처 및 기술 스택 선택을 기록한다. ADR은 선택 자체만이 아니라 왜 그 선택을 했는지, 어떤 대안을 버렸는지, 그 결과로 어떤 trade-off가 생겼는지를 보존한다.

ADR은 구현 명세가 아니다. 결정이 내려진 뒤의 상세 인터페이스, 설정, 검증 기준은 후속 Spec, Plan, Task, Operations 문서에서 관리한다.

## Audience

이 README의 주요 독자:

- System Architects
- Developers
- Reviewers
- AI Agents

## Scope

### In Scope

- 주요 프레임워크, 플랫폼, 런타임 서비스 선정 결정
- 시스템 통신 프로토콜과 경계 결정
- 데이터베이스, 메시징, 관측성, 워크플로, AI, tooling 계층의 기술 선택
- 네트워크 표준화 정책 결정
- 관련 PRD, ARD, Spec, Plan 문서로의 추적성

### Out of Scope

- 아키텍처 참조 모델과 품질 속성 정의 (`docs/02.architecture/requirements` 담당)
- 상세 기술 명세와 구현 계약 (`docs/03.specs` 담당)
- 단순 코드 변경 로그
- 일반 사용 가이드나 운영 절차
- 일시적인 트러블슈팅 기록

## Structure

```text
docs/02.architecture/decisions/
├── 0001-traefik-nginx-hybrid.md
├── 0002-keycloak-oauth2-proxy-choice.md
├── ...
├── 0026-standardize-infra-net.md        # Canonical infra_net ADR
└── README.md                            # This file
```

## Current Inventory

- 23 ADR leaf documents are present.
- `0001` through `0011` cover base service and tier selection decisions.
- `0015` through `0026` cover analytics, hardening/HA, and network decisions.
- [`0026-standardize-infra-net.md`](./0026-standardize-infra-net.md) is the canonical `infra_net` ADR for this stage.

## How to Work in This Area

1. 결정을 제안하기 전에 상위 PRD와 관련 ARD를 먼저 읽는다.
2. 새 ADR을 추가하기 전에 기존 ADR을 확인한다.
3. 새 ADR은 [`../../99.templates/adr.template.md`](../../99.templates/adr.template.md)에서 시작한다.
4. 모든 링크는 이 폴더 아래의 대상 ADR 위치 기준으로 다시 계산한다.
5. 하나의 ADR은 하나의 결정을 다룬다.
6. accepted decision은 관련 ARD와 Spec에 반영한다.

## Documentation Standards

- ADR은 implementation step이 아니라 decision을 기록한다.
- 각 ADR은 context, decision, non-goals, consequences, alternatives, related documents를 포함한다.
- 번호가 부여된 canonical ADR이 있으면 같은 목적의 dated duplicate를 만들지 않는다.
- accepted ADR과 충돌하는 새 결정은 새 ADR 또는 명시적인 supersession 경로가 필요하다.

## AI Agent Guidance

1. ADR을 수정하기 전에 이 README를 먼저 읽는다.
2. 대체 파일을 추가하지 말고 canonical ADR을 in-place로 수정한다.
3. `infra_net` decision reference는 [`0026-standardize-infra-net.md`](./0026-standardize-infra-net.md)를 canonical로 본다.
4. secret 값을 문서화하지 않고, untracked local state에서 runtime truth를 추론하지 않는다.

## Related Documents

- **Architecture Stage**: [Architecture index](../README.md)
- **PRD**: [Product requirements](../../01.requirements/README.md)
- **ARD**: [Architecture reference documents](../requirements/README.md)
- **Spec**: [Technical specifications](../../03.specs/README.md)
- **Plan**: [Execution plans](../../04.execution/plans/README.md)
- **Template**: [ADR template](../../99.templates/adr.template.md)
