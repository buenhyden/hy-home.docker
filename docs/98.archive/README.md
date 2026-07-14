---
layer: archive
---
<!-- Target: docs/98.archive/README.md -->

# 98.archive

> 현재 구현과 상충해 active chain에서 제거한 old, deprecated, legacy 문서의 tombstone stage입니다.

## Overview

`docs/98.archive/`는 원문 보존 공간이 아니라 migration 추적 공간입니다.
Archive tombstone은 원래 문서 경로, archive 사유, 현재 대체 문서만 기록하고
stale 본문을 다시 노출하지 않습니다.

## Audience

- Documentation Writers
- AI Agents
- Repository Maintainers

## Scope

### In Scope

- 현재 구현과 상충해 active chain에서 제거한 whole-document tombstone
- 원래 경로와 대체 문서 추적
- archive migration ledger
- 검증된 provenance tombstone과 승인된 immutable evidence snapshot 경로

### Out of Scope

- 현재 판단 기준으로 사용할 요구사항, 설계, spec, plan, task, 운영 절차
- 원문 stale body 보존
- active 문서의 Related Documents 대상

## Structure

```text
98.archive/
├── 01.requirements/     # Stage 01에서 제거된 문서 tombstone
├── 02.architecture/     # Stage 02에서 제거된 문서 tombstone
├── 03.specs/            # Stage 03에서 제거된 문서 tombstone
├── 04.execution/        # Stage 04에서 제거된 문서 tombstone
├── 05.operations/       # Stage 05에서 제거된 문서 tombstone
└── README.md            # This file
```

## Migration Ledger

아래 표는 현재 `hand-maintained`이며 `transitional until Wave D`입니다.
Generated ledger라고 주장하지 않으며, Wave D에서 기존 tombstone의 provenance를
정비하고 canonical lifecycle generator를 승인하기 전까지 이 상태를 유지합니다.
분류와 증거 조건은
[corpus migration contract](../99.templates/support/corpus-migration-contract.md),
archive provenance와 retention 조건은
[archive and retention contract](../99.templates/support/archive-retention-contract.md)를
따릅니다.

