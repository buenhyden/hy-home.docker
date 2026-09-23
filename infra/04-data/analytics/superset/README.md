---
title: "Superset"
version: "1.0.0"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-09-23"
created: "2026-09-23"
---

<!-- [ID:04-data:analytics-superset] -->
# Superset

> On-demand OPTIONAL BI web application with Keycloak native OIDC, querying the lakehouse through Trino.

## Overview

Superset은 `bi` profile로 선택되는 **OPTIONAL** BI 웹입니다. metadata는 `mng-pg`의
feature 소유 database에 두고, 로그인은 Keycloak native OIDC(client `home-superset`,
PKCE)로만 합니다. 처음 로그인한 사용자는 데이터 접근이 없는 `Gamma`이며 Admin이
역할을 부여합니다. `superset-init`이 lakehouse database(`trino://superset@trino:8080/lakehouse`)를
등록하므로, `lakehouse` profile을 함께 선택하면 Iceberg table을 조회할 수 있습니다.

## Audience

이 README의 주요 독자:

- Data analysts
- Operators
- AI Agents

## Scope

### In Scope

- Web server, metadata database provisioning and the init job.
- Keycloak OIDC login and the `lakehouse` Trino connection.

### Out of Scope

- Celery workers, alerts and reports, thumbnails and a shared cache.
- Group-based role mapping. Superset logs in through native OIDC, so the
  OAuth2 Proxy `/admins` allowlist does not apply; the owner kept Gamma sign-up
  with roles granted by an Admin (2026-09-24).

## Structure

```text
superset/
├── README.md               # This file
├── Dockerfile              # apache/superset plus requirements.txt
├── requirements.txt        # PostgreSQL driver, Authlib, Trino dialect (Renovate)
├── superset_config.py      # Secrets from files, OIDC, proxy settings
├── docker-compose.yml      # superset-db-provision, superset-init, superset
└── provisioning/
    └── mng-pg.sql          # Feature-owned role and database
```

## Tech Stack

| Category | Technology | Notes |
| :--- | :--- | :--- |
| **Application** | Apache Superset (base image in `Dockerfile`) | One gunicorn process, 1 CPU, 1 GiB, read-only root |
| **Metadata** | PostgreSQL on `mng-pg` | Database and role `superset` |
| **Login** | Keycloak OIDC through Flask-AppBuilder | PKCE S256; registration role `Gamma` |
| **Data** | Trino SQLAlchemy dialect | `lakehouse` catalog |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `SUPERSET_DB_USER` | No | Metadata role (default: superset). |
| `SUPERSET_DB_NAME` | No | Metadata database (default: superset). |
| `SUPERSET_OIDC_CLIENT_ID` | No | Keycloak client ID (default: home-superset). |
| `DEFAULT_URL` | Yes | Base domain of the route and the Keycloak issuer. |

Secrets: `superset_secret_key` (AUTO-020), `superset_db_password` (PG-028),
`superset_oidc_client_secret` (IAM-013), read by `superset_config.py`.

## Available Scripts

Starting the service requires runtime approval; first setup is in RUN-0097.

| Command | Description |
| :--- | :--- |
| `docker compose --profile bi up -d superset` | Provision, migrate, then start. |
| `docker compose --profile bi run --rm superset-init` | Re-run migration after an upgrade. |

## Validation

- `HYHOME_COMPOSE_PROFILES=bi bash scripts/validation/validate-docker-compose.sh`
- `HYHOME_PG_REHEARSAL=1 python3 -m unittest tests.validation.test_compose_baseline_gates.FeatureProvisioningRehearsalTests.test_6_superset_migrates_and_serves_on_its_own_database`

## Troubleshooting

- `superset: secret … must be one non-empty line`: the named secret file is empty or has several lines.
- Login error after Keycloak: redirect URI or client secret mismatch; follow RUN-0097.
- No data after login: the user is `Gamma` until an Admin grants a role.

## Related Documents

- **Guide**: Superset Usage Guide (`docs/05.operations/catalog/04-data/0097-superset/guide.md`)
- **Policy**: Superset Operations Policy (`docs/05.operations/catalog/04-data/0097-superset/policy.md`)
- **Runbook**: Superset Runbook (`docs/05.operations/catalog/04-data/0097-superset/runbook.md`)
- [Documentation index](../../../../docs/README.md)

---

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Superset leaf in `04-data/analytics`; services: `superset-db-provision`, `superset-init`, `superset`; unconditional root include, profile-selected, in [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/analytics/superset/docker-compose.yml` |
| Config files | `Dockerfile`, `requirements.txt`, `superset_config.py`, `docker-compose.yml`, `provisioning/mng-pg.sql` |
| Config values | profiles: `bi` |
| Compose linkage | unconditional root include, profile-selected, in [root docker-compose.yml](../../../../docker-compose.yml) -> `infra/04-data/analytics/superset/docker-compose.yml` |
| Networks | `edge_net`, `mng_data_net`, `object_net` |
| Volumes | `./superset_config.py:/app/pythonpath/superset_config.py:ro`, `${DEFAULT_CERT_DIR}/rootCA.pem:/etc/ssl/certs/hy-home-rootCA.pem:ro` |
| Ports | none; Traefik route `superset.${DEFAULT_URL}` |
| Labels | `hy-home.tier`, Traefik router `superset` |
| Secret refs | `superset_secret_key`, `superset_db_password`, `superset_oidc_client_secret`, `mng_postgres_password` (provisioning only) |
| Healthcheck | `curl -fsS http://localhost:8088/health` |
| Operations | Guide (`docs/05.operations/catalog/04-data/0097-superset/guide.md`), Policy (`docs/05.operations/catalog/04-data/0097-superset/policy.md`), Runbook (`docs/05.operations/catalog/04-data/0097-superset/runbook.md`) |
| Validation | [validate-docker-compose.sh](../../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | Check `/health` and the init job log, then follow the runbook. |

## How to Work in This Area

1. Renovate updates `requirements.txt` and the `FROM` image; a Superset bump also changes the `image:` tag and the version projection, then needs `superset-init`.
2. Keep every credential in a secret file read by `superset_config.py`.
3. Grant roles to named users only; registration stays `Gamma`.

Runtime image authority is [docker-compose.yml](docker-compose.yml);
the [derived Compose image projection](../../../tech-stack.versions.json) is drift evidence.
