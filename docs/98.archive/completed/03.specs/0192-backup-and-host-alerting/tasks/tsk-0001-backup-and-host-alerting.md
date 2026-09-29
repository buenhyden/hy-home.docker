---
title: "Backup and Host Alerting"
version: "0.4.0"
type: "sdlc/task"
status: "completed"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0192-TSK-0001"
parent_ids:
- "SPEC-0192"
- "SPEC-0192-PLAN-0001"
created: "2026-09-29"
---

# Backup and Host Alerting

## Objective

Execute W1 to W3 of the [Plan](../plan.md) and record the evidence for every
acceptance criterion of [SPEC-0192](../spec.md).

## Inputs

- SPEC-0182 Task 0002, entries of 2026-09-29: the preflight stop at 17.5 GiB
  free and the `n8n` 503 period.
- 2026-09-29 measurements: Alertmanager Slack notifications 49 sent, 0
  failed; a throwaway node-exporter v1.12.1 with the systemd collector failed
  with "An AppArmor policy prevents this" on the D-Bus connection;
  `node_filesystem_avail_bytes{mountpoint="/"}` is collected.

## Work Log

- 2026-09-29: Spec, Plan, and Task drafted.
- 2026-09-29 W1: `BackupAndHostAlertingContractTests` was added first and
  ran 4 tests with 3 failures and 1 error, then passed after the change.
  The first full gate failed only on the m0021 inventory, whose
  `node-exporter` Persistence cell lacked the new mount; that row was
  refreshed from `render_service_inventory` and the hand-written mount cell
  updated, after which `check-operations-catalog.py` passed.
- 2026-09-29 W2: `BACKUP_STATE_REPO_DIR/metrics` was created as the host user
  (`0755`) before `node-exporter` and `n8n` were recreated on their existing
  images; Prometheus reloaded through `/-/reload`. A backup run exited 0 in
  53 s (state snapshot `3f3baa66`, host snapshot `7e5e6521`, `restic check`
  clean) and wrote `hyhome_backup.prom` (`0644`).
- 2026-09-29 W3: the full gate and both suites passed on `a0bd0b8b6`.

## Verification Evidence

| Acceptance criterion | Plan work unit | Task result | Durable owner |
| --- | --- | --- | --- |
| 1 | W1 | PASS: `BackupAndHostAlertingContractTests` failed 3 and errored 1 of 4 before the change and passed after it (`a0bd0b8b6`) | [contract tests](../../../../tests/validation/test_compose_baseline_gates.py) |
| 2 | W2 | PASS: node-exporter serves `hyhome_backup_last_success_timestamp_seconds` with `node_textfile_scrape_error 0`; Prometheus returned an age of 31 s; `HyhomeBackupStale` went from pending (evaluated before the first scrape) to inactive at 12:13:59Z | [hyhome-backup.sh](../../../../infra/09-tooling/restic/bin/hyhome-backup.sh) |
| 3 | W1 | PASS: `promtool check rules` (prom/prometheus v3.14.0) on `alert_rules.local.infra.yml`: SUCCESS, 9 rules | [host backup rules](../../../../infra/06-observability/prometheus/config/alert_rules/alert_rules.local.infra.yml) |
| 3 | W2 | PASS: after `/-/reload` both rules report health `ok`; `HostSystemDiskLow` inactive with 45 GiB free | [host backup rules](../../../../infra/06-observability/prometheus/config/alert_rules/alert_rules.local.infra.yml) |
| 4 | W2 | PASS: after the recreate `n8n` is healthy, its health check runs `/healthz/readiness`, and readiness returns 200 | [n8n Compose](../../../../infra/07-workflow/n8n/docker-compose.yml) |
| 5 | W1 | PASS: RUN-0021 step 1 creates the metrics directory and step 4 names the metric, both alerts and the response to each (`a0bd0b8b6`) | [RUN-0021](../../../05.operations/runbooks/0021-backup-and-restore.md) |
| 6 | W3 | PASS: at `a0bd0b8b6`, `run-ci-gate.py --profile full` rc 0; `tests/lib` 945 OK; `tests/validation` 679 OK (23 skipped) | N/A: run evidence for this change |

## Review Evidence

None yet.

## Commit Ledger

| Commit | Unit | Change |
| --- | --- | --- |
| `f2febc2c8` | Package | Spec, Plan, and Task drafted; registry allocation |
| `a0bd0b8b6` | W1 | Success timestamp, textfile mount, both rules, `n8n` readiness check, tests, RUN-0021 and the m0021 row |

## Rulings

- 2026-09-29: Owner approved the package, the W2 runtime changes
  (recreate `node-exporter` and `n8n`, one backup run) and the pushes.

## Deferred Items

None yet.
