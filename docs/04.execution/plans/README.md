# Execution Plans

> 이 경로는 실행 계획 및 마일스톤(Work Breakdown, Risks)을 관리한다.

## Overview

`docs/04.execution/plans`는 특정 기능의 개발이나 인프라 수정 작업의 구체적인 실행 계획을 보관한다. 작업 단계(Phases), 예상 일정, 리스크 관리 및 자원 할당 등 구현에 필요한 로드맵을 정의하여 실행의 신뢰성을 확보한다.

## Audience

이 README의 주요 독자:

- Project Managers
- Developers
- System Architects
- AI Agents

## Scope

### In Scope

- 프로젝트별 상세 작업 분할 구조 (WBS)
- 마일스톤 및 주요 일정 계획 (Phases)
- 리스크 식별 및 완화 전략 (Mitigation)
- 네트워크 및 서비스 수정 실행 계획 (Plan)

### Out of Scope

- 상세 설계 명세 (Spec 담당)
- 실제 구현 작업 내역 (Task 담당)
- 중장기 전략 로드맵 (Roadmap 담당)
- 운영 정책 및 통제 (Operations 담당)

## Structure

```text
docs/04.execution/plans/
├── 2026-03-26-01-gateway-standardization.md
├── 2026-03-26-02-auth-standardization.md
├── ...
├── 2026-04-10-infra-team-agent-cross-validation.md
├── 2026-04-01-standardize-infra-net.md  # infra_net 표준화 실행 계획
├── 2026-05-09-harness-agent-first-engineering.md  # Latest: Harness / Agent-first Engineering 계획
├── 2026-05-09-infra-secrets-docs-refresh.md  # Infra, secrets, docs 운영 문서 최신화 계획
├── 2026-05-09-scripts-lifecycle-contract-cleanup.md  # scripts lifecycle contract cleanup 계획
├── 2026-05-10-llm-wiki-agent-first-completion.md  # LLM Wiki generator/index/curator completion 계획
├── 2026-05-17-scripts-ci-qa-cleanup.md  # scripts CI/CD 및 QA cleanup 계획
├── 2026-05-17-requirements-standardization.md  # docs/01.requirements PRD contract remediation 계획
└── README.md                              # This file
```

## How to Work in This Area

1. 구현 전 [plan.template.md](../../99.templates/plan.template.md)를 활용하여 작업 계획을 수립함.
2. 각 단계가 상세 명세(Spec)를 충분히 반영하고 있는지 확인함.
3. 활성 plan은 `docs/04.execution/plans/` 아래의 canonical 경로에만 둠. 비표준 `docs/*` 경로에는 active plan을 두지 않음.
4. 문서 상태(`draft`, `approved`, `completed`)를 명확히 관리함.
5. 예기치 않은 이슈 발생 시 계획을 수정하고 히스토리를 남김.

## Documentation Standards

- 가능한 경우 승인된 템플릿에서 시작한다.
- 제목과 구조는 사람과 AI Agent 모두가 해석 가능하도록 명시적으로 작성한다.
- 상위 문서와 하위 산출물 간 추적성을 유지한다.

## AI Agent Guidance

1. 이 README를 먼저 읽는다.
2. 실행 전 계획 단계에서 정의된 작업 분할(WBS)과 리스크 요인을 반드시 숙지한다.
3. 작업 수행 중 계획에서 벗어난 상황이 발생하면 계획 문서를 즉시 업데이트한다.

## Related Documents

- **Requirements**: [../../01.requirements/README.md](../../01.requirements/README.md)
- **Spec**: [../../03.specs/README.md](../../03.specs/README.md)
- **Task**: [../tasks/README.md](../tasks/README.md)
- **Architecture Decisions**: [../../02.architecture/decisions/README.md](../../02.architecture/decisions/README.md)
- **Operations**: [../../05.operations/README.md](../../05.operations/README.md)
- **Runbooks**: [../../05.operations/runbooks/README.md](../../05.operations/runbooks/README.md)
- **Harness / Agent-first Engineering Plan**: [2026-05-09-harness-agent-first-engineering.md](./2026-05-09-harness-agent-first-engineering.md)
- **Infra / Secrets / Docs Refresh Plan**: [2026-05-09-infra-secrets-docs-refresh.md](./2026-05-09-infra-secrets-docs-refresh.md)
- **Scripts Lifecycle Contract Cleanup Plan**: [2026-05-09-scripts-lifecycle-contract-cleanup.md](./2026-05-09-scripts-lifecycle-contract-cleanup.md)
- **LLM Wiki Agent-first Completion Plan**: [2026-05-10-llm-wiki-agent-first-completion.md](./2026-05-10-llm-wiki-agent-first-completion.md)
- **Scripts CI/CD & QA Cleanup Plan**: [2026-05-17-scripts-ci-qa-cleanup.md](./2026-05-17-scripts-ci-qa-cleanup.md)
- **Requirements Standardization Plan**: [2026-05-17-requirements-standardization.md](./2026-05-17-requirements-standardization.md)
