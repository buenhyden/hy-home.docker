# Product Requirements Documents (PRD)

> 이 경로는 제품 요구사항 정의(Vision, Use Case, Requirements)를 관리한다.

## Overview

`docs/01.prd`는 시스템이나 기능의 "Why"와 "What"을 정의하는 문서가 보관되는 장소다. 비즈니스 가치, 사용자 시나리오, 기능적/비기능적 요구사항을 기술하며 모든 설계와 구현의 출발점이 된다.

## Audience

이 README의 주요 독자:

- Developers
- Product Owners
- System Architects
- AI Agents

## Scope

### In Scope

- 제품 비전 및 목표 정의서
- 사용자 스토리 및 유즈케이스 명세
- 기능적 / 비기능적 요구사항 정의 (PRD)
- 핵심 성공 지표 (KPI/Metrics)

### Out of Scope

- 상세 기술 설계 (Spec 담당)
- 아키렉처 참조 모델 (ARD 담당)
- 상세 구현 코드
- 운영 및 유지보수 절차

## Structure

```text
docs/01.prd/
├── 2026-03-26-01-gateway-prd.md
├── 2026-03-26-02-auth-prd.md
├── 2026-03-26-03-security-prd.md
├── 2026-03-26-04-data-prd.md
├── 2026-03-26-05-messaging-prd.md
├── 2026-03-26-06-observability-prd.md
├── 2026-03-26-07-workflow-prd.md
├── 2026-03-26-08-ai-prd.md
├── 2026-03-26-09-tooling-prd.md
├── 2026-03-26-10-communication-prd.md
├── 2026-03-26-11-laboratory-prd.md
├── 2026-04-01-standardize-infra-net.md  # Latest: infra_net 표준화 요구사항
└── README.md                               # This file
```

## How to Work in This Area

1. 새 기능 제안 시 [prd.template.md](../99.templates/prd.template.md)를 사용하여 문서를 생성함.
2. 상위 비전이나 비즈니스 목표와 일치하는지 검토함.
3. 문서 상태(`draft`, `approved`, `deprecated`)를 명확히 관리함.
4. 승인 후에는 관련 `ARD`, `Spec`, `Plan` 문서를 생성하여 추적성을 유지함.

## Documentation Standards

- 가능한 경우 승인된 템플릿에서 시작한다.
- 제목과 구조는 사람과 AI Agent 모두가 해석 가능하도록 명시적으로 작성한다.
- 상위 문서와 하위 산출물 간 추적성을 유지한다.

## AI Agent Guidance

1. 이 README를 먼저 읽는다.
2. 기존 PRD 문서를 확인하여 중복 기능 정의를 피한다.
3. 요구사항 변경 시 연관된 `Spec`과 `Plan` 문서도 함께 검토하여 불일치를 방지한다.

## Related References

- **ARD**: [../02.ard/README.md]
- **Spec**: [../04.specs/README.md]
- **Plan**: [../05.plans/README.md]
