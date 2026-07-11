---
status: active
---

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
├── 2026-03-27-infra-service-optimization-priority-plan.md # Active umbrella infra optimization priority and quarterly roadmap plan
├── 2026-03-28-*-optimization-hardening-*.md # Historical hardening plans
├── 2026-04-10-infra-team-agent-cross-validation.md # Completed infra team agent cross-validation plan
├── 2026-05-09-*.md                         # Agent-first and scripts lifecycle plans
├── 2026-05-10-*.md                         # Docs taxonomy and LLM Wiki plans
├── 2026-05-17-*.md                         # Completed docs/scripts remediation plans
├── 2026-05-18-execution-stage-remediation.md # Completed bounded execution-stage remediation
├── 2026-05-18-docs-05-operations-purpose-remediation.md # Completed operations purpose remediation
├── 2026-05-18-docs-bounded-consistency-audit.md # Completed bounded docs consistency audit
├── 2026-05-18-targeted-docs-precision-remediation.md # Completed targeted docs precision remediation
├── 2026-05-22-agent-hook-completion-style-automation.md # Completed agent hook completion/style automation
├── 2026-05-22-spec-execution-implementation-audit.md # Completed spec/plan/task implementation audit
├── 2026-05-22-data-analytics-execution-traceability.md # Completed data analytics traceability closure
├── 2026-05-22-lifecycle-readme-debt-closure.md # Completed lifecycle README debt closure
├── 2026-05-22-workspace-docs-agent-governance-remediation.md # Completed workspace docs and agent governance remediation
├── 2026-05-22-workspace-governance-bounded-reaudit.md # Completed workspace governance bounded re-audit
├── 2026-05-24-workspace-audit-improvement.md # Completed workspace audit improvement plan
├── 2026-05-24-workspace-audit-input-task-gap-closure.md # Completed workspace audit input-task gap closure plan
├── 2026-05-24-workspace-audit-grill-review.md # Completed workspace audit grill review plan
├── 2026-05-25-home-docker-workspace-audit-improvement.md # Completed home docker workspace audit improvement plan
├── 2026-05-25-home-docker-revalidation-deferred-follow-up.md # Completed home docker revalidation deferred follow-up plan
├── 2026-05-25-large-scale-authored-ssot-review.md # Completed large-scale authored SSoT review plan
├── 2026-05-31-claude-harness-governance-verification.md # Completed Claude harness governance verification plan
├── 2026-06-02-agent-governance-decision-items-plan.md # Completed agent governance decision-item and attachment-gap continuation plan
├── 2026-06-02-agent-governance-phase-1-revalidation.md # Completed agent governance Phase 1 revalidation plan
├── 2026-06-02-agent-governance-phase-2-strategy-integration.md # Completed agent governance Phase 2 strategy integration plan
├── 2026-06-02-agent-governance-phase-3-approved-surface-activation.md # Completed agent governance Phase 3 approved surface activation plan
├── 2026-06-02-agent-governance-phase-4-closure-reconciliation.md # Completed agent governance Phase 4 closure reconciliation plan
├── 2026-06-02-docs-implementation-reconciliation.md # Completed docs implementation reconciliation plan
├── 2026-06-03-governance-surgical-reverification.md # Completed governance surgical re-verification and tech-stack drift closure plan
├── 2026-07-03-document-contract-remediation-batches.md # Completed document contract remediation batch plan
├── 2026-07-03-workspace-document-contract-audit-pack.md # Completed workspace document contract audit pack plan
├── 2026-07-03-template-system-contract-standardization.md # Completed Stage 99 template contract/frontmatter standardization plan
├── 2026-07-02-template-system-reorganization.md # Completed Stage 99 template system reorganization plan
├── 2026-07-04-document-restructure-audit-contract-archive.md # Completed second-wave document restructure plan
├── 2026-07-05-agentic-engineering-implementation-audit-pack.md # Completed Stage 90 agentic engineering implementation audit pack plan
├── 2026-07-05-agentic-research-pack-refresh.md # Completed Stage 90 agentic research pack refresh plan
├── 2026-07-05-provider-workspace-artifact-path-parity.md # Completed provider `_workspace/repo-support` parity plan
├── 2026-07-05-provider-semantic-parity-validator.md # Completed provider semantic parity validator plan
├── 2026-07-05-compose-profile-service-coverage-snapshot.md # Completed generated Compose profile/service coverage snapshot plan
├── 2026-07-05-gap-routing-recommendation.md # Completed gap-to-stage routing recommendation plan
├── 2026-07-05-agent-output-eval-fixtures.md # Completed agent-output eval fixture pack plan
├── 2026-07-05-qa-gate-recommendation-ci-summary.md # Completed QA gate recommendation CI summary plan
├── 2026-07-05-audit-pack-coverage-report.md # Completed audit-pack coverage report plan
├── 2026-07-06-llm-wiki-stage-category-coverage.md # Completed LLM Wiki stage/category coverage plan
├── 2026-07-06-tech-stack-version-provenance.md # Completed tech-stack version provenance plan
├── 2026-07-06-provider-hook-parity-matrix.md # Completed provider hook parity matrix plan
├── 2026-07-06-agent-output-eval-runner.md # Completed local advisory agent-output eval runner plan
├── 2026-07-06-agent-output-eval-ci-gate.md # Completed agent-output eval fixture freshness CI gate plan
├── 2026-07-06-dependency-vulnerability-audit-gate.md # Completed Storybook Next.js dependency vulnerability audit gate plan
├── 2026-07-10-agentic-research-pack-consolidation.md # Completed canonical research-pack consolidation plan; post-closure review PASS/APPROVED
├── 2026-07-06-security-automation-readiness-snapshot.md # Completed security automation readiness snapshot plan
├── 2026-07-06-audit-implementation-matrix-snapshot.md # Completed audit implementation matrix snapshot plan
├── 2026-07-06-sdlc-document-contract-corpus-normalization.md # Completed SDLC document contract corpus normalization plan
├── 2026-07-05-template-system-numbered-sdlc-paths.md # Completed numbered PRD/Spec path migration plan
├── 2026-07-05-workspace-support-surface-contract.md # Completed `_workspace` repo-support surface contract plan
└── README.md                               # This file
```

## How to Work in This Area

1. 새 plan은 [plan template](../../99.templates/templates/sdlc/plan.template.md)을 복사해 작성합니다.
2. Related Documents 링크는 `docs/04.execution/plans/<file>.md` 위치 기준으로 계산합니다.
3. 활성 plan은 이 폴더 아래 canonical 경로에만 둡니다. 비표준 `docs/*` 경로에는 active plan을 만들지 않습니다.
4. 계획에는 work breakdown, verification plan, risks, completion criteria가 있어야 합니다.
5. 예기치 않은 이슈가 발생하면 plan을 갱신하거나, historical evidence를 바꾸기 어렵다면 governance memory note로 남깁니다.

## Plan Contract

Plan은 implementation task list가 아니라 실행 설계입니다. 다음 질문에 답해야 합니다.

| Question                        | Plan Section                                         |
| ------------------------------- | ---------------------------------------------------- |
| 왜 지금 이 작업을 하는가        | `## Context`                                         |
| 범위와 비범위는 무엇인가        | `## Goals & In-Scope`, `## Non-Goals & Out-of-Scope` |
| 어떤 순서로 진행하는가          | `## Work Breakdown`                                  |
| 실패 가능성과 완화책은 무엇인가 | `## Risks & Mitigations`                             |
| 완료를 무엇으로 증명하는가      | `## Verification Plan`, `## Completion Criteria`     |

실제 수행 결과는 sibling [tasks README](../tasks/README.md)에 따라 task 문서로 기록합니다.

Completed plan status must be supported by `## Completion Criteria`, explicit
closure evidence, and sibling task evidence. Do not treat preserved execution
recipe checkboxes inside older completed plans as current open work unless the
task evidence or progress log records the same item as unresolved.

## Documentation Standards

- 가능한 경우 승인된 템플릿에서 시작한다.
- 제목과 구조는 사람과 AI Agent 모두가 해석 가능하도록 명시적으로 작성한다.
- 상위 문서와 하위 산출물 간 추적성을 유지한다.
- Related Documents는 실제 Markdown 링크로 작성한다.
- 오래된 plan의 historical evidence는 의미 보존을 우선하되, 현재 구현과 상충하면 `docs/98.archive/` tombstone으로 이동한다.

## AI Agent Guidance

1. 이 README를 먼저 읽는다.
2. 실행 전 계획 단계에서 정의된 작업 분할(WBS)과 리스크 요인을 반드시 숙지한다.
3. 작업 수행 중 계획에서 벗어난 상황이 발생하면 계획 문서를 갱신하거나 task evidence에 deviation을 기록한다.
4. 오래된 plan이 현재 template과 맞지 않아도 즉시 대량 재작성하지 않는다. 단, 현재 구현과 상충하면 승인된 범위 안에서 active chain에서 제거하고 archive tombstone으로 이동한다.

## Related Documents

- **Requirements**: [../../01.requirements/README.md](../../01.requirements/README.md)
- **Spec**: [../../03.specs/README.md](../../03.specs/README.md)
- **Task**: [../tasks/README.md](../tasks/README.md)
- **Architecture Decisions**: [../../02.architecture/decisions/README.md](../../02.architecture/decisions/README.md)
- **Operations**: [../../05.operations/README.md](../../05.operations/README.md)
- **Runbooks**: [../../05.operations/runbooks/README.md](../../05.operations/runbooks/README.md)
- **Infra Team Agent Cross-Validation Plan**: [2026-04-10-infra-team-agent-cross-validation.md](./2026-04-10-infra-team-agent-cross-validation.md)
- **Infra Service Optimization Priority Plan**: [2026-03-27-infra-service-optimization-priority-plan.md](./2026-03-27-infra-service-optimization-priority-plan.md) — active umbrella roadmap for Quick Wins and 2026 Q2/Q3 operations-standard follow-up
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
- **Agent Hook Completion and Style Automation Plan**: [2026-05-22-agent-hook-completion-style-automation.md](./2026-05-22-agent-hook-completion-style-automation.md)
- **Lifecycle README Debt Closure Plan**: [2026-05-22-lifecycle-readme-debt-closure.md](./2026-05-22-lifecycle-readme-debt-closure.md)
- **Workspace Docs and Agent Governance Remediation Plan**: [2026-05-22-workspace-docs-agent-governance-remediation.md](./2026-05-22-workspace-docs-agent-governance-remediation.md)
- **Workspace Governance Bounded Re-audit Plan**: [2026-05-22-workspace-governance-bounded-reaudit.md](./2026-05-22-workspace-governance-bounded-reaudit.md)
- **Workspace Audit Improvement Plan**: [2026-05-24-workspace-audit-improvement.md](./2026-05-24-workspace-audit-improvement.md)
- **Workspace Audit Input Task Gap Closure Plan**: [2026-05-24-workspace-audit-input-task-gap-closure.md](./2026-05-24-workspace-audit-input-task-gap-closure.md)
- **Workspace Audit Grill Review Plan**: [2026-05-24-workspace-audit-grill-review.md](./2026-05-24-workspace-audit-grill-review.md)
- **Home Docker Workspace Audit Improvement Plan**: [2026-05-25-home-docker-workspace-audit-improvement.md](./2026-05-25-home-docker-workspace-audit-improvement.md)
- **Home Docker Revalidation Deferred Follow-up Plan**: [2026-05-25-home-docker-revalidation-deferred-follow-up.md](./2026-05-25-home-docker-revalidation-deferred-follow-up.md)
- **Large-Scale Authored SSoT Review Plan**: [2026-05-25-large-scale-authored-ssot-review.md](./2026-05-25-large-scale-authored-ssot-review.md)
- **Spec Execution Implementation Audit Plan**: [2026-05-22-spec-execution-implementation-audit.md](./2026-05-22-spec-execution-implementation-audit.md)
- **Data Analytics Execution Traceability Plan**: [2026-05-22-data-analytics-execution-traceability.md](./2026-05-22-data-analytics-execution-traceability.md)
- **Workspace Doc & Governance Consistency (2026-05b) Plan**: [2026-05-29-workspace-consistency-2026-05b.md](./2026-05-29-workspace-consistency-2026-05b.md)
- **Claude Harness Governance Verification Plan**: [2026-05-31-claude-harness-governance-verification.md](./2026-05-31-claude-harness-governance-verification.md)
- **Agent Governance Decision Items and Attachment-Gap Plan**: [2026-06-02-agent-governance-decision-items-plan.md](./2026-06-02-agent-governance-decision-items-plan.md)
- **Agent Governance Phase 1 Revalidation Plan**: [2026-06-02-agent-governance-phase-1-revalidation.md](./2026-06-02-agent-governance-phase-1-revalidation.md)
- **Agent Governance Phase 2 Strategy Integration Plan**: [2026-06-02-agent-governance-phase-2-strategy-integration.md](./2026-06-02-agent-governance-phase-2-strategy-integration.md)
- **Agent Governance Phase 3 Approved Surface Activation Plan**: [2026-06-02-agent-governance-phase-3-approved-surface-activation.md](./2026-06-02-agent-governance-phase-3-approved-surface-activation.md)
- **Agent Governance Phase 4 Closure Reconciliation Plan**: [2026-06-02-agent-governance-phase-4-closure-reconciliation.md](./2026-06-02-agent-governance-phase-4-closure-reconciliation.md)
- **Docs Implementation Reconciliation Plan**: [2026-06-02-docs-implementation-reconciliation.md](./2026-06-02-docs-implementation-reconciliation.md)
- **Governance Surgical Re-Verification Plan**: [2026-06-03-governance-surgical-reverification.md](./2026-06-03-governance-surgical-reverification.md)
- **Document Contract Remediation Batch Plan**: [2026-07-03-document-contract-remediation-batches.md](./2026-07-03-document-contract-remediation-batches.md)
- **Document Restructure Audit, Contract, and Archive Plan**: [2026-07-04-document-restructure-audit-contract-archive.md](./2026-07-04-document-restructure-audit-contract-archive.md)
- **Agentic Research Pack Refresh Plan**: [2026-07-05-agentic-research-pack-refresh.md](./2026-07-05-agentic-research-pack-refresh.md)
- **Agentic Engineering Implementation Audit Pack Plan**: [2026-07-05-agentic-engineering-implementation-audit-pack.md](./2026-07-05-agentic-engineering-implementation-audit-pack.md)
- **Provider Workspace Artifact Path Parity Plan**: [2026-07-05-provider-workspace-artifact-path-parity.md](./2026-07-05-provider-workspace-artifact-path-parity.md)
- **Provider Semantic Parity Validator Plan**: [2026-07-05-provider-semantic-parity-validator.md](./2026-07-05-provider-semantic-parity-validator.md)
- **Compose Profile Service Coverage Snapshot Plan**: [2026-07-05-compose-profile-service-coverage-snapshot.md](./2026-07-05-compose-profile-service-coverage-snapshot.md)
- **Gap Routing Recommendation Plan**: [2026-07-05-gap-routing-recommendation.md](./2026-07-05-gap-routing-recommendation.md)
- **Agent Output Eval Fixtures Plan**: [2026-07-05-agent-output-eval-fixtures.md](./2026-07-05-agent-output-eval-fixtures.md)
- **QA Gate Recommendation CI Summary Plan**: [2026-07-05-qa-gate-recommendation-ci-summary.md](./2026-07-05-qa-gate-recommendation-ci-summary.md)
- **Audit Pack Coverage Report Plan**: [2026-07-05-audit-pack-coverage-report.md](./2026-07-05-audit-pack-coverage-report.md)
- **LLM Wiki Stage Category Coverage Plan**: [2026-07-06-llm-wiki-stage-category-coverage.md](./2026-07-06-llm-wiki-stage-category-coverage.md)
- **Agent Output Eval CI Gate Plan**: [2026-07-06-agent-output-eval-ci-gate.md](./2026-07-06-agent-output-eval-ci-gate.md)
- **Dependency Vulnerability Audit Gate Plan**: [2026-07-06-dependency-vulnerability-audit-gate.md](./2026-07-06-dependency-vulnerability-audit-gate.md)
- **Agentic Research Pack Consolidation Plan**: [2026-07-10-agentic-research-pack-consolidation.md](./2026-07-10-agentic-research-pack-consolidation.md)
- **Audit Implementation Matrix Snapshot Plan**: [2026-07-06-audit-implementation-matrix-snapshot.md](./2026-07-06-audit-implementation-matrix-snapshot.md)
- **SDLC Document Contract Corpus Normalization Plan**: [2026-07-06-sdlc-document-contract-corpus-normalization.md](./2026-07-06-sdlc-document-contract-corpus-normalization.md)
- **Workspace Support Surface Contract Plan**: [2026-07-05-workspace-support-surface-contract.md](./2026-07-05-workspace-support-surface-contract.md)
- **Template System Numbered SDLC Paths Plan**: [2026-07-05-template-system-numbered-sdlc-paths.md](./2026-07-05-template-system-numbered-sdlc-paths.md)
- **Workspace Document Contract Audit Pack Plan**: [2026-07-03-workspace-document-contract-audit-pack.md](./2026-07-03-workspace-document-contract-audit-pack.md)
- **Template System Reorganization Plan**: [2026-07-02-template-system-reorganization.md](./2026-07-02-template-system-reorganization.md)
- **Template System Contract Standardization Plan**: [2026-07-03-template-system-contract-standardization.md](./2026-07-03-template-system-contract-standardization.md)
