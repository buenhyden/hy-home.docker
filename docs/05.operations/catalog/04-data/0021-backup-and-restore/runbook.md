---
title: "Backup and Restore Runbook"
version: "1.1.0"
type: "operation/runbook"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-22"
layer: "operations"
artifact_id: "RUN-0021"
parent_ids:
- "GDE-0021"
created: "2026-09-22"
---

# Backup and Restore Runbook

## When to Use

Use to prepare the backup repositories, switch `mng-pg` to the pgBackRest
image, run or verify a backup, restore PostgreSQL to a point in time in
isolation, restore files from Restic, or delete old snapshots. Every step that
restarts a service, writes a repository or deletes snapshots needs its own
approval naming the target.

## Procedure

Run commands from the repository root of the running checkout. Never print
secret files or the rendered Compose model.

### 1. Prepare `.env`, directories and keys (once, before the change is checked out on the host)

Sync `.env` first: until `BACKUP_STATE_REPO_DIR` is set, recreating `mng-pg`
fails on a missing repository path.

```bash
bash scripts/operations/gen-secrets.sh --sync-metadata
bash scripts/operations/gen-secrets.sh
state=/home/hyunyoun/backups                 # the BACKUP_STATE_REPO_DIR value (SSD)
host=/home/hyunyoun/storage/backups          # the BACKUP_HOST_REPO_DIR value (data disk)
sudo install -d -o 70 -g 70 -m 0750 "$state/pgbackrest"
install -d -m 0700 "$state/restic" "$state/staging" "$host/restic"
```

Expected: `.env` gains `BACKUP_STATE_REPO_DIR`, `BACKUP_HOST_REPO_DIR`,
`BACKUP_STATE_MAX_GIB` and `POSTGRES_ARCHIVE_TIMEOUT` with existing values
untouched, the directories exist with the listed owners, and BKP-001/BKP-002
files exist. Copy both key
values to offline custody before the first backup. Stop if a path already holds
data you did not create.

### 2. Switch `mng-pg` to the pgBackRest image (approval: restarts every management-DB consumer)

Preconditions: a fresh logical dump to a 0600 file, for example
`docker exec mng-pg sh -c 'pg_dumpall -U "$POSTGRES_USER"' > "$state/pre-pgbackrest.sql"`,
and at least 20 GiB free under the state directory.

```bash
docker compose build mng-pg
docker compose up -d --no-deps mng-pg
docker exec -u postgres mng-pg pgbackrest --stanza=mng stanza-create
docker exec -u postgres mng-pg pgbackrest --stanza=mng check
```

Expected: `mng-pg` healthy, `stanza-create` and `check` end with `completed
successfully`, `SHOW archive_mode` returns `on`. Until `stanza-create` succeeds,
`archive_command` fails and WAL stays in `pg_wal`; past
`archive-push-queue-max` (4 GiB) pgBackRest drops WAL to protect the disk,
which leaves a point-in-time recovery gap until the next full backup.
Rollback: restore the previous image line in Compose and `up -d --no-deps mng-pg`;
set `archive_mode=off` first if the repository is unavailable.

### 3. Initialize Restic and install the timer (once)

```bash
docker compose --profile backup run --rm --no-deps restic init
sudo install -m 0644 infra/09-tooling/restic/systemd/hyhome-backup.service /etc/systemd/system/
sudo install -m 0644 infra/09-tooling/restic/systemd/hyhome-backup.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now hyhome-backup.timer
```

`init` skips a repository that already exists and never re-keys it.

### 4. Run or verify a backup

```bash
sudo systemctl start hyhome-backup.service
journalctl -u hyhome-backup.service -n 80 --no-pager
docker exec -u postgres mng-pg pgbackrest --stanza=mng info
docker compose --profile backup run --rm --no-deps restic snapshots
```

Expected: exit 0, a new pgBackRest backup, two new Restic snapshots, `restic
check` "no errors were found", and an empty `staging/`. Exit 75 means another
run holds the lock; exit 64 means a missing directory, less than 20 GiB free,
or a repository on the same filesystem as, or inside, its source. A run that
logs "over the 5 GiB budget; Restic backup skipped" exits 1 with pgBackRest
done and Restic untouched: review the logged sizes and request the approved
`forget-prune` (step 7) or a larger budget. The unit stops after four hours; staging is still
emptied, and a stale Restic lock is cleared with `restic unlock` once no Restic
process runs.

When SeaweedFS is running, the run also pauses vacuum and exports filer
metadata; error text from `weed shell`, an empty export, or only one of master
and filer running makes the run exit 1 (RUN-0024).

### 5. Point-in-time restore of `mng-pg` into isolation

Restore into a new directory, never over the live `PGDATA`. Image names come
from Compose, which owns the pins:

