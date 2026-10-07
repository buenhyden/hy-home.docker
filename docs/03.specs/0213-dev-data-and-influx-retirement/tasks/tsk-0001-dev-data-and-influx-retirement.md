---
title: "DEV Data Boundary and InfluxDB Retirement Task"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-07"
layer: "specs"
artifact_id: "SPEC-0213-TSK-0001"
parent_ids:
- "SPEC-0213-PLAN-0001"
created: "2026-10-07"
---

# DEV Data Boundary and InfluxDB Retirement Task

## Objective

Accept ADR-0047, close the DEV/MNG variable coupling, add connection budgets,
retire every active InfluxDB surface and record the backup evidence.

## Inputs and Authorization

The current user request on 2026-10-07 asks to execute prompt 01 of the
analysis pack: DEV/MNG separation, the Timescale selection, InfluxDB removal
and the related policy, validator and document changes, with per-unit commits
and a per-Spec PR merge. It names no HOME restart, data purge or migration
target, so those lanes stay `NOT_RUN`. Baseline: `main` `e6ca3c030`
(SPEC-0212 merged). Registry issues SPEC-0213.

## Work Log

### Preserved Implementation

`dev-pg` already builds `hy-home/dev-pg:18.6-ts2.30.2-pgbackrest2.57` from
`timescale/timescaledb:2.30.2-pg18@sha256:cdf97a4b…` with pgBackRest
`2.57.0-r0`. Its Dockerfile records a synthetic build/load and offline restore
on 2026-10-03; that is dated evidence, not a result of this Task. The project
provisioner already creates NOLOGIN owner and migrator/runtime/reader roles,
binds roles and databases with ownership markers, takes a database-scoped
advisory lock, revokes PUBLIC, sets default privileges and never rotates an
existing password. dbt and Debezium already target `dev-pg`/`platform_dev`.
The Debezium publication is schema-scoped (`app`, `debezium_heartbeat`), not
`FOR ALL TABLES`. None of this is re-described as a migration.

### W1 Decision and Documents

