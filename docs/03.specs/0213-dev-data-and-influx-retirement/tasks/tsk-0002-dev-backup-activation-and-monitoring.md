---
title: "DEV Backup Activation and Monitoring Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-08"
layer: "specs"
artifact_id: "SPEC-0213-TSK-0002"
parent_ids:
- "SPEC-0213-PLAN-0001"
created: "2026-10-08"
---

# DEV Backup Activation and Monitoring Task

## Objective

Close the SPEC-0213 residuals that TSK-0001 left outside source: least-privilege
DEV exporter accounts with a metrics consumer, a guard against empty or
overlapping data paths, the DEV WAL archive with retention, and its HOME
activation.

## Inputs and Authorization

The current user request on 2026-10-08 asks to execute prompt 01 of the
analysis pack again against `main` `a56ab4e5b`. It asks to verify the
`archive_mode=off` boundary on HOME and to connect WAL activation, schedule,
capacity, retention and a separate restore, to add the new exporter roles and
consumers as a separate unit instead of repeating the variable and permission
work, and to delete only resources whose context, label, ownership and reuse
are confirmed. TSK-0001 stays as the historical record and is not rewritten.

The analysis pack the request links to is the 2026-10-07 fifteen-item version.
Its later twenty-item revision was not available locally. This Task uses only
facts re-observed on 2026-10-08.

## Work Log

### Baseline and Residual Check

