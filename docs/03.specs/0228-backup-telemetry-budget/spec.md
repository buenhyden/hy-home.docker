---
title: "Backup Telemetry and Budget"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "specs"
artifact_id: "SPEC-0228"
parent_ids:
- "REQ-0026"
- "ADR-0041"
created: "2026-10-10"
---

# Backup Telemetry and Budget

## Overview

The nightly HOME backup of 2026-10-10 skipped its Restic step and failed: the
state repository had reached 5,227 MiB against the 5 GiB
`BACKUP_STATE_MAX_GIB` budget, so the offsite copy was skipped too. Snapshots
had grown from 275 MiB on 2026-09-22 to 2.97 GiB on 2026-10-08, almost all of
it the SeaweedFS volume files of the Loki and Tempo collections, which hold
short-retention telemetry and are rewritten daily. All 17 snapshots are under
30 days old, so the existing `forget-prune` retention would delete none of
them. The owner chose to stop backing up that telemetry and to raise the
budget to 8 GiB.

## Scope

In scope: the Restic state exclude list, the budget value in `.env.example`
and the HOME `.env`, their tests, the backup and telemetry documents and the
offsite ADR note, and the completion records of SPEC-0225 to SPEC-0227. Out
of scope: deleting snapshots, the offsite target, and the OpenBao snapshot
token gap the same run reported.

## Contracts

1. The state set skips `loki-bucket_*` and `tempo-bucket_*` under the
   SeaweedFS volume tree; every other SeaweedFS collection is still copied.
2. Loki logs and Tempo traces are not restored after a loss; they are
   collected again.
3. The state repository budget is 8 GiB; no snapshot is deleted to meet it.

## Acceptance Criteria

1. A Restic dry run with the new exclude list selects no Loki or Tempo file.
2. Tests pin the exclusions and the budget; the documents state both.
3. HOME uses the new budget and the next scheduled run backs up the state set.
4. The changed gate, the staged style check and `candidate-quality` pass.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-backup-telemetry-budget.md)
