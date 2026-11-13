---
title: "Superset"
version: "1.1.1"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
created: "2026-09-23"
---

<!-- [ID:04-data:analytics-superset] -->

# Superset

> Keycloak native OIDC를 사용하는 on-demand BI 웹 애플리케이션 LAB입니다.

## Purpose

### Service Role

Superset은 독립 Compose project인 [Superset LAB](docker-compose.yml)(`lab-superset`
profile)입니다. root Compose에 포함되지 않고 HOME network에 연결되지 않으며 Traefik
route도 없습니다. UI는 `${LAB_HOST_BIND_IP}:${LAB_SUPERSET_HOST_PORT:-18092}`에만
게시됩니다. metadata는 `LAB_SUPERSET_DB_HOST`가 가리키는 mng-pg의 feature 소유
database에 두고, 로그인은 `LAB_SUPERSET_DEFAULT_URL`의 gateway 이름으로 찾는 Keycloak
native OIDC(client `home-superset`, PKCE)로만 합니다. 처음 로그인한 사용자는 데이터
접근이 없는 `Gamma`이며 Admin이 역할을 부여합니다.

HOME은 mng-pg를 LAB network에 게시하지 않고, 등록된 redirect URI는 이전 gateway host
기준이므로 LAB endpoint와 redirect 등록은 owner 승인 대상(미결정)입니다. 그 전까지는
render 검증만 하며 LAB 로그인 성공을 주장하지 않습니다. `superset-init`이 등록하는
lakehouse database(`trino://superset@trino:8080/lakehouse`)는 `trino` host에 도달할 수
있는 곳에서만 해석되므로, 현재 선언으로는 Superset LAB에서 Trino 질의가 되지 않습니다.

#### Audience

이 README의 주요 독자:

- Data analysts
- Operators

#### In Scope

- 웹 서버, metadata database 프로비저닝, init job.
- Keycloak OIDC 로그인과 `lakehouse` Trino database 등록.

#### Out of Scope

- Celery worker, alert/report, 썸네일, 공유 캐시.
- Group 기반 role 매핑. Superset은 native OIDC로 로그인하므로 OAuth2 Proxy
  `/admins` allowlist는 적용되지 않으며 owner는 Admin이 role을 부여하는
  Gamma 가입 방식을 유지했습니다(2026-09-24).

#### Structure

```text
labs/superset/
├── docker-compose.yml      # 독립 LAB entrypoint
├── promotion.yaml          # SPEC-0263 승격 manifest
├── README.md               # 이 파일
├── Dockerfile              # apache/superset와 requirements.txt
├── requirements.txt        # PostgreSQL driver, Authlib, Trino dialect(Renovate)
├── superset_config.py      # 파일 기반 secret, OIDC, proxy 설정
└── provisioning/
    └── mng-pg.sql          # feature 소유 role과 database
```

서비스 정의(`superset-db-provision`, `superset-init`, `superset`)는
[labs/superset/docker-compose.yml](docker-compose.yml)이 소유합니다.

### Supported Environment

| Category | Technology | Notes |
| :--- | :--- | :--- |
| **Application** | Apache Superset(`Dockerfile`의 base image) | gunicorn 프로세스 1개, 1 CPU, 1 GiB, read-only root |
| **Metadata** | `LAB_SUPERSET_DB_HOST`의 PostgreSQL | database와 role `superset` |
| **Login** | Flask-AppBuilder를 통한 Keycloak OIDC | PKCE S256; 등록 role `Gamma` |
| **Data** | Trino SQLAlchemy dialect | `lakehouse` catalog(별도 lakehouse LAB) |

## Interfaces

### Inputs and Outputs

UI는 `${LAB_HOST_BIND_IP:-127.0.0.1}:${LAB_SUPERSET_HOST_PORT:-18092}` -> 8088에 게시하고 Keycloak OIDC로 로그인하며 `lakehouse` Trino database를 등록한다. 환경 변수는 아래 표와 같다.

#### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `LAB_SUPERSET_DB_HOST` | Yes | 승인된 mng-pg endpoint host. 비어 있으면 render가 거부됩니다. |
| `LAB_SUPERSET_DEFAULT_URL` | Yes | Keycloak issuer를 찾는 HOME gateway 도메인. |
| `LAB_SUPERSET_CA_FILE` | Yes | Keycloak 호출용 HOME root CA 파일 경로. |
| `LAB_SUPERSET_DB_PORT` | No | Metadata DB 포트(기본값: 5432). |
| `LAB_SUPERSET_DB_USER` | No | Metadata role(기본값: superset). |
| `LAB_SUPERSET_DB_NAME` | No | Metadata database(기본값: superset). |
| `LAB_SUPERSET_OIDC_CLIENT_ID` | No | Keycloak client ID(기본값: home-superset). |
| `LAB_SUPERSET_HOST_PORT` | No | UI 호스트 포트(기본값: 18092). |

