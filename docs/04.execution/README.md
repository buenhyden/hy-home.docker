---
status: active
---

# 04.execution

> 승인된 명세를 실행 순서와 검증 가능한 작업 증거로 전환하는 stage

## Overview

`docs/04.execution`은 `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`에서 승인된 내용을 실제 실행 흐름으로 바꾸는 stage입니다.

계획은 `plans/`에 둡니다. 계획 문서는 실행 순서, 리스크, 검증 명령, 완료 기준을 정의합니다.

작업 증거는 `tasks/`에 둡니다. 작업 문서는 실제 수행 상태, 검증 결과, 남은 이슈를 audit 가능한 형태로 기록합니다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- Project Maintainers
- AI Agents

## Scope

### In Scope

- 승인된 spec에서 파생된 implementation plan
- 실행 순서, work breakdown, risk control, rollback 기준
- task status, validation evidence, completion evidence
- docs, governance, infra 변경의 traceability
- 관련 spec, operations, reference 문서로의 연결

### Out of Scope

- 요구사항 정의 (`docs/01.requirements` 담당)
- 아키텍처 요구사항과 결정 기록 (`docs/02.architecture` 담당)
- 상세 기술 명세 (`docs/03.specs` 담당)
- 운영 가이드, 정책, 런북, 사고 기록 (`docs/05.operations` 담당)
- 장기 전략 또는 분류 보고서 (`docs/90.references` 또는 architecture stage 담당)

## Structure

```text
docs/04.execution/
├── plans/      # 실행 순서, 리스크, 검증 기준을 정의하는 implementation plans
├── tasks/      # 구현/검증 작업 상태와 evidence를 기록하는 task documents
└── README.md   # This file
```

## Completed Remediation Evidence

- [Infra team agent cross-validation plan](plans/2026-04-10-infra-team-agent-cross-validation.md) - completed plan for canonical workflow cross-validation design and runtime catalog alignment
- [Infra team agent cross-validation task](tasks/2026-04-10-infra-team-agent-cross-validation.md) - completion evidence for canonical agent design, non-stage docs removal, and runtime handoff surfaces
- [Requirements standardization plan](plans/2026-05-17-requirements-standardization.md) - completed plan for PRD contract and taxonomy remediation
- [Requirements standardization task](tasks/2026-05-17-requirements-standardization.md) - completion evidence for PRD/template cleanup and generated navigation freshness
- [Scripts CI/CD and QA cleanup plan](plans/2026-05-17-scripts-ci-qa-cleanup.md) - completed plan for canonical script inventory, QA/CI tooling, and hook routing cleanup
- [Scripts CI/CD and QA cleanup task](tasks/2026-05-17-scripts-ci-qa-cleanup.md) - completion evidence for purpose-folder script ownership and QA/CI tooling surface
- [Execution stage remediation plan](plans/2026-05-18-execution-stage-remediation.md) - completed plan for execution README/template/current-artifact remediation
- [Agent hook completion and style automation plan](plans/2026-05-22-agent-hook-completion-style-automation.md) - completed hook plan for logical commit gating, style validation, and post-edit formatting
- [Agent hook completion and style automation task](tasks/2026-05-22-agent-hook-completion-style-automation.md) - execution evidence for Hook Development and Hookify rule updates
- [Data analytics execution traceability plan](plans/2026-05-22-data-analytics-execution-traceability.md) - completed plan for closing the missing execution evidence link for `04-data-analytics`
- [Data analytics execution traceability task](tasks/2026-05-22-data-analytics-execution-traceability.md) - execution evidence for analytics spec-to-plan/task traceability and static compose checks
- [Spec execution implementation audit plan](plans/2026-05-22-spec-execution-implementation-audit.md) - completed audit plan for spec/plan/task implementation coverage and evidence-backed remediation
- [Spec execution implementation audit task](tasks/2026-05-22-spec-execution-implementation-audit.md) - execution evidence for spec link coverage, stale state cleanup, and hook smoke tests
- [Workspace governance bounded re-audit plan](plans/2026-05-22-workspace-governance-bounded-reaudit.md) - completed bounded re-audit plan for docs, governance, memory, hook guidance, and validator drift
- [Workspace governance bounded re-audit task](tasks/2026-05-22-workspace-governance-bounded-reaudit.md) - execution evidence for the bounded re-audit and agent improvement pass
- [Lifecycle README debt closure plan](plans/2026-05-22-lifecycle-readme-debt-closure.md) - completed plan for closing lifecycle, README readiness, and hook guidance debt
- [Lifecycle README debt closure task](tasks/2026-05-22-lifecycle-readme-debt-closure.md) - execution evidence for lifecycle README debt closure
- [Workspace docs and agent governance remediation plan](plans/2026-05-22-workspace-docs-agent-governance-remediation.md) - completed plan for lifecycle, template, cross-link, and agent runtime governance remediation
- [Workspace docs and agent governance remediation task](tasks/2026-05-22-workspace-docs-agent-governance-remediation.md) - execution evidence for the workspace docs and agent governance remediation
- [Targeted documentation precision remediation plan](plans/2026-05-18-targeted-docs-precision-remediation.md) - evidence-gated remediation plan for target stage docs and root README
- [Targeted documentation precision remediation task](tasks/2026-05-18-targeted-docs-precision-remediation.md) - execution evidence for the precision remediation pass
- [Docs bounded consistency audit plan](plans/2026-05-18-docs-bounded-consistency-audit.md) - README entrypoint, stale inventory, and validator-backed drift remediation plan
- [Docs bounded consistency audit task](tasks/2026-05-18-docs-bounded-consistency-audit.md) - execution evidence for the bounded consistency audit
- [Workspace audit 2026-05 plan](plans/2026-05-26-workspace-audit.md) - implementation plan for gap registry, lifecycle docs, env/secrets comparison, skill stubs, and memory update
- [Workspace audit 2026-05 task](tasks/2026-05-26-workspace-audit.md) - execution evidence for stage README lifecycle sections, env/secrets comparison reports, and session spec traceability

