---
status: completed
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
  - Attachment gap coverage for clarification duty, concept inventory, template deviation audit, Codex harness alignment, model policy, and evidence closure.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Do not rewrite completed Phase 1/2/3/4 historical artifacts as incidental cleanup.
  - Do not make HADS mandatory.
  - Do not promote new Docker hard validators without a separate approval gate.
  - Do not retire `.codex/agents/*.md` compatibility prompt files.
- **Out of Scope**:
  - Stage 00 architecture replacement, template source rewrites, validator edits, and Codex TOML adapter edits that are not backed by existing policy and validator evidence.
  - Docker service start/stop/recreate, image rebuilds, migrations, deployment, or live network changes.
  - Secrets, credential values, private keys, shell history, token-bearing logs, remote GitHub settings, or user-global Codex settings.

## Attachment Gap Coverage

The attached decision scope is treated as an input contract for the continuation work. Items not present in the initial decision-items plan are covered by the WBS rows below rather than by rewriting completed Phase 1/2 historical evidence.

| Attached Requirement | Current Coverage | Coverage WBS | Required Evidence |
| --- | --- | --- | --- |
| Treat ambiguity and conflicting constraints as blocking before planning, implementation, model/config changes, or completion. | Partially covered by `Clarification Duty` and task checklists. | PLN-DI-009 | Stage 00 completion/pre-task checklist text and Codex provider boundary. |
| Inventory Agent, Skill, Rule, Hook, Sub-agent, Output Style, Workflow, Memory, QA/CI/CD, Model Policy, and Template Contract from current to desired governance state. | Core concepts existed, but lacked an explicit current-to-desired matrix. | PLN-DI-010 | Stage 00 governance coverage matrix. |
| Audit `docs/01`-`docs/05`, `docs/90`, and `docs/99` template deviation handling without broad rewrites. | Template mapping existed; exception evidence criteria were implicit. | PLN-DI-011 | Documentation protocol, Stage Authoring Matrix, and template README exception criteria. |
| Align Skill / `SKILL.md` lifecycle terminology with Stage 00 function catalog. | Skill surfaces were identified; lifecycle stages were not named consistently in one gate. | PLN-DI-012 | Workflow lifecycle gate plus Codex runtime surface notes. |
| Align `AGENTS.md`, `.codex/README.md`, `.codex/agents/*.toml`, and `.codex/agents/*.md` with Stage 00 harness rules. | Codex provider notes covered most boundaries; root and runtime README needed explicit gate wording. | PLN-DI-013 | Root shim and Codex runtime README alignment notes; adapter drift checks. |
| Keep Model Policy and `model_reasoning_effort` changes behind validation/uncertainty gates. | Model policy existed in Stage 00 and Codex notes. | PLN-DI-014 | Provider notes and checklist gates; no model/reasoning edits without validator support. |
| Define QA/CI/CD local checks, CI-only gates, hooks/scripts, and skipped-check rationale by change type. | QA and GitHub docs had local/remote boundary but lacked a change-type matrix. | PLN-DI-015 | QA scope and GitHub governance matrices; task evidence records skipped-check rationale. |
| Close PLAN/TASK/progress traceability for this continuation. | Initial plan existed; task evidence was not yet created. | PLN-DI-016 | Task evidence document, plan/task README links, progress log, and LLM Wiki freshness. |

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
| PLN-DI-009 | Make clarification duty a blocking gate before risky planning, implementation, model/config changes, and completion claims. | `docs/00.agent-governance/README.md`, `rules/task-checklists.md`, `providers/codex.md`, `AGENTS.md` | REQ-AGG-NFR-01 | Checklists and provider notes require clarification or explicit assumption evidence before state changes when ambiguity can affect outcome. |
| PLN-DI-010 | Add a current-to-desired governance coverage matrix for Agent, Skill, Rule, Hook, Sub-agent, Output Style, Workflow, Memory, QA/CI/CD, Model Policy, and Template Contract. | `docs/00.agent-governance/README.md` | REQ-AGG-FUN-01 | Matrix keeps Stage 00 as SSoT and identifies desired enforcement/evidence for each concept. |
| PLN-DI-011 | Define template deviation audit and exception criteria for `docs/01`-`docs/05`, `docs/90`, and `docs/99`. | `rules/documentation-protocol.md`, `rules/stage-authoring-matrix.md`, `docs/99.templates/README.md` | REQ-AGG-FUN-05 | Deviations require file, expected template, reason, approval/evidence owner, and validation evidence in task records. |
| PLN-DI-012 | Standardize Skill / `SKILL.md` lifecycle wording: discovery -> applicability -> provider loading -> canonical artifact -> validation evidence. | `rules/workflows.md`, `agents/README.md`, `.codex/README.md`, provider notes | REQ-AGG-FUN-04 | Function catalog and provider skill surfaces use the same lifecycle terms without making provider skill files the governance source. |
| PLN-DI-013 | Align Codex harness surfaces while keeping `.codex/agents/*.md` as compatibility prompts and `.codex/agents/*.toml` as validated adapter definitions. | `AGENTS.md`, `.codex/README.md`, `providers/codex.md` | REQ-AGG-FUN-02 | Harness docs state Stage 00 wins over provider Markdown and TOML must pass model/reasoning validator policy. |
| PLN-DI-014 | Preserve Model Policy and `model_reasoning_effort` uncertainty gates. | `providers/codex.md`, `rules/task-checklists.md`, `subagent-protocol.md` | REQ-AGG-NFR-02 | No model/reasoning changes occur unless Stage 00 policy, sync script, and validator encode the same permitted value. |
| PLN-DI-015 | Add QA/CI/CD command, hook, script, CI-only, and skipped-check rationale matrix by change type. | `scopes/qa.md`, `rules/github-governance.md`, task evidence conventions | REQ-AGG-FUN-07 | Change types map to local checks, CI-only gates, hook/script evidence, and explicit skip rationale. |
| PLN-DI-016 | Close PLAN/TASK/progress evidence traceability for this continuation. | `docs/04.execution/tasks/2026-06-02-agent-governance-missing-items-implementation.md`, plan/task READMEs, `memory/progress.md`, LLM Wiki index | REQ-AGG-NFR-05 | Task evidence, indexes, progress log, and LLM Wiki index are updated and validated. |

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
| VAL-DI-008 | Baseline | Validate quickwin and template-security baselines. | `bash scripts/validation/check-quickwin-baseline.sh`; `bash scripts/validation/check-template-security-baseline.sh` | PASS. |
| VAL-DI-009 | Attachment Gap | Confirm the attached requirements are represented in WBS and evidence. | Manual review of this plan and task evidence | Each attached requirement maps to PLN-DI-009 through PLN-DI-016 or an explicit out-of-scope approval gate. |
| VAL-DI-010 | Model/Prompt Safety | Scan governance and Codex surfaces for unsupported model names and unresolved placeholders. | `rg -n "gpt-5\\.1\|gemini-3-pro\|unsupported\|TBD\|TODO" docs/00.agent-governance .codex AGENTS.md docs/04.execution` | No blocking unresolved model/prompt placeholders in changed scope; any historical or advisory hit is recorded. |
| VAL-DI-011 | Provider Drift | Re-run provider sync after Codex/Stage 00 documentation changes. | `bash scripts/operations/sync-provider-surfaces.sh` | No generated drift, or generated changes are inspected and recorded. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Historical Phase 1/2 evidence is overwritten while trying to update current facts. | High | Add continuation/addendum artifacts and indexes; do not rewrite completed artifacts unless explicitly approved. |
| Stage 00 adapter architecture is redesigned unnecessarily. | High | Preserve ADR-0027 and focus only on drift-check clarity and validation coverage. |
| HADS rollout creates broad document churn. | High | Keep HADS advisory; use `docs/90.references` pilot only after separate approval. |
| Docker hardening guidance breaks existing services if converted directly into hard validators. | High | Promote only repo-proven, low-risk checks; leave compatibility-sensitive items as manual review boundaries. |
| QA/CI/CD rules become too heavy for docs-only or policy-only changes. | Medium | Define change-type-specific verification and require skipped-check rationale. |
| Node automation works interactively but fails in agent shells. | Medium | Use explicit `/home/hy/.local/bin` PATH handling or `scripts/operations/use-qa-ci-tools.sh`. |
| Codex harness alignment accidentally retires compatibility Markdown prompts. | Medium | Keep `.codex/agents/*.md` as compatibility prompt context until a separate approved retirement plan exists. |
| Model alias or reasoning-effort values drift ahead of validators. | High | Treat model/reasoning changes as blocked unless Stage 00 policy, sync script, and validators all encode the same value. |
| Template deviation cleanup causes broad historical churn. | Medium | Record deviations and exceptions in task evidence; do not rewrite already-valid historical artifacts. |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Future implementation must pass repo contracts, doc traceability, provider sync, LLM Wiki freshness, diff hygiene, and Graphify health reporting.
- **Sandbox / Canary Rollout**: N/A for this plan. Runtime Docker canary is required only if a later approved implementation changes Compose behavior or live services.
- **Human Approval Gate**: Required before HADS mandatory rollout, Docker hard-validator promotion, Codex Markdown prompt retirement, Stage 00 policy changes, validator changes, runtime changes, deployment changes, or remote GitHub protection changes.
- **Rollback Trigger**: Revert the follow-up implementation if it creates duplicate governance, weakens Stage 00 authority, introduces unapproved hard gates, or breaks provider parity.
- **Prompt / Model Promotion Criteria**: No model, model alias, or reasoning-effort value changes are part of this plan.

