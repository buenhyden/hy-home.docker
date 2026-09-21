---
title: "Tooling dbt Transformation Job"
version: "1.0.0"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-21"
created: "2026-09-21"
---

# Tooling dbt Transformation Job

> Command-line dbt Core with the PostgreSQL adapter, transforming the application database into a dedicated schema.

## Overview

dbt runs as a one-shot job, not a web service, so it has no route, no OIDC
client and no long-running container. It connects to `mng-pg` as its own `dbt`
role, reads the application source schema and writes only the target schema
(`analytics` by default). Lifecycle: **OPTIONAL**, selected only by
`analytics-engineering`; it is not part of HOME.

## Audience

- **Analytics engineers** writing and running models.
- **Operators** provisioning the role and reviewing side effects of `run`/`build`.
- **AI agents** changing this package under the owning Guide, Policy and Runbook.

## Scope

- **Included**: dbt image, profile, project skeleton, feature-owned role/grant provisioning.
- **Excluded**: application schema ownership, scheduling (Airflow owns orchestration), BI serving.

## Structure

```text
.
├── Dockerfile                  # python slim + pinned dbt-core and dbt-postgres
├── docker-entrypoint.sh        # Reads dbt_db_password into DBT_PASSWORD, then runs dbt
├── docker-compose.yml          # dbt job and dbt-db-provision
├── profiles/profiles.yml       # hyhome profile; every connection value comes from env
├── projects/
│   ├── dbt_project.yml         # target/log/packages paths on the job's /tmp tmpfs
│   └── models/platform/        # hyhome_dbt_connectivity smoke model and test
├── provisioning/mng-pg.sql     # Role, source read grants, target schema (feature-owned)
└── README.md
```

## Tech Stack

| Component | Source | Purpose |
| --- | --- | --- |
| `dbt` | [Dockerfile](Dockerfile) (dbt-core, dbt-postgres) | Transformation CLI |
| `dbt-db-provision` | [Compose](docker-compose.yml), PostgreSQL client image | Runs [mng-pg.sql](provisioning/mng-pg.sql) through the shared [provisioning runner](../../04-data/operational/mng-db/pg/provision/run-feature-provision.sh) |

Runtime pins are owned by the Compose/Dockerfile declarations; the
[derived Compose image projection](../../tech-stack.versions.json) provides drift verification.

## Configuration

| Field | Value |
| --- | --- |
| Profile | `analytics-engineering` (also selects `mng-pg`, `mng-pg-init`) |
| Default command | `debug` — validates profile and connection; writes only to `/tmp` |
| Side effects | `compile` renders SQL (no database writes); `run`/`build` create or replace views/tables in `DBT_SCHEMA`; `--full-refresh` rebuilds incremental models; `test` runs read queries |
| Environment keys | `DBT_DB_USER`, `DBT_DB_NAME` (defaults to `SERVICE_POSTGRES_DB`), `DBT_SCHEMA`, `DBT_SOURCE_SCHEMA`, `DBT_THREADS`, `POSTGRES_PORT`; the source owner for default privileges is `SERVICE_POSTGRES_USERNAME` |
| Secret | `dbt_db_password` (PG-023); provisioning also reads `mng_postgres_password` |
| Grants | `CONNECT` on the database, `USAGE` and `SELECT` on the source schema (plus default privileges for tables the application owner creates later), ownership of the target schema; no `CREATE` on the database |
| Writable paths | `/tmp/dbt/{target,logs,packages}` on tmpfs; project and profiles are read-only mounts |
| Network | `infra_net`; no port |

## Validation

- `HYHOME_COMPOSE_PROFILES=analytics-engineering bash scripts/validation/validate-docker-compose.sh`
- `python3 -m unittest tests.validation.test_compose_baseline_gates`
- `HYHOME_PG_REHEARSAL=1 python3 -m unittest tests.validation.test_compose_baseline_gates.FeatureProvisioningRehearsalTests`

`dbt --version` or a successful `debug` is not evidence that any model ran.

## How to Work in This Area

1. Provision `secrets/db/postgres/dbt_password.txt` through the registered secret workflow.
2. Run `docker compose --profile core --profile analytics-engineering run --rm dbt debug` in an
   approved environment, then `... run --rm dbt compile`.
3. Only after reviewing the target schema, run `... run --rm dbt build --select <models>`.
4. Declare business sources in `projects/models/` with their own `sources.yml`; keep grants in
   `provisioning/mng-pg.sql`.

## Related Documents

- **Guide**: dbt usage guide (`docs/05.operations/catalog/09-tooling/0090-dbt/guide.md`)
- **Policy**: dbt operations policy (`docs/05.operations/catalog/09-tooling/0090-dbt/policy.md`)
- **Runbook**: dbt recovery runbook (`docs/05.operations/catalog/09-tooling/0090-dbt/runbook.md`)
- [Documentation index](../../../docs/README.md)
