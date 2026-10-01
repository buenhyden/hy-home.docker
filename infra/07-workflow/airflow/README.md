---
title: "Airflow (07-workflow)"
version: "1.2.4"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
created: "2025-11-12"
---

# Airflow (07-workflow)

> Apache Airflow + CeleryExecutor + 네이티브 Keycloak Auth Manager입니다.

## Overview

Airflow는 `hy-home.docker`의 code-first 워크플로우 오케스트레이션 엔진입니다.
Compose 파일 하나에서 핵심 서비스와 선택적인 전용 Valkey를 구성합니다.

UI/API 인증은 OAuth2 Proxy ForwardAuth가 아니라
`KeycloakAuthManager`를 통해 Keycloak에 직접 연결합니다.

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

- 개별 DAG 비즈니스 로직
- 외부 소스 인프라

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
- Python constraints 선택: [Dockerfile](Dockerfile)의 `PYTHON_VERSION`은 constraints URL을 선택하며 base image의 interpreter 버전을 바꾸지 않습니다. 실제 interpreter와 constraints의 일치는 별도 빌드 검증이 필요합니다.
- provider: `apache-airflow-providers-keycloak`, [Dockerfile](Dockerfile)에 고정됨
- auth manager:
  `airflow.providers.keycloak.auth_manager.keycloak_auth_manager.KeycloakAuthManager`
- client: `home-airflow`
- realm: `hy-home.realm`
- client secret: Docker Secret
- Airflow internal JWT secret: Docker Secret
- API base URL: `https://airflow.${DEFAULT_URL}`
- local CA: certifi + 마운트된 mkcert root
- API server: `--proxy-headers`
- trusted proxy: [docker-compose.yml](docker-compose.yml)의 `FORWARDED_ALLOW_IPS`에 선언됨 (`edge_net`)
- Airflow route:
  `traefik.http.routers.airflow.middlewares: gateway-standard-chain@file`
- OAuth2 Proxy ForwardAuth: **Airflow에는 적용되지 않음**

### Token Boundary

Keycloak token:

- OIDC login
- Authorization Services

Airflow internal JWT:

- application session/API
- `airflow_api_jwt_secret`

두 토큰은 별개입니다.

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

기존 non-team 구성에서 provider 0.9.0으로 업그레이드한 이후: <!-- runtime-version-exception: migration — permission migration is required when crossing this provider boundary -->

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
| Executor | CeleryExecutor | 분산 실행 |
| Broker | Valkey | 공유/전용 |
| DB | PostgreSQL | 관리용 DB |

## Available Scripts

```bash
HYHOME_COMPOSE_PROFILES='workflow dev' bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh 07-workflow
docker compose exec airflow-apiserver airflow db check
docker compose exec airflow-apiserver airflow dags list
```

## Troubleshooting

- config PermissionError -> 공유 볼륨 소유자/런타임 UID 확인
- DB migration -> 동일 이미지에서 `airflow db migrate` 실행
- JWT alg/format -> ForwardAuth 토큰 충돌 확인
- `invalid_scope` -> Keycloak Authorization bootstrap 확인
- role 404 -> 필수 realm role 확인
- callback 403 -> `_oauth_state` 확인
- Pool/DAG/Asset only 403 -> 리소스 authorization 확인

### Convergence contract

- Airflow core/Flower/StatsD 서비스는 `workflow`/`workflow-airflow`에서 **HOME**이며 Airflow Valkey와 그 exporter는 `dedicated-valkey`에서 **OPTIONAL**입니다.
- Root preflight: `docker compose --profile workflow config --quiet`. Root start: `docker compose --profile workflow up -d airflow-apiserver airflow-scheduler airflow-dag-processor airflow-worker airflow-triggerer flower airflow-statsd-exporter`.
- `dedicated-valkey`는 해당 쌍만 시작합니다. 실제로 선택하려면 `AIRFLOW_VALKEY_HOST`와 `AIRFLOW_VALKEY_SECRET`을 함께 일치시켜야 합니다.
- 안정적인 진입점: [docs/README.md](../../../docs/README.md). 정확한 Stage 05 경로: `docs/05.operations/guides/0050-airflow.md`; ID: `GDE-0050`, `POL-0050`, `RUN-0050`. 격리 복구는 계획되어 있으나 아직 실행되지 않았습니다.

## Related Documents

- **Architecture**: `docs/02.architecture/descriptions/0007-workflow-architecture.md`
- **Guide**: `docs/05.operations/guides/0050-airflow.md`
- **Policy**: `docs/05.operations/policies/0050-airflow.md`
- **Runbook**: `docs/05.operations/runbooks/0050-airflow.md`
- **Auth Integration**: `docs/05.operations/guides/0079-application-auth-integration.md`
- **Incident**: `docs/05.operations/incidents/2026/inc-0002-airflow-keycloak-native-auth/incident.md`

런타임 고정 값은 Compose/Dockerfile 선언이 소유하고 [파생된 Compose 이미지 프로젝션](../../tech-stack.versions.json)으로 드리프트를 검증합니다.
