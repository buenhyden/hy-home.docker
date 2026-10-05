---
title: "Common Authorization and Safe Authoring Plan"
version: "1.0.1"
type: "sdlc/plan"
status: "in-progress"
owner: "@buenhyden"
updated: "2026-10-05"
layer: "specs"
artifact_id: "SPEC-0207-PLAN-0001"
parent_ids:
- "SPEC-0207"
created: "2026-10-04"
---

# Common Authorization and Safe Authoring Plan

## Overview

Implement bounded P01 policy convergence through Task 0001's authorization
work and Task 0002's execution-boundary follow-up, preserving one current
authority per rule and recording only observed local evidence. Task 0003
adds the current authority and blocker reconciliation in W5, preserving those
completed implementation scopes and separating declarations, enforcement,
execution evidence, and actual authorization.

The original user-authorized local main finish is recorded in the
[SPEC-0209 handoff](../0209-common-document-contract-adoption/tasks/tsk-0001-common-document-contract-adoption.md#local-integration-handoff).
Task 0003 records current separately approved reconciliation and delivery scope.
The completed Tasks retain their original implementation scopes and evidence.

### Dependencies

- Current trusted user authorization recorded in Task 0003 for its bounded
  document reconciliation, checks, review, and separately approved delivery.
- REQ-0024, AD-0027, ADR-0032, canonical policy owners, provider registry, and
  the Task's source/consumer matrix.
- Read-only policy review before final completion; focused documentation and
  governance checks. Remote integration requires separate approval and evidence.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1, 2, 3, 5, 7 | Inventory and route current authority and follow-up consumers. | None | TSK-0001, TSK-0002 | Original Task evidence and current source review. |
| W2 | 2, 3, 4, 5 | Converge canonical authorization, safe-authoring, review, and budget policy. | W1 | TSK-0001 | Original Task 0001 evidence. |
| W3 | 4, 6, 7 | Preserve prior verification and complete the execution-boundary follow-up. | W2 | TSK-0001, TSK-0002 | Original per-Task evidence and actual follow-up checks. |
| W4 | 6 | Verify and review the follow-up's final exact diff. | W3 | TSK-0002 | Original Task 0002 evidence. |
| W5 | 1, 2, 3, 4, 5, 6 | Reconcile current P01 authority, facts, and blocker lanes while retaining canonical contracts. | W1, W2, W3, W4 | TSK-0003 | Current source comparison, public changed gate, final Task document checks, and independent exact-diff review. |

### Historical Assignment Boundaries

Task 0001's original pairs are `1/W1`, `2/W2`, `3/W2`, `4/W2`, `5/W2`,
`6/W3`, and `7/W3`. Task 0002's original pairs are `1/W1`, `2/W1`, `3/W1`,
`5/W1`, `7/W1`, `4/W3`, and `6/W4`. The current table preserves their union;
shared row routing does not establish additional historical coverage or
acceptance for either Task. Execution and completion evidence remain in the
actual Tasks; the Spec and Plan make no new completion claim.

### Work Details

1. W1: inventory and route authority. Record policy-to-role-to-skill-to-
   provider-to-hook-to-consumer paths and conflicts only where a real consumer
   exists. Map each rule to one current owner and a disposition.
2. W2: converge canonical policy. Amend approval boundaries, environment
   constraints, workflows, and agentic policy so authorization, record
   validation, review, safe authoring, safety denial, and budget preflight have
   distinct owners.
3. W3: complete the execution-boundary follow-up. Route duplicate local
   pre-commit wording to quality standards, preserve the warning/block hook
   actions, and make fixed input-free payload denial reasons observable without
   changing authoring, authorization, or native sandbox semantics.
4. W4: verify and review the final exact diff. Run focused document/policy and
   hook checks, record actual results and independent review, then prepare one
   logical local commit. The prior local merge `2bba11baa1009e673a763a727b0a9e3d7e0bb5a7`
   is preserved; Task 0002's original follow-up scope excluded an additional
   local main merge. The latest authorized local main finish follows the
   SPEC-0209 handoff above. Remote
   push, PR, merge, and hosted checks remain `NOT_RUN` without separate approval.

5. W5: compare current main with the fixed audit revision; classify same-meaning
   duplication, different purposes, direct contradictions, stale facts, and
   verification gaps in Task 0003. Amend only this Spec, this Plan, and that new
   Task. Preserve policies, templates, completed Tasks, and the separate recovery
   worktree. Freeze the three-file input before QA and independent review. Each
   fresh attempt's actual approved bound is recorded in Task 0003: one initial
   batch plus one narrower P01 document correction. A required failure outside
   this slice blocks acceptance and commit without expanding repair.

### Rulings

- `approval-boundaries.md` is the current authorization owner.
- Task/schema/CLI/archive fields are structural records, never authentication.
- Historical evidence preserves provenance and cannot authorize a current action.
- Review stays independent and read-only; doc-writer remains the policy writer.

## Verification Plan

Run the applicable documentation metadata/link and changed-profile governance
checks once after the final local diff. Run provider rendering only if a provider
surface changes. Record missing tools, sandbox limits, and hosted checks as
`NOT_RUN` or `BLOCKED`, never as a pass.

## Risks and Rollback

Ambiguous wording can create a parallel owner or overstate native capabilities.
Rollback is one logical revert of the P01 policy/package change after preserving
the Task evidence. Document reconciliation does not itself modify secret,
runtime, provider, or sandbox state; remote delivery follows only its separately
approved Task scope and actual protected-branch checks.

## Related Documents

- [Specification](spec.md)
- [Task 0001: policy convergence](tasks/tsk-0001-policy-convergence.md)
- [Task 0002: execution boundary and safe diagnostics](tasks/tsk-0002-execution-boundary-and-safe-diagnostics.md)
- [Task 0003: current authority and blocker reconciliation](tasks/tsk-0003-current-authority-and-blocker-reconciliation.md)
