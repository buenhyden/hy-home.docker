---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-06-02-agent-governance-phase-2-strategy-integration.md -->

# Agent Governance Phase 2 Strategy Integration Plan

## Overview (KR)

이 문서는 Agent Governance Phase 1 revalidation에서 확인한 후속 항목을 Phase 2 실행 evidence로 닫는 계획서다.

Phase 2는 새 정책 체계나 adapter 모델을 만들지 않는다. 현행 Stage 00 canonical adapter, skill lifecycle, QA/CI matrix, Codex tooling shim, Docker hard/manual gate 경계가 이미 구현되어 있으므로, Phase 1 backlog를 현재 구현 사실에 맞게 disposition하고 Stage 04 evidence로 정리한다.

## Context

Phase 1 revalidation recorded the current Agent Governance baseline:

- Stage 00 remains the governance SSoT and canonical adapter catalog.
- ADR-0027 remains the accepted architecture for the Stage 00 canonical adapter model.
- External skills are governance/process lenses, not separate active document taxonomies.
- Docker and DevOps expectations are split between repo-proven hard gates and manual review boundaries.
- QA/CI/CD evidence is defined by change type, with local checks, CI-only gates, and skipped-check rationale.
- Node/npm/rtk automation must use explicit `/home/hy/.local/bin` paths or `scripts/operations/use-qa-ci-tools.sh` in non-interactive shells.
- Graphify is useful for navigation but advisory while cross-root inferred edges remain.

This plan converts those observations into a bounded Stage 04 closure artifact without editing Stage 00 policy, provider adapters, runtime infrastructure, secrets, deployment state, remote GitHub state, model policy, or broad HADS scope.

## Goals & In-Scope

- **Goals**:
  - Close Phase 1 backlog disposition in Stage 04 execution evidence.
  - Confirm already-satisfied items against current Stage 00 and Stage 04 records.
  - Record minor cleanup closure and design follow-up closure without reopening completed artifacts.
  - Keep redesign candidates deferred behind separate approval gates.
  - Map the requested skill groups to current workflow/process lenses.
- **In Scope**:
  - New Phase 2 plan/task artifacts under canonical Stage 04 paths.
  - Stage 04 plan/task README entries.
  - Progress log evidence.
  - LLM Wiki index regeneration because docs are added.
  - Graphify refresh and advisory health recording when the CLI is available.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Do not rewrite Stage 00 policy or ADR-0027.
  - Do not broaden mandatory HADS validation beyond `docs/90.references/hads/`.
  - Do not add a new Docker hard validator in this pass.
  - Do not recreate retired `.codex/agents/*.md` prompt adapters.
  - Do not create active non-stage taxonomies for external skills.
- **Out of Scope**:
  - Docker runtime start/stop/recreate, image rebuilds, migrations, deployments, or live network changes.
  - Secrets, credential files, private keys, shell history, token-bearing logs, or user-global Codex settings.
  - Remote GitHub protection, branch-rule, or deployment mutation.
  - Provider adapter contract, model, or reasoning-effort changes.
  - Broad historical rewrite of completed artifacts.

## Phase 1 Backlog Disposition