Secrets는 `${LAB_SECRET_DIR}/superset/`의 LAB 전용 파일이며 원래 이름으로 마운트됩니다:
`lab_superset_secret_key` -> `superset_secret_key`, `lab_superset_db_password` ->
`superset_db_password`, `lab_superset_oidc_client_secret` -> `superset_oidc_client_secret`,
provisioning 전용 `lab_superset_mng_postgres_password` -> `mng_postgres_password`.
`superset_config.py`가 읽습니다. HOME 값을 복사하려면 별도 승인이 필요합니다.

### Security Boundary

`lab_superset_net`만 사용하며 HOME network와 Traefik route가 없다. secret은 `lab_superset_secret_key`, `lab_superset_db_password`, `lab_superset_oidc_client_secret`, 프로비저닝 전용 `lab_superset_mng_postgres_password`이며 값은 문서에 쓰지 않는다.

## Development

### Local Workflow

아래 `LAB`은 저장소 루트에서
`docker compose --env-file labs/.env -f labs/superset/docker-compose.yml --profile lab-superset`입니다.
`config`는 render만 합니다. 컨테이너를 시작하는 명령은
`python3 scripts/operations/lab.py check|up|down superset`의 lease 규칙
([LAB 안내](../README.md#local-workflow))을 따르며, 최초 설정은 RUN-0097을 따릅니다.

| Command | Description |
| :--- | :--- |
| `LAB config --quiet` | render만; 필수 입력이 비어 있으면 거부. |
| `LAB up -d superset` | Provisioning, migration 후 시작. |
| `LAB run --rm superset-init` | 업그레이드 후 migration 재실행. |

#### Usage

1. Renovate가 `requirements.txt`와 `FROM` 이미지를 갱신합니다. Superset 버전이 오르면 `image:` tag와 버전 투영도 바뀌며 `superset-init`이 필요합니다.
2. 모든 credential은 `superset_config.py`가 읽는 secret 파일에 유지하십시오.
3. named user에게만 role을 부여하십시오. 등록은 계속 `Gamma`입니다.

런타임 이미지 권한은 [labs/superset/docker-compose.yml](docker-compose.yml)이 소유하며
[derived Compose 이미지 투영](../../infra/tech-stack.versions.json)은 drift 증거입니다.

### Checks

- `docker compose --env-file labs/.env -f labs/superset/docker-compose.yml --profile lab-superset config --quiet`
- `python3 -m unittest tests.validation.test_lab_isolation`
- `HYHOME_PG_REHEARSAL=1 python3 -m unittest tests.validation.test_compose_baseline_gates.FeatureProvisioningRehearsalTests.test_6_superset_migrates_and_serves_on_its_own_database`

## Operations

### Runbook Links

- **Guide**: Superset Usage Guide (`docs/05.operations/guides/15-labs/0097-superset.md`)
- **Policy**: Superset Operations Policy (`docs/05.operations/policies/15-labs/0097-superset.md`)
- **Runbook**: Superset Runbook (`docs/05.operations/runbooks/15-labs/0097-superset.md`)
- [LAB 탐색](../README.md)
- [문서 인덱스](../../docs/README.md)
- [RUN-0107 lab-promotion](../../docs/05.operations/runbooks/15-labs/0107-lab-promotion.md)

### Observability and Recovery

- `superset: secret … must be one non-empty line`: named secret 파일이 비어 있거나 여러 줄입니다.
- Keycloak 이후 로그인 오류: redirect URI 또는 client secret 불일치; RUN-0097을 따르십시오.
- 로그인 후 데이터가 없음: Admin이 role을 부여하기 전까지 사용자는 `Gamma`입니다.

#### Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Superset LAB; services: `superset-db-provision`, `superset-init`, `superset` |
| Config files | `Dockerfile`, `requirements.txt`, `superset_config.py`, `provisioning/mng-pg.sql` |
| Config values | profiles: `lab-superset` |
| Compose linkage | 독립 Compose project `hy-home-lab-superset`([labs/superset/docker-compose.yml](docker-compose.yml)); root include 없음 |
| Networks | `lab_superset_net`(`hy-home-lab-superset`); HOME network 없음 |
| Volumes | `./superset/superset_config.py:/app/pythonpath/superset_config.py:ro`, `${LAB_SUPERSET_CA_FILE}:/etc/ssl/certs/hy-home-rootCA.pem:ro` |
| Ports | `${LAB_HOST_BIND_IP:-127.0.0.1}:${LAB_SUPERSET_HOST_PORT:-18092}:8088`; Traefik route 없음 |
| Labels | `hy-home.tier: lab`, `traefik.enable: 'false'` |
| Secret refs | `lab_superset_secret_key`, `lab_superset_db_password`, `lab_superset_oidc_client_secret`, `lab_superset_mng_postgres_password`(provisioning 전용) |
| Healthcheck | `curl -fsS http://localhost:8088/health` |
| Operations | Guide (`docs/05.operations/guides/15-labs/0097-superset.md`), Policy (`docs/05.operations/policies/15-labs/0097-superset.md`), Runbook (`docs/05.operations/runbooks/15-labs/0097-superset.md`) |
| Validation | `config --quiet` render, `tests.validation.test_lab_isolation` |
| Troubleshooting | 활성 lease 안에서 `/health`와 init job 로그를 확인한 뒤 runbook을 따름 |