## Execution Contract

`plans/`와 `tasks/`는 같은 작업을 다루더라도 책임이 다릅니다.

| Artifact | Responsibility                                           | Must Not Become                               |
| -------- | -------------------------------------------------------- | --------------------------------------------- |
| Plan     | 실행 순서, dependency, risk, rollback, verification plan | 실제 수행 로그 또는 완료 evidence             |
| Task     | 수행 상태, 검증 결과, deviation, completion evidence     | 새 요구사항, architecture decision, 또는 spec |

같은 문장을 plan과 task에 중복해서 복사하지 않습니다. Plan은 “무엇을 어떤 순서로 할지”를 유지하고, Task는 “무엇을 실제로 했고 무엇으로 검증했는지”를 유지합니다.

## How to Work in This Area

1. 실행 전에는 [plan template](../99.templates/plan.template.md)을 사용해 `plans/YYYY-MM-DD-topic.md`를 작성합니다.
2. 실행 중에는 [task template](../99.templates/task.template.md)을 사용해 `tasks/YYYY-MM-DD-topic.md`에 상태와 evidence를 기록합니다.
3. 기존 historical plan/task는 의미를 보존합니다. 오래된 template drift는 대량 재작성하지 않고 별도 memory note로 관리합니다.
4. 새 파일을 추가하거나 이동하면 해당 parent README와 `## Related Documents` 링크를 대상 위치 기준으로 갱신합니다.
5. 완료 전에는 `check-doc-traceability.sh`, 관련 repository contract, link/pseudo-link scan을 실행합니다.

## Documentation Standards

- 새 plan/task는 `status: draft` 또는 실제 상태 frontmatter를 포함합니다.
- 새 plan/task는 `<!-- Target: ... -->` 주석으로 canonical target을 명시합니다.
- Related Documents는 클릭 가능한 Markdown 링크로 작성합니다. 코드 span pseudo-link만 남기지 않습니다.
- Plan은 작업 순서와 검증 기준을 설명하고, Task는 실행 evidence를 기록합니다.
- Historical execution evidence는 문서 의미가 바뀌지 않는 범위에서만 정리합니다.

## AI Agent Guidance

1. 먼저 이 README와 하위 [plans README](plans/README.md), [tasks README](tasks/README.md)를 읽습니다.
2. 구현 전에는 관련 spec과 plan을 찾고, 실행 후에는 task evidence와 progress log를 갱신합니다.
3. Graphify는 탐색 보조로만 사용하고, 완료 판단은 tracked docs와 repository validators로 확인합니다.
4. 오래된 execution artifact의 template drift를 발견하면 즉시 대량 재작성하지 말고 범위와 위험을 기록합니다.

## Stage Handoff

구현과 검증이 완료된 운영 절차, 통제 기준, 반복 절차는 [`docs/05.operations/`](../05.operations/README.md)로 이관한다. Plan은 "무엇을 어떤 순서로 할지", Task는 "무엇을 실제로 했고 무엇으로 검증했는지"를 유지한다. 상세 매핑은 [`stage-authoring-matrix.md`](../00.agent-governance/rules/stage-authoring-matrix.md)를 따른다.

## Related Documents