| Bucket | Phase 1 Item | Phase 2 Disposition | Evidence Surface |
| --- | --- | --- | --- |
| Already satisfied | Stage 01/02 Agent Governance PRD/ARD/ADR chain | Keep as baseline; no document rewrite. | PRD, ARD, ADR-0027, Phase 1 task evidence. |
| Already satisfied | Provider adapter parity | Re-run provider sync and record `no drift`. | `sync-provider-surfaces.sh`, Codex provider notes. |
| Already satisfied | QA/CI/CD change-type matrix | Treat current QA scope as the active verification contract. | `docs/00.agent-governance/scopes/qa.md`. |
| Already satisfied | Stage 00 canonical adapter model | Preserve ADR-0027 and current Stage 00 ownership. | Governance hub, workflows, provider notes. |
| Minor cleanup closed | Phase 1 evidence discoverability | Dedicated Phase 1 plan/task already close this gap. | Phase 1 revalidation artifacts and README links. |
| Minor cleanup closed | Node/npm/rtk PATH caveat | Keep the tooling shim rule as evidence; no tooling mutation. | Codex provider notes and Phase 1 task evidence. |
| Design follow-up closed by current Stage 00 | Skill strategy absorption | Existing workflow maps external strategies to canonical stages. | `rules/workflows.md` and this Phase 2 task evidence. |
| Design follow-up closed by current Stage 00 | Docker hard/manual gate split | Existing infra scope distinguishes manual review from hard validators. | `scopes/infra.md`, hardening gate evidence. |
| Redesign candidate deferred | Stage 00 adapter replacement | No contradiction found; defer unless ADR-0027 is superseded. | Human approval gate only. |
| Redesign candidate deferred | Broad HADS rollout | No broad rollout in Phase 2; defer to separate rollout plan. | HADS reference profile boundary. |

## Skill Strategy Mapping

