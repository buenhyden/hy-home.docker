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

## Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Decision and documents | 1 | W1 | Metadata and link checks | Pending | NOT_RUN | Pending | pending |
| Variable boundary | 2 | W2 | Non-interference render and unit test | Pending | NOT_RUN | Pending | pending |
| Isolated provisioning | 3 | W2 | Isolated dev-pg run | Pending | NOT_RUN | Pending | pending |
| Influx source absence | 4 | W3 | Root render and reference scan | Pending | NOT_RUN | Pending | pending |
| HOME data check | 5 | W3 | Value-free data directory inspection | Pending | NOT_RUN | Pending | pending |
| Backup chain and canary | 6 | W4 | Isolated offline backup/restore | Pending | NOT_RUN | Pending | pending |

## Review and Completion

Not complete.

## Related Documents

- [Spec](../spec.md)
- [Plan](../plan.md)
