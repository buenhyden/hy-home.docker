# Architecture Reference Documents (ARD)

> 이 경로는 아키텍처 참조 모델 및 품질 속성 정의를 관리한다.

## Overview

`docs/02.ard`는 제품의 상위 시스템 설계, 책임 경계, 데이터 흐름, 그리고 성능/보안/안정성 등의 품질 속성을 정의하는 참조 문서를 보관한다. 시스템의 각 계층이 유기적으로 어떻게 작동하는지 설명하는 역할을 한다.

## Audience

이 README의 주요 독자:

- System Architects
- Developers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- 도메인별/시스템별 계층 구조 정의
- 품질 지표 (SLIs/SLOs) 기준 문서
- 시스템 구성 요소 간 인터페이스 및 데이터 흐름
- AI 에이전트 아키텍처 요구사항

### Out of Scope

- 기술 스펙 또는 구현 상세 (Spec 담당)
- 기술 결정 기록 (ADR 담당)
- 비즈니스 요구사항 정의서 (PRD 담당)
- 운영 세부 지침

## Structure

```text
docs/02.ard/
├── 2026-03-26-01-gateway-ard.md
├── 2026-03-26-02-auth-ard.md
├── 2026-03-26-03-security-ard.md
├── 2026-03-26-04-data-ard.md
├── 2026-03-26-05-messaging-ard.md
├── 2026-03-26-06-observability-ard.md
├── 2026-03-26-07-workflow-ard.md
├── 2026-03-26-08-ai-ard.md
├── 2026-03-26-09-tooling-ard.md
├── 2026-03-26-10-communication-ard.md
├── 2026-03-26-11-laboratory-ard.md
├── 2026-04-01-standardize-infra-net.md  # Latest: infra_net 표준 아키텍처
└── README.md                               # This file
```

## How to Work in This Area

1. 신규 시스템 아키텍처 설계 시 [ard.template.md](../99.templates/ard.template.md)를 활용함.
2. PRD에서 정의된 요구사항이 충분히 반영되었는지 확인함.
3. 문서 상태(`refining`, `stable`, `refactored`)를 명확히 관리함.
4. 주요 구조적 변경 시 관련 `ADR` 또는 `Spec` 문서와 함께 갱신함.

## Documentation Standards

- 가능한 경우 승인된 템플릿에서 시작한다.
- 제목과 구조는 사람과 AI Agent 모두가 해석 가능하도록 명시적으로 작성한다.
- 상위 문서와 하위 산출물 간 추적성을 유지한다.

## AI Agent Guidance

1. 이 README를 먼저 읽는다.
2. 기존 아키텍처 참조 모델을 확인하여 구조적 일치성을 유지한다.
3. 아키텍처 변경 시 연관된 `ADR` 문서가 작성되었는지 확인한다.

## Related References

- **PRD**: [../01.prd/README.md]
- **ADR**: [../03.adr/README.md]
- **Spec**: [../04.specs/README.md]
