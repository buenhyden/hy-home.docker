---
title: "Terminal Task Resolves Correction Task"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0037"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-29"
---

# Terminal Task Resolves Correction Task

## Overview

### Objective

Execute W53: let the Spec validator accept the one owner-approved correction
of a completed Task, so SPEC-0211 criteria 2 and 3 can be recorded. This
Task owns criterion 48 only.

## Inputs and Authorization

SPEC-0211 TSK-0002 is completed. Its `Final hosted candidate recovery` PASS
row answered the two earlier hosted FAIL rows, `First hosted candidate RED`
and `Hosted retry`, which have the same Check and Work Unit. Its `Resolves`
cell names only `Final hosted candidate`. A completed Task is frozen, and
`Resolves` reaches only rows in its own Task, so those two rows block an
accepted decision for criteria 2 and 3. On 2026-10-29 the owner chose a
one-off correction of that cell. The input is `main` at merged PR #633.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0037 | draft | ready | #inputs-and-authorization |
| SPEC-0212-TSK-0037 | ready | in-progress | #objective |
| SPEC-0212-TSK-0037 | in-progress | completed | #evidence |

### Change

`_TERMINAL_TASK_RESOLVES_CORRECTIONS` in
`scripts/lib/document_governance/spec_packages.py` names the Task path, the
row, its old `Resolves` cell and the corrected cell. The terminal Task
comparison applies that change to the earlier body before comparing, so the
corrected row matches and any other change still fails. Once the correction
is merged, the earlier body no longer carries the old cell and the entry has
no effect. The SPEC-0211 change that edits the row and records the two
acceptances is a separate pull request.

The first version, `415ce7437`, applied the correction to the earlier body
unconditionally. An unchanged TSK-0002 then no longer matched, and
`check-contracts` failed with `terminal Task body or identity changed`. The
end-to-end check above had only tried the corrected row. The comparison now
accepts the earlier body or its corrected form, and a fourth test covers the
unchanged Task.

A package-wide `Resolves` was not used: a resolving row in another Task would
need W70, which the Plan assigns only to TSK-0002.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Correction RED | 48 | W53 | `TerminalTaskResolvesCorrectionTests` | This branch with the correction map emptied | FAIL | The registered correction does not match | required | - |
| Correction GREEN | 48 | W53 | `TerminalTaskResolvesCorrectionTests` | This branch | PASS | Four tests OK: the correction matches, an unchanged Task matches, another `Resolves` change fails, and another Task gets no correction | required | Correction RED |
| Unchanged Task regression | 48 | W53 | `check-document-metadata.py --mode check-contracts` | `415ce7437` with TSK-0002 unchanged | FAIL | `terminal Task body or identity changed` | required | - |
| Unchanged Task fix | 48 | W53 | `check-document-metadata.py --mode check-contracts` | This branch with TSK-0002 unchanged | PASS | 0 violations | required | Unchanged Task regression |
| End-to-end check | 48 | W53 | `check-document-metadata.py --mode check-contracts` with the corrected TSK-0002 row applied and then restored | This branch | PASS | 0 violations | required | - |
| Spec package tests | 48 | W53 | `python3 -m unittest tests.lib.document_governance.test_spec_packages` | This branch | PASS | 91 tests OK in 347 s | required | - |
| Lint | 48 | W53 | `ruff check` and `ruff format --check` | Changed Python files | PASS | No findings | required | - |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 48 | accepted | Correction GREEN, Unchanged Task fix, End-to-end check, Spec package tests, Lint | The validator accepts exactly the one approved correction and still rejects every other change to a completed Task. | SPEC-0212 TSK-0037 |

## Review and Completion

This Task completes on the evidence above. Hosted checks and the merge are
observed on the pull request.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Investigation records](tsk-0036-investigation-records-and-currency-fixes.md)
