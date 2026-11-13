---
title: "SonarQube Code Quality"
version: "1.1.2"
type: "common/readme"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
created: "2025-11-12"
---

<!-- [ID:11-quality:sonarqube] -->

# SonarQube Code Quality

> 지속적인 코드 품질 검사 및 보안 스캐닝 LAB입니다.

## Purpose

### Service Role

SonarQube는 정적 애플리케이션 보안 테스트(SAST)와 코드 품질 지표를 제공합니다.
독립 Compose project인 [SonarQube LAB](docker-compose.yml)(`sast` profile)이며 root
Compose에 포함되지 않고 HOME network에 연결되지 않으며 Traefik route도 없습니다. UI는
`${LAB_HOST_BIND_IP}:${LAB_SONARQUBE_HOST_PORT:-18094}`에만 게시됩니다. 데이터베이스는
`LAB_SONARQUBE_DB_HOST`가 가리키는 mng-pg이며 HOME `mng-pg-init`이 `sonarqube` role을
계속 프로비저닝합니다. HOME은 mng-pg를 LAB network에 게시하지 않으므로 owner가
endpoint를 승인하기 전(미결정)까지는 render 검증만 합니다.

#### Audience

이 README의 주요 독자:

- Developers (PR 분석)
- Security Engineers (취약점 스캔)
- Operators

#### In Scope

- SonarQube Community Edition 서비스.
- 승인된 외부 PostgreSQL endpoint와의 통합.
- ElasticSearch 기반 검색 인덱스 관리.

#### Out of Scope

- CI/CD 파이프라인 구현 (개별 프로젝트 저장소에서 관리).
- 관리 데이터베이스 수명주기 (HOME `04-data`에서 관리).
- Traefik route와 게이트웨이 SSO.
- SonarLint IDE 설정 (클라이언트 측).

#### Structure

```text
labs/sonarqube/
├── README.md          # 서비스 README
├── docker-compose.yml # 독립 LAB entrypoint
└── promotion.yaml     # SPEC-0263 승격 manifest
```

서비스 정의는 [labs/sonarqube/docker-compose.yml](docker-compose.yml)이 소유합니다.

### Supported Environment

| Category | Technology | Notes |
| :--- | :--- | :--- |
| **Service** | SonarQube Community Build | 런타임 이미지는 [Compose](docker-compose.yml)에만 선언됨 |
| **Database** | PostgreSQL | `LAB_SONARQUBE_DB_HOST`의 승인된 endpoint |
| **Network** | `lab_sonarqube_net` | HOME network·Traefik 없음 |
| **Storage** | Bind Mount | `${LAB_DATA_DIR}/sonarqube/{data,logs}` |

현재 Community Build 후보는 공식 공급자의 같은 연도 직접 업그레이드 경로,
PostgreSQL 지원 범위와 producer entrypoint를 대조해 소스로 준비합니다. JDBC
password를 secret에서 내보내는 wrapper·Java 옵션을 유지합니다. 새 후보의 DB
migration·plugin·OIDC·health 실행과 backup·복원은 아직 인수하지 않았습니다. 이미
DB/schema가 바뀐 경우에는 image tag 하향만으로 복구하지 않으며 소유자의 검증된
backup·복원 절차가 필요합니다.

## Interfaces

### Inputs and Outputs

UI는 `${LAB_HOST_BIND_IP:-127.0.0.1}:${LAB_SONARQUBE_HOST_PORT:-18094}` -> 9000에 게시하고 승인된 외부 PostgreSQL endpoint(`LAB_SONARQUBE_DB_HOST`)와 연동한다. 환경 변수는 아래 표와 같다.

#### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `LAB_SONARQUBE_DB_HOST` | Yes | 승인된 mng-pg endpoint host. 비어 있으면 render가 거부됩니다. |
| `LAB_SONARQUBE_DB_PORT` | No | DB 포트(기본값: 5432). |
| `LAB_SONARQUBE_DB_NAME` | No | 대상 데이터베이스 이름(기본값: sonarqube). |
| `LAB_SONARQUBE_DB_USER` | No | 데이터베이스 사용자명(기본값: sonarqube). |
| `LAB_SONARQUBE_HOST_PORT` | No | UI 호스트 포트(기본값: 18094). |
| `LAB_DATA_DIR` | Yes | 격리된 LAB data root. |