| Skill / Strategy Group | Phase 2 Integration |
| --- | --- |
| Superpowers process skills | Use as workflow discipline for brainstorming, planning, executing, verification, and branch finishing; canonical artifacts remain repository stage docs. |
| TDD, debugging, verification skills | Apply through QA scope; docs-only governance work records TDD as N/A with validation evidence. |
| Review skills | Apply through the code-review workflow and git governance, not a parallel review taxonomy. |
| HADS and documentation skills | Keep HADS mandatory only in the approved reference profile; use templates and human-readable prose elsewhere. |
| Docker/container skills | Use as manual review lenses unless a repo-proven validator already enforces the rule. |
| DevOps/CI/CD skills | Map to QA matrix, GitHub governance, secrets boundary, and operations/runbook evidence. |
| Architecture skills | Use for ARD/ADR quality and Stage 00 consistency review; do not replace ADR-0027 here. |
| QA skills | Use for change-type verification, generated-artifact freshness, and explicit skipped-check rationale. |

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-P2-001 | Create the Phase 2 strategy integration plan from the approved user plan and Phase 1 evidence. | `docs/04.execution/plans/2026-06-02-agent-governance-phase-2-strategy-integration.md` | REQ-AGG-MET-01 | Plan uses required template sections, has no placeholders, and links baseline artifacts. |
| PLN-P2-002 | Create the paired task evidence with backlog disposition, skill mapping, verification summary, and scope safety. | `docs/04.execution/tasks/2026-06-02-agent-governance-phase-2-strategy-integration.md` | REQ-AGG-MET-04 | Task records actual evidence without Stage 00, runtime, secret, remote, model, or adapter changes. |
| PLN-P2-003 | Register the new artifacts in Stage 04 indexes and progress log. | Stage 04 READMEs, `memory/progress.md` | REQ-AGG-MET-01 | Indexes and progress log point to the current Phase 2 artifacts. |
| PLN-P2-004 | Refresh generated documentation index because docs are added. | `docs/90.references/llm-wiki/index.md` | REQ-AGG-MET-02 | LLM Wiki regeneration and freshness check pass. |
| PLN-P2-005 | Refresh Graphify when available and run repository validation gates. | `graphify-out/`, task evidence | REQ-AGG-MET-02 | Diff hygiene, repo contracts, doc traceability, provider sync, LLM Wiki, and Graphify health are recorded. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-P2-001 | Hygiene | Confirm Markdown diff has no whitespace errors. | `git diff --check` | No output and zero exit status. |
| VAL-P2-002 | Structural | Validate repository documentation and contract rules. | `bash scripts/validation/check-repo-contracts.sh` | PASS with `failures=0`. |
| VAL-P2-003 | Traceability | Validate execution and operations traceability contracts. | `bash scripts/validation/check-doc-traceability.sh` | PASS with `failures=0`. |
| VAL-P2-004 | Provider | Confirm provider adapters remain synchronized. | `bash scripts/operations/sync-provider-surfaces.sh` | PASS with `no drift`. |
| VAL-P2-005 | Knowledge Index | Refresh and verify generated LLM Wiki index because docs are added. | `bash scripts/knowledge/generate-llm-wiki-index.sh`; `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | Regeneration completes and freshness check passes. |
| VAL-P2-006 | Graph Boundary | Refresh graph output when available and record advisory reason. | `/home/hy/.local/bin/graphify update .`; `bash scripts/knowledge/report-graphify-health.sh` | Graph output refreshed; advisory status is acceptable when corroborated. |
| VAL-P2-007 | Scope Safety | Confirm only task-owned docs/generated evidence changed. | `git status --short` and diff review | No Stage 00 policy, runtime, secret, remote, model, or provider adapter changes. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Phase 2 repeats already completed governance implementation. | Medium | Record disposition against existing Stage 00 and Stage 04 evidence instead of rewriting policy. |
| External skill mapping creates a parallel taxonomy. | Medium | Keep skills as process lenses mapped to canonical stage artifacts. |
| Redesign candidates are treated as approved implementation. | High | Record ADR-0027 replacement and broad HADS rollout as deferred approval-gated work only. |
| Graphify advisory output is treated as authority. | Medium | Corroborate claims against tracked Stage 00 docs, Stage 04 artifacts, and validators. |
| Generated artifacts drift after adding docs. | Medium | Regenerate LLM Wiki and Graphify output, then verify freshness/health. |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Repository validation, doc traceability, provider sync, LLM Wiki freshness, and Graphify health reporting.
- **Sandbox / Canary Rollout**: N/A. This is documentation/evidence-only work.
- **Human Approval Gate**: Required before any later Stage 00 policy rewrite, broad HADS rollout, Docker/runtime mutation, new Docker hard validator, model policy change, provider adapter redesign, remote GitHub mutation, or secrets access.
- **Rollback Trigger**: Revert this artifact set if it weakens Stage 00 authority, creates duplicate active taxonomy, or breaks repository contracts.
- **Prompt / Model Promotion Criteria**: N/A. No prompt, model, or reasoning-effort values change in this pass.

## Completion Criteria

- [x] Scoped Phase 2 Stage 04 plan/task artifacts created.
- [x] Phase 1 backlog disposition recorded.
- [x] Skill strategy mapping recorded as governance/process lenses.
- [x] Required Stage 04 indexes and progress log updated.
- [x] LLM Wiki and Graphify evidence refreshed or recorded.
- [x] Verification commands pass or record explicit advisory status.
- [x] No Stage 00 policy, Docker runtime, secret, deployment, remote GitHub, user-global Codex, model, or provider adapter changes are made.

## Related Documents

- **PRD**: [Agent Governance Standardization Product Requirements](../../01.requirements/2026-06-01-agent-governance-standardization.md)
- **ARD**: [Agent Governance Canonical Adapter ARD](../../02.architecture/requirements/0027-agent-governance-canonical-adapter.md)
- **ADR**: [ADR-0027: Stage 00 Canonical Adapter Model](../../02.architecture/decisions/0027-stage-00-canonical-adapter-model.md)
- **Task**: [Agent Governance Phase 2 Strategy Integration Task](../tasks/2026-06-02-agent-governance-phase-2-strategy-integration.md)
- **Phase 1 Plan**: [Agent Governance Phase 1 Revalidation Plan](./2026-06-02-agent-governance-phase-1-revalidation.md)
- **Phase 1 Task**: [Agent Governance Phase 1 Revalidation Task](../tasks/2026-06-02-agent-governance-phase-1-revalidation.md)
- **Baseline Plan**: [Agent Governance Decision Items Implementation Plan](./2026-06-02-agent-governance-decision-items-plan.md)
- **Baseline Task**: [Agent Governance Missing Items Implementation Task](../tasks/2026-06-02-agent-governance-missing-items-implementation.md)
- **Stage 00 Governance Hub**: [AI Agent Governance Hub](../../00.agent-governance/README.md)
- **Stage 00 Workflows**: [Workflows](../../00.agent-governance/rules/workflows.md)
