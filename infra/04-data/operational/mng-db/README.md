---
title: "Management Database (mng-db)"
version: "1.0.0"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-19"
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

## Structure

`mng-pg-data` maps to `${DEFAULT_MANAGEMENT_DIR}/pg`. The init job creates current
roles/databases for n8n, Keycloak, Airflow, Terrakube, SonarQube and the configured
application database. `mng-valkey-data` maps to
`${DEFAULT_MANAGEMENT_DIR}/valkey`, with AOF enabled for workflow broker/cache
state. Grafana is not wired to management PostgreSQL in current Compose.

PostgreSQL reads `mng_db_password`; init reads the service database password
secrets; Valkey/exporter read `mng_valkey_password`. Both engines use `infra_net` and publish host bindings through the root
`POSTGRES_HOST_PORT` and source-spelled `VALKEY_MNG_HOST_POST` key; exporters are internal.
PostgreSQL uses `pg_isready`, Valkey uses authenticated `PING`, exporters use HTTP
health checks, and init is completion-gated.
[`pg/init-scripts/init_users_dbs.sql`](pg/init-scripts/init_users_dbs.sql) owns
role/database initialization; engine configuration otherwise remains in Compose.

## How to Work in This Area

```bash
docker compose --env-file .env.example --profile mng config --quiet
docker compose --env-file .env.example --profile mng config --services
```

Run from the repository root. Do not use leaf-only Compose commands. PostgreSQL
backup requires globals plus every logical database; Valkey backup requires a
complete AOF set/manifest plus RDB checkpoint. Restore to isolated compatible
targets and get workflow-owner approval before replaying queue state.

## Related Documents

Use the [documentation entry point](../../../../docs/README.md) to locate Stage 05
subject `04-data/0028-management-database`, synthetic rehearsal RUN-0032 and HOME
backup policy POL-0021. Official sources: [PostgreSQL backup](https://www.postgresql.org/docs/current/backup.html),
[upgrade](https://www.postgresql.org/docs/current/upgrading.html), and
[Valkey persistence](https://valkey.io/topics/persistence/).
