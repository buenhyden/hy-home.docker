<!-- Target: docs/04.execution/tasks/README.md -->
# Execution Tasks

> 실제 구현 상태, 검증 결과, 완료 evidence를 기록하는 execution tracking 공간

## Overview

`docs/04.execution/tasks`는 실행 계획에 따라 수행된 작업 단위와 검증 evidence를 기록합니다.

Task 문서는 plan을 다시 설명하는 문서가 아닙니다. 어떤 작업이 실제로 수행되었고, 어떤 검증 명령이나 review evidence로 완료를 판단했는지 남기는 audit trail입니다.

## Audience

이 README의 주요 독자:

- Developers
- QA Engineers
- Product Managers
- AI Agents

## Scope

### In Scope

- task table and status tracking
- implementation and validation evidence
- issue/deviation notes discovered during execution
- test, eval, and documentation verification summary
- links to parent spec and parent plan

### Out of Scope

- 상위 아키텍처 비전 (`docs/02.architecture/` 담당)
- 실행 순서와 리스크 계획 (`docs/04.execution/plans/` 담당)
- 기술 스펙 또는 상세 명세 (`docs/03.specs/` 담당)
- 운영 절차와 정책 (`docs/05.operations/` 담당)
- 중장기 roadmap 또는 reference analysis (`docs/90.references/` 담당)

## Structure

```text
docs/04.execution/tasks/
├── 2026-03-26-*-tasks.md                    # Historical tier standardization task records
├── 2026-03-28-*-optimization-hardening-*.md # Historical hardening task records
├── 2026-05-09-*.md                          # Agent-first and docs refresh task records
├── 2026-05-10-*.md                          # Docs taxonomy and LLM Wiki task records
├── 2026-05-18-execution-stage-remediation.md # Completed bounded execution-stage remediation task record
├── 2026-05-18-docs-05-operations-purpose-remediation.md # Completed operations purpose remediation task record
├── 2026-05-18-docs-bounded-consistency-audit.md # Completed bounded docs consistency audit task record
├── 2026-05-18-targeted-docs-precision-remediation.md # Completed targeted docs precision remediation task record
├── 2026-05-22-lifecycle-readme-debt-closure.md # Completed lifecycle README debt closure task record
├── 2026-05-22-workspace-docs-agent-governance-remediation.md # Completed workspace docs and agent governance remediation task record
├── 2026-05-22-workspace-governance-bounded-reaudit.md # Completed workspace governance bounded re-audit task record
└── README.md                                # This file
```

## How to Work in This Area

1. 새 task 문서는 [task template](../../99.templates/task.template.md)을 복사해 작성합니다.
2. Related Documents 링크는 `docs/04.execution/tasks/<file>.md` 위치 기준으로 계산합니다.
3. 각 세부 task의 `Status`와 `Validation / Evidence`를 실제 진행에 맞게 갱신합니다.
4. 문서-only 작업도 검증 evidence를 남깁니다.
5. 작업 완료 후에는 최종 검증 명령과 결과를 `Verification Summary`에 남깁니다.

## Task Contract

Task 문서는 audit trail입니다. plan의 의도를 반복하기보다 수행 결과를 검증 가능하게 남깁니다.

| Evidence Type | Expected Content |
| --- | --- |
| Task Table | 작업 ID, type, parent spec/plan, evidence, status |
| Phase View | 수행 흐름을 빠르게 확인할 수 있는 선택적 checklist |
| Verification Summary | 실행한 명령, 결과, 수동 확인, 실패 또는 skip 사유 |
| Deviation Notes | 계획과 달라진 점, 최종 판단 근거, follow-up 필요 여부 |

완료된 historical task는 의미 보존을 우선합니다. 새 task 또는 현재 task를 갱신할 때만 최신 template 구조를 적용합니다.

## Documentation Standards

- 가능한 경우 승인된 템플릿에서 시작한다.
- 제목과 구조는 사람과 AI Agent 모두가 해석 가능하도록 명시적으로 작성한다.
- 상위 문서와 하위 산출물 간 추적성을 유지한다.
- Related Documents는 실제 Markdown 링크로 작성한다.
- Historical task evidence는 의미 보존을 우선한다.

## AI Agent Guidance

1. 이 README를 먼저 읽는다.
2. 실행 시 각 작업 단위의 의존성과 성공 기준을 명확히 이해하고 수행한다.
3. 수행된 모든 작업에 대해 가능한 경우 증거를 남긴다. raw logs, secret 값, shell history는 저장하지 않는다.
4. 계획과 다르게 실행된 경우 task document에 deviation과 최종 판단 근거를 기록한다.

## Related Documents

- **Plan**: [../plans/README.md](../plans/README.md)
- **Spec**: [../../03.specs/README.md](../../03.specs/README.md)
- **Operations**: [../../05.operations/README.md](../../05.operations/README.md)
- **Runbook**: [../../05.operations/runbooks/README.md](../../05.operations/runbooks/README.md)
- **Postmortem**: [../../05.operations/incidents/README.md](../../05.operations/incidents/README.md)
- **Execution stage remediation task**: [2026-05-18-execution-stage-remediation.md](./2026-05-18-execution-stage-remediation.md)
- **Operations Purpose Remediation Task**: [2026-05-18-docs-05-operations-purpose-remediation.md](./2026-05-18-docs-05-operations-purpose-remediation.md)
- **Docs Bounded Consistency Audit Task**: [2026-05-18-docs-bounded-consistency-audit.md](./2026-05-18-docs-bounded-consistency-audit.md)
- **Targeted Docs Precision Remediation Task**: [2026-05-18-targeted-docs-precision-remediation.md](./2026-05-18-targeted-docs-precision-remediation.md)
- **Harness / Agent-first Engineering Task**: [2026-05-09-harness-agent-first-engineering.md](./2026-05-09-harness-agent-first-engineering.md)
- **Infra / Secrets / Docs Refresh Task**: [2026-05-09-infra-secrets-docs-refresh.md](./2026-05-09-infra-secrets-docs-refresh.md)
- **LLM Wiki Agent-first Completion Task**: [2026-05-10-llm-wiki-agent-first-completion.md](./2026-05-10-llm-wiki-agent-first-completion.md)
- **Lifecycle README Debt Closure Task**: [2026-05-22-lifecycle-readme-debt-closure.md](./2026-05-22-lifecycle-readme-debt-closure.md)
- **Workspace Docs and Agent Governance Remediation Task**: [2026-05-22-workspace-docs-agent-governance-remediation.md](./2026-05-22-workspace-docs-agent-governance-remediation.md)
- **Workspace Governance Bounded Re-audit Task**: [2026-05-22-workspace-governance-bounded-reaudit.md](./2026-05-22-workspace-governance-bounded-reaudit.md)