| Original Path | Archive Path | Reason | Current Replacement |
| --- | --- | --- | --- |
| `docs/04.execution/plans/2026-05-30-ai-governance-reorg.md` | `docs/98.archive/04.execution/plans/2026-05-30-ai-governance-reorg.md` | Original plan claimed legacy `.agents/` removal and superseded provider-adapter assumptions that conflict with tracked `.agents/` implementation | `docs/04.execution/plans/2026-06-02-agent-governance-decision-items-plan.md` |
| `docs/04.execution/plans/2026-05-30-standardizing-agent-governance.md` | `docs/98.archive/04.execution/plans/2026-05-30-standardizing-agent-governance.md` | Original plan required `.codex/agents/*.md` YAML frontmatter and prohibited TOML, conflicting with TOML-only Codex adapters | `docs/04.execution/plans/2026-06-02-agent-governance-decision-items-plan.md` |
| `docs/04.execution/plans/2026-06-01-agent-governance-phase1-diagnostic.md` | `docs/98.archive/04.execution/plans/2026-06-01-agent-governance-phase1-diagnostic.md` | Diagnostic treated Codex Markdown prompts and broad HADS advisory status as active unresolved decisions | `docs/04.execution/plans/2026-06-02-agent-governance-decision-items-plan.md` |
| `docs/04.execution/plans/2026-06-01-agent-governance-phase2-alignment.md` | `docs/98.archive/04.execution/plans/2026-06-01-agent-governance-phase2-alignment.md` | Plan preserved Codex Markdown compatibility prompts and broad HADS advisory-only decisions that conflict with current implementation | `docs/04.execution/plans/2026-06-02-agent-governance-decision-items-plan.md` |
| `docs/04.execution/tasks/2026-05-30-standardizing-agent-governance.md` | `docs/98.archive/04.execution/tasks/2026-05-30-standardizing-agent-governance.md` | Task evidence recorded `.codex/agents/*.md` YAML frontmatter as the preserved Codex harness shape | `docs/04.execution/tasks/2026-06-02-agent-governance-missing-items-implementation.md` |
| `docs/04.execution/tasks/2026-06-01-agent-governance-phase1-diagnostic.md` | `docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase1-diagnostic.md` | Task pointed at obsolete Codex Markdown prompt and broad HADS advisory assumptions | `docs/04.execution/tasks/2026-06-02-agent-governance-missing-items-implementation.md` |
| `docs/04.execution/tasks/2026-06-01-agent-governance-phase3-implementation.md` | `docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase3-implementation.md` | Task depended on the archived Phase 2 plan as parent evidence | `docs/04.execution/tasks/2026-06-02-agent-governance-missing-items-implementation.md` |
| `docs/04.execution/tasks/2026-06-01-agent-governance-stage01-02-alignment.md` | `docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-stage01-02-alignment.md` | Task was tied to the archived Phase 2 alignment chain and pre-closure HADS/Codex boundaries | `docs/04.execution/tasks/2026-06-02-agent-governance-missing-items-implementation.md` |
| `docs/04.execution/tasks/2026-06-01-agent-governance-phase3-stage01-02-continuation.md` | `docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase3-stage01-02-continuation.md` | Task preserved pre-closure non-goals for HADS, Codex Markdown prompts, and hard validators | `docs/04.execution/tasks/2026-06-02-agent-governance-missing-items-implementation.md` |
| `docs/04.execution/tasks/2026-06-01-agent-governance-phase3-strategy-integration.md` | `docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase3-strategy-integration.md` | Task recorded HADS as advisory-only and `.codex/agents/*.md` as compatibility prompts | `docs/04.execution/tasks/2026-06-02-agent-governance-missing-items-implementation.md` |
| `docs/04.execution/tasks/2026-06-01-agent-governance-phase4-closure.md` | `docs/98.archive/04.execution/tasks/2026-06-01-agent-governance-phase4-closure.md` | Closure preserved non-goals that were later approved and implemented | `docs/04.execution/tasks/2026-06-02-agent-governance-missing-items-implementation.md` |
| `docs/05.operations/guides/07-workflow/01.airflow-dag-dev.md` | `docs/98.archive/05.operations/guides/07-workflow/01.airflow-dag-dev.md` | Duplicate DAG guide retained stale repo-local DAG path guidance; active guide now uses `${DEFAULT_WORKFLOW_DIR}/airflow/dags` | `docs/05.operations/guides/07-workflow/airflow-dag-basics.md` |
| `docs/05.operations/guides/08-ai/01.llm-inference.md` | `docs/98.archive/05.operations/guides/08-ai/01.llm-inference.md` | Duplicate Ollama inference guide with generic template residue and incomplete runbook handoff | `docs/05.operations/guides/08-ai/ollama.md` |
| `docs/05.operations/guides/08-ai/local-llm-setup.md` | `docs/98.archive/05.operations/guides/08-ai/local-llm-setup.md` | Duplicate local Ollama setup guide with generic template residue and no active runbook handoff | `docs/05.operations/guides/08-ai/ollama.md` |
| `docs/05.operations/guides/09-tooling/01.iac-automation.md` | `docs/98.archive/05.operations/guides/09-tooling/01.iac-automation.md` | Duplicate Terrakube/Terraform guide with generic template residue and no active runbook handoff | `docs/05.operations/guides/09-tooling/terrakube.md`; `docs/05.operations/guides/09-tooling/terraform.md` |
| `docs/05.operations/guides/03-security/01.setup.md` | `docs/98.archive/05.operations/guides/03-security/01.setup.md` | Duplicate Vault setup guide with stale service-local compose startup, direct container runtime commands, and generic template residue | `docs/05.operations/guides/03-security/vault.md` |
| `docs/05.operations/guides/07-workflow/airbyte.md` | `docs/98.archive/05.operations/guides/07-workflow/airbyte.md` | No tracked Airbyte implementation under `infra/07-workflow/airbyte` | `docs/03.specs/008-workflow/spec.md` |
| `docs/05.operations/guides/05-messaging/ksql-streaming.md` | `docs/98.archive/05.operations/guides/05-messaging/ksql-streaming.md` | ksqlDB is currently implemented under `infra/04-data/analytics/ksql`, not under `infra/05-messaging` | `docs/05.operations/guides/04-data/analytics/ksqldb.md` |
| `docs/05.operations/policies/07-workflow/airbyte.md` | `docs/98.archive/05.operations/policies/07-workflow/airbyte.md` | No tracked Airbyte implementation under `infra/07-workflow/airbyte` | `docs/03.specs/008-workflow/spec.md` |
| `docs/05.operations/runbooks/07-workflow/airbyte.md` | `docs/98.archive/05.operations/runbooks/07-workflow/airbyte.md` | No tracked Airbyte implementation under `infra/07-workflow/airbyte` | `docs/03.specs/008-workflow/spec.md` |

## How to Work in This Area

1. 승인된 manifest에서 대상과 소비자, 대체 문서, 보존 근거를 검토합니다.
2. Git provenance와 confidentiality 검증을 통과한 결과만 canonical Archive template로 작성합니다.
3. Active 문서는 tombstone을 current guidance로 역링크하지 않습니다.
4. Wave D 전에는 이 hand-maintained ledger를 Task 근거와 함께 갱신하며 generated output이라고 표시하지 않습니다.

## Related Documents

- [docs index](../README.md)
- [stage authoring matrix](../00.agent-governance/rules/stage-authoring-matrix.md)
- [documentation protocol](../00.agent-governance/rules/documentation-protocol.md)
- [archive template](../99.templates/templates/common/archive.template.md)
- [corpus migration contract](../99.templates/support/corpus-migration-contract.md)
- [archive and retention contract](../99.templates/support/archive-retention-contract.md)
