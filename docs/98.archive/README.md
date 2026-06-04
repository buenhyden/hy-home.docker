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
| `docs/05.operations/guides/07-workflow/airbyte.md` | `docs/98.archive/05.operations/guides/07-workflow/airbyte.md` | No tracked Airbyte implementation under `infra/07-workflow/airbyte` | `docs/03.specs/07-workflow/spec.md` |
| `docs/05.operations/guides/05-messaging/ksql-streaming.md` | `docs/98.archive/05.operations/guides/05-messaging/ksql-streaming.md` | ksqlDB is currently implemented under `infra/04-data/analytics/ksql`, not under `infra/05-messaging` | `docs/05.operations/guides/04-data/analytics/ksqldb.md` |
| `docs/05.operations/policies/07-workflow/airbyte.md` | `docs/98.archive/05.operations/policies/07-workflow/airbyte.md` | No tracked Airbyte implementation under `infra/07-workflow/airbyte` | `docs/03.specs/07-workflow/spec.md` |
| `docs/05.operations/runbooks/07-workflow/airbyte.md` | `docs/98.archive/05.operations/runbooks/07-workflow/airbyte.md` | No tracked Airbyte implementation under `infra/07-workflow/airbyte` | `docs/03.specs/07-workflow/spec.md` |

## How to Work in This Area

1. Archive 전 `rg`로 active 참조를 확인하고 제거합니다.
2. 원래 문서는 같은 상대 구조로 `docs/98.archive/<original-stage>/...`에 tombstone으로 이동합니다.
3. Tombstone은 `docs/99.templates/archive.template.md`를 따르고 원문 본문을 보존하지 않습니다.
4. Active 문서에서는 archive tombstone으로 역링크하지 않습니다.
5. 이 README의 Migration Ledger를 갱신합니다.

## Related Documents

- [docs index](../README.md)
- [stage authoring matrix](../00.agent-governance/rules/stage-authoring-matrix.md)
- [documentation protocol](../00.agent-governance/rules/documentation-protocol.md)
- [archive template](../99.templates/archive.template.md)
