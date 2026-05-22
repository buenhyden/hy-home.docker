<!-- Target: docs/04.execution/plans/README.md -->
# Execution Plans

> 실행 순서, 리스크, 검증 기준, 완료 조건을 관리하는 implementation plan 공간

## Overview

`docs/04.execution/plans`는 승인된 PRD, ARD, ADR, Spec을 실제 작업 순서로 바꾸는 실행 계획 stage입니다.

Plan 문서는 구현자가 무엇을 어떤 순서로 바꾸고, 어떤 리스크를 통제하며, 어떤 검증 명령으로 완료를 판단할지 설명합니다. 실행 evidence 자체는 sibling stage인 `../tasks/`에 기록합니다.

## Audience

이 README의 주요 독자:

- Project Managers
- Developers
- System Architects
- AI Agents

## Scope

### In Scope

- implementation work breakdown
- execution sequencing, milestones, dependency notes
- risk, mitigation, rollback, approval gate
- validation commands and pass criteria
- downstream task document links

### Out of Scope

- 상세 설계 명세 (`docs/03.specs/` 담당)
- 실제 구현 작업 내역과 검증 evidence (`docs/04.execution/tasks/` 담당)
- 중장기 전략, migration analysis, evergreen reference (`docs/90.references/` 또는 architecture stage 담당)
- 운영 정책, guide, runbook (`docs/05.operations/` 담당)

## Structure

```text
docs/04.execution/plans/
├── 2026-03-26-*.md                         # Historical tier standardization plans
├── 2026-03-28-*-optimization-hardening-*.md # Historical hardening plans
├── 2026-05-09-*.md                         # Agent-first and scripts lifecycle plans
├── 2026-05-10-*.md                         # Docs taxonomy and LLM Wiki plans
├── 2026-05-17-*.md                         # Recent docs/scripts remediation plans
├── 2026-05-18-execution-stage-remediation.md # Completed bounded execution-stage remediation
├── 2026-05-18-docs-05-operations-purpose-remediation.md # Completed operations purpose remediation
├── 2026-05-18-docs-bounded-consistency-audit.md # Completed bounded docs consistency audit
├── 2026-05-18-targeted-docs-precision-remediation.md # Completed targeted docs precision remediation
├── 2026-05-22-workspace-docs-agent-governance-remediation.md # Active workspace docs and agent governance remediation
└── README.md                               # This file
```

## How to Work in This Area

1. 새 plan은 [plan template](../../99.templates/plan.template.md)을 복사해 작성합니다.
2. Related Documents 링크는 `docs/04.execution/plans/<file>.md` 위치 기준으로 계산합니다.
3. 활성 plan은 이 폴더 아래 canonical 경로에만 둡니다. 비표준 `docs/*` 경로에는 active plan을 만들지 않습니다.
4. 계획에는 work breakdown, verification plan, risks, completion criteria가 있어야 합니다.
5. 예기치 않은 이슈가 발생하면 plan을 갱신하거나, historical evidence를 바꾸기 어렵다면 governance memory note로 남깁니다.

## Plan Contract

Plan은 implementation task list가 아니라 실행 설계입니다. 다음 질문에 답해야 합니다.

| Question | Plan Section |
| --- | --- |
| 왜 지금 이 작업을 하는가 | `## Context` |
| 범위와 비범위는 무엇인가 | `## Goals & In-Scope`, `## Non-Goals & Out-of-Scope` |
| 어떤 순서로 진행하는가 | `## Work Breakdown` |
| 실패 가능성과 완화책은 무엇인가 | `## Risks & Mitigations` |
| 완료를 무엇으로 증명하는가 | `## Verification Plan`, `## Completion Criteria` |

실제 수행 결과는 sibling [tasks README](../tasks/README.md)에 따라 task 문서로 기록합니다.

## Documentation Standards

- 가능한 경우 승인된 템플릿에서 시작한다.
- 제목과 구조는 사람과 AI Agent 모두가 해석 가능하도록 명시적으로 작성한다.
- 상위 문서와 하위 산출물 간 추적성을 유지한다.
- Related Documents는 실제 Markdown 링크로 작성한다.
- 오래된 plan의 historical evidence는 의미 보존을 우선한다.

## AI Agent Guidance

1. 이 README를 먼저 읽는다.
2. 실행 전 계획 단계에서 정의된 작업 분할(WBS)과 리스크 요인을 반드시 숙지한다.
3. 작업 수행 중 계획에서 벗어난 상황이 발생하면 계획 문서를 갱신하거나 task evidence에 deviation을 기록한다.
4. 오래된 plan이 현재 template과 맞지 않아도 즉시 대량 재작성하지 않는다. 범위가 승인된 경우에만 수정한다.

## Related Documents

- **Requirements**: [../../01.requirements/README.md](../../01.requirements/README.md)
- **Spec**: [../../03.specs/README.md](../../03.specs/README.md)
- **Task**: [../tasks/README.md](../tasks/README.md)
- **Architecture Decisions**: [../../02.architecture/decisions/README.md](../../02.architecture/decisions/README.md)
- **Operations**: [../../05.operations/README.md](../../05.operations/README.md)
- **Runbooks**: [../../05.operations/runbooks/README.md](../../05.operations/runbooks/README.md)
- **Execution stage remediation plan**: [2026-05-18-execution-stage-remediation.md](./2026-05-18-execution-stage-remediation.md)
- **Operations Purpose Remediation Plan**: [2026-05-18-docs-05-operations-purpose-remediation.md](./2026-05-18-docs-05-operations-purpose-remediation.md)
- **Docs Bounded Consistency Audit Plan**: [2026-05-18-docs-bounded-consistency-audit.md](./2026-05-18-docs-bounded-consistency-audit.md)
- **Targeted Docs Precision Remediation Plan**: [2026-05-18-targeted-docs-precision-remediation.md](./2026-05-18-targeted-docs-precision-remediation.md)
- **Harness / Agent-first Engineering Plan**: [2026-05-09-harness-agent-first-engineering.md](./2026-05-09-harness-agent-first-engineering.md)
- **Infra / Secrets / Docs Refresh Plan**: [2026-05-09-infra-secrets-docs-refresh.md](./2026-05-09-infra-secrets-docs-refresh.md)
- **Scripts Lifecycle Contract Cleanup Plan**: [2026-05-09-scripts-lifecycle-contract-cleanup.md](./2026-05-09-scripts-lifecycle-contract-cleanup.md)
- **LLM Wiki Agent-first Completion Plan**: [2026-05-10-llm-wiki-agent-first-completion.md](./2026-05-10-llm-wiki-agent-first-completion.md)
- **Scripts CI/CD & QA Cleanup Plan**: [2026-05-17-scripts-ci-qa-cleanup.md](./2026-05-17-scripts-ci-qa-cleanup.md)
- **Requirements Standardization Plan**: [2026-05-17-requirements-standardization.md](./2026-05-17-requirements-standardization.md)
- **Workspace Docs and Agent Governance Remediation Plan**: [2026-05-22-workspace-docs-agent-governance-remediation.md](./2026-05-22-workspace-docs-agent-governance-remediation.md)
