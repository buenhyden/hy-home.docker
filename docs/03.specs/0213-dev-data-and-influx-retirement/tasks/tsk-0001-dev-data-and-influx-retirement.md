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

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Decision and documents | 1 | W1 | `check-document-metadata.py --mode check-changed`; link gate | Commit `12aeec76b` | PASS | `violations=0`; links 0 failures | accepted |
| Variable boundary | 2 | W2 | Non-interference renders; RED/GREEN unit test | `.env.example` with synthetic overrides | PASS | W2 Variable Boundary and Provisioning | accepted |
| Isolated provisioning | 3 | W2 | Isolated dev-pg run, network-client auth | Project `s0213iso`, synthetic secrets | PASS | W2 Variable Boundary and Provisioning | accepted |
| Influx source absence | 4 | W3 | Root render and reference scan | Pending | NOT_RUN | Pending | pending |
| HOME data check | 5 | W3 | Value-free data directory inspection | Pending | NOT_RUN | Pending | pending |
| Backup chain and canary | 6 | W4 | Isolated offline backup/restore | Pending | NOT_RUN | Pending | pending |

## Review and Completion

Not complete.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
