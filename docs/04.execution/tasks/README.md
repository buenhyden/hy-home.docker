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
├── 2026-04-10-infra-team-agent-cross-validation.md # Completed infra team agent cross-validation task record
├── 2026-05-09-*.md                          # Agent-first and docs refresh task records
├── 2026-05-09-scripts-lifecycle-contract-cleanup.md # Completed retrospective scripts lifecycle task record
├── 2026-05-10-*.md                          # Docs taxonomy and LLM Wiki task records
├── 2026-05-17-requirements-standardization.md # Completed requirements standardization task record
├── 2026-05-17-scripts-ci-qa-cleanup.md       # Completed scripts CI/CD and QA cleanup task record
├── 2026-05-18-execution-stage-remediation.md # Completed bounded execution-stage remediation task record
├── 2026-05-18-docs-05-operations-purpose-remediation.md # Completed operations purpose remediation task record
├── 2026-05-18-docs-bounded-consistency-audit.md # Completed bounded docs consistency audit task record
├── 2026-05-18-targeted-docs-precision-remediation.md # Completed targeted docs precision remediation task record
├── 2026-05-22-agent-hook-completion-style-automation.md # Completed agent hook completion/style automation task record
├── 2026-05-22-spec-execution-implementation-audit.md # Completed spec/plan/task implementation audit task record
├── 2026-05-22-data-analytics-execution-traceability.md # Completed data analytics traceability task record
├── 2026-05-22-lifecycle-readme-debt-closure.md # Completed lifecycle README debt closure task record
├── 2026-05-22-workspace-docs-agent-governance-remediation.md # Completed workspace docs and agent governance remediation task record
├── 2026-05-22-workspace-governance-bounded-reaudit.md # Completed workspace governance bounded re-audit task record
├── 2026-05-24-workspace-audit-improvement.md # Completed workspace audit improvement task record
├── 2026-05-24-workspace-audit-input-task-gap-closure.md # Completed workspace audit input-task gap closure task record
├── 2026-05-24-workspace-audit-grill-review.md # Completed workspace audit grill review task record
├── 2026-05-25-home-docker-workspace-audit-improvement.md # Completed home docker workspace audit improvement task record
├── 2026-05-25-home-docker-revalidation-deferred-follow-up.md # Completed home docker revalidation deferred follow-up task record
├── 2026-05-25-large-scale-authored-ssot-review.md # Completed large-scale authored SSoT review task record
├── 2026-05-31-claude-harness-governance-verification.md # Completed Claude harness governance verification task record
├── 2026-06-02-agent-governance-missing-items-implementation.md # Completed decision-item attachment-gap implementation task record
├── 2026-06-02-agent-governance-phase-1-revalidation.md # Completed agent governance Phase 1 revalidation task record
├── 2026-06-02-agent-governance-phase-2-strategy-integration.md # Completed agent governance Phase 2 strategy integration task record
├── 2026-06-02-agent-governance-phase-3-approved-surface-activation.md # Completed agent governance Phase 3 approved surface activation task record
├── 2026-06-02-agent-governance-phase-4-closure-reconciliation.md # Completed agent governance Phase 4 closure reconciliation task record
├── 2026-06-02-docs-implementation-reconciliation.md # Completed docs implementation reconciliation task record
├── 2026-06-03-governance-surgical-reverification.md # Completed governance surgical re-verification and tech-stack drift closure task record
├── 2026-06-04-docs-implementation-audit.md # Active docs 01-05 content-vs-implementation audit and continuation evidence
├── 2026-06-05-harness-engineering.md # Completed workspace harness engineering implementation task record
├── 2026-06-05-language-policy-boundary-audit.md # Active language policy boundary audit and template normalization evidence
├── 2026-06-05-language-policy-normalization-batch-1.md # Active language policy spec/reference normalization evidence
├── 2026-06-05-language-policy-normalization-batch-2.md # Active language policy spec normalization evidence
├── 2026-06-05-language-policy-normalization-batch-3.md # Active language policy remaining spec normalization evidence
├── 2026-06-05-language-policy-plan-normalization-batch-1.md # Active language policy plan normalization evidence
├── 2026-06-05-language-policy-plan-normalization-batch-2.md # Active language policy plan normalization evidence
├── 2026-06-05-language-policy-plan-normalization-batch-3.md # Active language policy plan normalization evidence
├── 2026-06-05-language-policy-plan-normalization-batch-4.md # Active language policy plan normalization evidence
├── 2026-06-05-language-policy-plan-normalization-batch-5.md # Active language policy plan normalization evidence
├── 2026-06-05-language-policy-plan-normalization-batch-6.md # Active language policy plan normalization evidence
├── 2026-06-05-language-policy-plan-normalization-batch-7.md # Active language policy plan normalization evidence
├── 2026-06-05-language-policy-plan-normalization-batch-8.md # Active language policy plan normalization evidence
├── 2026-06-05-language-policy-task-normalization-batch-1.md # Active language policy task normalization evidence
├── 2026-06-05-language-policy-task-normalization-batch-2.md # Active language policy task normalization evidence
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

