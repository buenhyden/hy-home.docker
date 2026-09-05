---
title: "03.specs"
version: "1.0.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "specs"
---

# 03.specs

## Overview

docs/03.specs는 범위가 정해진 변경의 명세와 실행 packet을 관리합니다.
각 package의 spec.md는 관찰 가능한 동작과 acceptance를, plan.md는 구현
순서와 위험을, tasks/는 실제 실행·검증·검토 증거를 소유합니다. 장기적인
구조와 운영 의미는 Stage 01/02/05의 현재 문서로 승격합니다.

## Scope

- 포함: 진행 중인 변경의 Spec·Plan·Task와 Spec이 직접 소유하는 executable
  contract. 완료된 package는 보존 경로를 통해 찾습니다.
- 제외: 운영 절차, 감사·조사 데이터, 과거 실행 본문, 이전 경로의 복제본과
  redirect. 운영·참조 자료는 각 Stage의 현재 owner가, 처분된 실행 증거는
  Stage 98의 보존 package와 Task가 소유합니다. Git history는 원본과 복구를
  증명하며 필수 보존 본문을 대체하지 않습니다.

## Structure

- docs/03.specs/README.md: stage index
- docs/03.specs/<4-digit-id>-<slug>/spec.md: mandatory Spec
- docs/03.specs/<4-digit-id>-<slug>/plan.md: optional active Plan
- docs/03.specs/<4-digit-id>-<slug>/tasks/tsk-<4-digit-id>-<slug>.md:
  optional numbered Task
- docs/03.specs/<4-digit-id>-<slug>/contracts/: optional registered executable
  contracts

design.md, tests.md, singular task.md는 package role이 아닙니다.

### Current Package Index

이 인덱스는 진행 중인 package와 과거 package의 보존 경로를 함께 안내합니다.
`completed` 행은 역사적 실행 증거이며 현재 구현 권한이 아닙니다.

| ID | Package | Current roles |
| --- | --- | --- |
| SPEC-0093 | [Documentation Taxonomy Migration](../98.archive/completed/03.specs/0093-docs-taxonomy-agent-first-migration/spec.md) | completed, preserved under the archive |
| SPEC-0094 | [Harness and Agent-first Engineering](../98.archive/completed/03.specs/0094-harness-agent-first-engineering/spec.md) | completed, preserved under the archive |
| SPEC-0095 | [Infrastructure, Secrets, and Documentation Refresh](../98.archive/completed/03.specs/0095-infra-secrets-docs-refresh/spec.md) | completed, preserved under the archive |
| SPEC-0096 | [LLM Wiki Completion](../98.archive/completed/03.specs/0096-llm-wiki-agent-first-completion/spec.md) | completed, preserved under the archive |
| SPEC-0097 | [Workspace Revalidation](../98.archive/completed/03.specs/0097-home-docker-revalidation-deferred-follow-up/spec.md) | completed, preserved under the archive |
| SPEC-0098 | [infra_net Standardization](../98.archive/completed/03.specs/0098-standardize-infra-net/spec.md) | completed, preserved under the archive |
| SPEC-0154 | [Governance Consistency Convergence](../98.archive/completed/03.specs/0154-governance-consistency-convergence/spec.md) | completed, preserved under the archive |
| SPEC-0155 | [Validation Surface Reduction](../98.archive/completed/03.specs/0155-validation-surface-reduction/spec.md) | completed, preserved under the archive |
| SPEC-0156 | [Compose Enablement Model Convergence](../98.archive/completed/03.specs/0156-compose-enablement-model-convergence/spec.md) | completed, preserved under the archive with [Plan](../98.archive/completed/03.specs/0156-compose-enablement-model-convergence/plan.md) and [Task](../98.archive/completed/03.specs/0156-compose-enablement-model-convergence/tasks/tsk-0001-compose-enablement.md) |
| SPEC-0157 | [Script Surface Ownership Convergence](../98.archive/completed/03.specs/0157-script-surface-ownership-convergence/spec.md) | completed, preserved under the archive |
| SPEC-0158 | [Document Governance Lifecycle Convergence](../98.archive/completed/03.specs/0158-document-governance-lifecycle-convergence/spec.md) | completed, preserved under the archive |
| SPEC-0159 | [Document Taxonomy and Identity Convergence](../98.archive/completed/03.specs/0159-document-taxonomy-identity-convergence/spec.md) | completed, preserved under the archive |
| SPEC-0160 | [README Entrypoint Form Registration](../98.archive/completed/03.specs/0160-readme-entrypoint-form-registration/spec.md) | completed, preserved under the archive |
| SPEC-0161 | [Legacy Profile Layer Retirement](../98.archive/completed/03.specs/0161-legacy-profile-layer-retirement/spec.md) | completed, preserved under the archive |
| SPEC-0162 | [Validation Blind Spot Closure](../98.archive/completed/03.specs/0162-validation-blind-spot-closure/spec.md) | completed, preserved under the archive |
| SPEC-0163 | [Deferred Contract Enforcement](../98.archive/completed/03.specs/0163-deferred-contract-enforcement/spec.md) | completed, preserved under the archive |
| SPEC-0164 | [Lifecycle Vocabulary Alignment](../98.archive/completed/03.specs/0164-lifecycle-vocabulary-alignment/spec.md) | completed, preserved under the archive |
| SPEC-0165 | [Template Contract Enforcement](../98.archive/completed/03.specs/0165-template-contract-enforcement/spec.md) | completed, preserved under the archive |
| SPEC-0166 | [Formatting Authority Convergence](../98.archive/completed/03.specs/0166-formatting-authority-convergence/spec.md) | completed, preserved under the archive |
| SPEC-0167 | [Quality Gate Convergence](../98.archive/completed/03.specs/0167-quality-gate-convergence/spec.md) | completed, preserved under the archive |
| SPEC-0168 | [Entrypoint README Registration](../98.archive/completed/03.specs/0168-entrypoint-readme-registration/spec.md) | completed, preserved under the archive |
| SPEC-0169 | [Document Lifecycle Convergence](../98.archive/completed/03.specs/0169-document-lifecycle-convergence/spec.md) | completed, preserved under the archive with [Plan](../98.archive/completed/03.specs/0169-document-lifecycle-convergence/plan.md) and [Task](../98.archive/completed/03.specs/0169-document-lifecycle-convergence/tasks/tsk-0001-document-lifecycle-convergence.md) |
| SPEC-0170 | [Archive Preservation Model](../98.archive/completed/03.specs/0170-archive-preservation-model/spec.md) | completed, preserved under the archive with [Plan](../98.archive/completed/03.specs/0170-archive-preservation-model/plan.md) and [Task](../98.archive/completed/03.specs/0170-archive-preservation-model/tasks/tsk-0001-archive-preservation-model.md) |
| SPEC-0171 | [Compose Sibling Pair Resolution](../98.archive/completed/03.specs/0171-compose-sibling-pair-resolution/spec.md) | completed, preserved under the archive with [Plan](../98.archive/completed/03.specs/0171-compose-sibling-pair-resolution/plan.md) and [Task](../98.archive/completed/03.specs/0171-compose-sibling-pair-resolution/tasks/tsk-0001-sibling-pair-resolution.md) |
| SPEC-0172 | [Document Contract Convergence](../98.archive/completed/03.specs/0172-document-contract-convergence/spec.md) | completed record unchanged; divergent main [Spec](../98.archive/superseded/03.specs/0172-document-contract-convergence/spec.md), [Plan](../98.archive/superseded/03.specs/0172-document-contract-convergence/plan.md), and [Task](../98.archive/superseded/03.specs/0172-document-contract-convergence/tasks/tsk-0001-document-contract-convergence.md) preserved by the SPEC-0173 branch receipt |
| SPEC-0173 | [Governance and QA Surface Convergence](0173-governance-qa-surface-convergence/spec.md) | active with active [Plan](0173-governance-qa-surface-convergence/plan.md); Tasks 1-5 implementation milestones reviewed, Task 6 integrating and verifying final evidence |
| SPEC-0174 | [Governance and QA Convergence](../98.archive/superseded/03.specs/0174-governance-qa-convergence/spec.md) | superseded by SPEC-0173; cancelled [Plan](../98.archive/superseded/03.specs/0174-governance-qa-convergence/plan.md) and [Task](../98.archive/superseded/03.specs/0174-governance-qa-convergence/tasks/tsk-0001-converge-governance-and-qa.md) preserved with the full packet |