- **Requirements**: [../01.requirements/README.md](../01.requirements/README.md)
- **Architecture**: [../02.architecture/README.md](../02.architecture/README.md)
- **Specs**: [../03.specs/README.md](../03.specs/README.md)
- **Plans**: [plans/README.md](plans/README.md)
- **Tasks**: [tasks/README.md](tasks/README.md)
- **Operations**: [../05.operations/README.md](../05.operations/README.md)
- **Templates**: [../99.templates/README.md](../99.templates/README.md)
- **Documentation protocol**: [../00.agent-governance/rules/documentation-protocol.md](../00.agent-governance/rules/documentation-protocol.md)
- **Infra team agent cross-validation plan**: [plans/2026-04-10-infra-team-agent-cross-validation.md](plans/2026-04-10-infra-team-agent-cross-validation.md)
- **Infra team agent cross-validation task**: [tasks/2026-04-10-infra-team-agent-cross-validation.md](tasks/2026-04-10-infra-team-agent-cross-validation.md)
- **Requirements standardization plan**: [plans/2026-05-17-requirements-standardization.md](plans/2026-05-17-requirements-standardization.md)
- **Requirements standardization task**: [tasks/2026-05-17-requirements-standardization.md](tasks/2026-05-17-requirements-standardization.md)
- **Scripts CI/CD and QA cleanup plan**: [plans/2026-05-17-scripts-ci-qa-cleanup.md](plans/2026-05-17-scripts-ci-qa-cleanup.md)
- **Scripts CI/CD and QA cleanup task**: [tasks/2026-05-17-scripts-ci-qa-cleanup.md](tasks/2026-05-17-scripts-ci-qa-cleanup.md)
- **Agent hook completion and style automation plan**: [plans/2026-05-22-agent-hook-completion-style-automation.md](plans/2026-05-22-agent-hook-completion-style-automation.md)
- **Agent hook completion and style automation task**: [tasks/2026-05-22-agent-hook-completion-style-automation.md](tasks/2026-05-22-agent-hook-completion-style-automation.md)
- **Targeted documentation precision remediation plan**: [plans/2026-05-18-targeted-docs-precision-remediation.md](plans/2026-05-18-targeted-docs-precision-remediation.md)
- **Targeted documentation precision remediation task**: [tasks/2026-05-18-targeted-docs-precision-remediation.md](tasks/2026-05-18-targeted-docs-precision-remediation.md)
- **Docs bounded consistency audit plan**: [plans/2026-05-18-docs-bounded-consistency-audit.md](plans/2026-05-18-docs-bounded-consistency-audit.md)
- **Docs bounded consistency audit task**: [tasks/2026-05-18-docs-bounded-consistency-audit.md](tasks/2026-05-18-docs-bounded-consistency-audit.md)
- **Lifecycle README debt closure plan**: [plans/2026-05-22-lifecycle-readme-debt-closure.md](plans/2026-05-22-lifecycle-readme-debt-closure.md)
- **Lifecycle README debt closure task**: [tasks/2026-05-22-lifecycle-readme-debt-closure.md](tasks/2026-05-22-lifecycle-readme-debt-closure.md)
- **Workspace docs and agent governance remediation plan**: [plans/2026-05-22-workspace-docs-agent-governance-remediation.md](plans/2026-05-22-workspace-docs-agent-governance-remediation.md)
- **Workspace docs and agent governance remediation task**: [tasks/2026-05-22-workspace-docs-agent-governance-remediation.md](tasks/2026-05-22-workspace-docs-agent-governance-remediation.md)
- **Workspace governance bounded re-audit plan**: [plans/2026-05-22-workspace-governance-bounded-reaudit.md](plans/2026-05-22-workspace-governance-bounded-reaudit.md)
- **Workspace governance bounded re-audit task**: [tasks/2026-05-22-workspace-governance-bounded-reaudit.md](tasks/2026-05-22-workspace-governance-bounded-reaudit.md)
- **Spec execution implementation audit plan**: [plans/2026-05-22-spec-execution-implementation-audit.md](plans/2026-05-22-spec-execution-implementation-audit.md)
- **Spec execution implementation audit task**: [tasks/2026-05-22-spec-execution-implementation-audit.md](tasks/2026-05-22-spec-execution-implementation-audit.md)
- **Data analytics execution traceability plan**: [plans/2026-05-22-data-analytics-execution-traceability.md](plans/2026-05-22-data-analytics-execution-traceability.md)
- **Data analytics execution traceability task**: [tasks/2026-05-22-data-analytics-execution-traceability.md](tasks/2026-05-22-data-analytics-execution-traceability.md)
- **Workspace audit 2026-05 plan**: [plans/2026-05-26-workspace-audit.md](plans/2026-05-26-workspace-audit.md)
- **Workspace audit 2026-05 task**: [tasks/2026-05-26-workspace-audit.md](tasks/2026-05-26-workspace-audit.md)
