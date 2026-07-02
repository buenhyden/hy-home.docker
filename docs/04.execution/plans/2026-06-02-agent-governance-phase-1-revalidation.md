---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-06-02-agent-governance-phase-1-revalidation.md -->

# Agent Governance Phase 1 Revalidation Plan

## Overview

This document is the implementation plan for revalidating the Agent Governance Phase 1 diagnostic against the current repository state and organizing later improvement, supplementation, and redesign candidates as Stage 04 evidence.

This work is not implementation; it is investigation, analysis, and design organization. It uses the existing 2026-06-01 Phase 1 diagnostic and 2026-06-02 governance follow-up artifacts as the baseline, then checks whether the current documents, environment, systems, structure, and rules align with the workspace purpose.

## Context

The repository already has an explicit Agent Governance chain:

- Stage 01 PRD: Agent Governance Standardization.
- Stage 02 ARD/ADR: Stage 00 canonical adapter model.
- Stage 04 continuation evidence: decision-items plan and missing-items implementation task.
- Stage 00 policy: governance hub, workflows, task checklists, provider overlays, QA/CI/CD matrix, and template contract.

The current plan preserves that chain. Graphify remains advisory when `report-graphify-health.sh` reports cross-root inferred edges, so all conclusions must be corroborated against tracked Stage 00 docs, stage docs, provider surfaces, and validation scripts.

## Goals & In-Scope

- **Goals**:
  - Record a current-state Phase 1 revalidation without rewriting active policy.
  - Summarize document, environment, governance, provider adapter, Docker/DevOps/QA, and Node/npm/rtk toolchain state.
  - Classify improvement candidates into already satisfied, minor documentation cleanup, design follow-up, and redesign candidate buckets.
  - Confirm ADR-0027 remains the accepted architecture unless a concrete contradiction is found.
  - Map requested external skill groups into repository governance/process lenses rather than separate active taxonomies.
- **In Scope**:
  - Stage 04 plan/task artifacts and README links.
  - Progress-log evidence.
  - LLM Wiki freshness if added or renamed documents require regeneration.
  - Validation evidence for repo contracts, doc traceability, provider sync, and Graphify advisory status.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Do not implement Stage 00 policy rewrites in this pass.
  - Do not broaden HADS mandatory validation beyond `docs/90.references/data/hads/`.
  - Do not replace ADR-0027 or redesign the canonical adapter model without a concrete contradiction.
  - Do not create active non-stage specs, plans, or task logs for external skills.
- **Out of Scope**:
  - Docker runtime start/stop/recreate, image rebuilds, migrations, deployments, and live network changes.
  - Secrets, credential files, private keys, shell history, token-bearing logs, or user-global Codex settings.
  - Remote GitHub protection or branch-rule mutation.
  - Provider adapter model/reasoning changes.
  - Broad rewrite of historical artifacts that remain semantically aligned with current implementation.

## Current State Summary

| Area | Current State | Phase 1 Judgment |
| --- | --- | --- |
| Documents | Stage 01/02/04 Agent Governance traceability exists; active old conflicting evidence has been archived where needed. | Mostly satisfied; this revalidation adds a current Stage 04 diagnostic summary. |
| Governance structure | Stage 00 owns active policy, workflow, scope, provider overlay, memory, and template contract. | Keep as canonical; no architecture replacement needed. |
| Provider adapters | Claude/Gemini/Codex surfaces are adapters; Codex active agent surface is `.codex/agents/*.toml` only. | Verify with provider sync; do not create provider-local policy. |
| Docker / DevOps | Docker hardening has hard-gate coverage where repo-proven; compatibility-sensitive best practices remain manual review. | Keep validator/manual-review split; future hard gates need approval. |
| QA / CI/CD | QA scope and GitHub governance define change-type evidence, CI-only gates, and skipped-check rationale. | Satisfied baseline; revalidation records applicability. |
| Node/npm/rtk | Tools exist under `/home/hy/.local/bin`, but non-interactive shells may not expose them on `PATH`. | Future Node-based automation must source `scripts/operations/use-qa-ci-tools.sh` or use explicit paths. |
| Graphify | Existing graph is useful for navigation but advisory due cross-root inferred edges. | Use as hint only; corroborate with tracked docs and validators. |

## Improvement Backlog

