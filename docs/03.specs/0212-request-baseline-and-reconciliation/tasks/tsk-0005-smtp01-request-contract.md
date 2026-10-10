---
title: "SMTP01 Request Contract Task"
version: "1.0.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0005"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-10"
---

# SMTP01 Request Contract Task

## Objective

Record current routing and the SEC01 → SMTP01 → CLN01 order without expanding
authority to Wiki implementation, LAB runtime or learning applications.

## Inputs and Authorization

The input baseline is `a03c8930a5a15a82f4176bbcfe457bc2ce09db4b`. SEC01 is
the prerequisite on its owning-Spec branch and has no code here. SMTP01 owns
the source transition after SEC01; CLN01 owns old-file deletion after SMTP01.
The contract PR waits for SEC01 and precedes the SMTP source PR; no lane merges
unilaterally. This Task owns only the two parent documents and itself.

## Work Log

### W13 Current-request contract

`SOURCE` is the amended contract; `UNIT` is a value-free probe; `STATIC` is
Stage 99 validation. `ISOLATED`, `HOME`, `MIGRATION`, `ROTATION`, `RECOVERY`
and `DELIVERY` are separate and not inferred from this document change.

### Lifecycle verification history

The earlier completed-parent reopen candidate used an unregistered
`completed -> in-progress` edge and failed with three lifecycle-event violations.
This failed run is preserved here and is not a PASS. The legal contract-only
candidate keeps both parents completed and uses Task `draft -> ready -> completed`.
A separate probe passed, but final worktree validation remained pending at the
checkpoint below. The resumed corpus failure was traced to a blank line inside
SPEC-0204's registered Work Breakdown table, not to this Task's NOT_RUN row.
The blank line is removed while all evidence rows remain preserved.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0005 | draft | ready | #w13-current-request-contract |
| SPEC-0212-TSK-0005 | ready | completed | #review-and-completion |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Baseline RED | 8 | W13 | Value-free Python contract assertions, exit 1: `wiki-preparation-only contract is absent` | `a03c8930a5a15a82f4176bbcfe457bc2ce09db4b`; no secrets | PASS | Isolated SMTP01 worktree | accepted |
| Contract GREEN | 8 | W13 | Value-free Python contract assertions, exit 0 | Current W13 source; no secrets | PASS | Isolated SMTP01 worktree | accepted |
| Metadata validation | 8 | W13 | `check-document-metadata.py --mode check-active`, exit 0; 478 selected, 0 violations | Current W13 source | PASS | Isolated SMTP01 worktree | accepted |
| Lifecycle checkpoint before resumed validation | 8 | W13 | `check-document-corpus-lifecycle.py --base-ref a03c8930a5a15a82f4176bbcfe457bc2ce09db4b`; rerun required after legal lifecycle completion | Current W13 source | NOT_RUN | Isolated SMTP01 worktree | pending |
| Resumed lifecycle validation | 8 | W13 | `check-document-corpus-lifecycle.py --base-ref a03c8930a5a15a82f4176bbcfe457bc2ce09db4b`, exit 0; corpus and archive recovery 0 violations | Actual corrected SMTP01 worktree; completed-parent contract-only Task; contiguous 0204 tables | PASS | Lifecycle verification history | accepted |

## Review and Completion

This completed route-contract Task does not attest SMTP migration, deletion,
runtime recovery, PR delivery or merge. SEC01 delivery, the SMTP source PR and
CLN01 deletion remain separately owned and pending.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Completed P00 Task](tsk-0003-active-contract-and-exclusions.md)
