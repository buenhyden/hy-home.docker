---
title: "Airflow (07-workflow)"
version: "1.2.0"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-18"
created: "2025-11-12"
---

# Airflow (07-workflow)

> Apache Airflow 3.3.1 + CeleryExecutor + Native Keycloak Auth Manager.

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

- base: `apache/airflow:3.3.1`
- image: `hy-home/airflow:3.3.1-keycloak`
- Python: 3.13
- provider: `apache-airflow-providers-keycloak==0.9.0`
- auth manager:
  `airflow.providers.keycloak.auth_manager.keycloak_auth_manager.KeycloakAuthManager`
- client: `home-airflow`
- realm: `hy-home.realm`
- client secret: Docker Secret
- Airflow internal JWT secret: Docker Secret
- API base URL: `https://airflow.${DEFAULT_URL}`
- local CA: certifi + mounted mkcert root
- API server: `--proxy-headers`
- trusted proxy: `172.19.0.2`
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

After provider 0.9.0 upgrade on an existing non-team setup:

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
| Airflow | Apache Airflow | 3.3.1 |
| Keycloak Provider | apache-airflow-providers-keycloak | 0.9.0 |
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

## Related Documents

- **Architecture**: `docs/02.architecture/descriptions/0007-workflow-architecture.md`
- **Guide**: `docs/05.operations/catalog/07-workflow/0050-airflow/guide.md`
- **Policy**: `docs/05.operations/catalog/07-workflow/0050-airflow/policy.md`
- **Runbook**: `docs/05.operations/catalog/07-workflow/0050-airflow/runbook.md`
- **Auth Integration**: `docs/05.operations/catalog/02-auth/0079-application-auth-integration/guide.md`
- **Incident**: `docs/05.operations/incidents/2026/inc-0002-airflow-keycloak-native-auth/incident.md`
