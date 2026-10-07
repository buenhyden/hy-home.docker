---
title: "DEV Data Boundary and InfluxDB Retirement"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-07"
layer: "specs"
artifact_id: "SPEC-0213"
parent_ids:
- "REQ-0004"
- "REQ-0005"
- "AD-0004"
- "AD-0031"
- "ADR-0047"
created: "2026-10-07"
---

# DEV Data Boundary and InfluxDB Retirement

## Overview

Implement ADR-0047's data decisions. Keep the existing DEV TimescaleDB image,
platform/perf provisioners and pgBackRest chain. Keep MNG PostgreSQL plain.
Close the remaining DEV/MNG variable coupling, add per-role connection budgets,
and retire every active InfluxDB surface. SPEC-0212 conflicts C02–C08 are the
input.

## Scope

Included: ADR-0047 acceptance and amendment of the documents it changes,
DEV consumer variables, provisioner connection budgets with isolated proof,
removal of the InfluxDB service and its consumers, retirement of its
operations documents, a value-free data check, and the DEV backup/restore
linkage record.

Excluded: purging the preserved InfluxDB data directory, enabling WAL archive
or PITR, HOME container recreation, hypertable creation without a consumer,
direct hypertable CDC, and n8n or other unrelated upgrades.

## Contracts

1. Data placement: service metadata lives in MNG PostgreSQL, one database per
   service. Project business data lives in a DEV project database provisioned
   with owner (NOLOGIN), migrator, runtime and reader roles. `platform_dev` is
   the technical fixture, and `perf_db` keeps the existing quality contract.
   No study or language application database is created here.
2. DEV consumers reach `dev-pg` at its fixed internal port `5432` and the
   `postgres` admin database. They never read the MNG variables
   `POSTGRES_PORT` or `POSTGRES_DEFAULT_DB`, so changing those variables leaves
   every DEV consumer unchanged.
3. Each DEV login role has a connection budget set on every provisioning run:
   migrator 2, runtime 10 and reader 5. Provisioning fails before any SQL
   statement for unsafe names, an empty or malformed secret, a reused secret
   or a non-development environment. On a rerun it fails for ownership
   mismatches and never rotates an existing password. One project's roles
   cannot connect to another project's database.
4. No root profile closure, Traefik route, environment key, version
   projection, registered test or active document deploys or operates
   InfluxDB. Historical archive text, research and the SPEC-0212 record keep
   their wording. The operations Guide, Policy and Runbook move to Stage 98
   `retired/` with catalog rows.
5. Source removal and data disposal are separate. The InfluxDB data directory
   is preserved until an owner names it for purge. A purge first proves
   whether user data exists (no-data path) or exports and verifies it before
   removal (data path).
6. Backup recovery claims stay within proven evidence. With `archive_mode=off`
   no PITR is claimed. Each restore claim names its environment.

## Acceptance Criteria

1. ADR-0047 is accepted, and ADR-0039, ADR-0045, REQ-0005 and AD-0004, AD-0012,
   AD-0019 and AD-0024 state the retirement without contradiction.
2. A render with modified `POSTGRES_PORT` and `POSTGRES_DEFAULT_DB` leaves the
   DEV consumers' rendered environment unchanged, and a regression test
   enforces it.
3. An isolated `dev-pg` run proves connection budgets, login with a
   special-character password, rejection of an empty or reused secret, rerun
   idempotence, concurrent provisioning and cross-project denial.
4. The root `--profile '*'` model and its explicit `influxdb` target contain no
   InfluxDB service, and the retired surfaces list in the Task has no active
   remainder.
5. The Task records the HOME data check and the preserved data path without
   claiming purge or migration.
6. The Task records the DEV backup chain and an isolated offline
   backup/restore canary result, keeping HOME restore and PITR `NOT_RUN`.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-dev-data-and-influx-retirement.md)
- [ADR-0047](../../02.architecture/decisions/0047-dev-timescale-influx-retirement-and-load-tools.md)
- [SPEC-0212](../0212-request-baseline-and-reconciliation/spec.md)
- [Data architecture](../../02.architecture/descriptions/0004-data-architecture.md)