| Bucket | Item | Rationale | Follow-up Boundary |
| --- | --- | --- | --- |
| Already satisfied | Stage 01/02 Agent Governance PRD/ARD/ADR chain | PRD, ARD, and ADR-0027 already define the canonical adapter model. | No action beyond linking this revalidation evidence. |
| Already satisfied | Provider adapter parity | Provider sync currently reports no drift. | Re-run sync after provider-surface changes only. |
| Already satisfied | QA/CI/CD change-type matrix | QA scope and GitHub governance already define local, remote, and skipped-check evidence. | Keep using in task evidence. |
| Minor documentation cleanup | Phase 1 evidence discoverability | Phase 1 diagnostic existed in progress and related artifacts, but not as a dedicated current revalidation plan/task pair. | This plan/task closes the discoverability gap. |
| Minor documentation cleanup | Node/npm/rtk PATH caveat | Existing docs mention explicit PATH handling; revalidation should record observed shell behavior. | Record in task evidence; no tooling change. |
| Design follow-up | Skill strategy absorption | External Superpowers, HADS, Docker, DevOps, architecture, QA, and review skills need one consistent mapping to stage artifacts. | Keep in Stage 00 workflow/process docs unless a future approved plan changes policy. |
| Design follow-up | Docker hard-gate expansion | Some Docker best practices are manual review because direct validator promotion could cause broad churn. | Future hard validators require separate approval and repo-proven checks. |
| Redesign candidate | Stage 00 canonical adapter model replacement | No concrete contradiction found in the baseline. | Not recommended now; only revisit if Stage 00/provider parity breaks or ADR-0027 is superseded. |
| Redesign candidate | Broad HADS rollout | Current mandatory HADS profile is bounded and intentional. | Not recommended without separate rollout plan and approval. |

## Skill Strategy Mapping

