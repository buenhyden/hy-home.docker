---
title: "Task Evidence Table Integrity Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-06"
layer: "specs"
artifact_id: "SPEC-0210-PLAN-0001"
parent_ids:
- "SPEC-0210"
created: "2026-10-06"
---

# Task Evidence Table Integrity Plan

## Overview

Add a strict opt-in to the shared registered-table reader, activate it only for
generation 5 Work Breakdown and Evidence, and prove the boundary through focused
and public metadata checks. The Task owns actual execution, validation, review,
and acceptance records.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1, 2 | Add witnessed regressions and the strict generation 5 reader; materialize an explicit in-progress metadata fixture; move current auxiliary tables outside the registered Evidence section without changing their text. | None | TSK-0001 | Focused RED/GREEN, source-proof, current-corpus, and preservation checks. |
| W2 | 3 | Add contiguous-table authoring guidance and Stage 03 routing without adding a second execution-status owner. | W1 | TSK-0001 | Focused metadata, link, and style checks. |
| W3 | 3 | Freeze the owned input, run the public changed gate, obtain independent read-only review, and reconcile acceptance. | W1-W2 | TSK-0001 | Public gate and exact-diff review receipts. |

## Verification Plan

Write the fragmentation regressions before changing the reader and witness the
expected RED. After the minimal implementation, run only the new and modified
focused regressions, registered Ruff checks for the three Python files, and
scoped document metadata, link, and style checks. The authorized resumption
stages only the twelve owned files, inspects the public changed-gate plan, and
runs the selected changed gate once on its new frozen input. One narrower
P03-owned correction may receive one additional run on a distinct input. Final
receipt-only document changes receive only their minimum metadata, link, and
style checks.

## Risks and Rollback

A strict reader can expose auxiliary pipe tables in a registered section. The
authorized resumption corrects only the two observed current owners by moving
the section boundary while preserving their auxiliary and canonical table text.
Any other required failure remains a blocker and cannot weaken the rule or
expand ownership. Rollback reverts the single local logical commit if one is
created. Frozen and terminal documents are never rewritten for rollback.

## Related Documents

- [Specification](spec.md)
- [Task 0001](tasks/tsk-0001-task-evidence-table-integrity.md)
- [Stage 99 Plan template](../../99.templates/templates/specs/plan.template.md)
- [Stage 99 Task template](../../99.templates/templates/specs/task.template.md)