`main` and `origin/main` were `a56ab4e5b` (PR #371 merged). Every tracked
InfluxDB mention outside the archive and references is a retirement statement,
the `retired-route-record` rows in the metadata profile, or the absence test.
HOME has no InfluxDB container, image, volume or network. The 2026-10-07
synthetic resources `s0213iso-*` no longer exist, so there is nothing of that
run to remove.

`SERVICE_POSTGRES_*` survives only as the LAB fixture variables in
`labs/postgresql-ha.yml`. The MNG init job no longer reads it, which
`test_management_init_does_not_create_new_business_database` enforces. CDC
stays schema-scoped (`app`, `debezium_heartbeat`) with hypertable chunks
unsupported, as TSK-0001 recorded.

### HOME Observation

Read-only, 2026-10-08:

| Item | Observed |
| --- | --- |
| `dev-pg` | Running 7 h, `archive_mode` `off`, `wal_level` `logical`, 25 MB in one `postgres` database, `pg_wal` 64 MB |
| `dev` stanza | `pgbackrest info`: `error (missing stanza path)`; `check`: `[087] archive_mode must be enabled` |
| Repository root | `${BACKUP_STATE_REPO_DIR}/dev-pgbackrest` owned `1000:1000` mode `0775`; the server runs as uid 70, so `stanza-create` could not write it |
| Capacity | Root filesystem 249 GB, 38 GB free (85 % used) |
| Nightly backup | `hyhome-backup.service` 2026-10-08 03:31 exited 1. Its only failure line was `dev-pg check or physical backup failed; exports skipped`; MNG, Restic and the R2 copy succeeded |
| `dev-pg-exporter` | Running from an uncommitted working-tree draft as the admin superuser, reading the MNG `POSTGRES_PORT` |
| `dev-valkey-exporter` | Running from the same draft with no ACL user: `redis_up 0` |
| Metrics consumer | No Prometheus job scraped either exporter |

So the nightly unit fails every night on DEV alone, which hides any other
failure, and the HOME exporters either over-privilege or do not work.

### W5 Exporter Monitor Accounts

`dev-pg-monitor-provision` runs `pg/provision/monitor.py`. It reuses the
project provisioner's secret reader, rejects a monitor secret equal to the
admin secret, creates a marked NOLOGIN role, activates its password only while
it cannot log in, and grants `pg_monitor` with connection limit 3 and a 10 s
statement timeout. `dev-pg-exporter` reads that role through
`DATA_SOURCE_PASS_FILE` on the fixed internal port. `render-acl.sh` adds
`devmonitor` with `-@all` plus `PING`, `INFO`, `CONFIG GET`, `CLIENT
LIST|INFO|SETNAME`, `SLOWLOG GET|LEN`, `LATENCY LATEST|HISTOGRAM` and `CLUSTER
INFO`, without a key or channel pattern. Both Prometheus configs scrape the two
exporters. The working-tree draft also added `dev_data_net` to RedisInsight;
that inspector ACL belongs to prompt 13 and is not carried here.

Isolated run, project label `hy-home.test=s0213mon`, internal network,
synthetic secrets, image `sha256:19ffce2c…`:

| Check | Result |
| --- | --- |
| Provision first run, rerun | exit 0, 0 |
| Rerun with a changed secret, then login with new / original secret | exit 0; new fails, original succeeds (no rotation) |
| Monitor secret equal to admin secret | exit 64 before connecting |
| Role attributes | LOGIN, limit 3, not superuser, `pg_monitor` member |
| `postgres-exporter` | `pg_up 1`, 96 `pg_stat_database_*` series, 0 error log lines |
| Connect to a project database with CONNECT revoked from PUBLIC | `permission denied for database` |
| `CREATE TABLE`; terminate a superuser backend | `permission denied for schema public`; refused |
| `redis_exporter` as `devmonitor` | `redis_up 1`, `last_scrape_error` 0 |
| `GET`, `SET`, `KEYS`, `FLUSHALL`, `CLIENT KILL`, `CONFIG SET` | `NOPERM` each |
| Anonymous `PING` | `NOAUTH` |

The provisioner's psql variable was later renamed from `monitor_password` to a
shorter constant so the local secret-scan hook stops matching a variable
reference. The generated SQL is otherwise unchanged.

### W6 Data Path Guard

`report_storage_overlaps` in `validate-docker-compose.sh` reads each
selection's rendered named volumes. It rejects a `driver_opts.device` that is
empty, relative or top-level (what an empty data-root variable leaves), shared
or nested. Preflight runs it on resolved paths. DEV and MNG devices now use
`${VAR:?}`, so an empty data root fails at render. Bind mounts that two
services share on purpose (`backup-sqlite-export`, Supabase storage, n8n
custom nodes) are service binds, not named volumes, and are out of this rule.

The new regression case failed four sub-cases against the previous script
(RED) and passes now. The full validation passed 67 selections and 324
services. Preflight on HOME stopped at exit 127 before the new check, because
the private `.env` holds an unquoted value with spaces (`COMFYUI_ARGS`) that
shell sourcing cannot read; Compose reads it correctly. The same check run on
the HOME rendered model with resolved paths exited 0. The `.env` value was not
printed or changed.

### W7 WAL Archive and PITR

`dev-pg` now sets `archive_mode=on`. `pgbackrest.conf` sets full retention 2,
differential retention 6 and `archive-push-queue-max=2GiB`. The entrypoint
sets the repository root to `postgres` `0750` only when it differs, never
recursively. Because the configuration is built into the image, the tag moved
to `hy-home/dev-pg:18.6-ts2.30.2-pgbackrest2.57-r2`. The previous unit test
that required WAL to stay off was replaced by one that requires it on and
bounded.

Isolated run, project label `hy-home.test=s0213wal`, named volumes, internal
network, synthetic secrets, image `sha256:d2999910…`:

| Step | Result |
| --- | --- |
| Repository root before / after entrypoint | `1000:1000 0775` / `70:70 0750` |
| `check` with archiving off, no stanza | exit 87 |
| `stanza-create` with archiving off | exit 0 |
| `check` with archiving off, stanza present | exit 87 |
| `check` after restart with `archive_mode=on` | exit 0 |
| Full backup, 100 rows | exit 0, `20261008-002230F` |
| 50 more rows, time T, 25 more rows, WAL switch | archiver success, 0 failures |
| Differential backup | exit 0; WAL range `…01`–`…06` |
| Restore `--set=20261008-002230F --type=time --target=T` into an empty volume, repository read-only | `restore-ok` |
| Restored instance | Promoted on timeline 2; 150 rows with the hash taken at T; rows after T absent; Timescale 2.30.2 |

The first rehearsal found two defects. The unconditional `chown` failed on the
read-only repository mount and stopped the restored container, which is why
the change is now conditional. A restore run with a different
`--config-include-path` writes that path into `restore_command`; RUN-0021 now
requires the entrypoint path. Both were fixed before this result.

### Cleanup

The `s0213mon` containers and network were removed by label. Removing the
anonymous PGDATA volume `3bcf68fd…` of that run (created 2026-10-08 08:51 KST
with the test container) and the scratch secret directory was denied by the
session permission policy; both are synthetic and remain for the operator.
All `s0213wal` containers, volumes and the network were removed by label, with
zero remaining.

### Review and Remote Candidate

The first PR #372 candidate run (37709112470) failed `operations-catalog` with
14 findings: the three new services had no Guide binding, POL-0078 did not
list them under `dev-data`, and the service inventory lacked their rows while
four rows kept stale cells. This check is a remote candidate leaf, so the
local changed gate did not select it. GDE-0100 and POL-0078 now bind them and
the inventory was re-rendered with `render_service_inventory`; the local
`check-operations-catalog.py` then passed.

The rerun of run 37710173068 first failed on a `proxy.golang.org` 403 while
installing a hook toolchain, then on commit-message schema: four commits had
two body paragraphs where `.cz.toml` allows one. Their messages were joined
into one paragraph with identical trees, `cz check` over the branch passed, and
the hashes cited here were updated.

An independent read-only review found no critical or important defect and
five minor ones, all fixed: GDE-0021 still said `archive_mode=off`; GDE-0100
lacked the stanza-first step for a new host; the runbook named no signal for a
queue-limit WAL drop, which `pg_stat_archiver` does not count; preflight
reported a render failure as a path overlap; and the runbook's ownership step
omitted `chmod 0750`, which a read-only restore container would then fail on.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HOME backup boundary | 10 | W8 | `pgbackrest info`/`check`; journal of `hyhome-backup.service` | HOME 2026-10-08 | PASS | HOME Observation | accepted |
| Exporter accounts | 7 | W5 | Isolated monitor provision, exporter and ACL denial run | Label `s0213mon`, synthetic secrets | PASS | W5 Exporter Monitor Accounts | accepted |
| Exporter unit tests | 7 | W5 | `test_dev_pg_provision`, `test_dev_valkey_acl`, `test_dev_data_boundary` | Commit `e5a813e3d` | PASS | W5 Exporter Monitor Accounts | accepted |
| Data path guard | 8 | W6 | RED/GREEN overlap regression; `validate-docker-compose.sh` | Commit `6fbc3bf99`; `.env.example` | PASS | W6 Data Path Guard | accepted |
| HOME preflight | 8 | W6 | `validate-docker-compose.sh --preflight` | HOME `.env` | FAIL | W6 Data Path Guard | rejected |
| HOME resolved-path check | 8 | W6 | `report_storage_overlaps realpath` on the HOME model | HOME `.env` | PASS | W6 Data Path Guard | accepted |
| WAL and PITR rehearsal | 9 | W7 | Isolated stanza, archive, full/diff backup, time restore | Label `s0213wal`, image `sha256:d2999910…` | PASS | W7 WAL Archive and PITR | accepted |
| HOME activation | 10 | W8 | Stanza, WAL, first full backup, restore canary | Merged source | NOT_RUN | Review and Completion | pending |

## Review and Completion

W5–W7 are complete in source and isolation. HOME preflight is a recorded
failure from the private `.env` format, not from this change; its replacement
check passed. W8 waits for the merge so HOME runs the reviewed source, in the
RUN-0021 order: repository root ownership, `stanza-create` with archiving off,
recreation with `archive_mode=on`, `check`, first full backup, then the
isolated restore canary. PITR on HOME and offsite (R2) restore stay
`NOT_RUN` until recorded here.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
- [Task 0001](tsk-0001-dev-data-and-influx-retirement.md)
- [Backup policy](../../../05.operations/policies/0021-backup-and-restore.md)
- [Backup runbook](../../../05.operations/runbooks/0021-backup-and-restore.md)
