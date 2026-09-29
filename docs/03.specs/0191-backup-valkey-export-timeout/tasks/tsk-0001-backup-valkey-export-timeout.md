---
title: "Backup Valkey Export Timeout"
version: "0.4.0"
type: "sdlc/task"
status: "completed"
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
- 2026-09-29 W1: the assertions were added first; `BackupContractTests` ran
  6 tests with 1 failure, then passed after the script change. RUN-0021 step
  4 states the limit. Inside `mng-valkey`, `timeout 1 sleep 5` ended with
  status 143, and the unbounded export finished in 5 s (1098638 bytes)
  earlier the same day. The branch merged into `main` before the
  2026-09-30 03:37 KST run, which reads the script from the checkout.
- 2026-09-29 W2: a first verification run was void because the working tree
  switched branches while it ran; the rerun on `main` is recorded below.

## Verification Evidence

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W1 | PASS: `BackupContractTests` failed 1 of 6 before the script change and passed after it (`e57b9190b`) | [backup contract tests](../../../../tests/validation/test_compose_baseline_gates.py) |
| 2 | W1 | PASS: `timeout 1 sleep 5` in `mng-valkey` exited 143; the live export finished in 5 s, well inside 300 s | [hyhome-backup.sh](../../../../infra/09-tooling/restic/bin/hyhome-backup.sh) |
| 3 | W1 | PASS: RUN-0021 step 4 states the limit, the log line, the dropped file and exit 1 (`e57b9190b`) | [RUN-0021](../../../05.operations/runbooks/0021-backup-and-restore.md) |
| 4 | W2 | PASS: on `main` at `593b34022`, `run-ci-gate.py --profile full` rc 0; `tests/lib` 945 OK; `tests/validation` 675 with one failure, `test_timeout_still_cleans`, whose module reran OK (55 tests); pre-commit rc 0 | N/A: run evidence for this change |

## Review Evidence

- `test_timeout_still_cleans` failed once while another session ran the test
  suite on the same host: its injected timeout lost the race to a failed
  state query (`reason=source-state-query-failed`). It does not touch the
  backup script, and its module passed on rerun.

## Commit Ledger

| Commit | Unit | Change |
| --- | --- | --- |
| `dc416d695` | Package | Spec, Plan, and Task drafted; registry allocation |
| `e57b9190b` | W1 | Export bounded at 300 s; test and RUN-0021 |

## Rulings

- 2026-09-29: Owner approved backup action A (bound the export); failure
  alerting and a manual run were not chosen.

## Deferred Items

- Confirm the 2026-09-30 03:37 KST run; this is tracked in the SPEC-0182
  Task 0002 Deferred Items.
