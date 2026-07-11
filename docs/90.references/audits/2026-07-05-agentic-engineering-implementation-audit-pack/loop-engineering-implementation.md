---
status: active
artifact_id: audit:agentic-engineering-implementation:loop-engineering
artifact_type: audit
parent_ids: [audit:agentic-engineering-implementation:overview]
reviewed_at: 2026-07-12
review_cycle: per-remediation-task
---

<!-- Target: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/loop-engineering-implementation.md -->

# Reference: Loop Engineering Implementation

## Overview

This reference assesses `LOOP-01` through `LOOP-06` against tracked context,
delegation, hook, validation, eval, approval, memory, and evidence surfaces at
baseline `507cd505` on 2026-07-11.

## Purpose

Identify which feedback loops are documented, applied, automated, or measured
without treating provider executability as a repository evaluation contract.

## Repository Role

The report supports later Stage 03/04 improvement work. It does not replace
Stage 00 workflow rules, provider hooks, validation scripts, CI, or task review.

## Scope

### In Scope

- Observation/action, pre/post action, validation/eval, retry/stop,
  approval/resume, and evidence/observability loops.

### Out of Scope

- New eval jobs, provider hooks, CI gates, telemetry, or runtime mutation.
- Hidden-reasoning inspection or persistence of raw provider/runtime logs.

## Definitions / Facts

- A loop is depth 4 only when measured results feed a closed corrective cycle.
- Three fixed fixtures have automated freshness checks. Their presence does
  not supply a general semantic scorer or regression threshold.
- Spec 123's remediation chain completed independent review with final
  PASS/APPROVED, Critical 0, Important 0, Minor 0, and
  `READY_FOR_RECLOSURE: YES` in T-AER-012.

## Assessment Method

The audit mapped every canonical `LOOP-*` criterion to Stage 00 workflow and
approval rules, provider hook surfaces, validation/CI, memory, task evidence,
and fixture checks. Graphify was stale/advisory and did not support any status.

## Audit Criteria

| Criterion ID | External criterion | Workspace evidence | Status | Enforcement depth | Disposition | Canonical owner | Automation impact | Verification | Confidence |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| LOOP-01 | Run a bounded observe/action loop and return evidence to a controller. | Subagent protocol defines supervisor/worker handoff, scoped execution, result reporting, and separate review; provider-native execution differs and `.agents` remains pointer-based. | Partial | 2 | Improve | Stage 00 workflow supervisor and subagent protocol | Keep task review ledger; native execution compatibility is a provider follow-up. | Inspect `subagent-protocol.md`, active plan, task evidence, and provider role surfaces. | High for governance; medium for cross-provider runtime behavior. |
| LOOP-02 | Apply pre/post action feedback without assuming event-name parity. | Claude and Codex tracked hooks route selected lifecycle feedback through shared scripts; the generated parity matrix records seven native wrappers, seven native dispatches, and seven Gemini behavioral reminders. No tracked native Gemini hook adapter or live execution evidence exists. | Partial | 2 | Fix | Stage 00 hook contract and provider adapters | Retain synchronized semantic lifecycle and hook-parity checks; preserve the native-adoption boundary. | Run provider sync and hook-parity checks; inspect `.claude/settings.json`, `.codex/hooks.json`, shared scripts, and provider notes. | High for tracked behavior; live/provider-native execution remains unproved. |
| LOOP-03 | Combine validation with versioned semantic eval evidence. | Local validators, CI, task review, and three fixed fixtures exist; fixture freshness is automated, while scoring arbitrary output remains manual/advisory. | Partial | 3 | Improve | QA scope and eval follow-up owner | Retain fixture freshness; add scorer/baseline/threshold only after an approved eval contract. | `bash scripts/validation/run-agent-output-eval-fixtures.sh --check-fixtures` reports `3/3`. | High. |
| LOOP-04 | Diagnose before retry, bound attempts, and stop/escalate on unchanged failure. | Stage 00 subagent protocol allows one narrower retry then failure; task checklists and SDD review define stop/review behavior. No cross-provider mechanism measures retry causes or enforces identical stop semantics. | Partial | 2 | Improve | Workflow supervisor and task owner | Candidate structured attempt/result fields in future task evidence; no autonomous retry expansion. | Inspect subagent protocol error handling and current SDD task ledger. | High for written contract; medium for runtime enforcement. |
| LOOP-05 | Pause protected actions for exact approval and refresh state on resume. | Approval boundaries and task checklists require concrete scope/evidence; actual provider prompt state and durable resume behavior vary and are not uniformly tracked. | Partial | 2 | Improve | Stage 00 approval boundaries | Add scoped approval/resume evidence where high-risk tasks require it; avoid global-state inference. | Inspect `approval-boundaries.md`, `task-checklists.md`, and high-risk task evidence contract. | High for policy; runtime prompt propagation is provider-dependent. |
| LOOP-06 | Preserve reviewable observations while respecting redaction/privacy. | Diffs, commands, CI/SARIF, Stage 04 evidence, progress memory, and review packages exist. No unified trace backend, task-quality time series, or depth-4 feedback metric is tracked. | Partial | 2 | Improve | Stage 04 evidence owner and QA | Prefer concise generated evidence; a trace backend is not required absent a justified use case. | Inspect task/review ledgers, memory policy, and CI evidence surfaces. | High for tracked evidence; telemetry enablement is unknown. |

## Findings

- All six loops have a repository surface, so none is `Missing`; each remains
  `Partial` because native parity, semantic scoring, enforcement, or measurement
  is incomplete.
- The strongest loop is deterministic validation/fixture freshness at depth 3.
  No loop reaches depth 4.
- Review and task evidence close individual work items, but the repository does
  not yet measure semantic agent performance across versions.

## Gap / Follow-up

| Gap | Disposition | Canonical owner |
| --- | --- | --- |
| Provider hook/event native and live acceptance | Retain tracked semantic/hook parity; verify native execution only in separate approved scope. | Stage 00 provider owners and executing runtime owner |
| General semantic scorer and calibrated regression threshold | Improve only after dataset/privacy/scorer design. | QA/eval follow-up |
| Cross-provider retry/resume observability | Improve task evidence first; do not add telemetry without a justified contract. | Workflow supervisor |
| Closed-loop depth measurement | Add only if actionable metrics and an owner are defined. | Stage 03/04 future work |

## Automation Impact

Current automation covers fixture catalog integrity and deterministic checks.
Provider-semantic checks and scored agent evals are candidates, not adopted
requirements.

## Source Rules

- Provider features are facts from the canonical research ledger.
- Workspace loop status is derived from tracked files and reproduced commands.
- Provider telemetry and hidden reasoning are never inferred as workspace evidence.

## Sources

- [Loop research](../../research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md)
- [Agent-output fixtures](../../data/governance/agent-output-eval-fixtures.md)
- [Subagent protocol](../../../00.agent-governance/subagent-protocol.md)
- [Approval boundaries](../../../00.agent-governance/rules/approval-boundaries.md)
- [Task evidence](../../../04.execution/tasks/2026-07-11-agentic-engineering-audit-remediation.md)

## Maintenance

- **Owner**: Agentic Workflow Specialist / QA Engineer.
- **Review Cadence**: After provider, hook, validation, review, or eval changes.
- **Update Trigger**: Any `LOOP-*` state, depth, or evidence changes.

## Related Documents

- [Audit pack README](./README.md)
- [Harness implementation audit](./harness-engineering-implementation.md)
- [Provider implementation audit](./provider-harness-loop-implementation.md)
- [Agent instruction/catalog/model audit](./agent-instructions-catalog-vibe-models.md)
