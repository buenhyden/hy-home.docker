---
title: "Archive Check Runtime Task"
version: "0.1.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0212-TSK-0014"
parent_ids:
- "SPEC-0212-PLAN-0001"
created: "2026-10-29"
---

# Archive Check Runtime Task

## Overview

### Objective

Execute W30: find the real cause of the slower corpus check after TSK-0012 and
remove it. This Task owns criterion 25 only.

## Inputs and Authorization

On 2026-10-29 the owner asked to continue the remaining work. The input is
branch `docs/archive-disposition-dryrun` after TSK-0013. The authorization
covers this branch, its pull request, and merge through the protected path.

## Work Log

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0212-TSK-0014 | draft | ready | #inputs-and-authorization |
| SPEC-0212-TSK-0014 | ready | in-progress | #cause |
| SPEC-0212-TSK-0014 | in-progress | completed | #evidence |

### Cause

TSK-0012 attributed the slower run to validating the 196 assessment rows twice.
A call count disproved that: the two `validate_archive_assessments()` calls
took 45 s of a 347 s run. A profile located the cost in
`validate_assessment_snapshot()`, which called `_historical_units()` once per
history-only row, 786 times in one run (291 s). TSK-0012's `--full-history -m`
correction had made each call larger, so the per-row repeat dominated.

### Change

`validate_assessment_snapshot()` now computes historical units once per call,
and `_historical_units()` maps each distinct path once. Findings are unchanged.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Call count | 25 | W30 | Wrapped `validate_archive_assessments()` during one corpus run | Branch after TSK-0013 | PASS | 2 calls, 45 s of 347 s | required | - |
| Profile | 25 | W30 | `python3 -m cProfile` over the corpus check | Branch after TSK-0013 | PASS | `_historical_units()` 786 calls, 291 s | required | - |
| Archive regressions | 25 | W30 | `python3 -m unittest tests.lib.document_governance.test_archive tests.lib.document_governance.test_archive_assessments` | This branch; Python 3.12.3 | PASS | 103 tests | required | - |
| Corpus check | 25 | W30 | `/usr/bin/time` around `check-document-corpus-lifecycle.py` | This branch | PASS | 0 violations; 178 s, against 95 s on `main` | required | - |

The remaining difference from `main` was not profiled further and stays open.

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 25 | accepted | Call count, Profile, Archive regressions, Corpus check | The per-row history scan is removed; the earlier stated cause is corrected here because TSK-0012 is immutable. | SPEC-0212 TSK-0014 |

## Review and Completion

This Task completes on the evidence above. Hosted checks and the merge are
observed on the pull request.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Archive removal Task](tsk-0012-archive-history-only-removal.md)
