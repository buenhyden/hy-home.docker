# 01. PRD (Product Requirements)

> 제품의 목표, 사용자 가치, 그리고 성공 기준을 정의한 문서 저장소

## Overview

`docs/01.prd/` 경로는 `hy-home.docker` 프로젝트의 모든 기능 및 시스템에 대한 제품 요구사항 문서(PRD)를 관리한다. PRD는 모든 개발 작업의 출발점(SSoT)이며, '무엇을(What)' 개발하고 '왜(Why)' 필요한지에 집중하여 정의한다. 구체적인 구현 방법이나 기술 스택보다는 사용자 가치와 비즈니스 요구사항을 우선적으로 다룬다.

## Audience

이 README의 주요 독자:

- Product Managers / Planners
- Software Architects
- Developers
- AI Agents (Context for 'What' and 'Why')

## Scope

### In Scope

- 시스템 및 기능별 제품 요구사항 정의서 (`YYYY-MM-DD-<name>.md`)
- 사용자 페르소나 및 유즈케이스 정의
- 기능적/비기능적 요구사항 및 성공 지표(KPI)
- 에이전트 동작 요구사항 (Agentic features)

### Out of Scope

- 상세 아키텍처 설계 (-> `02.ard/`)
- 기술적 의사결정 기록 (-> `03.adr/`)
- 상세 기술 명세 및 API 설계 (-> `04.specs/`)
- 구현 및 검증 계획 (-> `05.plans/`, `06.tasks/`)

## Structure

```text
01.prd/
├── 2026-03-26-01-gateway.md    # Gateway Tier 요구사항
├── 2026-03-26-02-auth.md       # Auth Tier 요구사항
├── 2026-03-26-03-security.md   # Security Tier 요구사항
├── 2026-03-26-04-data.md       # Data Tier 요구사항
├── 2026-03-26-04-data-analytics.md # Analytics Tier 요구사항
├── 2026-03-26-05-messaging.md  # Messaging Tier 요구사항
├── 2026-03-26-06-observability.md # Observability Tier 요구사항
├── 2026-03-26-07-workflow.md    # Workflow Tier 요구사항
├── 2026-03-26-08-ai.md            # AI Tier 제품 요구사항
├── 2026-03-26-09-tooling.md       # Tooling Tier 제품 요구사항
├── 2026-03-26-10-communication.md  # Communication Tier 제품 요구사항
├── 2026-03-26-11-laboratory.md     # Laboratory Tier 제품 요구사항
└── README.md                       # This file
```

## How to Work in This Area

1. 새 기능을 기획하거나 시스템 요구사항을 정의할 때 `docs/99.templates/prd.template.md`를 복사하여 시작한다.
2. 파일명은 `YYYY-MM-DD-<feature-name>.md` 형식을 준수한다.
3. 요구사항 ID(`REQ-PRD-FUN-XX`)를 명확히 부여하여 하위 문서(Spec, Task)에서 추적 가능하게 한다.
4. 작성이 완료되면 관련 `02.ard/`, `04.specs/` 문서와 상호 참조 링크를 갱신한다.

## Documentation Standards

- 정확히 하나의 의미 있는 H1 제목을 사용한다.
- 모든 링크는 상대 경로를 사용한다.
- 구현 세부 사항(Implementation details)은 포함하지 않는다.
- 상단에 `Overview (KR)` 요약을 반드시 포함한다.

## Related References

- [02.ard (Architecture)](../02.ard/README.md)
- [03.adr (Decisions)](../03.adr/README.md)
- [04.specs (Specifications)](../04.specs/README.md)
- [99.templates (Templates)](../99.templates/README.md)

---
*Maintained by Product & Planning Team*
