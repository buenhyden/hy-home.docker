---
status: active
---
<!-- Target: docs/04.execution/plans/2026-06-02-agent-governance-decision-items-plan.md -->

# Agent Governance Decision Items Implementation Plan

## Overview (KR)

이 문서는 Agent Governance Phase 1 진단과 후속 Stage 01/02/04 정렬 이후 남은 결정 항목을 실행 가능한 후속 로드맵으로 정리한다.

기존 completed Phase 1/2 문서는 historical baseline으로 보존한다. 이 plan은 현재 `main` 기준으로 필요한 보정, 인덱싱, 정책 경계 정리, 검증 기준을 별도 continuation plan으로 고정한다.

## Context

Phase 1 diagnostic은 Stage 00 canonical adapter model, provider runtime surfaces, Docker/QA/CI/CD scopes, Graphify advisory report, and `/home/hy/.local/bin` Node/npm/rtk facts를 확인했다. 이후 Stage 01/02 alignment가 추가되어 Agent Governance PRD, canonical adapter ARD, and Stage 00 canonical adapter ADR traceability gap은 닫힌 상태다.

이번 plan은 남은 결정 항목을 구현 단계로 넘기기 위한 실행 설계다. 즉시 Stage 00 policy, templates, validators, Docker runtime, Codex adapter, remote GitHub state, or user-global Codex settings를 변경하지 않는다.

Graphify remains advisory when `report-graphify-health.sh` reports `surprising_cross_root_inferred_edges`; architecture and completion claims must be corroborated against tracked Stage 00 docs, stage docs, and repository validators.

## Goals & In-Scope

- **Goals**:
  - Preserve Phase 1/2 historical evidence while adding current-state correction paths.
  - Convert remaining decision items into sequenced, approval-gated execution work.
  - Keep Stage 00 as the canonical policy and adapter catalog source.
  - Define verification evidence required before any later implementation is considered complete.
- **In Scope**:
  - Stage 04 plan/task index improvements.
  - Stage 00 drift-checking and provider adapter parity planning.
  - Skill lifecycle, HADS pilot, Docker hardening boundary, QA/CI/CD matrix, and Node toolchain automation planning.
  - Documentation-only updates to plan and index surfaces.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Do not rewrite completed Phase 1/2/3/4 historical artifacts as incidental cleanup.
  - Do not make HADS mandatory.
  - Do not promote new Docker hard validators without a separate approval gate.
  - Do not retire `.codex/agents/*.md` compatibility prompt files.
- **Out of Scope**:
  - Stage 00 policy edits, template edits, validator edits, and Codex TOML adapter edits in this plan-writing task.
  - Docker service start/stop/recreate, image rebuilds, migrations, deployment, or live network changes.
  - Secrets, credential values, private keys, shell history, token-bearing logs, remote GitHub settings, or user-global Codex settings.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-DI-001 | Preserve the completed Phase 1 historical baseline and add a current-state correction path instead of editing old evidence. | Future Stage 04 addendum or task evidence, `docs/04.execution/plans/README.md` | REQ-AGG-MET-01 | New work links to Phase 1 diagnostic, Phase 2 alignment plan, PRD, ARD, and ADR without rewriting completed evidence. |
