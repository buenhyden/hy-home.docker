---
title: "Superset Usage Guide"
version: "1.0.0"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-23"
layer: "operations"
artifact_id: "GDE-0097"
parent_ids:
- "POL-0097"
implementation_services:
  infra/04-data/analytics/superset/docker-compose.yml:
  - superset-db-provision
  - superset-init
  - superset
created: "2026-09-23"
---

# Superset Usage Guide

## Usage

### Purpose and classification

Superset is the OPTIONAL BI web application, selected by `bi`. It explores
and charts lakehouse tables through Trino. Grafana stays the operational
observability tool; Superset is for data analysis.

### Current implementation

- **Image.** [Superset Compose](../../../../../infra/04-data/analytics/superset/docker-compose.yml)
  builds `apache/superset` plus the PostgreSQL driver, Authlib and the Trino
  dialect pinned in `requirements.txt`.
- **Metadata.** `superset-db-provision` creates the `superset` role and
  database on `mng-pg` through the shared feature runner. `superset-init` runs
  `superset db upgrade`, `superset init` and registers the `lakehouse` database
  as `trino://superset@trino:8080/lakehouse`. All three are idempotent.
- **Login.** Native Keycloak OIDC (client `home-superset`, PKCE S256) through
  Flask-AppBuilder. The first login creates a `Gamma` user, which sees no
  data; an Admin grants roles. The route uses `gateway-standard-chain@file`
  only, as for the other native OIDC services.
- **Secrets.** The signing key, the database password and the client secret
  are Docker secret files read by `superset_config.py`. The database URI with
  the password is built in memory; nothing puts a credential in the
  environment or on a command line. The local root CA is added to the public
  bundle for the Keycloak calls.
- **Runtime.** One gunicorn process, 1 CPU and 1 GiB, read-only root with
  tmpfs for `SUPERSET_HOME`; networks `edge_net` (Traefik, Keycloak alias),
  `mng_data_net` (`mng-pg`) and `object_net` (Trino).

### Commands and side effects

| Command | Effect |
| --- | --- |
| `docker compose --profile bi up -d superset` | Provisions the database, migrates, then starts the web server |
| `docker compose --profile bi --profile lakehouse up -d superset trino` | Same, with the lakehouse engine available for queries |
| `docker compose --profile bi run --rm superset-init` | Re-runs migration and role sync (after an upgrade) |
| `docker compose --profile bi exec superset superset fab create-admin --username <keycloak username> …` | Creates an Admin before that user's first OIDC login |

## Common Checks

- `HYHOME_COMPOSE_PROFILES=bi bash scripts/validation/validate-docker-compose.sh`
- `HYHOME_PG_REHEARSAL=1 python3 -m unittest tests.validation.test_compose_baseline_gates.FeatureProvisioningRehearsalTests.test_6_superset_migrates_and_serves_on_its_own_database`

## Runbook Handoff

Use the [runbook](runbook.md) for first setup, login failures and upgrades.

## Traceability

- [Policy](policy.md) (`POL-0097`)
- [Runbook](runbook.md) (`RUN-0097`)
- [Application auth integration guide](../../02-auth/0079-application-auth-integration/guide.md)
- [Lakehouse guide](../0094-lakehouse/guide.md)

## Related Documents

- [Superset package README](../../../../../infra/04-data/analytics/superset/README.md)
- [Superset Compose source](../../../../../infra/04-data/analytics/superset/docker-compose.yml) and [derived version projection](../../../../../infra/tech-stack.versions.json)
- [Superset configuration](https://superset.apache.org/docs/configuration/configuring-superset)
