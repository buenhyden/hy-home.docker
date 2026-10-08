---
title: "DEV Data Boundary and InfluxDB Retirement"
version: "0.2.0"
type: "sdlc/spec"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-08"
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

The 2026-10-08 extension adds least-privilege accounts and scrape jobs for
the DEV exporters, a guard against empty or overlapping data paths, and the
DEV WAL archive with its retention, activation order and restore canary.

Excluded: purging the preserved InfluxDB data directory, hypertable creation
without a consumer query, direct hypertable CDC, offsite (R2) restore, and n8n
or other unrelated upgrades.

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
6. Backup recovery claims stay within proven evidence. No PITR is claimed for
   an environment until a restore to a chosen time has been checked there.
   Each restore claim names its environment.
7. DEV exporters never hold an administrator credential. `dev-pg-exporter`
   logs in as `dev_pg_monitor`, a marked `pg_monitor` member with a connection
   budget of 3 and no project database access. `dev-valkey-exporter` logs in
   as `devmonitor`, an ACL user with no key or channel pattern. Prometheus
   scrapes both.
8. A named volume's host path is never empty, relative, top-level, shared with
   another named volume or nested in one. The Compose validation rejects each
   case, preflight checks resolved paths, and DEV/MNG data roots fail at render
   when empty.
9. `dev-pg` archives WAL continuously to the `dev` stanza with full retention 2,
   differential retention 6 and a 2 GiB archive queue limit. The stanza exists
   before `archive_mode=on` takes effect. A hypertable is added only for a
   named consumer query and must state its time column, unique key, run
   idempotency, late-arrival rule, chunk interval and indexes, aggregate
   refresh, retention and backfill. Run, attempt, verdict and artifact rows stay
   relational.

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
7. An isolated run proves both exporters report the engine up through their
   monitor accounts, and that those accounts are denied writes, key reads and
   project database connections.
8. A regression test fails the Compose validation for nested, shared, empty
   and relative named-volume paths, and the full selection set passes.
9. An isolated run proves stanza creation with archiving off, `check` passing
   only after `archive_mode=on`, full and differential backups, and a restore
   to a chosen time that matches the row count and hash at that time.
10. The HOME activation (stanza, WAL, first full backup, restore canary) is
    recorded with its exact steps, or kept `NOT_RUN` with the reason.

## Related Documents

- [Plan](plan.md)
- [Task](tasks/tsk-0001-dev-data-and-influx-retirement.md)
- [Task 0002](tasks/tsk-0002-dev-backup-activation-and-monitoring.md)
- [ADR-0047](../../02.architecture/decisions/0047-dev-timescale-influx-retirement-and-load-tools.md)
- [SPEC-0212](../0212-request-baseline-and-reconciliation/spec.md)
- [Data architecture](../../02.architecture/descriptions/0004-data-architecture.md)
