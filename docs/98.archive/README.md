---
layer: archive
---

<!-- Target: docs/98.archive/README.md -->

# 98.archive

> 승인된 typed Stage 98 기록의 단일 대상이며, current guidance나 일반 본문
> 저장소가 아닙니다.

## Overview

`docs/98.archive/`는 문서 archive의 유일한 대상입니다. README를 제외한 모든
파일은 다음 네 machine profile 가운데 정확히 하나를 선택합니다.

- `change-plan`: `changes/chg-<id>-<slug>/plan.md`
- `change-task`: `changes/chg-<id>-<slug>/task.md`
- `tombstone`: `tombstones/<stage>/<stable-id>-<slug>.md`; `<stage>`는
  `01.requirements`, `02.architecture`, `03.specs`, `05.operations` 중 하나
- `migration`: `migrations/mig-<id>-<slug>.md`

Change Plan과 Task는 완료된 한 change packet의 본문과 상관관계를 보존합니다.
Tombstone은 제거된 원문을 복제하지 않는 간결한 provenance 기록이고,
Migration은 경로 변경 ledger를 보존합니다. 모든 ID와 경로는 stable하며 날짜는
`archived_at` 같은 typed frontmatter에만 기록합니다. 정확한 필드 조건은
[archive and retention contract](../99.templates/support/archive-retention-contract.md)와
[metadata profiles](../99.templates/support/document-metadata-profiles.yaml)를
따릅니다.

## Audience

- Documentation Writers
- AI Agents
- Repository Maintainers

## Scope

### In Scope

- 완료된 change packet의 상관된 Plan과 Task
- stable source identity를 유지하는 간결한 tombstone
- stable `mig-<id>` identity를 사용하는 migration record
- 검증된 relation, disposition, Git provenance, preservation metadata
- 아래의 명시적으로 bounded된 historical provenance ledger

### Out of Scope

- 현재 판단 기준으로 사용할 요구사항, 설계, spec, plan, task, 운영 절차
- change packet이 아닌 제거 문서의 원문 본문 보존
- source stage를 복제하는 archive directory
- 날짜나 연도 partition을 archive identity로 사용
- active 문서의 Related Documents 대상

## Structure

```text
98.archive/
├── changes/
│   └── chg-<id>-<slug>/
│       ├── plan.md
│       └── task.md
├── tombstones/
│   ├── 01.requirements/
│   ├── 02.architecture/
│   ├── 03.specs/
│   └── 05.operations/
│       └── <stable-id>-<slug>.md
├── migrations/
│   └── mig-<id>-<slug>.md
└── README.md
```

## Non-Authoritative Historical Provenance Ledger

이 절은 이전 archive 이동의 non-authoritative historical provenance만 보존하며
not routing입니다. 아래의 retired 경로는 현재 target이나 template 선택 지침이
아닙니다. 새 기록과 migrated 기록은 위의 typed stable 경로만 사용합니다.

