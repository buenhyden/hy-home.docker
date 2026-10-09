---
title: "Backup Telemetry and Budget Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-10"
layer: "specs"
artifact_id: "SPEC-0228-PLAN-0001"
parent_ids:
- "SPEC-0228"
created: "2026-10-10"
---

# Backup Telemetry and Budget Plan

## Overview

Exclude the telemetry collections, raise the budget, document both, apply the
budget on HOME and confirm with the next scheduled run.

## Work Breakdown

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| W1 | 1, 2 | Exclude list, budget, test and dry run | None | TSK-0001 | Task evidence |
| W2 | 2 | Backup, telemetry and ADR documents; earlier Task completion records | W1 | TSK-0001 | Task evidence |
| W3 | 3 | HOME `.env` value; next scheduled run | W2 | TSK-0001 | Task evidence |
| W4 | 4 | Changed gate, staged style check, candidate quality, merge | W2 | TSK-0001 | Task evidence |

## Verification Plan

A Restic dry run against the live SeaweedFS tree in a throwaway repository,
the restic tests, the document checks, the gate, and the journal and
snapshot listing of the next scheduled run.

## Risks and Rollback

- Logs and traces are lost if SeaweedFS is lost; the owner accepted this.
- Existing snapshots still hold telemetry until they age out, so the
  repository stays above 5 GiB for up to 30 days; the 8 GiB budget covers it.
- Rollback: revert the commits and set `BACKUP_STATE_MAX_GIB` back to 5.

## Related Documents

- [Spec](spec.md)
- [Task](tasks/tsk-0001-backup-telemetry-budget.md)
