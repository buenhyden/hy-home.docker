---
title: "Restic Backup Jobs"
version: "1.0.0"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-22"
---

# Restic Backup Jobs

## Overview

One-shot jobs that snapshot HOME state into two encrypted Restic repositories on
different physical disks, plus the host orchestrator and timer that also drive
pgBackRest in `mng-pg`.

## Audience

Operators who run, verify or restore backups, and reviewers of the backup
boundary.

## Scope

In scope: the file-safe data-disk trees allowlisted in
[`sets/state-include.txt`](sets/state-include.txt), consistent exports
(PostgreSQL globals, Valkey RDB, three SQLite databases), `secrets/` and `.env`.
Out of scope: everything not allowlisted, in particular live engine
directories, which have their own method in POL-0021, and offsite copies (not
provided).

## Structure

```text
restic/
├── docker-compose.yml     # restic and backup-sqlite-export (profile backup)
├── backup.sh              # snapshots | init | backup | check | forget-prune | cmd
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
