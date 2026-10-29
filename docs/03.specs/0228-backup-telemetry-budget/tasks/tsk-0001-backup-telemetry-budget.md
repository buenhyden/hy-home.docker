---
title: "Backup Telemetry and Budget Task"
version: "0.2.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-10-29"
layer: "specs"
artifact_id: "SPEC-0228-TSK-0001"
parent_ids:
- "SPEC-0228-PLAN-0001"
created: "2026-10-10"
---

# Backup Telemetry and Budget Task

## Overview

### Objective

Make the nightly state backup fit its budget again without deleting restore
points.

## Inputs and Authorization

While checking SPEC-0226's restic evidence, the 2026-10-10 run was found to
have failed. On 2026-10-10 the owner chose "Exclude telemetry + 8 GiB":
stop backing up the Loki and Tempo SeaweedFS collections and raise
`BACKUP_STATE_MAX_GIB` to 8, deleting no snapshot.

## Work Log

### Findings

| Item | Value |
| --- | --- |
| Run 2026-10-10 03:36 KST | Restic skipped: state repository 5,227 MiB over 5 GiB; offsite skipped; exit 1 |
| Earlier runs | Succeeded 2026-09-30 to 10-04 and 10-08 to 10-09; failed 09-26 to 09-29 (timeout) and 10-05 to 10-08 (exit code) |
| Repository | Restic 4,498 MiB, pgBackRest 706 MiB, DEV pgBackRest 11 MiB |
| Snapshots | 17 per set, 2026-09-22 to 10-08; state size 275 MiB to 2.97 GiB |
| Largest source | SeaweedFS volume tree 2,301 MiB, mostly `loki-bucket_*` and `tempo-bucket_*` files |

The same run also skipped the OpenBao Raft snapshot because no snapshot token
is present; that gap is outside this spec.

### W1 Exclusion and Budget

`state-exclude.txt` gains `/src/state/volumes/data/seaweedfs/volume/loki-bucket_*`
and `tempo-bucket_*`; `.env.example` sets `BACKUP_STATE_MAX_GIB=8`. A dry run
of the pinned Restic image against the live SeaweedFS volume tree, into a
throwaway repository, listed no Loki or Tempo file and would add 333 MiB
(88 MiB stored) instead of about 2.3 GB.

### W2 Documents

POL-0021, GDE-0021, RUN-0021, POL-0048, the Restic README and ADR-0041 state
the exclusion, that telemetry is not restored, and the 8 GiB budget. The
SPEC-0225, SPEC-0226 and SPEC-0227 Tasks record their passing remote
candidates and merges.

### W3 HOME

The HOME `.env` value of `BACKUP_STATE_MAX_GIB` became 8 (key set unchanged,
values not printed) and `docker compose --profile backup config` renders 8.
The exclusion takes effect once the HOME checkout is on the merge, and the
next scheduled run (2026-10-11 03:33 KST) is the end-to-end check; it was not
started by hand.

### Owner decision 2026-10-29

The owner decided on 2026-10-29 to close the package on existing evidence.
PR #404 merged as `f75275651` with a passing hosted `candidate-quality` (run
38002771899, head `75a682505`). The HOME budget of 8 GiB was applied in W3, and
the 2026-10-13 `hyhome-state` snapshot `ae96be5f` (SPEC-0237 TSK-0001) shows
the scheduled backup took the state set after the budget change. Criteria 1
and 2 are accepted on their existing PASS rows.

The Evidence and Criterion Acceptance tables moved to the current shape (a
`Required` column and a `Current Owner` column, existing rows kept as they
were) so this acceptance can be recorded.

### Spec approval

The owner ratified the Spec on 2026-10-29.

### Plan approval

The owner ratified the Plan on 2026-10-29.

### Lifecycle Events

| Artifact | From | To | Evidence |
| --- | --- | --- | --- |
| SPEC-0228 | draft | approved | #spec-approval |
| SPEC-0228-PLAN-0001 | draft | approved | #plan-approval |
| SPEC-0228-TSK-0001 | draft | ready | #inputs-and-authorization |
| SPEC-0228-TSK-0001 | ready | in-progress | #owner-decision-2026-10-29 |
| SPEC-0228-TSK-0001 | in-progress | completed | #review-and-completion |

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Dry run and tests | 1, 2 | W1 | Restic dry run; restic tests | `80f882f1e` | PASS | W1 Exclusion and Budget | required | - |
| Documents | 2 | W2 | markdownlint; metadata; links | `0e1701950` | PASS | W2 Documents | required | - |
| HOME | 3 | W3 | `.env` value; next scheduled run | — | NOT_RUN | W3 HOME | required | - |
| Changed gate | 4 | W4 | Hardening; `run-ci-gate.py --profile changed --local-only`, base `39126d5bf`; operations catalog | `60917e9e7` | PASS | Review and Completion | required | - |
| Staged style check | 4 | W4 | `run-ci-precommit.sh --mode local-staged` | `60917e9e7` | PASS | Review and Completion | required | - |
| Remote candidate | 4 | W4 | `candidate-quality` | — | NOT_RUN | Review and Completion | required | - |
| Rerun of HOME | 3 | W3 | `.env` value; next scheduled run | W3 `.env` value of 8 rendered by `docker compose --profile backup config`; `hyhome-backup.service` run of 2026-10-13 completed the state step and produced `hyhome-state` snapshot `ae96be5f` (2026-10-13 13:06:50 UTC), recorded in SPEC-0237 TSK-0001 | PASS | Review and Completion | required | HOME |
| Rerun of Remote candidate | 4 | W4 | `candidate-quality` | PR #404 head `75a682505`, run 38002771899, merged as `f75275651` | PASS | Review and Completion | required | Remote candidate |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Decision | Current Owner |
| --- | --- | --- | --- | --- |
| 1 | accepted | Dry run and tests | Generation 5 row acceptance | SPEC-0228 TSK-0001 |
| 2 | accepted | Dry run and tests, Documents | Generation 5 row acceptance | SPEC-0228 TSK-0001 |
| 3 | accepted | Rerun of HOME | HOME uses the 8 GiB budget and the scheduled 2026-10-13 run backed up the state set (snapshot `ae96be5f`); the run failed only on the separate OpenBao token gap. | SPEC-0228 TSK-0001 |
| 4 | accepted | Changed gate, Staged style check, Rerun of Remote candidate | Local checks PASS; hosted `candidate-quality` PASS on PR #404. | SPEC-0228 TSK-0001 |

## Review and Completion

The local checks passed on `60917e9e7`. Not complete: `candidate-quality`, the
merge and the next scheduled run remain.

On 2026-10-29 the owner closed the package. PR #404 merged as `f75275651`
after a passing hosted `candidate-quality` (run 38002771899). The first
scheduled run was not recorded here; the 2026-10-13 run recorded in SPEC-0237
TSK-0001 is the evidence for criterion 3. That evidence lists paths only, so it
does not re-prove the Loki and Tempo exclusion, which criterion 1 covers.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
