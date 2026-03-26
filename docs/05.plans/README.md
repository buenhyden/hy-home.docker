# 05. plans

> 프로젝트의 실행 계획(Implementation Plan)과 마일스톤을 관리하는 저장소

## Overview

`docs/05.plans/` 경로는 `hy-home.docker` 에코시스템의 모든 작업 단위에 대한 구체적인 실행 계획서들을 관리한다. 각 계획서는 특정 기능의 구현이나 시스템 변경이 어떤 순서로 진행되는지, 발생 가능한 위험은 무엇인지, 그리고 완료를 어떻게 검증할 것인지를 상세히 기술하여 작업의 가시성과 안정성을 확보한다.

## Audience

이 README의 주요 독자:

- Project Managers / Leads
- Developers (Execution reference)
- QA Engineers (Verification criteria)
- AI Agents (Step-by-step task orchestration)

## Scope

### In Scope

- 기능/시스템별 실행 계획서 (`YYYY-MM-DD-<name>.md`)
- 작업 분해 구조 (Work Breakdown Structure, WBS)
- 검증 계획 (Verification Plan) 및 마일스톤
- 위험 요소 및 완화 전략 (Risks & Mitigations)

### Out of Scope

- 상위 요구사항 정의 (-> `01.prd/`)
- 아키텍처 참조 모델 (-> `02.ard/`)
- 실제 구현 완료 증적 기록 (-> `06.tasks/`)
- 운영 중 발생한 사건 기록 (-> `10.incidents/`)

## Structure

```text
05.plans/
├── 2026-03-26-01-gateway-standardization.md    # Gateway 문서 표준화 계획
├── 2026-03-26-02-auth-standardization.md       # Auth 문서 표준화 계획
├── 2026-03-26-03-security-standardization.md   # Security 문서 표준화 계획
├── 2026-03-26-04-data-standardization.md       # Data 문서 표준화 계획
├── 2026-03-26-05-messaging-standardization.md  # Messaging 문서 표준화 계획
├── 2026-03-26-06-observability-standardization.md # Observability 문서 표준화 계획
├── 2026-03-26-08-ai-standardization.md      # AI Tier 표준화 계획
├── 2026-03-26-09-tooling-standardization.md # Tooling Tier 표준화 계획
├── 2026-03-26-10-communication-standardization.md # Communication 문서 표준화 계획
└── README.md                                 # This file
```

## How to Work in This Area

1. 새로운 작업을 시작하거나 대규모 변경을 계획할 때 `docs/99.templates/plan.template.md`를 복사하여 작성한다.
2. 파일명은 `YYYY-MM-DD-<feature-name>.md` 형식을 준수한다.
3. 모든 계획서에는 명확한 **검증 기준(Verification Criteria)**이 포함되어야 한다.
4. 작업 진행 상황에 따라 계획서의 완료 기준(Completion Criteria) 항목을 체크하여 상태를 표시한다.

## Documentation Standards

- 모든 활성 계획(Active Plan)은 명시적인 검증 명령어나 방법을 포함해야 한다.
- 실행 순서, 위험 제어, 롤아웃 전략이 상세히 기술되어야 한다.
- 상위 PRD/ARD/Spec 문서와의 연결 고리를 명확히 한다.

## Related References

- [01.prd (Requirements)](../01.prd/README.md)
- [04.specs (Specifications)](../04.specs/README.md)
- [06.tasks (Tasks)](../06.tasks/README.md)
- [99.templates (Templates)](../99.templates/README.md)

---
*Maintained by Project Management Team*