| Original Path                                                                           | Archive Path                                                                                       | Reason                                                                                                                                           | Current Replacement                                                                                      |
| --------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| `docs/04.execution/plans/2026-05-30-ai-governance-reorg.md`                             | `docs/98.archive/04.execution/plans/2026-05-30-ai-governance-reorg.md`                             | Original plan claimed legacy `.agents/` removal and superseded provider-adapter assumptions that conflict with tracked `.agents/` implementation | `docs/04.execution/plans/2026-06-02-agent-governance-decision-items-plan.md`                             |
| `docs/04.execution/plans/2026-05-30-standardizing-agent-governance.md`                  | `docs/98.archive/04.execution/plans/2026-05-30-standardizing-agent-governance.md`                  | Original plan required `.codex/agents/*.md` YAML frontmatter and prohibited TOML, conflicting with TOML-only Codex adapters                      | `docs/04.execution/plans/2026-06-02-agent-governance-decision-items-plan.md`                             |
| `docs/04.execution/plans/2026-06-01-agent-governance-phase1-diagnostic.md`              | `docs/98.archive/04.execution/plans/2026-06-01-agent-governance-phase1-diagnostic.md`              | Diagnostic treated Codex Markdown prompts and broad HADS advisory status as active unresolved decisions                                          | `docs/04.execution/plans/2026-06-02-agent-governance-decision-items-plan.md`                             |
| `docs/04.execution/plans/2026-06-01-agent-governance-phase2-alignment.md`               | `docs/98.archive/04.execution/plans/2026-06-01-agent-governance-phase2-alignment.md`               | Plan preserved Codex Markdown compatibility prompts and broad HADS advisory-only decisions that conflict with current implementation             | `docs/04.execution/plans/2026-06-02-agent-governance-decision-items-plan.md`                             |
| `docs/04.execution/tasks/2026-05-30-standardizing-agent-governance.md`                  | `docs/98.archive/04.execution/tasks/2026-05-30-standardizing-agent-governance.md`                  | Task evidence recorded `.codex/agents/*.md` YAML frontmatter as the preserved Codex harness shape                                                | `docs/04.execution/tasks/2026-06-02-agent-governance-missing-items-implementation.md`                    |
| `docs/04.execution/tasks/2026-06-01-agent-governance-phase1-diagnostic.md`              | `docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase1-diagnostic.md`              | Task pointed at obsolete Codex Markdown prompt and broad HADS advisory assumptions                                                               | `docs/04.execution/tasks/2026-06-02-agent-governance-missing-items-implementation.md`                    |
| `docs/04.execution/tasks/2026-06-01-agent-governance-phase3-implementation.md`          | `docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase3-implementation.md`          | Task depended on the archived Phase 2 plan as parent evidence                                                                                    | `docs/04.execution/tasks/2026-06-02-agent-governance-missing-items-implementation.md`                    |
| `docs/04.execution/tasks/2026-06-01-agent-governance-stage01-02-alignment.md`           | `docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-stage01-02-alignment.md`           | Task was tied to the archived Phase 2 alignment chain and pre-closure HADS/Codex boundaries                                                      | `docs/04.execution/tasks/2026-06-02-agent-governance-missing-items-implementation.md`                    |
| `docs/04.execution/tasks/2026-06-01-agent-governance-phase3-stage01-02-continuation.md` | `docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase3-stage01-02-continuation.md` | Task preserved pre-closure non-goals for HADS, Codex Markdown prompts, and hard validators                                                       | `docs/04.execution/tasks/2026-06-02-agent-governance-missing-items-implementation.md`                    |
| `docs/04.execution/tasks/2026-06-01-agent-governance-phase3-strategy-integration.md`    | `docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase3-strategy-integration.md`    | Task recorded HADS as advisory-only and `.codex/agents/*.md` as compatibility prompts                                                            | `docs/04.execution/tasks/2026-06-02-agent-governance-missing-items-implementation.md`                    |
| `docs/04.execution/tasks/2026-06-01-agent-governance-phase4-closure.md`                 | `docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase4-closure.md`                 | Closure preserved non-goals that were later approved and implemented                                                                             | `docs/04.execution/tasks/2026-06-02-agent-governance-missing-items-implementation.md`                    |
| `docs/05.operations/guides/07-workflow/01.airflow-dag-dev.md`                           | `docs/98.archive/05.operations/guides/07-workflow/01.airflow-dag-dev.md`                           | Duplicate DAG guide retained stale repo-local DAG path guidance; active guide now uses `${DEFAULT_WORKFLOW_DIR}/airflow/dags`                    | `docs/05.operations/guides/07-workflow/airflow-dag-basics.md`                                            |
| `docs/05.operations/guides/08-ai/01.llm-inference.md`                                   | `docs/98.archive/05.operations/guides/08-ai/01.llm-inference.md`                                   | Duplicate Ollama inference guide with generic template residue and incomplete runbook handoff                                                    | `docs/05.operations/guides/08-ai/ollama.md`                                                              |
| `docs/05.operations/guides/08-ai/local-llm-setup.md`                                    | `docs/98.archive/05.operations/guides/08-ai/local-llm-setup.md`                                    | Duplicate local Ollama setup guide with generic template residue and no active runbook handoff                                                   | `docs/05.operations/guides/08-ai/ollama.md`                                                              |
| `docs/05.operations/guides/09-tooling/01.iac-automation.md`                             | `docs/98.archive/05.operations/guides/09-tooling/01.iac-automation.md`                             | Duplicate Terrakube/Terraform guide with generic template residue and no active runbook handoff                                                  | `docs/05.operations/guides/09-tooling/terrakube.md`; `docs/05.operations/guides/09-tooling/terraform.md` |
| `docs/05.operations/guides/03-security/01.setup.md`                                     | `docs/98.archive/05.operations/guides/03-security/01.setup.md`                                     | Duplicate Vault setup guide with stale service-local compose startup, direct container runtime commands, and generic template residue            | `docs/05.operations/guides/03-security/vault.md`                                                         |
| `docs/05.operations/guides/07-workflow/airbyte.md`                                      | `docs/98.archive/05.operations/guides/07-workflow/airbyte.md`                                      | No tracked Airbyte implementation under `infra/07-workflow/airbyte`                                                                              | `docs/03.specs/008-workflow/spec.md`                                                                     |
| `docs/05.operations/guides/05-messaging/ksql-streaming.md`                              | `docs/98.archive/05.operations/guides/05-messaging/ksql-streaming.md`                              | ksqlDB is currently implemented under `infra/04-data/analytics/ksql`, not under `infra/05-messaging`                                             | `docs/05.operations/guides/04-data/analytics/ksqldb.md`                                                  |
| `docs/05.operations/policies/07-workflow/airbyte.md`                                    | `docs/98.archive/05.operations/policies/07-workflow/airbyte.md`                                    | No tracked Airbyte implementation under `infra/07-workflow/airbyte`                                                                              | `docs/03.specs/008-workflow/spec.md`                                                                     |
| `docs/05.operations/runbooks/07-workflow/airbyte.md`                                    | `docs/98.archive/05.operations/runbooks/07-workflow/airbyte.md`                                    | No tracked Airbyte implementation under `infra/07-workflow/airbyte`                                                                              | `docs/03.specs/008-workflow/spec.md`                                                                     |

