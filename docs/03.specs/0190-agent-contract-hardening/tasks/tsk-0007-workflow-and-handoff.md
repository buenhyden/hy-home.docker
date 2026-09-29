---
title: "Bounded Workflow and Handoff Contracts"
version: "0.1.0"
type: "sdlc/task"
status: "ready"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0190-TSK-0007"
parent_ids:
- "SPEC-0190"
- "SPEC-0190-PLAN-0001"
created: "2026-09-29"
---

# Bounded Workflow and Handoff Contracts

## Objective

Implement Plan W7: current Task-owned approval, failure/resume, budget and
knowledge contracts, with deterministic recorded-output refusal evaluations.

## Inputs

- [Approved Spec](../spec.md), [approved Plan](../plan.md), and
  [W6 evidence](tsk-0006-recovery-contract-review.md).
- User approval covers exact local edits, tests, review and logical commits;
  no native/paid call, installation, remote or operational action.
- Exact 18-file W7 map: doc-writer owns 15 documents; qa-engineer owns evaluator,
  catalog and its existing tests. Rules-engineer is an independent reviewer.
  Root owns Task evidence, lifecycle and index. Writers do not overlap files.

## Work Log

Read-only preparation confirmed existing policy, knowledge and prompt owners.
Reuse AOE-LOOP-001 and score_text/run_regressions; retain its fixture identity
and threshold. Do not introduce a runtime budget engine or a second ledger.
W6 implementation and focused acceptance precede W7 implementation GO.

## Verification Evidence

NOT_RUN: E/ET refusal regressions, metadata/link checks and independent semantic
review. Cover stale HEAD/digest, wrong worktree, revoked approval, overlapping
writer, partial result, expired knowledge, injected instructions, exhausted or
shared budget, bounded 429/backoff and unsupported native success claims.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| R06/R07/R08/R14/R17/R19/R21/R22/R30/R38 | W7 | NOT_RUN | Existing policy, knowledge, prompt and evaluator owners |

## Review Evidence

Independent policy and evaluator review pending. Recorded model-free outputs
cannot demonstrate actual native budget enforcement or provider runtime use.

## Commit Ledger

Create real draft, ready and in-progress predecessors before implementation GO.
The W6 final connection commit remains separately scoped and precedes activation.

## Rulings

- Design, written-Spec and written-Plan approvals are distinct.
- Handoff derives from the Task; receiver rechecks actual repository/worktree,
  HEAD/digests, approval, ownership, partial state and shared remaining budget.
- Knowledge carries verified facts, provenance, freshness and invalidation in
  existing sections; it does not acquire mutable execution state or secrets.
- Keep evals at its current root path through W7. REQ/AD reflect the owner's
  selected .agents/evaluations migration; W9 performs the actual cutover.
- Shared Git release/tag rules move to current governance ownership; do not edit
  preserved runbooks or introduce editor IDs, issue sync or guessed account limits.

## Deferred Items

W9 owns evaluation migration and recovery fixture/threshold. W10 owns native,
editor, hosted and real budget enforcement evidence; applicable gaps stay open.
