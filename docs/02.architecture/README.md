---
status: active
---

# Architecture

## Overview

`docs/02.architecture`는 Stage 01 요구사항을 시스템 경계, 이해관계자 관심사,
뷰, 데이터·제어 흐름, 품질 시나리오와 중요한 선택으로 연결한다.
Architecture Description은 현재 구조를 설명하고 ADR은 선택, 대안, 근거,
결과와 supersession을 기록한다.

## Audience

- System Architects
- Developers
- Reviewers
- AI Agents

## Scope

이 stage는 현재 25개의 Architecture Description과 25개의 ADR을 보유한다.
구현 세부와 검증 계약은 Stage 03, 실행 상태는 현재 변경 패킷, 운영 절차는
Stage 05가 소유한다.

## Structure

```text
docs/02.architecture/
├── descriptions/
│   ├── ad-0001-gateway-architecture.md
│   ├── ...
│   └── ad-0028-operational-readiness-closure.md
├── decisions/
│   ├── adr-0001-traefik-nginx-hybrid.md
│   ├── ...
│   └── adr-0028-local-isolated-readiness-evidence.md
└── README.md
```

## Current Inventory

- [`descriptions/`](descriptions/README.md): stakeholder concerns, boundaries,
  views, flows, quality scenarios, requirement disposition와 관련 결정.
- [`decisions/`](decisions/README.md): 하나의 material choice, alternatives,
  rationale, consequences, confirmation과 supersession.

## How to Work in This Area

1. 상위 [Product Requirements](../01.requirements/README.md)를 확인한다.
2. 새 설명은
   [`architecture-description.template.md`](../99.templates/templates/sdlc/architecture-description.template.md)를 사용한다.
3. 새 결정은 [`adr.template.md`](../99.templates/templates/sdlc/adr.template.md)를 사용한다.
4. Description은 실제 상위 요구사항, ADR은 실제 Description을
   `parent_ids`로 연결한다.
5. 구현과 운영 사실은 해당 Spec과 Operations 문서에서 확인하고, 확인되지
   않은 아키텍처 사실을 만들지 않는다.

## Documentation Standards

- Description은 `ad-<4-digit-id>-<slug>.md`와
  `artifact_type: architecture-description`을 사용한다.
- ADR은 `adr-<4-digit-id>-<slug>.md`와 `artifact_type: adr`을 사용한다.
- 호환·redirect 문서나 병렬 용어 체계를 만들지 않는다.
- 날짜는 경로가 아니라 typed metadata에 둔다.

## Related Documents

- [Product Requirements](../01.requirements/README.md)
- [Architecture Descriptions](descriptions/README.md)
- [Architecture Decisions](decisions/README.md)
- [Specifications](../03.specs/README.md)
- [Operations](../05.operations/README.md)
- [Documentation Templates](../99.templates/README.md)