### Stage 03 Specification Archive (2026-08-08)

The table below records the source-to-destination mapping for the 32 terminal
(`completed` or `superseded`) Stage 03 specifications relocated into
`docs/98.archive/03.specs/` because forward-pointer tombstones proved
impossible: the metadata validator derives a document's profile from its
path alone and rejects `status: archived` on any path that is not an
archive path, so no tombstone could carry the status that defines it. Each
destination carries full Git provenance (`archived_commit`, `archived_blob`)
under the `evidence-preserve` disposition; see each `spec.md`'s own
`## Archive Metadata` and `## Archive Ledger` sections.

| Original Path                                                               | Archived Path                                                                          |
| --------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `docs/03.specs/099-template-system-numbered-sdlc-paths/spec.md`             | `docs/98.archive/03.specs/099-template-system-numbered-sdlc-paths/spec.md`             |
| `docs/03.specs/100-template-system-contract-standardization/spec.md`        | `docs/98.archive/03.specs/100-template-system-contract-standardization/spec.md`        |
| `docs/03.specs/101-template-system-reorganization/spec.md`                  | `docs/98.archive/03.specs/101-template-system-reorganization/spec.md`                  |
| `docs/03.specs/104-agentic-research-pack-refresh/spec.md`                   | `docs/98.archive/03.specs/104-agentic-research-pack-refresh/spec.md`                   |
| `docs/03.specs/106-workspace-support-surface-contract/spec.md`              | `docs/98.archive/03.specs/106-workspace-support-surface-contract/spec.md`              |
| `docs/03.specs/107-provider-semantic-parity-validator/spec.md`              | `docs/98.archive/03.specs/107-provider-semantic-parity-validator/spec.md`              |
| `docs/03.specs/108-compose-profile-service-coverage-snapshot/spec.md`       | `docs/98.archive/03.specs/108-compose-profile-service-coverage-snapshot/spec.md`       |
| `docs/03.specs/109-gap-routing-recommendation/spec.md`                      | `docs/98.archive/03.specs/109-gap-routing-recommendation/spec.md`                      |
| `docs/03.specs/110-agent-output-eval-fixtures/spec.md`                      | `docs/98.archive/03.specs/110-agent-output-eval-fixtures/spec.md`                      |
| `docs/03.specs/111-qa-gate-recommendation-ci-summary/spec.md`               | `docs/98.archive/03.specs/111-qa-gate-recommendation-ci-summary/spec.md`               |
| `docs/03.specs/112-audit-pack-coverage-report/spec.md`                      | `docs/98.archive/03.specs/112-audit-pack-coverage-report/spec.md`                      |
| `docs/03.specs/113-llm-wiki-stage-category-coverage/spec.md`                | `docs/98.archive/03.specs/113-llm-wiki-stage-category-coverage/spec.md`                |
| `docs/03.specs/114-tech-stack-version-provenance/spec.md`                   | `docs/98.archive/03.specs/114-tech-stack-version-provenance/spec.md`                   |
| `docs/03.specs/115-provider-hook-parity-matrix/spec.md`                     | `docs/98.archive/03.specs/115-provider-hook-parity-matrix/spec.md`                     |
| `docs/03.specs/116-agent-output-eval-runner/spec.md`                        | `docs/98.archive/03.specs/116-agent-output-eval-runner/spec.md`                        |
| `docs/03.specs/117-security-automation-readiness-snapshot/spec.md`          | `docs/98.archive/03.specs/117-security-automation-readiness-snapshot/spec.md`          |
| `docs/03.specs/118-audit-implementation-matrix-snapshot/spec.md`            | `docs/98.archive/03.specs/118-audit-implementation-matrix-snapshot/spec.md`            |
| `docs/03.specs/119-sdlc-document-contract-corpus-normalization/spec.md`     | `docs/98.archive/03.specs/119-sdlc-document-contract-corpus-normalization/spec.md`     |
| `docs/03.specs/120-agent-output-eval-ci-gate/spec.md`                       | `docs/98.archive/03.specs/120-agent-output-eval-ci-gate/spec.md`                       |
| `docs/03.specs/121-dependency-vulnerability-audit-gate/spec.md`             | `docs/98.archive/03.specs/121-dependency-vulnerability-audit-gate/spec.md`             |
| `docs/03.specs/122-agentic-research-pack-consolidation/spec.md`             | `docs/98.archive/03.specs/122-agentic-research-pack-consolidation/spec.md`             |
| `docs/03.specs/123-agentic-engineering-audit-remediation/spec.md`           | `docs/98.archive/03.specs/123-agentic-engineering-audit-remediation/spec.md`           |
| `docs/03.specs/124-compose-runtime-readiness-remediation/spec.md`           | `docs/98.archive/03.specs/124-compose-runtime-readiness-remediation/spec.md`           |
| `docs/03.specs/125-infrastructure-operations-readiness-remediation/spec.md` | `docs/98.archive/03.specs/125-infrastructure-operations-readiness-remediation/spec.md` |
| `docs/03.specs/126-security-supply-chain-remediation/spec.md`               | `docs/98.archive/03.specs/126-security-supply-chain-remediation/spec.md`               |
| `docs/03.specs/127-deployment-release-engineering-remediation/spec.md`      | `docs/98.archive/03.specs/127-deployment-release-engineering-remediation/spec.md`      |
| `docs/03.specs/128-agentic-audit-harness-consolidation/spec.md`             | `docs/98.archive/03.specs/128-agentic-audit-harness-consolidation/spec.md`             |
| `docs/03.specs/129-document-contract-canonicalization/spec.md`              | `docs/98.archive/03.specs/129-document-contract-canonicalization/spec.md`              |
| `docs/03.specs/130-template-contract-system-canonicalization/spec.md`       | `docs/98.archive/03.specs/130-template-contract-system-canonicalization/spec.md`       |
| `docs/03.specs/131-document-corpus-lifecycle-migration-foundation/spec.md`  | `docs/98.archive/03.specs/131-document-corpus-lifecycle-migration-foundation/spec.md`  |
| `docs/03.specs/132-agent-governance-harness-convergence/spec.md`            | `docs/98.archive/03.specs/132-agent-governance-harness-convergence/spec.md`            |
| `docs/03.specs/133-target-surface-contract-convergence/spec.md`             | `docs/98.archive/03.specs/133-target-surface-contract-convergence/spec.md`             |

### End Non-Authoritative Historical Provenance Ledger

## How to Work in This Area

1. 기록 목적에 따라 `change-plan`, `change-task`, `tombstone`, `migration` 중
   하나의 profile과 stable target을 선택합니다.
2. 승인된 manifest, source identity, consumers, replacement, Git provenance,
   confidentiality evidence를 검증합니다.
3. [archive template](../99.templates/templates/common/archive.template.md)로
   작성하고 metadata 및 path identity gate를 통과합니다.
4. Active 문서는 Stage 98을 current guidance로 링크하지 않습니다.
5. Retired 경로의 조회에는 위의 bounded ledger와 Git provenance만 사용합니다.

## Related Documents

- [docs index](../README.md)
- [stage authoring matrix](../00.agent-governance/rules/stage-authoring-matrix.md)
- [documentation protocol](../00.agent-governance/rules/documentation-protocol.md)
- [archive template](../99.templates/templates/common/archive.template.md)
- [document corpus migration contract](../99.templates/support/document-corpus-migration-contract.yaml)
- [metadata profiles](../99.templates/support/document-metadata-profiles.yaml)
- [archive and retention contract](../99.templates/support/archive-retention-contract.md)