| Evidence Type        | Expected Content                                      |
| -------------------- | ----------------------------------------------------- |
| Task Table           | 작업 ID, type, parent spec/plan, evidence, status     |
| Phase View           | 수행 흐름을 빠르게 확인할 수 있는 선택적 checklist    |
| Verification Summary | 실행한 명령, 결과, 수동 확인, 실패 또는 skip 사유     |
| Deviation Notes      | 계획과 달라진 점, 최종 판단 근거, follow-up 필요 여부 |

완료된 historical task는 의미 보존을 우선합니다. 다만 현재 구현과 상충하는 historical task는 active index에서 제거하고 `docs/98.archive/` tombstone ledger로 이동합니다.

## Documentation Standards

- 가능한 경우 승인된 템플릿에서 시작한다.
- 제목과 구조는 사람과 AI Agent 모두가 해석 가능하도록 명시적으로 작성한다.
- 상위 문서와 하위 산출물 간 추적성을 유지한다.
- Related Documents는 실제 Markdown 링크로 작성한다.
- Historical task evidence는 의미 보존을 우선하되, 현재 구현과 상충하면 archive tombstone으로 이동한다.

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
- **Infra Team Agent Cross-Validation Task**: [2026-04-10-infra-team-agent-cross-validation.md](./2026-04-10-infra-team-agent-cross-validation.md)
- **Requirements Standardization Task**: [2026-05-17-requirements-standardization.md](./2026-05-17-requirements-standardization.md)
- **Scripts CI/CD and QA Cleanup Task**: [2026-05-17-scripts-ci-qa-cleanup.md](./2026-05-17-scripts-ci-qa-cleanup.md)
- **Execution stage remediation task**: [2026-05-18-execution-stage-remediation.md](./2026-05-18-execution-stage-remediation.md)
- **Operations Purpose Remediation Task**: [2026-05-18-docs-05-operations-purpose-remediation.md](./2026-05-18-docs-05-operations-purpose-remediation.md)
- **Docs Bounded Consistency Audit Task**: [2026-05-18-docs-bounded-consistency-audit.md](./2026-05-18-docs-bounded-consistency-audit.md)
- **Targeted Docs Precision Remediation Task**: [2026-05-18-targeted-docs-precision-remediation.md](./2026-05-18-targeted-docs-precision-remediation.md)
- **Harness / Agent-first Engineering Task**: [2026-05-09-harness-agent-first-engineering.md](./2026-05-09-harness-agent-first-engineering.md)
- **Infra / Secrets / Docs Refresh Task**: [2026-05-09-infra-secrets-docs-refresh.md](./2026-05-09-infra-secrets-docs-refresh.md)
- **Scripts Lifecycle Contract Cleanup Task**: [2026-05-09-scripts-lifecycle-contract-cleanup.md](./2026-05-09-scripts-lifecycle-contract-cleanup.md)
- **LLM Wiki Agent-first Completion Task**: [2026-05-10-llm-wiki-agent-first-completion.md](./2026-05-10-llm-wiki-agent-first-completion.md)
- **Lifecycle README Debt Closure Task**: [2026-05-22-lifecycle-readme-debt-closure.md](./2026-05-22-lifecycle-readme-debt-closure.md)
- **Workspace Docs and Agent Governance Remediation Task**: [2026-05-22-workspace-docs-agent-governance-remediation.md](./2026-05-22-workspace-docs-agent-governance-remediation.md)
- **Workspace Governance Bounded Re-audit Task**: [2026-05-22-workspace-governance-bounded-reaudit.md](./2026-05-22-workspace-governance-bounded-reaudit.md)
- **Workspace Audit Improvement Task**: [2026-05-24-workspace-audit-improvement.md](./2026-05-24-workspace-audit-improvement.md)
- **Workspace Audit Input Task Gap Closure Task**: [2026-05-24-workspace-audit-input-task-gap-closure.md](./2026-05-24-workspace-audit-input-task-gap-closure.md)
- **Workspace Audit Grill Review Task**: [2026-05-24-workspace-audit-grill-review.md](./2026-05-24-workspace-audit-grill-review.md)
- **Home Docker Workspace Audit Improvement Task**: [2026-05-25-home-docker-workspace-audit-improvement.md](./2026-05-25-home-docker-workspace-audit-improvement.md)
- **Home Docker Revalidation Deferred Follow-up Task**: [2026-05-25-home-docker-revalidation-deferred-follow-up.md](./2026-05-25-home-docker-revalidation-deferred-follow-up.md)
- **Large-Scale Authored SSoT Review Task**: [2026-05-25-large-scale-authored-ssot-review.md](./2026-05-25-large-scale-authored-ssot-review.md)
- **Agent Hook Completion and Style Automation Task**: [2026-05-22-agent-hook-completion-style-automation.md](./2026-05-22-agent-hook-completion-style-automation.md)
- **Spec Execution Implementation Audit Task**: [2026-05-22-spec-execution-implementation-audit.md](./2026-05-22-spec-execution-implementation-audit.md)
- **Data Analytics Execution Traceability Task**: [2026-05-22-data-analytics-execution-traceability.md](./2026-05-22-data-analytics-execution-traceability.md)
- **Workspace Doc & Governance Consistency (2026-05b) Task**: [2026-05-29-workspace-consistency-2026-05b.md](./2026-05-29-workspace-consistency-2026-05b.md)
- **Claude Harness Governance Verification Task**: [2026-05-31-claude-harness-governance-verification.md](./2026-05-31-claude-harness-governance-verification.md)
- **Agent Governance Missing Items Implementation Task**: [2026-06-02-agent-governance-missing-items-implementation.md](./2026-06-02-agent-governance-missing-items-implementation.md)
- **Agent Governance Phase 1 Revalidation Task**: [2026-06-02-agent-governance-phase-1-revalidation.md](./2026-06-02-agent-governance-phase-1-revalidation.md)
- **Agent Governance Phase 2 Strategy Integration Task**: [2026-06-02-agent-governance-phase-2-strategy-integration.md](./2026-06-02-agent-governance-phase-2-strategy-integration.md)
- **Agent Governance Phase 3 Approved Surface Activation Task**: [2026-06-02-agent-governance-phase-3-approved-surface-activation.md](./2026-06-02-agent-governance-phase-3-approved-surface-activation.md)
- **Agent Governance Phase 4 Closure Reconciliation Task**: [2026-06-02-agent-governance-phase-4-closure-reconciliation.md](./2026-06-02-agent-governance-phase-4-closure-reconciliation.md)
- **Docs Implementation Reconciliation Task**: [2026-06-02-docs-implementation-reconciliation.md](./2026-06-02-docs-implementation-reconciliation.md)
- **Governance Surgical Re-Verification Task**: [2026-06-03-governance-surgical-reverification.md](./2026-06-03-governance-surgical-reverification.md)
- **Docs 01-05 Content-vs-Implementation Audit Task**: [2026-06-04-docs-implementation-audit.md](./2026-06-04-docs-implementation-audit.md) — active audit and continuation evidence
- **Workspace Harness Engineering Task**: [2026-06-05-harness-engineering.md](./2026-06-05-harness-engineering.md) — completed harness validation wrapper and contract alignment evidence
- **Language Policy Boundary Audit Task**: [2026-06-05-language-policy-boundary-audit.md](./2026-06-05-language-policy-boundary-audit.md) — active language boundary audit and template normalization evidence
- **Language Policy Normalization Batch 1 Task**: [2026-06-05-language-policy-normalization-batch-1.md](./2026-06-05-language-policy-normalization-batch-1.md) — active spec/reference language normalization evidence
- **Language Policy Normalization Batch 2 Task**: [2026-06-05-language-policy-normalization-batch-2.md](./2026-06-05-language-policy-normalization-batch-2.md) — active spec language normalization evidence
- **Language Policy Normalization Batch 3 Task**: [2026-06-05-language-policy-normalization-batch-3.md](./2026-06-05-language-policy-normalization-batch-3.md) — active remaining spec language normalization evidence
- **Language Policy Plan Normalization Batch 1 Task**: [2026-06-05-language-policy-plan-normalization-batch-1.md](./2026-06-05-language-policy-plan-normalization-batch-1.md) — active plan language normalization evidence
- **Language Policy Plan Normalization Batch 2 Task**: [2026-06-05-language-policy-plan-normalization-batch-2.md](./2026-06-05-language-policy-plan-normalization-batch-2.md) — active plan language normalization evidence
- **Language Policy Plan Normalization Batch 3 Task**: [2026-06-05-language-policy-plan-normalization-batch-3.md](./2026-06-05-language-policy-plan-normalization-batch-3.md) — active plan language normalization evidence
- **Language Policy Plan Normalization Batch 4 Task**: [2026-06-05-language-policy-plan-normalization-batch-4.md](./2026-06-05-language-policy-plan-normalization-batch-4.md) — active plan language normalization evidence
- **Language Policy Plan Normalization Batch 5 Task**: [2026-06-05-language-policy-plan-normalization-batch-5.md](./2026-06-05-language-policy-plan-normalization-batch-5.md) — active plan language normalization evidence
- **Language Policy Plan Normalization Batch 6 Task**: [2026-06-05-language-policy-plan-normalization-batch-6.md](./2026-06-05-language-policy-plan-normalization-batch-6.md) — active plan language normalization evidence
- **Language Policy Plan Normalization Batch 7 Task**: [2026-06-05-language-policy-plan-normalization-batch-7.md](./2026-06-05-language-policy-plan-normalization-batch-7.md) — active plan language normalization evidence
- **Language Policy Plan Normalization Batch 8 Task**: [2026-06-05-language-policy-plan-normalization-batch-8.md](./2026-06-05-language-policy-plan-normalization-batch-8.md) — active final plan language normalization evidence
- **Language Policy Task Normalization Batch 1 Task**: [2026-06-05-language-policy-task-normalization-batch-1.md](./2026-06-05-language-policy-task-normalization-batch-1.md) — active task language normalization evidence
- **Language Policy Task Normalization Batch 2 Task**: [2026-06-05-language-policy-task-normalization-batch-2.md](./2026-06-05-language-policy-task-normalization-batch-2.md) — active task language normalization evidence