## Completion Criteria

- [x] Phase 1/2 historical evidence remains preserved.
- [x] Current-state correction path is documented through continuation artifacts.
- [x] Stage 00 adapter model remains canonical and drift checks are not weakened.
- [x] Skill lifecycle, HADS, Docker hardening, QA/CI/CD, and Node automation decisions are mapped to concrete follow-up tasks.
- [x] Attachment gap coverage is mapped to PLN-DI-009 through PLN-DI-016 or explicit human approval gates.
- [x] Stage 00, Codex runtime notes, and task evidence state clarification duty, model/reasoning gates, template deviation handling, and QA/CI/CD change-type evidence.
- [x] Verification commands pass or record explicit skipped-check rationale.
- [x] Required README and progress log entries are current.

## Related Documents

- **PRD**: [Agent Governance Standardization Product Requirements](../../01.requirements/2026-06-01-agent-governance-standardization.md)
- **ARD**: [Agent Governance Canonical Adapter ARD](../../02.architecture/requirements/0027-agent-governance-canonical-adapter.md)
- **ADR**: [ADR-0027: Stage 00 Canonical Adapter Model](../../02.architecture/decisions/0027-stage-00-canonical-adapter-model.md)
- **Phase 1 Diagnostic**: [Agent Governance Phase 1 Diagnostic](./2026-06-01-agent-governance-phase1-diagnostic.md)
- **Phase 2 Alignment Plan**: [Agent Governance Phase 2 Alignment Plan](./2026-06-01-agent-governance-phase2-alignment.md)
- **Phase 3 Strategy Task**: [Agent Governance Phase 3 Strategy Integration Task](../tasks/2026-06-01-agent-governance-phase3-strategy-integration.md)
- **Missing Items Implementation Task**: [Agent Governance Missing Items Implementation Task](../tasks/2026-06-02-agent-governance-missing-items-implementation.md)
- **Stage 00 Governance Hub**: [AI Agent Governance Hub](../../00.agent-governance/README.md)
- **Stage Authoring Matrix**: [Stage Authoring Matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Documentation Protocol**: [Documentation Protocol](../../00.agent-governance/rules/documentation-protocol.md)
- **Codex Provider Notes**: [Codex Provider Notes](../../00.agent-governance/providers/codex.md)
- **Operations Index**: [Operations index](../../05.operations/README.md)
