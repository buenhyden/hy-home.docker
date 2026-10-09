---
title: "Backup Telemetry and Budget Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "specs"
artifact_id: "SPEC-0228-TSK-0001"
parent_ids:
- "SPEC-0228-PLAN-0001"
created: "2026-10-10"
---

# Backup Telemetry and Budget Task

## Objective

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

Pending.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Dry run and tests | 1, 2 | W1 | Restic dry run; restic tests | `80f882f1e` | PASS | W1 Exclusion and Budget | accepted |
| Documents | 2 | W2 | markdownlint; metadata; links | `0e1701950` | PASS | W2 Documents | accepted |
| HOME | 3 | W3 | `.env` value; next scheduled run | — | NOT_RUN | W3 HOME | pending |
| Validation | 4 | W4 | Changed gate, staged style check, `candidate-quality` | — | NOT_RUN | Review and Completion | pending |

## Review and Completion

Not complete: HOME, validation and the merge remain.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
