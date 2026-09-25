---
title: "Backup and Restore Guide"
version: "1.0.0"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-22"
layer: "operations"
artifact_id: "GDE-0021"
parent_ids:
- "POL-0021"
implementation_services:
  infra/09-tooling/restic/docker-compose.yml:
  - restic
  - backup-sqlite-export
created: "2026-09-22"
---

# Backup and Restore Guide

## Usage

### What owns which copy

| Tool | Owns | Does not own |
| --- | --- | --- |
| pgBackRest inside `mng-pg` | Physical backups of the management PostgreSQL cluster, continuous WAL archive, point-in-time recovery | Any other engine; logical per-database exports |
| Restic (`restic` job) | Encrypted, deduplicated snapshots of the allowlisted file-safe trees in `sets/state-include.txt`, consistent exports, `secrets/` and `.env` | Everything not allowlisted, in particular live engine directories (PostgreSQL, Valkey, Kafka, OpenBao Raft, TSDB, log, search and LAB stores) and ComfyUI models |
| `backup-sqlite-export` job | Consistent copies of the Grafana, Gatus and Open WebUI SQLite databases through the Online Backup API | Other SQLite files |
| Host orchestrator `hyhome-backup.sh` | Order, single-run lock, cross-disk preflight, PostgreSQL globals and Valkey RDB exports | Retention deletes (`forget-prune`) |

A copy of a running PostgreSQL data directory is never a database backup; the
PostgreSQL recovery path is pgBackRest only.

### Destinations

Two repositories cross the host's two physical disks so a single disk failure
leaves one copy:

- `BACKUP_STATE_REPO_DIR` (system SSD): pgBackRest repository `pgbackrest/`,
  Restic repository `restic/` for data-disk state, and export staging `staging/`.
  Its total size is capped by `BACKUP_STATE_MAX_GIB` (5).
- `BACKUP_HOST_REPO_DIR` (data disk): Restic repository `restic/` for
  `secrets/` and `.env`, which live on the SSD.

The orchestrator refuses a repository on the same filesystem as, or inside,
the data it protects. Both repositories are on one host, so offsite recovery is
not provided.

### Schedule and load

`hyhome-backup.timer` fires daily at 03:30 KST with up to 30 minutes of random
delay; the run stops after four hours. pgBackRest takes a full backup on Sunday and a differential backup on
other days; `archive_timeout` bounds unarchived WAL to five minutes. The unit
runs at `Nice=10` with the idle I/O class and Restic gets a low block-I/O
weight. Renovate (Monday 00:00–01:00) and Spark table maintenance (Sunday
05:00) never overlap this window.

### Capacity and growth (measured 2026-09-22)

| Repository | Input measured | Bound |
| --- | --- | --- |
| pgBackRest (SSD) | all databases 96 MB; WAL about 14 MB/h (330 MB/day before compression; forced switches every `archive_timeout` pad segments with zeros that zstd removes) | two full backups plus their differentials and WAL (about two weeks); planning estimate under 2 GB, to be replaced by the logged size |
| Restic state (SSD) | allowlisted trees about 0.3 GB (registry 236 MB, Open WebUI uploads, Airflow DAGs/config/plugins) plus exports about 10 MB | deduplicated; grows by daily changes until `forget-prune`, planning estimate under 5 GB per year |
| Restic host (data disk) | `secrets/` and `.env`, kilobytes | negligible |
| Staging | exports only during a run | emptied on every exit |

Growth is linear, not exponential: nothing is re-copied from a previous backup,
and the orchestrator refuses a repository inside a backed-up source. Airflow
logs (175 MB, about 64 MB/day) and caches are deliberately outside the
allowlist. Each run logs the three repository sizes to the journal; the budget
is enforced: after pgBackRest has expired old backups the orchestrator measures
`BACKUP_STATE_REPO_DIR` and, at or over `BACKUP_STATE_MAX_GIB`, skips the
Restic step and fails the run instead of deleting anything. The estimates above
total under 3 GB (under 2 GB pgBackRest, about 0.3 GB Restic at start). The
20 GiB free-space floor applies to the SSD.

### Keys

`secrets/backup/pgbackrest_cipher_pass.txt` (BKP-001) encrypts the pgBackRest
repository and `secrets/backup/restic_password.txt` (BKP-002) both Restic
repositories. They are backed up inside the host repository, which needs the
same Restic password to open, so keep an offline copy of both values outside
this host. Losing them makes every backup unreadable.

## Common Checks

Checks that change no backup data (Restic still writes a short-lived lock):

```bash
docker exec -u postgres mng-pg pgbackrest --stanza=mng info
docker compose --profile backup run --rm --no-deps restic snapshots
systemctl list-timers hyhome-backup.timer
journalctl -u hyhome-backup.service -n 50 --no-pager
```

Healthy output shows `status: ok` with a recent backup and a WAL archive range,
recent `hyhome-state` and `hyhome-host` snapshots, and a successful last run.

## Runbook Handoff

Initial setup, a manual run, restores, point-in-time recovery and retention
deletes are procedures in [RUN-0021](../runbooks/0021-backup-and-restore.md).

## Traceability

- Policy: [POL-0021](../policies/0021-backup-and-restore.md)
- Implementation: [Restic Compose](../../../infra/09-tooling/restic/docker-compose.yml),
  [Restic package](../../../infra/09-tooling/restic/README.md),
  [pgBackRest image](../../../infra/04-data/operational/mng-db/pg/backup/Dockerfile)

## Related Documents

- [Management database runbook](../runbooks/0028-management-database.md)
- [Storage exhaustion runbook](../runbooks/0035-storage-exhaustion.md)
