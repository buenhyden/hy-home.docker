---
title: "Restic Backup Jobs"
version: "1.1.0"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-25"
---

# Restic Backup Jobs

## Overview

One-shot jobs that snapshot HOME state into two encrypted Restic repositories on
different physical disks, copy both to one Cloudflare R2 repository offsite
(ADR-0041), plus the host orchestrator and timer that also drive pgBackRest in
`mng-pg`.

## Audience

Operators who run, verify or restore backups, and reviewers of the backup
boundary.

## Scope

In scope: the file-safe data-disk trees allowlisted in
[`sets/state-include.txt`](sets/state-include.txt), consistent exports
(PostgreSQL globals, Valkey RDB, three SQLite databases), `secrets/` and `.env`.
Out of scope: everything not allowlisted, in particular live engine
directories, which have their own method in POL-0021. The pgBackRest
repository reaches R2 inside the state Restic repository (daily remote RPO);
there is no direct pgBackRest S3 repository.

## Structure

```text
restic/
├── docker-compose.yml     # restic, restic-offsite, backup-sqlite-export (profile backup)
├── backup.sh              # snapshots | init | backup | check | forget-prune | cmd
├── offsite.sh             # R2: snapshots | init | copy | check | cmd (no deletes)
├── export_sqlite.py       # Online Backup API copies with integrity check
├── sets/                  # state-include, state-exclude, host-exclude
├── bin/hyhome-backup.sh   # host orchestrator (lock, disk preflight, order)
└── systemd/               # hyhome-backup.service and .timer
```

## Tech Stack

The Restic and Python images are pinned in [`docker-compose.yml`](docker-compose.yml);
pgBackRest is pinned in the
[`mng-pg` image](../../04-data/operational/mng-db/pg/backup/Dockerfile).

## Configuration

- Profile `backup` (category automation, never HOME). `restic` defaults to
  `snapshots`, so `up` changes nothing.
- `restic` runs as root with only `DAC_OVERRIDE`, `network_mode: none` and
  every source mounted read-only; only `/repo/state` and `/repo/host` are
  writable. Repositories and staging use `create_host_path: false`.
- `backup-sqlite-export` mounts the Grafana, Gatus and Open WebUI data
  directories writable only because WAL readers need the `-shm` file; it writes
  0600 copies owned by UID 1000 into staging.
- `restic` has `mem_limit: 1g` for the repository index and tmpfs cache;
  `cmd` refuses `forget`/`prune`, which run only through `forget-prune`.
- Environment keys: `BACKUP_STATE_REPO_DIR`, `BACKUP_HOST_REPO_DIR`,
  `BACKUP_STATE_MAX_GIB`,
  `DEFAULT_MOUNT_VOLUME_PATH`, `DEFAULT_OBSERVABILITY_DIR`, `DEFAULT_AI_MODEL_DIR`,
  `SECRETS_GID`. Secret: `restic_password` (BKP-002).
- The orchestrator reads paths from `docker compose config`, never sources
  `.env`, takes a `flock` lock (exit 75 when busy), exits 64 when less than
  20 GiB is free or a repository shares a filesystem with (or sits inside) its
  source, skips the Restic step and fails when `BACKUP_STATE_REPO_DIR` is at or
  over `BACKUP_STATE_MAX_GIB` (5) after pgBackRest expiry, and always empties
  staging on exit.
- `restic-offsite` is the only backup job with egress (`restic_offsite_net`);
  it mounts only the two local repositories read-only (`DAC_READ_SEARCH`) and
  runs `restic copy --no-lock --from-repo` into
  `s3:https://<BACKUP_OFFSITE_R2_ACCOUNT_ID>.r2.cloudflarestorage.com/<BACKUP_OFFSITE_R2_BUCKET>`.
  Secrets: `restic_password` (source), `restic_offsite_password` (BKP-003),
  `r2_access_key_id` (BKP-004), `r2_secret_access_key` (BKP-005); the script
  exports the R2 keys without printing them. The orchestrator skips it while
  either key is empty, runs `copy` after a successful local backup and check,
  and `check --read-data-subset 10%` on Sundays; a failure fails the unit.
- `mng-pg` has a local build and no registry: use
  `docker compose pull --ignore-buildable` for pulls.

## Validation

```bash
python3 -m unittest tests.validation.test_compose_baseline_gates.BackupContractTests
HYHOME_BACKUP_REHEARSAL=1 python3 -m unittest tests.validation.test_compose_baseline_gates.BackupRestoreRehearsalTests
systemd-analyze verify infra/09-tooling/restic/systemd/hyhome-backup.service infra/09-tooling/restic/systemd/hyhome-backup.timer
```

## How to Work in This Area

Add a new source by deciding its consistent method first: a file-safe tree gets
an allowlist line; a live engine gets an export step in `bin/hyhome-backup.sh`
and no line only once it is safe to copy. Keep deletes in `forget-prune` behind its confirmation variable.
Setup, runs and restores follow the backup Runbook.

## Related Documents

Use the [documentation entry point](../../../docs/README.md) to reach Stage 05
subject `04-data/0021-backup-and-restore` (GDE/POL/RUN-0021).