## How to Work in This Area

1. Load the governing Requirement, Architecture Description, and ADR.
2. Create or update spec.md with the registered Spec template.
3. Add a Plan and numbered Tasks only for an approved active change.
4. Record actual work only in the current Task.
5. Record acceptance coverage and the promotion receipt in the current Task,
   linking durable updates in Stage 01/02/05 or an explicit N/A rationale.
6. Validate metadata, lifecycle, links, implementation alignment, and the
   registered Gate profile.
7. Complete and preserve the package only after promotion, recovery, and
   inbound-consumer checks. Follow the [SDLC](../00.agent-governance/sdlc.md)
   for clarify, analyze, implementation, and verification order.

### Package Lifecycle

- 현재 Requirement와 Architecture가 변경 범위를 충족하면 재사용합니다.
- Spec·Plan·Task의 정확한 상태와 전이는 Registry가 소유합니다.
- 완료 전에 acceptance와 실제 검증 결과를 연결하고 장기 의미를 현재
  Stage 01/02/05 owner에 승격합니다. 승격 근거는 현재 Task의
  `Verification Evidence` 한 곳에 기록합니다.
- 완료 package의 Spec·Plan·Task는 Stage 98의 해당 보존 경로로 이동합니다.
  Git recovery만을 근거로 실행 본문을 삭제하거나 frozen 내용을 다시 쓰지
  않습니다. 철회와 완료의 처분 기록은 [문서 보존 정책](../00.agent-governance/policies/documentation-protocol.md#document-retention-and-retirement)을 따릅니다.

### Role Contract

| Role | Responsibility |
| --- | --- |
| Spec | bounded observable behavior, scope, failure modes, and acceptance contract |
| Plan | approved prospective sequence, risk, rollback, completion criteria |
| Task | actual work log, command result, review, commit, and deferral evidence |
| Contract | registered executable interface owned by the Spec |

## Related Documents

- [Requirements](../01.requirements/README.md)
- [Architecture](../02.architecture/README.md)
- [Operations](../05.operations/README.md)
- [Stage authoring matrix](../00.agent-governance/policies/stage-authoring-matrix.md)
- [Document Registry](../99.templates/registry.json)
- [Spec template](../99.templates/templates/specs/spec.template.md)
- [Plan template](../99.templates/templates/specs/plan.template.md)
- [Task template](../99.templates/templates/specs/task.template.md)
