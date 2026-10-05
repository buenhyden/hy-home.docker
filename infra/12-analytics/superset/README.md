---
title: "Superset"
version: "1.0.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-05"
created: "2026-09-23"
---

<!-- [ID:04-data:analytics-superset] -->
# Superset

> on-demand OPTIONAL BI 웹 애플리케이션으로, Keycloak native OIDC를 사용하고 Trino를 통해 lakehouse를 조회합니다.

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

- 웹 서버, metadata database 프로비저닝, init job.
- Keycloak OIDC 로그인과 `lakehouse` Trino 연결.

### Out of Scope

- Celery worker, alert/report, 썸네일, 공유 캐시.
- Group 기반 role 매핑. Superset은 native OIDC로 로그인하므로 OAuth2 Proxy
  `/admins` allowlist는 적용되지 않으며 owner는 Admin이 role을 부여하는
  Gamma 가입 방식을 유지했습니다(2026-09-24).

## Structure

```text
superset/
├── README.md               # 이 파일
├── Dockerfile              # apache/superset와 requirements.txt
├── requirements.txt        # PostgreSQL driver, Authlib, Trino dialect(Renovate)
├── superset_config.py      # 파일 기반 secret, OIDC, proxy 설정
├── docker-compose.yml      # superset-db-provision, superset-init, superset
└── provisioning/
    └── mng-pg.sql          # feature 소유 role과 database
```

## Tech Stack

| Category | Technology | Notes |
| :--- | :--- | :--- |
| **Application** | Apache Superset(`Dockerfile`의 base image) | gunicorn 프로세스 1개, 1 CPU, 1 GiB, read-only root |
| **Metadata** | `mng-pg` 위의 PostgreSQL | database와 role `superset` |
| **Login** | Flask-AppBuilder를 통한 Keycloak OIDC | PKCE S256; 등록 role `Gamma` |
| **Data** | Trino SQLAlchemy dialect | `lakehouse` catalog |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `SUPERSET_DB_USER` | No | Metadata role(기본값: superset). |
| `SUPERSET_DB_NAME` | No | Metadata database(기본값: superset). |
| `SUPERSET_OIDC_CLIENT_ID` | No | Keycloak client ID(기본값: home-superset). |
| `DEFAULT_URL` | Yes | 라우트와 Keycloak issuer의 base 도메인. |

Secrets: `superset_secret_key` (AUTO-020), `superset_db_password` (PG-028),
`superset_oidc_client_secret` (IAM-013), `superset_config.py`가 읽음.

## Available Scripts

서비스 시작에는 runtime 승인이 필요합니다. 최초 설정은 RUN-0097을 따릅니다.

| Command | Description |
| :--- | :--- |
| `docker compose --profile bi up -d superset` | Provisioning, migration 후 시작. |
| `docker compose --profile bi run --rm superset-init` | 업그레이드 후 migration 재실행. |

## Validation

- `HYHOME_COMPOSE_PROFILES=bi bash scripts/validation/validate-docker-compose.sh`
- `HYHOME_PG_REHEARSAL=1 python3 -m unittest tests.validation.test_compose_baseline_gates.FeatureProvisioningRehearsalTests.test_6_superset_migrates_and_serves_on_its_own_database`

## Troubleshooting

- `superset: secret … must be one non-empty line`: named secret 파일이 비어 있거나 여러 줄입니다.
- Keycloak 이후 로그인 오류: redirect URI 또는 client secret 불일치; RUN-0097을 따르십시오.
- 로그인 후 데이터가 없음: Admin이 role을 부여하기 전까지 사용자는 `Gamma`입니다.

## Related Documents

- **Guide**: Superset Usage Guide (`docs/05.operations/guides/0097-superset.md`)
- **Policy**: Superset Operations Policy (`docs/05.operations/policies/0097-superset.md`)
- **Runbook**: Superset Runbook (`docs/05.operations/runbooks/0097-superset.md`)
- [문서 인덱스](../../../docs/README.md)

---

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | `12-analytics`의 Superset leaf; services: `superset-db-provision`, `superset-init`, `superset`; [root docker-compose.yml](../../../docker-compose.yml)에서 무조건 root include, profile로 선택됨 -> `infra/12-analytics/superset/docker-compose.yml` |
| Config files | `Dockerfile`, `requirements.txt`, `superset_config.py`, `docker-compose.yml`, `provisioning/mng-pg.sql` |
| Config values | profiles: `bi` |
| Compose linkage | [root docker-compose.yml](../../../docker-compose.yml)에서 무조건 root include, profile로 선택됨 -> `infra/12-analytics/superset/docker-compose.yml` |
| Networks | `edge_net`, `mng_data_net`, `object_net` |
| Volumes | `./superset_config.py:/app/pythonpath/superset_config.py:ro`, `${DEFAULT_CERT_DIR}/rootCA.pem:/etc/ssl/certs/hy-home-rootCA.pem:ro` |
| Ports | 없음; Traefik route `superset.${DEFAULT_URL}` |
| Labels | `hy-home.tier`, Traefik router `superset` |
| Secret refs | `superset_secret_key`, `superset_db_password`, `superset_oidc_client_secret`, `mng_postgres_password`(provisioning 전용) |
| Healthcheck | `curl -fsS http://localhost:8088/health` |
| Operations | Guide (`docs/05.operations/guides/0097-superset.md`), Policy (`docs/05.operations/policies/0097-superset.md`), Runbook (`docs/05.operations/runbooks/0097-superset.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | `/health`와 init job 로그를 확인한 뒤 runbook을 따름 |

## Usage

1. Renovate가 `requirements.txt`와 `FROM` 이미지를 갱신합니다. Superset 버전이 오르면 `image:` tag와 버전 투영도 바뀌며 `superset-init`이 필요합니다.
2. 모든 credential은 `superset_config.py`가 읽는 secret 파일에 유지하십시오.
3. named user에게만 role을 부여하십시오. 등록은 계속 `Gamma`입니다.

런타임 이미지 권한은 [docker-compose.yml](docker-compose.yml)이 소유하며
[derived Compose 이미지 투영](../../tech-stack.versions.json)은 drift 증거입니다.
