---
title: "Airflow (07-workflow)"
version: "1.2.1"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-22"
created: "2025-11-12"
---

# Airflow (07-workflow)

> Apache Airflow + CeleryExecutor + Native Keycloak Auth Manager.

## Overview

Airflow는 `hy-home.docker`의 code-first workflow orchestration engine이다.
Compose 파일 하나에서 core services와 optional dedicated Valkey를 구성한다.

UI/API authentication은 OAuth2 Proxy ForwardAuth가 아니라
`KeycloakAuthManager`를 통해 Keycloak에 직접 연결한다.

## Audience

- Data Engineers
- SREs
- AI Agents

## Scope

### In Scope

- apiserver
- scheduler
- dag-processor
- worker
- triggerer
- Flower
- StatsD
- DB/broker/auth wiring

### Out of Scope

- individual DAG business logic
- external source infra

## Structure

```text
airflow/
├── Dockerfile
├── docker-compose.yml
├── config/
└── README.md
```

## Current Implementation Notes

- base: [Dockerfile declaration](Dockerfile)
- image: [declared runtime image](../../tech-stack.versions.json)
- Python: 3.13
- provider: `apache-airflow-providers-keycloak`, pinned in [Dockerfile](Dockerfile)
- auth manager:
  `airflow.providers.keycloak.auth_manager.keycloak_auth_manager.KeycloakAuthManager`
- client: `home-airflow`
- realm: `hy-home.realm`
- client secret: Docker Secret
- Airflow internal JWT secret: Docker Secret
- API base URL: `https://airflow.${DEFAULT_URL}`
- local CA: certifi + mounted mkcert root
- API server: `--proxy-headers`
- trusted proxy: `172.19.0.2` (`infra_net`) and `10.250.1.2` (`edge_net`)
- Airflow route:
  `traefik.http.routers.airflow.middlewares: gateway-standard-chain@file`
- OAuth2 Proxy ForwardAuth: **not applied to Airflow**

### Token Boundary

Keycloak token:

- OIDC login
- Authorization Services

Airflow internal JWT:

- application session/API
- `airflow_api_jwt_secret`

두 token은 별개다.

## Service Readiness

| Field | Evidence |
| --- | --- |
| API | `airflow-apiserver` |
| Auth | Keycloak Auth Manager |
| DB | `mng-pg` |
| Broker | `mng-valkey` or `airflow-valkey` |
| Secret | DB/Fernet/JWT/Keycloak client |
| Health | `/api/v2/monitor/health` |

## Keycloak Bootstrap

Required realm roles:

```text
Viewer
User
Op
Admin
SuperAdmin
```

```bash
docker compose exec airflow-apiserver   airflow keycloak-auth-manager create-all     --username keycloak_admin     --user-realm master     --password
```

After provider 0.9.0 upgrade on an existing non-team setup: <!-- runtime-version-exception: migration — permission migration is required when crossing this provider boundary -->

```bash
docker compose exec airflow-apiserver   airflow keycloak-auth-manager create-permissions     --username keycloak_admin     --user-realm master     --password
```

## How to Work in This Area

1. Airflow guide/policy/runbook 확인.
2. DAG lifecycle guide 확인.
3. auth route는 gateway-only 유지.
4. secret 원문을 로그/문서에 기록하지 않는다.
5. provider upgrade 시 Keycloak permission migration 검토.
6. failure는 endpoint matrix로 authentication vs authorization을 구분.

## Tech Stack

| Category | Technology | Version |
| --- | --- | --- |
| Airflow | Apache Airflow | declared version |
| Keycloak Provider | apache-airflow-providers-keycloak | declared version |
| Executor | CeleryExecutor | distributed |
| Broker | Valkey | shared/dedicated |
| DB | PostgreSQL | management DB |

## Available Scripts

```bash
HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh 07-workflow
docker compose exec airflow-apiserver airflow db check
docker compose exec airflow-apiserver airflow dags list
```

## Troubleshooting

- config PermissionError -> shared volume owner/runtime UID
- DB migration -> same image `airflow db migrate`
- JWT alg/format -> ForwardAuth token collision 확인
- `invalid_scope` -> Keycloak Authorization bootstrap
- role 404 -> required realm roles
- callback 403 -> `_oauth_state`
- Pool/DAG/Asset only 403 -> resource authorization

### Convergence contract

- Airflow core/Flower/StatsD services are **HOME** on `workflow`/`workflow-airflow`; Airflow Valkey and its exporter are **OPTIONAL** on `dedicated-valkey`.
- Root preflight: `docker compose --profile workflow config --quiet`. Root start: `docker compose --profile workflow up -d airflow-apiserver airflow-scheduler airflow-dag-processor airflow-worker airflow-triggerer flower airflow-statsd-exporter`.
- `dedicated-valkey` only starts the pair; actual selection requires matching `AIRFLOW_VALKEY_HOST` and `AIRFLOW_VALKEY_SECRET`.
- Stable entry point: [docs/README.md](../../../docs/README.md). Exact Stage 05 path `docs/05.operations/catalog/07-workflow/0050-airflow/`; IDs `GDE-0050`, `POL-0050`, `RUN-0050`. Its isolated restore is planned and unexecuted.

## Related Documents

- **Architecture**: `docs/02.architecture/descriptions/0007-workflow-architecture.md`
- **Guide**: `docs/05.operations/catalog/07-workflow/0050-airflow/guide.md`
- **Policy**: `docs/05.operations/catalog/07-workflow/0050-airflow/policy.md`
- **Runbook**: `docs/05.operations/catalog/07-workflow/0050-airflow/runbook.md`
- **Auth Integration**: `docs/05.operations/catalog/02-auth/0079-application-auth-integration/guide.md`
- **Incident**: `docs/05.operations/incidents/2026/inc-0002-airflow-keycloak-native-auth/incident.md`

Runtime pins are owned by the Compose/Dockerfile declarations; the [derived Compose image projection](../../tech-stack.versions.json) provides drift verification.