| PLN-DI-002 | Keep the Stage 00 canonical adapter model; plan drift-check hardening rather than architecture replacement. | `docs/00.agent-governance/providers/agents-md.md`, `subagent-protocol.md`, `scripts/operations/sync-provider-surfaces.sh`, `scripts/validation/check-repo-contracts.sh` | REQ-AGG-FUN-01, REQ-AGG-FUN-02 | Provider sync reports no drift and any new adapter rule maps back to Stage 00. |
| PLN-DI-003 | Define the skill lifecycle as discovery -> applicability -> provider loading -> canonical artifact -> validation evidence. | `docs/00.agent-governance/rules/workflows.md`, `rules/task-checklists.md`, provider notes, skill adapter docs | REQ-AGG-FUN-04 | Skill guidance distinguishes workspace functions, provider adapters, and external strategy skills without creating a second governance layer. |
| PLN-DI-004 | Add a curated Stage 04 execution evidence index or summary for governance/audit plans. | `docs/04.execution/plans/README.md`, `docs/04.execution/tasks/README.md`, optional future Stage 04 summary | REQ-AGG-NFR-05 | Historical artifacts remain linked, and readers can find current canonical governance evidence without broad rewrites. |
| PLN-DI-005 | Keep HADS advisory by default and design only an optional `docs/90.references` pilot unless separately approved. | `docs/90.references/`, `docs/00.agent-governance/rules/documentation-protocol.md`, `docs/99.templates/README.md` | REQ-AGG-FUN-05 | No active template or stage document requires HADS block tags unless a future approved rollout changes the contract. |
| PLN-DI-006 | Split Docker hardening expectations into hard validators and manual review boundaries. | `docs/00.agent-governance/scopes/infra.md`, `scopes/security.md`, `scripts/hardening/`, `scripts/validation/` | REQ-AGG-FUN-06 | New checks fail only on repo-proven rules; service-specific or compatibility-sensitive guidance remains manual review. |
| PLN-DI-007 | Define a QA/CI/CD matrix by change type: local check, CI-only gate, skipped-check rationale, and required evidence. | `docs/00.agent-governance/scopes/qa.md`, `rules/github-governance.md`, `scripts/README.md`, task evidence conventions | REQ-AGG-FUN-07 | Docs-only, policy-only, behavior, runtime, and CI changes each map to the smallest meaningful verification set. |
| PLN-DI-008 | Standardize Node/npm/rtk automation assumptions around explicit PATH handling or the QA/CI tooling shim. | `scripts/operations/use-qa-ci-tools.sh`, `scripts/README.md`, future automation docs | REQ-AGG-FUN-08 | Non-interactive shell examples use `/home/hy/.local/bin` explicitly or source the tooling shim before Node-based commands. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-DI-001 | Hygiene | Confirm Markdown diff has no whitespace errors. | `git diff --check` | No output and zero exit status. |
| VAL-DI-002 | Structural | Validate repository contracts after adding the plan and README/progress links. | `bash scripts/validation/check-repo-contracts.sh` | PASS with `failures=0`. |
| VAL-DI-003 | Traceability | Validate execution/operations traceability contracts. | `bash scripts/validation/check-doc-traceability.sh` | PASS with `failures=0`. |
| VAL-DI-004 | Provider | Confirm provider adapters remain synchronized. | `bash scripts/operations/sync-provider-surfaces.sh` | PASS with `no drift`. |
| VAL-DI-005 | Knowledge Index | Confirm the generated LLM Wiki index is fresh. | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS. |
| VAL-DI-006 | Graph Boundary | Record Graphify health and advisory reasons. | `bash scripts/knowledge/report-graphify-health.sh` | Status recorded; advisory status does not block when corroborated against tracked docs. |
| VAL-DI-007 | Scope Safety | Confirm no runtime, secret, deployment, remote GitHub, or user-global Codex state was changed. | `git status --short --branch` and command audit | Only approved documentation files changed. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Historical Phase 1/2 evidence is overwritten while trying to update current facts. | High | Add continuation/addendum artifacts and indexes; do not rewrite completed artifacts unless explicitly approved. |
| Stage 00 adapter architecture is redesigned unnecessarily. | High | Preserve ADR-0027 and focus only on drift-check clarity and validation coverage. |
| HADS rollout creates broad document churn. | High | Keep HADS advisory; use `docs/90.references` pilot only after separate approval. |
| Docker hardening guidance breaks existing services if converted directly into hard validators. | High | Promote only repo-proven, low-risk checks; leave compatibility-sensitive items as manual review boundaries. |
| QA/CI/CD rules become too heavy for docs-only or policy-only changes. | Medium | Define change-type-specific verification and require skipped-check rationale. |
| Node automation works interactively but fails in agent shells. | Medium | Use explicit `/home/hy/.local/bin` PATH handling or `scripts/operations/use-qa-ci-tools.sh`. |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Future implementation must pass repo contracts, doc traceability, provider sync, LLM Wiki freshness, diff hygiene, and Graphify health reporting.
- **Sandbox / Canary Rollout**: N/A for this plan. Runtime Docker canary is required only if a later approved implementation changes Compose behavior or live services.
- **Human Approval Gate**: Required before HADS mandatory rollout, Docker hard-validator promotion, Codex Markdown prompt retirement, Stage 00 policy changes, validator changes, runtime changes, deployment changes, or remote GitHub protection changes.
- **Rollback Trigger**: Revert the follow-up implementation if it creates duplicate governance, weakens Stage 00 authority, introduces unapproved hard gates, or breaks provider parity.
- **Prompt / Model Promotion Criteria**: No model, model alias, or reasoning-effort value changes are part of this plan.

## Completion Criteria

- [ ] Phase 1/2 historical evidence remains preserved.
- [ ] Current-state correction path is documented through continuation artifacts.
- [ ] Stage 00 adapter model remains canonical and drift checks are not weakened.
- [ ] Skill lifecycle, HADS, Docker hardening, QA/CI/CD, and Node automation decisions are mapped to concrete follow-up tasks.
- [ ] Verification commands pass or record explicit skipped-check rationale.
- [ ] Required README and progress log entries are current.

## Related Documents

- **PRD**: [Agent Governance Standardization Product Requirements](../../01.requirements/2026-06-01-agent-governance-standardization.md)
- **ARD**: [Agent Governance Canonical Adapter ARD](../../02.architecture/requirements/0027-agent-governance-canonical-adapter.md)
- **ADR**: [ADR-0027: Stage 00 Canonical Adapter Model](../../02.architecture/decisions/0027-stage-00-canonical-adapter-model.md)
- **Phase 1 Diagnostic**: [Agent Governance Phase 1 Diagnostic](./2026-06-01-agent-governance-phase1-diagnostic.md)
- **Phase 2 Alignment Plan**: [Agent Governance Phase 2 Alignment Plan](./2026-06-01-agent-governance-phase2-alignment.md)
- **Phase 3 Strategy Task**: [Agent Governance Phase 3 Strategy Integration Task](../tasks/2026-06-01-agent-governance-phase3-strategy-integration.md)
- **Stage 00 Governance Hub**: [AI Agent Governance Hub](../../00.agent-governance/README.md)
- **Stage Authoring Matrix**: [Stage Authoring Matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Documentation Protocol**: [Documentation Protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Codex Provider Notes**: [Codex Provider Notes](../../00.agent-governance/providers/codex.md)
- **Operations Index**: [Operations index](../../05.operations/README.md)
