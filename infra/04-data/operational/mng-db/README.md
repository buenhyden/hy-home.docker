---
title: "Management Database (mng-db)"
version: "1.1.0"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-22"
created: "2025-12-03"
---

# Management database

## Overview

This package defines the repository's HOME management PostgreSQL and Valkey.

## Audience

It is intended for operators and maintainers of shared management state.

## Scope

[`docker-compose.yml`](docker-compose.yml) defines HOME `mng-pg`, `mng-pg-init`,
`mng-pg-exporter`, `mng-valkey`, and `mng-valkey-exporter`. Profiles `mng`, `core`,
`dev`, and `local` select both engines/init; exporters use `mng` and `dev`.
`mlops`, `data-science`, `analytics-engineering` and `cdc` also select `mng-pg`
and `mng-pg-init` for dependency closure only. The declared `mng-pg` command
enables logical WAL (`wal_level=logical` plus slot, sender and retention caps) for
CDC and continuous WAL archiving to pgBackRest; a running instance keeps its old
settings until an approved recreate.

`mng-pg` is built from [`pg/backup/Dockerfile`](pg/backup/Dockerfile): the plain
PostgreSQL image plus the pinned Alpine pgBackRest package, so `archive_command`
runs inside the server as the `postgres` user (UID/GID 70).
[`pg/backup/pgbackrest.conf`](pg/backup/pgbackrest.conf) defines stanza `mng`
with an encrypted repository at `/var/lib/pgbackrest`, bound to
`${BACKUP_STATE_REPO_DIR}/pgbackrest` on the other physical disk
(`create_host_path: false`). [`pg/backup/entrypoint.sh`](pg/backup/entrypoint.sh)
writes the `pgbackrest_cipher_pass` secret into a 0600 include file under
`/tmp/pgbackrest/conf.d` before the official entrypoint starts; the passphrase
never enters the environment or tracked configuration. An empty or
whitespace-bearing secret stops the container with exit 64.

## Structure

`mng-pg-data` maps to `${DEFAULT_MANAGEMENT_DIR}/pg`. The init job creates current
roles/databases for n8n, Keycloak, Airflow, Terrakube, SonarQube and the configured
application database. `mng-valkey-data` maps to
`${DEFAULT_MANAGEMENT_DIR}/valkey`, with AOF enabled for workflow broker/cache
state. Grafana is not wired to management PostgreSQL in current Compose.

PostgreSQL reads `mng_postgres_password` and `pgbackrest_cipher_pass`; init reads the service database password
secrets; Valkey/exporter read `mng_valkey_password`. Both engines use `infra_net` and publish host bindings through the root
`POSTGRES_HOST_PORT` and source-spelled `VALKEY_MNG_HOST_POST` key; exporters are internal.
PostgreSQL uses `pg_isready`, Valkey uses authenticated `PING`, exporters use HTTP
health checks, and init is completion-gated.
[`pg/init-scripts/init_users_dbs.sql`](pg/init-scripts/init_users_dbs.sql) owns
base role/database initialization and never reads optional-capability secrets.
[`pg/provision/run-feature-provision.sh`](pg/provision/run-feature-provision.sh)
is the shared input handler for feature-owned jobs (`mlflow-db-provision`,
`dbt-db-provision`, `debezium-db-provision`): it validates identifiers and secret
files before connecting and passes secrets through the psql environment
(`\getenv`), never argv. Each feature keeps its SQL and grants in its own package.
Engine configuration otherwise remains in Compose.

## How to Work in This Area

```bash
docker compose --env-file .env.example --profile mng config --quiet
docker compose --env-file .env.example --profile mng config --services
```

Run from the repository root. Do not use leaf-only Compose commands. PostgreSQL
recovery is pgBackRest (physical backup, WAL archive, point-in-time restore);
Valkey recovery uses an RDB export. Both run from the host backup job and
restore only into isolated targets first; get workflow-owner approval before
replaying queue state. The synthetic rehearsal is
`HYHOME_BACKUP_REHEARSAL=1 python3 -m unittest tests.validation.test_compose_baseline_gates.BackupRestoreRehearsalTests`.

## Related Documents

Use the [documentation entry point](../../../../docs/README.md) to locate Stage 05
subject `04-data/0028-management-database`, synthetic rehearsal RUN-0032 and the
backup subject `04-data/0021-backup-and-restore` (POL/GDE/RUN-0021). Official sources: [PostgreSQL backup](https://www.postgresql.org/docs/current/backup.html),
[upgrade](https://www.postgresql.org/docs/current/upgrading.html), and
[Valkey persistence](https://valkey.io/topics/persistence/), and the
[pgBackRest user guide](https://pgbackrest.org/user-guide.html).
