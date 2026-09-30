---
title: "Bounded Workflow and Handoff Contracts"
version: "1.0.0"
type: "sdlc/task"
status: "completed"
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
W6 implementation and focused acceptance completed in `74a008056` before GO.
The document writer completed exactly 15 files; independent rules review passed
on approval/refusal envelopes, scoped knowledge provenance, release ownership,
and evaluation code/data boundaries. Evaluator review also passed after bounded lexical corrections.

A separate read-only migration audit found that the old root evaluation README
is absent from the metadata base corpus. Plan amendment `267b7ee44` adds only
an exact historical-baseline mapping in the existing lifecycle helper and its
registry regression tests to future W9. No W9 implementation has begun.

## Verification Evidence

A final self-probe found a mixed negation/affirmative claim falsely passing:
static checks do not prove native acceptance, but show runtime success.
Its witnessed RED was fixed by narrowing the existing direct-prohibition
exemption; the shared engine was unchanged. Final rerun: E fixtures 10/10 and
regressions 38/38 PASS, ET 54/54 PASS in 17.947s. Independent exact-delta review
CLEAR with safe/unsafe paired selectors 2/2 PASS in 0.090s. Earlier receipts
below remain dated checkpoints; this rerun is the final evaluator acceptance.

- E RED: 10/10 catalog checks, 26/38 regressions; exit 1 because 12 unsafe
  continuations passed the old evaluator.
- Final E: fixtures 10/10 and regressions 38/38 PASS, exit 0. Final ET: 54/54
  PASS, exit 0, 18.065s; independent ET rerun 54/54 in 18.509s.
- Existing score_text/run_regressions interfaces, ten fixture IDs and 0.50 LOOP
  threshold remain unchanged. New cases use the existing scoring engine.
- Metadata checkpoints: selected=15 and selected=16, violations=0,
  legacy_exceptions=0, transition_overrides=0. Final completion check: selected=18, violations=0, legacy_exceptions=0,
  transition_overrides=0 against predecessor 837e05b7a.
- Entrypoint links: 987 documents, 9925 links, failures=0, warnings=0, exit 0.
- Independent 15-document policy and three-file evaluator review PASS/CLEAR.
- Cases cover stale HEAD/digest, wrong worktree, revoked approval, overlapping
  writer, partial result, expired knowledge, injected instructions, exhausted or
  shared budget, bounded 429/backoff and unsupported native success claims.

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| R06/R07/R08/R14/R17/R19/R21/R22/R30/R38 | W7 | Local contracts and recorded-output checks PASS; native enforcement remains unobserved | Existing policy, knowledge, prompt and evaluator owners |

## Review Evidence

Independent rules review and evaluator code review: PASS/CLEAR. Corrections
made handoff inputs/outputs complete, kept unavailable approval a pre-review
blocker, preserved dated knowledge provenance, separated evaluator code/data
from Markdown profiles, and retained the exact changelog tag-string rule.

Evaluator review verified multiline/label-free safe refusals, generic BLOCKED,
refusal synonyms, subject-first and past unsafe continuation, leading-no and
negated hazards, bounded 429 fields, and static-native claim/negation symmetry.
Recorded model-free outputs cannot demonstrate actual HEAD, remaining balances,
native budget enforcement or provider runtime use; lexical coverage is bounded.
No account limits, editor actions, issue sync or new runtime engine were invented.

## Commit Ledger

Task predecessors: draft `fb8895b6a`, ready `33eaa28b4`, in-progress `b097e11c1`;
each metadata transition passed against its actual predecessor. The separate
W9 Plan amendment is `267b7ee44`. The reviewed 18 implementation files,
Plan checklist and this completed Task form one logical W7 commit; Git owns
its final hash.

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
