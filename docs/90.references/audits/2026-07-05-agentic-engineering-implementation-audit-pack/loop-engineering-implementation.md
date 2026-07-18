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
- Eight versioned fixtures and ten synthetic positive/negative regressions have
  exact catalog fields, deterministic scorers, calibrated thresholds, bounded
  inputs, and automated freshness checks. They validate the repository harness,
  not live provider model quality.
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
| LOOP-02 | Apply pre/post action feedback without assuming event-name parity. | The typed event contract renders seven Claude and seven Gemini native mappings plus six Codex mappings; Codex `SessionEnd` is explicitly unsupported. Shared scripts and repository checks validate the tracked semantics, but live provider interception remains unproved. | Partial | 3 | Retain | Stage 00 hook contract and provider adapters | Retain synchronized semantic lifecycle, hook-parity checks, and the unsupported-event boundary. | Run provider sync and hook-parity checks; inspect `.claude/settings.json`, `.codex/hooks.json`, `.gemini/settings.json`, shared scripts, and provider notes. | High for tracked behavior; live/provider-native execution remains unproved. |
| LOOP-03 | Combine validation with versioned semantic eval evidence. | Local validators, CI/local routing, Stage 04 review, eight fixed fixtures, ten synthetic regressions, exact thresholds, and deterministic bounded scorers form a versioned repository feedback loop. No network model call or live comparative-quality claim is made. | Implemented | 4 | Retain | QA scope and eval owner | Retain calibrated fixture/regression checks; design live provider evaluation separately if later approved. | `bash scripts/validation/run-agent-output-eval-fixtures.sh --check-fixtures --check-regressions` reports exact pass markers for `8/8` and `10/10`. | High. |
| LOOP-04 | Diagnose before retry, bound attempts, and stop/escalate on unchanged failure. | Four typed harness loops bind positive attempt limits, exact stop conditions, failure actions, event ownership, independent-review inequality, and a single controlled all-files attempt. The contract and synthetic regressions reject unbounded or unchanged retry semantics. | Implemented | 3 | Retain | Workflow supervisor and task owner | Preserve typed bounds and task evidence; do not add autonomous retry expansion. | Run the harness contract/evaluator suites and inspect the typed loop contract plus current SDD task ledger. | High for the enforced repository contract; provider runtime behavior remains separate. |
| LOOP-05 | Pause protected actions for exact approval and refresh state on resume. | Approval boundaries and task checklists require concrete scope/evidence; actual provider prompt state and durable resume behavior vary and are not uniformly tracked. | Partial | 2 | Improve | Stage 00 approval boundaries | Add scoped approval/resume evidence where high-risk tasks require it; avoid global-state inference. | Inspect `approval-boundaries.md`, `task-checklists.md`, and high-risk task evidence contract. | High for policy; runtime prompt propagation is provider-dependent. |
| LOOP-06 | Preserve reviewable observations while respecting redaction/privacy. | Diffs, commands, CI/SARIF, Stage 04 evidence, progress memory, and review packages exist, and the synthetic repository loop reaches depth 4. No unified trace backend, cross-task quality time series, or live comparative-quality telemetry is tracked. | Partial | 2 | Improve | Stage 04 evidence owner and QA | Prefer concise generated evidence; a trace backend is not required absent a justified use case. | Inspect task/review ledgers, memory policy, CI evidence surfaces, and exact evaluator markers. | High for tracked evidence; unified/live telemetry enablement is unknown. |

## Findings

- All six loops have a repository surface, so none is `Missing`. LOOP-03 and
  LOOP-04 are implemented through calibrated synthetic evaluation and typed
  stop/retry enforcement; provider-native/live parity, durable approval resume,
  and unified telemetry remain Partial.
- The deterministic fixture/regression loop reaches depth 4 for repository
  harness semantics. It does not measure comparative live model performance.

## Gap / Follow-up

| Gap | Disposition | Canonical owner |
| --- | --- | --- |
| Provider hook/event native and live acceptance | Retain tracked semantic/hook parity; verify native execution only in separate approved scope. | Stage 00 provider owners and executing runtime owner |
| Live or comparative model-quality scorer | The deterministic synthetic scorer is implemented; require a separate dataset/privacy/provider-runtime design for live evaluation. | QA/eval follow-up |
| Cross-provider retry/resume observability | Improve task evidence first; do not add telemetry without a justified contract. | Workflow supervisor |
| Cross-task and live closed-loop quality time series | Repository-semantic depth 4 is already measured; add broader metrics only if actionable measures, privacy boundaries, and an owner are defined. | Stage 03/04 future work |

## Automation Impact

Current automation covers exact fixture/regression catalogs, deterministic
scoring, typed loop bounds, and routed harness checks. Live provider acceptance
and comparative model evaluation remain separate candidates, not adopted
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
