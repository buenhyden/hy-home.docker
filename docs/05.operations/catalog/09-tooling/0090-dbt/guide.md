---
title: "dbt Usage Guide"
version: "1.0.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-21"
layer: "operations"
artifact_id: "GDE-0090"
parent_ids:
- "POL-0090"
implementation_services:
  infra/09-tooling/dbt/docker-compose.yml:
  - dbt
  - dbt-db-provision
created: "2026-09-21"
---

# dbt Usage Guide

## Usage

### Purpose and classification

dbt is an OPTIONAL command-line transformation job selected by
`analytics-engineering`. It has no web UI, so no route or OIDC client exists or
is needed.

### Current implementation

- [dbt Compose](../../../../../infra/09-tooling/dbt/docker-compose.yml) defines
  `dbt-db-provision`, which runs the feature SQL, and the `dbt` job.
- The role `DBT_DB_USER` connects to `DBT_DB_NAME` (defaults to
  `SERVICE_POSTGRES_DB`). It can read `DBT_SOURCE_SCHEMA`, including tables the
  application owner creates later, and owns `DBT_SCHEMA`. It cannot create
  schemas or write the source schema.
- Project and profiles are read-only mounts. `target/`, `logs/` and `packages/`
  live on the job's `/tmp` tmpfs and disappear with the container.
- The project ships only `hyhome_dbt_connectivity`, a smoke view proving the
  connection and target-schema write access. Business models are not defined yet.

### Commands and side effects

| Command | Database effect | Proves |
| --- | --- | --- |
| `dbt --version` | None | The image starts; nothing about the database |
| `dbt debug` (default) | Opens a connection | Profile and credentials work |
| `dbt compile` | Read-only introspection | SQL renders against the catalog |
| `dbt run` / `dbt build` | Creates or replaces relations in `DBT_SCHEMA`; `build` also runs tests | Selected models materialize |
| `dbt run --full-refresh` | Drops and rebuilds incremental models | Rebuild; can be long and loses incremental state |
| `dbt test` | Read queries | Data tests pass |

Run commands with `docker compose --profile core --profile analytics-engineering run --rm dbt <command>`.
`dbt test --store-failures` would need `CREATE` on the database for audit
schemas, which is intentionally not granted.

## Common Checks

- `HYHOME_COMPOSE_PROFILES=analytics-engineering bash scripts/validation/validate-docker-compose.sh`
- `python3 -m unittest tests.validation.test_compose_baseline_gates`

## Runbook Handoff

Use the [runbook](runbook.md) for provisioning failure, permission errors and
target-schema recovery.

## Traceability

- [Policy](policy.md) (`POL-0090`)
- [Runbook](runbook.md) (`RUN-0090`)
- [Tooling architecture](../../../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [dbt command reference](https://docs.getdbt.com/reference/dbt-commands)
- [dbt Postgres setup](https://docs.getdbt.com/docs/core/connect-data-platform/postgres-setup)
