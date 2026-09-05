---
title: "03.specs"
version: "1.0.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-04"
layer: "specs"
---

# 03.specs

## Overview

docs/03.specs는 current capability contract와 승인된 변경의 일시적 실행
packet을 관리합니다. 각 package의 spec.md는 구현 경계와 acceptance를
소유합니다. plan.md와 tasks/는 변경이 실제로 진행되는 동안에만 존재합니다.

## Scope

- 포함: 현재 capability Spec, 완료된 change outcome Spec, 진행 중인 변경의
  active Plan·Task, Spec이 직접 소유하는 executable contract.
- 제외: 운영 절차, 감사·조사 데이터, 과거 실행 본문, 이전 경로의 복제본과
  redirect. 해당 자료는 각 Stage의 현재 owner 또는 Git history가 소유합니다.

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
| SPEC-0172 | [Document Contract Convergence](0172-document-contract-convergence/spec.md) | active with active [Plan](0172-document-contract-convergence/plan.md) and in-progress [Task](0172-document-contract-convergence/tasks/tsk-0001-document-contract-convergence.md) |
| SPEC-0173 | [Governance and QA Surface Convergence](0173-governance-qa-surface-convergence/spec.md) | active with active [Plan](0173-governance-qa-surface-convergence/plan.md), Task 1 in progress, and Tasks 2-6 draft |

## How to Work in This Area

1. Load the governing Requirement, Architecture Description, and ADR.
2. Create or update spec.md with the registered Spec template.
3. Add a Plan and numbered Tasks only for an approved active change.
4. Record actual work only in the current Task.
5. Write durable behavior back to the Spec, Stage 01/02, and Stage 05 owners.
6. Validate metadata, lifecycle, links, implementation alignment, and the
   registered Gate profile.
7. Terminalize the Spec and remove execution bodies only after recovery and
   inbound-consumer checks.

### Package Lifecycle

- Capability Spec은 구현이 current인 동안 active로 유지할 수 있으며 Plan이나
  Task가 없어도 됩니다.
- Change Spec은 승인 후 active가 되고 current Plan과 Task를 사용합니다.
- Active Task는 active Spec과 active Plan을 parent로 가집니다.
- 변경이 끝나면 outcome을 Spec과 다른 current owner에 먼저 write back하고
  Spec을 completed로 전환합니다.
- Terminal Plan과 Task는 current consumer가 없고 Git regular-blob recovery가
  확인되면 삭제합니다. Body clone이나 redirect는 만들지 않습니다.

### Role Contract

| Role | Responsibility |
| --- | --- |
| Spec | current capability or completed change outcome |
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