```bash
pg_image="$(docker compose config --images mng-pg)"
target='2026-09-22 06:13:56+00'   # a time after the last wanted commit
scratch="$(mktemp -d)"
chmod 0755 "$scratch"   # the postgres user (UID 70) must traverse it
docker run --rm \
  -v "$PWD/secrets/backup/pgbackrest_cipher_pass.txt:/run/secrets/pgbackrest_cipher_pass:ro" \
  -v "$state/pgbackrest":/var/lib/pgbackrest:ro \
  -v "$scratch:/var/lib/postgresql/data" \
  --entrypoint sh "$pg_image" -ec '
    mkdir -p /tmp/pgbackrest/conf.d
    printf "[global]\nrepo1-cipher-pass=%s\n" "$(cat /run/secrets/pgbackrest_cipher_pass)" > /tmp/pgbackrest/conf.d/cipher.conf
    chown -R postgres /tmp/pgbackrest
    install -d -o postgres -g postgres -m 0700 /var/lib/postgresql/data/pgdata
    gosu postgres pgbackrest --config-include-path=/tmp/pgbackrest/conf.d --stanza=mng \
      --type=time "--target='"$target"'" --target-action=promote --archive-mode=off restore'
```

Start the restored copy with the same image entrypoint, the cipher secret and
the repository mounted read-only, on an internal network, because recovery
reads WAL through `archive-get`:

```bash
docker network create --internal restore-check
docker run -d --name mng-pg-restore-check --network restore-check \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -e PGBACKREST_CONFIG_INCLUDE_PATH=/tmp/pgbackrest/conf.d \
  -v "$PWD/secrets/backup/pgbackrest_cipher_pass.txt:/run/secrets/pgbackrest_cipher_pass:ro" \
  -v "$state/pgbackrest":/var/lib/pgbackrest:ro \
  -v "$scratch:/var/lib/postgresql/data" \
  "$pg_image" postgres -c archive_mode=off
```

Expected log lines: `recovery stopping before commit`, `selected new timeline
ID`. Verify application rows with `psql`, then remove the container and network
and delete the scratch copy. Replacing the live cluster is a separate approved
cutover.

### 6. Restore files from Restic

Restore into a scratch directory with a plain container; the hardened job has
no rights to reapply ownership:

```bash
restic_image="$(docker compose --profile backup config --images restic)"
scratch="$(mktemp -d)"
docker run --rm -e RESTIC_PASSWORD_FILE=/pw \
  -v "$PWD/secrets/backup/restic_password.txt:/pw:ro" \
  -v "$state/restic:/repo:ro" -v "$scratch:/out" \
  "$restic_image" -r /repo --no-lock restore latest --target /out --include /src/state/exports
```

Use `"$host/restic"` for `secrets/` and `.env`.
Compare with `sha256sum`, then copy only the reviewed files back.

SeaweedFS is restored as one set: `--include /src/state/volumes/data/seaweedfs`
together with `/src/state/exports/seaweedfs-filer.meta` from the same snapshot,
then RUN-0024 (volume and master trees in place, empty filer store,
`fs.meta.load`).

### 7. Delete old snapshots (approval: irreversible)

```bash
docker compose --profile backup run --rm --no-deps \
  -e HYHOME_PRUNE_CONFIRM=delete-old-snapshots restic forget-prune
```

Keeps 30 daily, 13 weekly and 12 monthly snapshots per set. pgBackRest expires
its own backups by `repo1-retention-full=2`.

## Evidence

Record the command, exit status, pgBackRest backup label, Restic snapshot IDs,
restored row counts or file hashes and elapsed time. Never record key values,
dump contents or rendered configuration.

## Rollback or Recovery

- `archive_command` failing: `pgbackrest --stanza=mng check` shows the cause;
  fix the repository path or ownership, or set `archive_mode=off` with approval
  before `pg_wal` fills the disk ([RUN-0035](../0035-storage-exhaustion/runbook.md)).
- Wrong or lost key: pgBackRest `info` reports `status: error`; Restic reports
  `wrong password or no key found`. Recover the key from offline custody; there
  is no other way to read the repository.
- Interrupted Restic run: rerun; `restic unlock` only after confirming no
  other Restic process runs.

## Escalation

Escalate to the owner when a restore rehearsal fails, when both disks report
errors, or when a key is lost.

## Traceability

- Guide: [GDE-0021](guide.md); Policy: [POL-0021](policy.md)
- Runtime pins: [Restic Compose](../../../../../infra/09-tooling/restic/docker-compose.yml)
  and the [`mng-pg` image](../../../../../infra/04-data/operational/mng-db/pg/backup/Dockerfile)
- Rehearsal: `HYHOME_BACKUP_REHEARSAL=1 python3 -m unittest tests.validation.test_compose_baseline_gates.BackupRestoreRehearsalTests`

## Related Documents

- [pgBackRest user guide](https://pgbackrest.org/user-guide.html)
- [Restic: preparing a repository](https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html)
- [Restic: removing snapshots](https://restic.readthedocs.io/en/stable/060_forget.html)