### Security Boundary

`lab_sonarqube_net`만 사용하며 HOME network와 Traefik route가 없다. secret은 `lab_sonarqube_db_password`(`/run/secrets/sonarqube_db_password`)만 참조하고 값은 문서에 쓰지 않는다.

## Development

### Local Workflow

아래 `LAB`은 저장소 루트에서
`docker compose --env-file labs/.env -f labs/sonarqube/docker-compose.yml --profile sast`입니다.
`config`는 render만 합니다. 컨테이너를 시작하는 명령은
`python3 scripts/operations/lab.py check|up|down sonarqube`의 lease 규칙
([LAB 안내](../README.md#local-workflow))을 따릅니다.

| Command | Description |
| :--- | :--- |
| `LAB config --services` | 선택된 LAB 서비스를 확인합니다(render-only). |
| `LAB logs --tail=200 sonarqube` | 활성 lease 안에서 실행 중인 SonarQube를 점검합니다. |

#### Usage

1. [labs/sonarqube/docker-compose.yml](docker-compose.yml)과 [LAB 안내](../README.md)를 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.

런타임 고정 값은 Compose 선언이 소유하고 [파생된 Compose 이미지 프로젝션](../../infra/tech-stack.versions.json)으로 드리프트를 검증합니다.

### Checks

- `docker compose --env-file labs/.env -f labs/sonarqube/docker-compose.yml --profile sast config --quiet`
- `python3 -m unittest tests.validation.test_lab_isolation`

## Operations

### Runbook Links

- **Guide**: SonarQube Guide (`docs/05.operations/guides/15-labs/0066-sonarqube.md`)
- **Policy**: SonarQube Operations (`docs/05.operations/policies/15-labs/0066-sonarqube.md`)
- **Runbook**: SonarQube Runbook (`docs/05.operations/runbooks/15-labs/0066-sonarqube.md`)
- [LAB 탐색](../README.md)
- [Documentation index](../../docs/README.md)

### Observability and Recovery

- render가 거부되면 `LAB_SONARQUBE_DB_HOST`, `LAB_DATA_DIR`, LAB secret 파일 경로를 먼저 확인합니다.
- 데이터베이스나 quality-gate 설정을 변경하기 전에 SonarQube 로그와 연결된 런북을 확인합니다.

#### Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | SonarQube LAB; 서비스: `sonarqube` |
| Config files | [labs/sonarqube/docker-compose.yml](docker-compose.yml) |
| Config values | env 키: `SONAR_JDBC_URL`, `SONAR_JDBC_USERNAME`, `SONAR_JDBC_PASSWORD`(entrypoint가 secret `sonarqube_db_password`에서 export; image는 `_FILE` 형식을 읽지 않음), `SONAR_WEB_JAVAOPTS`, `SONAR_SEARCH_JAVAOPTS`; 프로필: `sast` |
| Compose linkage | 독립 Compose project `hy-home-lab-sonarqube`; root include 없음 |
| Networks | `lab_sonarqube_net`(`hy-home-lab-sonarqube`); HOME network 없음 |
| Volumes | `sonarqube-data`(`${LAB_DATA_DIR}/sonarqube/data`) -> `/opt/sonarqube/data`, `sonarqube-logs`(`${LAB_DATA_DIR}/sonarqube/logs`) -> `/opt/sonarqube/logs` |
| Ports | `${LAB_HOST_BIND_IP:-127.0.0.1}:${LAB_SONARQUBE_HOST_PORT:-18094}:9000` |
| Labels | `hy-home.tier: lab`, `traefik.enable: 'false'` |
| Secret refs | `${LAB_SECRET_DIR}/sonarqube/db_password.txt`의 `lab_sonarqube_db_password`; 마운트: `/run/secrets/sonarqube_db_password` |
| Healthcheck | `/api/system/health` |
| Operations | Guide (`docs/05.operations/guides/15-labs/0066-sonarqube.md`), Policy (`docs/05.operations/policies/15-labs/0066-sonarqube.md`), Runbook (`docs/05.operations/runbooks/15-labs/0066-sonarqube.md`) |
| Validation | `config --quiet` render, `tests.validation.test_lab_isolation` |
| Troubleshooting | render로 시작한 뒤 활성 lease 안에서 서비스 로그와 연결된 운영/런북 근거를 확인합니다. |
