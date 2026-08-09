---
status: active
---

# Architecture Descriptions

## Overview

`docs/02.architecture/descriptions`는 시스템 또는 관심사별 현재 아키텍처를
설명한다. 각 문서는 이해관계자 관심사, 경계와 제약, 품질 속성과 시나리오,
viewpoints와 views, 데이터·제어 흐름, 인프라, 요구사항 disposition과 관련
ADR을 기록한다.

## Audience

- System Architects
- Developers
- Operators
- AI Agents

## Scope

이 디렉터리는 현재 25개의 Description을 보유한다. Description은 구현
계획이나 운영 절차를 소유하지 않고, 실제로 연결된 PRD, ADR, Spec과
Operations 문서의 역할을 대체하지 않는다.

## Structure

```text
docs/02.architecture/descriptions/
├── ad-0001-gateway-architecture.md
├── ad-0002-auth-architecture.md
├── ...
├── ad-0027-agent-governance-canonical-adapter.md
├── ad-0028-operational-readiness-closure.md
└── README.md
```

## Current Inventory

- `ad-0001`부터 `ad-0014`: 기본 tier와 서비스 아키텍처.
- `ad-0018`부터 `ad-0026`: hardening, HA와 network 후속 아키텍처.
- [`ad-0027-agent-governance-canonical-adapter.md`](./ad-0027-agent-governance-canonical-adapter.md):
  Stage 00 adapter architecture.
- [`ad-0028-operational-readiness-closure.md`](./ad-0028-operational-readiness-closure.md):
  local-isolated readiness evidence architecture.

## How to Work in This Area

1. 상위 [PRD](../../01.requirements/README.md)를 확인한다.
2. 같은 system, tier 또는 concern을 설명하는 문서가 있는지 확인한다.
3. 새 문서는
   [`architecture-description.template.md`](../../99.templates/templates/sdlc/architecture-description.template.md)를 사용한다.
4. 현재 구현과 저장소 사실만 설명하고 확인되지 않은 runtime 구조를 만들지
   않는다.
5. material choice는 [ADR](../decisions/README.md)에 기록한다.

## Documentation Standards

- `ad-<4-digit-id>-<slug>.md`, `artifact_id: ad-<id>`,
  `artifact_type: architecture-description`을 일치시킨다.
- `parent_ids`는 실제 상위 PRD, SRS 또는 Interface Requirement만 포함한다.
- 관련 결정과 구현 명세가 존재하면 typed link로 연결한다.
- Description은 selection rationale나 실행 절차를 복제하지 않는다.

## AI Agent Guidance

Agent는 기존 문서를 제자리에서 수정하고 대체·redirect 파일을 만들지 않는다.
secret 값, 관찰하지 않은 runtime 상태 또는 존재하지 않는 interface를
아키텍처 사실로 기록하지 않는다.

## Related Documents

- [Architecture](../README.md)
- [Product Requirements](../../01.requirements/README.md)
- [Architecture Decisions](../decisions/README.md)
- [Specifications](../../03.specs/README.md)
- [Operations](../../05.operations/README.md)
- [Architecture Description Template](../../99.templates/templates/sdlc/architecture-description.template.md)
