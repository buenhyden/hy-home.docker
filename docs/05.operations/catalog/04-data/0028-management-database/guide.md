---
title: "Management Database Usage Guide"
version: "1.0.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "GDE-0028"
parent_ids:
- "POL-0028"
implementation_services:
  infra/04-data/operational/mng-db/docker-compose.yml:
  - 'mng-pg'
  - 'mng-pg-exporter'
  - 'mng-pg-init'
  - 'mng-valkey'
  - 'mng-valkey-exporter'
created: "2026-05-10"
---

# Management Database Usage Guide

## Usage

The management database is a five-service HOME dependency for authentication,
workflow and tooling. `mng-pg` stores the `n8n`, `keycloak`, `airflow`,
`terrakube`, `sonarqube`, `postgres`, and configured application databases.
`mng-valkey` is the shared Airflow/n8n broker/cache. Grafana is not wired to
management PostgreSQL in current Compose; it owns `grafana-data` and uses its
current default database configuration.

### Current implementation

[`infra/04-data/operational/mng-db/docker-compose.yml`](../../../../../infra/04-data/operational/mng-db/docker-compose.yml)
defines `mng-pg`, `mng-pg-init`, `mng-pg-exporter`, `mng-valkey`, and
`mng-valkey-exporter`. Profiles `mng`, `core`, `dev`, and `local` select both
engines and init; exporters are selected by `mng` and `dev`.

PostgreSQL owns `mng-pg-data` at `${DEFAULT_MANAGEMENT_DIR}/pg` and uses the
`mng_db_password` secret. The base init job reads only the base
service-specific database password secrets and creates those roles/databases
idempotently. Optional capabilities provision their own objects in separate
feature jobs (`mlflow-db-provision`, `dbt-db-provision`,
`debezium-db-provision`) that share the input-validating
[runner](../../../../../infra/04-data/operational/mng-db/pg/provision/run-feature-provision.sh)
but keep their SQL and grants in their own packages. `mlops`, `data-science`,
`analytics-engineering` and `cdc` also select `mng-pg` and `mng-pg-init` for
dependency closure; the base job never reads their credentials, so `core`,
`mng`, `dev` and `local` start without them.

The declared command sets `wal_level=logical`, `max_replication_slots`,
`max_wal_senders` and `max_slot_wal_keep_size` for CDC. A running instance keeps
its previous settings until an approved recreate, which restarts every consumer
of the management database. Logical WAL adds a small amount of WAL volume; slots
are created only by a registered CDC connector. Valkey owns
`mng-valkey-data` at `${DEFAULT_MANAGEMENT_DIR}/valkey`, enables AOF, and reads
`mng_valkey_password`. Both use `mng_data_net`; PostgreSQL and Valkey host bindings
come from root environment keys. Health checks and resources come from shared
templates.

### Images, configuration and resource controls

The Compose file is authoritative for pinned upstream PostgreSQL, Valkey and the
two exporter image families; repository Renovate may propose updates and the
version projection is derived. PostgreSQL uses `POSTGRES_PASSWORD_FILE`,
`POSTGRES_USER`, `POSTGRES_DB`, `PGDATA`, `POSTGRES_HOSTNAME` and `POSTGRES_PORT`;
init adds `SERVICE_POSTGRES_USERNAME` and `SERVICE_POSTGRES_DB`. Root port keys
control host bindings. `mng-pg` extends `template-stateful-db-med`, `mng-valkey`
`template-stateful-low`, init `template-job-low`, and exporters
`template-infra-readonly-low`; engine/exporter health checks are declared. Current
consumers connect over `mng_data_net`; init creates roles/databases after PostgreSQL
health, while exporters observe the engines.

### Static preflight

```bash
docker compose --env-file .env.example --profile mng config --quiet
docker compose --env-file .env.example --profile mng config --services
```

Run from the repository root. Do not render or start the leaf file alone. Do not
rerun init, rotate credentials, query HOME databases or change broker queues
without an approved runtime task.

### Backup, recovery and upgrades

PostgreSQL requires a logical dump of global roles plus every database. Valkey
requires one complete AOF set/manifest and an RDB checkpoint; an incident owner
must decide whether stale queued work is safe to replay. [RUN-0028](runbook.md)
defines isolated restore order and application validation.

PostgreSQL major upgrades use logical dump/restore or another separately approved
upstream method. Minor image and Valkey changes still require release notes,
backup and rollback. Never attach a new major PostgreSQL image to the existing
`PGDATA` or copy live database files.

### Official references

- [PostgreSQL backup and restore](https://www.postgresql.org/docs/current/backup.html)
- [pg_restore](https://www.postgresql.org/docs/current/app-pgrestore.html)
- [PostgreSQL upgrading](https://www.postgresql.org/docs/current/upgrading.html)
- [PostgreSQL license](https://www.postgresql.org/about/licence/)
- [Valkey persistence](https://valkey.io/topics/persistence/)

## Common Checks

Confirm exact root profiles, services, health/resource controls, writable-state
ownership, secret references, exposure and the engine-specific recovery boundary.
A static pass is configuration evidence only; runtime and restore remain separate.

## Traceability

- Artifact: `GDE-0028`; governing policy: `POL-0028`.
- Runtime authority: `infra/04-data/operational/mng-db/docker-compose.yml`.

## Related Documents

- [Operations policy](policy.md)
- [Health and recovery runbook](runbook.md)
- [Backup policy](../0021-backup-and-restore/policy.md)
