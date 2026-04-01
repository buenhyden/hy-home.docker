# Component Specifications (Specs)

> 이 경로는 컴포넌트/기능별 상세 설계 명세(Data, API, Logic, Agent-Design)를 관리한다.

## Overview

`docs/04.specs`는 시스템의 세부 구현을 위한 구체적인 명세를 보관한다. 아키텍처(ARD)와 결정(ADR)을 바탕으로 실제 데이터 스키마, API 인터페이스, 비즈니스 로직 및 에이전트 설계 방식을 상세히 기술한다.

## Audience

이 README의 주요 독자:

- Developers
- System Architects
- AI Agents
- QA Engineers

## Scope

### In Scope

- 데이터 모델링 및 DB 스키마 정의
- API 엔드포인트 및 요청/응답 형식 명세
- 주요 비즈니스 로직 순서도 및 알고리즘
- 에이전트 도구(Tool) 및 페르소나 설계
- 네트워크 인프라 상세 요구사항 (Spec)

### Out of Scope

- 상위 요구사항 (PRD 담당)
- 상위 아키텍처 비전 (ARD 담당)
- 실행 계획 (Plan 담당)
- 실제 소스 코드 구현

## Structure

```text
docs/04.specs/
├── 01-gateway-specs.md
├── 02-auth-specs.md
├── 03-security-specs.md
├── 04-data-specs.md
├── 05-messaging-specs.md
├── 06-observability-specs.md
├── 07-workflow-specs.md
├── 08-ai-specs.md
├── 09-tooling-specs.md
├── 10-communication-specs.md
├── 11-laboratory-specs.md
├── standardize-infra-net/
│   └── spec.md              # Latest: infra_net 상세 설계 명세
└── README.md                # This file
```

## How to Work in This Area

1. 기능 구현 전 [spec.template.md](../99.templates/spec.template.md)를 활용하여 명세서를 작성함.
2. 데이터 모델이나 API 변경 시 영향도를 미리 분석하여 명시함.
3. 문서 상태(`refining`, `finalized`, `deprecated`)를 명확히 함.
4. 구현 완료 후 변경된 사항이 있다면 실제 코드와 일치하도록 갱신함.

## Documentation Standards

- 가능한 경우 승인된 템플릿에서 시작한다.
- 제목과 구조는 사람과 AI Agent 모두가 해석 가능하도록 명시적으로 작성한다.
- 상위 문서와 하위 산출물 간 추적성을 유지한다.

## AI Agent Guidance

1. 이 README를 먼저 읽는다.
2. 코드 변경 전 이 영역의 스펙 문서를 우선 참조하여 설계 의도를 파악한다.
3. 스펙과 실제 구현 사이의 불일치를 발견하면 즉시 보고하거나 문서를 수정한다.

## Related References

- **PRD**: [../01.prd/README.md]
- **ARD**: [../02.ard/README.md]
- **ADR**: [../03.adr/README.md]
- **Plan**: [../05.plans/README.md]
