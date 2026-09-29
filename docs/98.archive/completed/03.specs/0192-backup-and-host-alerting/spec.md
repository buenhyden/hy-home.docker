---
title: "Backup and Host Alerting Specification"
version: "0.5.0"
type: "sdlc/spec"
status: "completed"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0192"
parent_ids:
- "REQ-0027"
created: "2026-09-29"
---

# Backup and Host Alerting Specification

## Overview

Three failures on 2026-09-26 to 09-29 raised no alert although Alertmanager
delivers to Slack (49 notifications, 0 failed):

- `hyhome-backup.service` ended with `timeout` four nights in a row, and no
  Restic snapshot was taken after 2026-09-25.
- The system disk that holds `BACKUP_STATE_REPO_DIR` fell to 17.5 GiB free,
  under the backup's 20 GiB preflight floor, so the next run would have
  stopped at once. Prometheus already collects `node_filesystem_avail_bytes`
  for `/`, but no rule reads it.
- After the `mng-pg` recreate, `n8n` answered every route except `/healthz`
  with 503 for about six hours while its health check stayed green.
  `PrometheusInfraTargetsMissing` fired for `n8n-monitor`, but only because
  the metrics route failed too.

## Boundaries and Inputs

In scope: a success timestamp written by
`infra/09-tooling/restic/bin/hyhome-backup.sh`, the node-exporter textfile
collector that reads it, alert rules for backup staleness and system-disk
space, the `n8n` health check, their contract tests, and RUN-0021.

Out of scope: the systemd collector (Docker's default AppArmor profile denies
node-exporter the D-Bus connection, measured 2026-09-29, and removing that
profile is not wanted), the unit files, other services' health checks, and
alert routing.

## Behavior Contract

1. A run that ends with status 0 writes
   `hyhome_backup_last_success_timestamp_seconds` to
   `BACKUP_STATE_REPO_DIR/metrics/hyhome_backup.prom`, replacing the file
   atomically and leaving it world-readable; a failed run leaves the previous
   value.
2. node-exporter reads that directory through a read-only bind mount that
   Compose never creates.
3. `HyhomeBackupStale` fires when the last success is more than 26 h old, or
   when the metric has been absent for 26 h.
4. `HostSystemDiskLow` fires when `/` has less than 25 GiB free for 15 min,
   before the backup's 20 GiB floor is reached.
5. The `n8n` health check calls `/healthz/readiness`, which fails while the
   database connection is lost.

## Technical Approach

- After the size line, when `status` is 0, write the metric to a temporary
  file in the metrics directory, set mode `0644`, and rename it.
- Add `--collector.textfile.directory=/textfile` and a long-syntax bind of
  `${BACKUP_STATE_REPO_DIR}/metrics` with `create_host_path: false` to
  `node-exporter`.
- Add both rules to `alert_rules.local.infra.yml` in a host group, with the
  runbook links to RUN-0021.
- Replace `/healthz` with `/healthz/readiness` in the `n8n` health check only;
  workers and task runners keep theirs.

## Interfaces and Data

New metric: `hyhome_backup_last_success_timestamp_seconds` (gauge, Unix
seconds). No new environment key; the mount reuses `BACKUP_STATE_REPO_DIR`.

## Failure Modes and Guardrails

| Failure | Guard |
| --- | --- |
| Docker creates a root-owned metrics directory the script cannot write | `create_host_path: false`; the directory is created by the host user before node-exporter is recreated |
| A killed or timed-out run cannot write its own failure | Only success writes; staleness detects every other end |
| The alert fires between rollout and the first successful run | The absence branch waits 26 h |
| Readiness fails during startup and marks `n8n` unhealthy | The existing 15 s start period and 5 retries; readiness returned 200 about 10 s after start on 2026-09-29 |

## Acceptance Contract

1. Contract tests assert the success-only atomic write, the read-only
   textfile mount with `create_host_path: false`, both rules and their
   thresholds, and the `n8n` readiness check; they fail before the change and
   pass after it.
2. After an approved node-exporter recreate and a backup run,
   `hyhome_backup_last_success_timestamp_seconds` is present in Prometheus
   and `HyhomeBackupStale` is inactive.
3. `promtool check rules` passes, and both new rules evaluate without error
   in the running Prometheus.
4. After an approved `n8n` recreate the container is healthy and readiness
   returns 200.
5. RUN-0021 names the metric, both alerts, and the response to each.
6. `run-ci-gate.py --profile full`, `tests/lib` and `tests/validation` pass.

## Traceability

- REQ-0027: the HOME development host.
- RUN-0021 and POL-0021: backup and restore.
- SPEC-0182 Task 0002: the failure records of 2026-09-29.
- SPEC-0191: the export timeout, which removed one cause of stale backups.

## Open Questions

None.

## Operational Impact

The script change takes effect on the next backup run. The textfile mount
and the health check take effect only when `node-exporter` and `n8n` are
recreated, each with owner approval; Prometheus reloads the rules.
