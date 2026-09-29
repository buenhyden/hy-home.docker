---
title: "Backup Valkey Export Timeout"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0191-TSK-0001"
parent_ids:
- "SPEC-0191"
- "SPEC-0191-PLAN-0001"
created: "2026-09-29"
---

# Backup Valkey Export Timeout

## Objective

Execute W1 and W2 of the [Plan](../plan.md) and record the evidence for every
acceptance criterion of [SPEC-0191](../spec.md).

## Inputs

- The `hyhome-backup.service` journal status lines of 2026-09-23 to
  2026-09-29 (no export content): successful runs log "SYNC sent to primary"
  about 5 s after `REPLCONF rdb-only`; failed runs log nothing after it.
- The owner's approval of 2026-09-29 for backup action A.

## Work Log

- 2026-09-29: Spec, Plan, and Task drafted on branch
  `fix/backup-valkey-export-timeout`.

## Verification Evidence

Not started.

## Review Evidence

None yet.

## Commit Ledger

None yet.

## Rulings

- 2026-09-29: Owner approved backup action A (bound the export); failure
  alerting and a manual run were not chosen.

## Deferred Items

None yet.