ADR-0047 moved from `proposed` to `accepted` (0.2.0). REQ-0005 FR-0001 now
states the retirement, and its problem statement, STORY-01 and scope name DEV
TimescaleDB. ADR-0039's time-series bullet and ADR-0045's Data list point to
ADR-0047. AD-0004 drops the `influxdb` package row and states the retirement.
AD-0012 states it. AD-0019 and AD-0024 drop InfluxDB from their component and
dependency lists. The ADR index describes ADR-0047 as accepted and notes that
it replaces ADR-0039's time-series item. `check-document-metadata.py --mode
check-changed` at commit `12aeec76b` reported `selected=13 violations=0`, and
the link gate passed.

### W2 Variable Boundary and Provisioning

`dbt-db-provision`, `dbt` and `debezium-db-provision` read the MNG variables
`POSTGRES_PORT`/`POSTGRES_DEFAULT_DB` while targeting `dev-pg`. They now use the
fixed internal `5432` and `postgres`, matching the connector JSON. The new
`test_dev_consumers_do_not_read_management_postgres_variables` failed on five
values before the change (RED) and passes after it. Non-interference renders
(`env -i`, `.env.example`, `--profile '*'`): with `POSTGRES_PORT=6543` and
`POSTGRES_DEFAULT_DB=synthetic_other`, all seven DEV services render the same
environment, and only the 15 MNG consumers change. With
`DEV_PG_HOST_PORT=35999` and `DEV_PG_ADMIN_USER=synthetic_dev_admin`, only the
five DEV services change.

The provisioner now sets `CONNECTION LIMIT` 2/10/5 for migrator/runtime/reader
on every run, outside the activation branch.

The isolated run used project `s0213iso`, an internal network, synthetic
secrets and the local image `sha256:19ffce2c…` (built 2026-10-03, linux/amd64).
Results:

| Check | Exit | Observation |
| --- | --- | --- |
| Parallel provisioning A, B and A again, then A rerun | 0,0,0; 0 | Advisory locks serialize; idempotent |
| Role budgets | 0 | migrator 2, runtime 10, reader 5; owners NOLOGIN with no limit |
| Third concurrent migrator session | 1 rejected of 3 | `too many connections for role` |
| Timescale extension in project DB | 0 | `2.30.2` |
| Empty secret / reused secret manifests | 64 / 64 | Rejected before connecting |
| Unmarked pre-existing owner role | 3 | `role ownership mismatch`; no database created |
| Network login with special-character password (scram) | 0 | Login succeeded |
| Network login with a wrong password | failed | `password authentication failed` |
| Cross-project connect A to B, B to A | failed | `permission denied for database` |
| Rerun with changed secret, then login with new / old secret | 0; failed / 0 | Existing password not rotated |
| Owner table via migrator `SET ROLE`; runtime read; reader insert | 0; 0 (100 rows); 3 | Default privileges hold; reader write denied |

The first pass ran the password checks over `127.0.0.1` inside the container.
The image's `pg_hba.conf` trusts loopback, so that pass did not test password
authentication and is void. The network-client rerun above replaces it.
Network clients use `scram-sha-256`. The loopback trust is the upstream
image default and is reachable only inside the container.

### W3 InfluxDB Retirement

Removed from the active surface: `infra/04-data/influxdb/` (Compose leaf with
its Traefik route labels and profile, README, `migration/validate_mapping.py`),
the root include and its empty secret-section header, `INFLUXDB_PORT` in
`.env.example` and, key-only, in the private `.env` (key sets compared equal
afterwards without printing values), the `influxdb` profile row in POL-0078,
the `app-token` row in the gateway auth inventory test and GUIDE-0079, the
`test_influx_mapping` registration in `.github/workflow-contract.yml` and its
gate test, the tier-layout `DATA` entry, the Grafana README row, the Grafana
mixin note in GUIDE-0041, POL-0006 targets, the GDE-0017 identity in
POL/RUN-0030 and RUN-0035, the three operations README rows,
`infra/04-data/README.md`, and the research inventory row the operations
catalog check binds to current services. `sync-tech-stack-versions.sh --write`
regenerated the projection (remove=1). The generator also picked up another
worker's unstaged `ollama` tag change in the working tree; that hunk was
reverted so this commit carries only the InfluxDB removal.

The migration helper is retired with the leaf, without a successor. The
continuing guarantee it held, a verified mapping before data movement, is not
needed: see the data check below. GDE/POL/RUN-0017 moved byte-identical to
`docs/98.archive/retired/05.operations/{guides,policies,runbooks}/` with
`retired` catalog rows sourced from `e6ca3c030`. `git diff -M100%` shows
three pure renames, and `git cat-file -e` confirms each source path. The
bodies keep their frozen bytes, including `status: "active"`; the catalog row,
not the body, records the withdrawal. History, research text other
than the bound inventory row, and the archive keep their wording. The new
`test_retired_influxdb_has_no_active_deployment` checks absence from the
deployable model; it is not a repository-wide string ban. It failed against
the previous root include (RED) and passes now.

Render after removal: `--profile '*'` has 118 services with no InfluxDB
service, and `docker compose config influxdb` exits 1 (`no such service`).

The local-only gate (with the pinned pre-commit 4.6.1 exposed alone on
`PATH`; global 4.6.2 fails the pin check) first failed two tests. The public
environment count fell from 212 to 211, and the optional count from 164 to
163, because `INFLUXDB_PORT` was an optional key; the fixture counts now
match. `test_registry_matches_compose_image_declarations` failed only on
`Ollama` because another worker's unstaged working-tree tag
(`ollama/ollama:0.40.0`) differs from the tracked `0.35.0`; this commit does
not carry that file.

### HOME Data Check

Read-only, value-free inspection on 2026-10-07 at the HOME host (Compose
project `hy-home-infra`, 40 running containers): no `influxdb` container,
volume or image exists. The former bind root
`<DATA_ROOT>/data/influxdb` exists (13 MiB, 897 files, newest 2026-09-19).
Its contents by name and type are one catalog snapshot
(`data/node0/catalog/v3/snapshot`), a table-index marker, and a plugin
Python virtual environment. There are no Parquet files and no WAL files.
This matches the owner statement of 2026-10-02 (no stored data) recorded in
the retired README. The no-data path applies: there is nothing to export or
convert.

The directory is preserved. Purging it is a destructive operation and needs a
separate owner instruction naming the path. Without a container, no restart
blocking is needed: no root profile or service can recreate it.

### W4 Backup Chain and Restore Canary

The DEV chain is already linked; no source change was needed. `dev-pg` mounts
`${BACKUP_STATE_REPO_DIR}/dev-pgbackrest` (`create_host_path: false`) with the
encrypted `dev` stanza and a cipher passed only through the entrypoint include
file. `infra/09-platform-ops/restic/bin/hyhome-backup.sh` runs `pgbackrest
check`, then a diff or weekly full backup and globals/schema exports with
image and revision metadata. It does this only when the check passes. With
`archive_mode=off` the check fails, so HOME DEV backups do not run until WAL
activation is separately approved. `backup.sh` adds `state/dev-pgbackrest` to
the Restic source list, and RUN-0021 owns the restore procedure (`--set`
label, empty target, no `latest`, no PGDATA reuse). Without continuous WAL
there is no PITR claim.

Isolated canary in project `s0213iso`: 100 owner-owned rows in
`proj_a.app.canary` were hashed. Then the source was stopped,
`pgbackrest --no-online stanza-create` and `--no-online --force --type=full
backup` ran (exit 0), and label `20261007-120930F` was restored with `--set`
from a read-only repository mount into an empty volume (exit 0). The restored
instance started and matched the row count and hash. It kept Timescale
`2.30.2` and the role budgets 2/10/5, and accepted the special-character
password over the network. This is offline synthetic evidence. It is not
HOME backup, WAL, PITR, offsite or RPO/RTO evidence.

Cleanup is incomplete: removal of the isolated containers
(`s0213iso-pg`, `s0213iso-restored`), networks (`s0213iso-net`,
`s0213iso-net2`) and volumes (`s0213iso-data`, `-repo`, `-restore`) was denied
by the session permission policy. They hold synthetic data only and remain
for the operator to remove.

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Decision and documents | 1 | W1 | `check-document-metadata.py --mode check-changed`; link gate | Commit `12aeec76b` | PASS | W1 Decision and Documents | accepted |
| Variable boundary | 2 | W2 | Non-interference renders; RED/GREEN unit test | `.env.example` with synthetic overrides | PASS | W2 Variable Boundary and Provisioning | accepted |
| Isolated provisioning | 3 | W2 | Isolated dev-pg run, network-client auth | Project `s0213iso`, synthetic secrets | PASS | W2 Variable Boundary and Provisioning | accepted |
| Influx source absence | 4 | W3 | Root render, explicit target, reference scan, RED/GREEN absence test | `.env.example`; working tree | PASS | W3 InfluxDB Retirement | accepted |
| HOME data check | 5 | W3 | `docker ps -a`/volume/image list; directory size, count and file-type scan | HOME host, 2026-10-07 | PASS | HOME Data Check | accepted |
| Backup chain and canary | 6 | W4 | Source chain read; isolated offline full backup, `--set` restore, row/hash match | Project `s0213iso`, label `20261007-120930F` | PASS | W4 Backup Chain and Restore Canary | accepted |
| Remote candidate | 2, 3, 4 | W2, W3 | PR #370 `candidate-quality` run 37628494658 | Head `26d2e9717` | PASS | PR #370 | accepted |
| HOME restore, WAL and PITR | 6 | W4 | HOME stanza, WAL archive and restore | No approved target | NOT_RUN | W4 Backup Chain and Restore Canary | pending |

## Review and Completion

Source and isolated work is complete, and the remote PR candidate passed on
`26d2e9717`.
HOME restore, WAL/PITR, data purge and isolated-resource cleanup stay
separate and are not claimed.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