| Skill / Strategy Group | Repository Adaptation |
| --- | --- |
| `using-superpowers`, `brainstorming`, `writing-plans`, `executing-plans` | Treat as workflow discipline; canonical artifacts remain PRD/ARD/ADR/Spec/Plan/Task in repository stages. |
| `test-driven-development`, `systematic-debugging`, `verification-before-completion` | Apply through QA scope: TDD for behavior changes, root-cause evidence for bugs, fresh verification before completion claims. |
| `finishing-a-development-branch` | Apply through GitHub governance and git workflow; branch completion still requires repository checks and user-approved merge/PR action. |
| `requesting-code-review`, `receiving-code-review`, `code-review-excellence` | Apply through code-review workflow: self-review, local checks, structured findings, explicit resolution or reasoned pushback. |
| `documentation-standards:hads`, documentation writer/coauthoring/humanizer skills | HADS remains mandatory only for `docs/90.references/data/hads/`; other documentation uses template contract, stage taxonomy, and human-readable style. |
| Docker/container skills | Use as review lenses for Compose, Dockerfile, security, optimization, and orchestration; hard validators only for repo-proven rules. |
| DevOps/CI/CD skills | Map secrets, GitHub Actions, and deployment-pipeline strategy into GitHub governance, QA matrix, and operations/runbook boundaries. |
| Architecture and senior QA skills | Use as design/review lenses for ARD/ADR quality attributes and verification strategy; do not create parallel architecture or QA taxonomies. |

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-P1R-001 | Create the Phase 1 revalidation plan from the approved user plan and current repository baseline. | `docs/04.execution/plans/2026-06-02-agent-governance-phase-1-revalidation.md` | REQ-AGG-MET-01 | Plan uses template sections, has no placeholders, and links upstream/downstream artifacts. |
| PLN-P1R-002 | Create paired task evidence with current state findings, backlog classification, skill mapping, and verification record. | `docs/04.execution/tasks/2026-06-02-agent-governance-phase-1-revalidation.md` | REQ-AGG-MET-04 | Task captures evidence without runtime, secret, deployment, remote, or model changes. |
| PLN-P1R-003 | Register the new artifacts in Stage 04 indexes and progress log. | Stage 04 READMEs, `memory/progress.md` | REQ-AGG-MET-01 | Parent indexes and progress log point to the current revalidation artifacts. |
| PLN-P1R-004 | Refresh generated documentation index if required by added files. | `docs/90.references/llm-wiki/llm-wiki-index.md` | REQ-AGG-MET-02 | LLM Wiki check passes after regeneration. |
| PLN-P1R-005 | Run repository validation gates and record Graphify advisory status. | Task evidence | REQ-AGG-MET-02 | Diff hygiene, repo contracts, doc traceability, provider sync, and Graphify health are recorded. |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-P1R-001 | Hygiene | Confirm Markdown diff has no whitespace errors. | `git diff --check` | No output and zero exit status. |
| VAL-P1R-002 | Structural | Validate repository documentation and contract rules. | `bash scripts/validation/check-repo-contracts.sh` | PASS with `failures=0`. |
| VAL-P1R-003 | Traceability | Validate execution and operations traceability contracts. | `bash scripts/validation/check-doc-traceability.sh` | PASS with `failures=0`. |
| VAL-P1R-004 | Provider | Confirm provider adapters remain synchronized. | `bash scripts/operations/sync-provider-surfaces.sh` | PASS with `no drift`. |
| VAL-P1R-005 | Knowledge Index | Refresh and verify generated LLM Wiki index because docs are added. | `bash scripts/knowledge/generate-llm-wiki-index.sh`; `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | Regeneration completes and freshness check passes. |
| VAL-P1R-006 | Graph Boundary | Record graph health and advisory reason. | `bash scripts/knowledge/report-graphify-health.sh` | Status recorded; advisory status is acceptable when claims are corroborated. |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Revalidation turns into policy implementation. | High | Limit edits to Stage 04 indexes, task evidence, progress log, and generated index freshness. |
| Stage 00 canonical adapter model is redesigned without need. | High | Keep ADR-0027 accepted; list redesign only as conditional future candidate. |
| External skill guidance creates parallel active taxonomy. | Medium | Map skills to canonical repository stages and Stage 00 workflows only. |
| Graphify advisory output is treated as proof. | Medium | Corroborate against tracked Stage 00 docs, stage docs, provider surfaces, and validators. |
| Node-based automation fails in non-interactive shells. | Medium | Record `scripts/operations/use-qa-ci-tools.sh` as the required PATH shim for Node/npm/rtk commands. |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Repository validation, doc traceability, provider sync, LLM Wiki freshness, and Graphify health reporting.
- **Sandbox / Canary Rollout**: N/A. This is documentation/evidence-only work.
- **Human Approval Gate**: Required before any later Stage 00 policy rewrite, broad HADS rollout, Docker/runtime mutation, model policy change, remote GitHub mutation, or protected provider adapter redesign.
- **Rollback Trigger**: Revert this artifact set if it introduces duplicate active taxonomy, weakens Stage 00 authority, or breaks repository contracts.
- **Prompt / Model Promotion Criteria**: N/A. No prompt, model, or reasoning-effort values change in this pass.

## Completion Criteria

- [x] Scoped Stage 04 plan/task artifacts created.
- [x] Current-state summary and improvement backlog recorded.
- [x] Skill strategy mapping recorded as governance/process lenses.
- [x] Required indexes and progress log updated.
- [x] Verification commands pass or record explicit advisory status.
- [x] No Stage 00 policy, Docker runtime, secret, deployment, remote GitHub, user-global Codex, model, or provider adapter changes are made.

## Related Documents

- **PRD**: [Agent Governance Standardization Product Requirements](../../01.requirements/2026-06-01-agent-governance-standardization.md)
- **ARD**: [Agent Governance Canonical Adapter ARD](../../02.architecture/requirements/0027-agent-governance-canonical-adapter.md)
- **ADR**: [ADR-0027: Stage 00 Canonical Adapter Model](../../02.architecture/decisions/0027-stage-00-canonical-adapter-model.md)
- **Task**: [Agent Governance Phase 1 Revalidation Task](../tasks/2026-06-02-agent-governance-phase-1-revalidation.md)
- **Baseline Plan**: [Agent Governance Decision Items Implementation Plan](./2026-06-02-agent-governance-decision-items-plan.md)
- **Baseline Task**: [Agent Governance Missing Items Implementation Task](../tasks/2026-06-02-agent-governance-missing-items-implementation.md)
- **Stage 00 Governance Hub**: [AI Agent Governance Hub](../../00.agent-governance/README.md)
- **Stage Authoring Matrix**: [Stage Authoring Matrix](../../00.agent-governance/rules/stage-authoring-matrix.md)
