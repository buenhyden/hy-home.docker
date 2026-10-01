---
title: "SonarQube Code Quality"
version: "1.0.3"
type: "common/package-readme"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-01"
created: "2025-11-12"
---

<!-- [ID:11-quality:sonarqube] -->
# SonarQube Code Quality

> 지속적인 코드 품질 검사 및 보안 스캐닝입니다.

## Overview

SonarQube는 정적 애플리케이션 보안 테스트(SAST)와 코드 품질 지표를 제공합니다. 플랫폼의 PostgreSQL 관리 데이터베이스와 통합해 데이터를 영속화하고 안전한 외부 접근에는 Traefik을 사용합니다.

## Audience

이 README의 주요 독자:

- Developers (PR 분석)
- Security Engineers (취약점 스캔)
- Operators
- AI Agents

## Scope

### In Scope

- SonarQube Community Edition 서비스.
- 외부 관리 PostgreSQL과의 통합.
- ElasticSearch 기반 검색 인덱스 관리.
- Traefik 라우팅 설정.

### Out of Scope

- CI/CD 파이프라인 구현 (개별 프로젝트 저장소에서 관리).
- 관리 데이터베이스 수명주기 (`04-data`에서 관리).
- SonarLint IDE 설정 (클라이언트 측).

## Structure

```text
sonarqube/
├── README.md           # This file
└── docker-compose.yml  # Service definition
```

## Tech Stack

| Category | Technology | Notes |
| :--- | :--- | :--- |
| **Service** | SonarQube Community Build | 런타임 이미지는 [Compose](docker-compose.yml)에만 선언됨 |
| **Database** | PostgreSQL | 관리용 클러스터 |
| **Network** | Traefik | SSL 종료 |
| **Storage** | Bind Mount | `${DEFAULT_TOOLING_DIR}/sonarqube` |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `SONARQUBE_PORT` | No | 리스닝 포트(기본값: 9000). |
| `SONARQUBE_DBNAME` | Yes | 대상 데이터베이스 이름. |
| `SONARQUBE_DB_USER` | Yes | 데이터베이스 사용자명. |

## Available Scripts

저장소 루트에서 다음 읽기 전용 확인 명령을 실행합니다. SonarQube를 시작하거나 변경하려면 런타임 승인이 필요합니다.

| Command | Description |
| :--- | :--- |
| `docker compose --profile sast config --services` | 선택된 root-project 서비스를 확인합니다. |
| `docker compose --profile sast logs --tail=200 sonarqube` | 승인된 실행 중인 SonarQube 서비스를 점검합니다. |

## Validation

- SonarQube에 영향을 주는 README나 Compose 참조를 변경한 후에는 `bash scripts/hardening/check-all-hardening.sh 11-quality`을 실행합니다.
- SonarQube 문서를 준비 완료로 표시하기 전에 `python3 scripts/validation/run-ci-gate.py --profile changed`를 실행합니다.

## Troubleshooting

- SonarQube DB, 네트워크, 시크릿 참조가 계속 선언되어 있는지 hardening 점검으로 먼저 확인합니다.
- 데이터베이스나 quality-gate 설정을 변경하기 전에 SonarQube 로그와 연결된 런북을 확인합니다.

## Related Documents

- **Guide**: SonarQube Guide (`docs/05.operations/guides/0066-sonarqube.md`)
- **Policy**: SonarQube Operations (`docs/05.operations/policies/0066-sonarqube.md`)
- **Runbook**: SonarQube Runbook (`docs/05.operations/runbooks/0066-sonarqube.md`)
- [Documentation index](../../../docs/README.md)

---

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | `11-quality`의 SonarQube Code Quality 서비스 leaf; 서비스: `sonarqube`; [root docker-compose.yml](../../../docker-compose.yml) -> `infra/11-quality/sonarqube/docker-compose.yml` 경로로 무조건 루트 include되며 프로필로 선택됨 |
| Config files | `docker-compose.yml` |
| Config values | env 키: `SONAR_JDBC_URL`, `SONAR_JDBC_USERNAME`, `SONAR_JDBC_PASSWORD_FILE`, `SONAR_WEB_JAVAOPTS`, `SONAR_SEARCH_JAVAOPTS`; 프로필: `tooling`, `sast` |
| Compose linkage | [root docker-compose.yml](../../../docker-compose.yml) -> `infra/11-quality/sonarqube/docker-compose.yml` 경로로 무조건 루트 include되며 프로필로 선택됨 |
| Networks | `edge_net`, `mng_data_net` |
| Volumes | `sonarqube-data-volume:/opt/sonarqube/data:rw`, `sonarqube-logs-volume:/opt/sonarqube/logs:rw`, `sonarqube-data-volume`, `sonarqube-logs-volume` |
| Ports | `${SONARQUBE_PORT:-9000}` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.sonarqube.rule`, `traefik.http.routers.sonarqube.entrypoints`, `traefik.http.routers.sonarqube.tls`, `traefik.http.routers.sonarqube.middlewares`, `traefik.http.services.sonarqube.loadbalancer.server.port` |
| Secret refs | 이름: `sonarqube_db_password`; 마운트: `/run/secrets/sonarqube_db_password` |
| Healthcheck | `sonarqube`에 Compose 헬스체크가 선언되어 있음 |
| Operations | Guide (`docs/05.operations/guides/0066-sonarqube.md`), Policy (`docs/05.operations/policies/0066-sonarqube.md`), Runbook (`docs/05.operations/runbooks/0066-sonarqube.md`) |
| Validation | [check-all-hardening.sh](../../../scripts/hardening/check-all-hardening.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | hardening 점검으로 시작한 뒤 승인된 런타임 컨텍스트에서 서비스 로그와 연결된 운영/런북 근거를 확인합니다. |

## How to Work in This Area

1. 상위 tier README와 해당 서비스의 `docker-compose*.yml` 또는 설정 파일을 먼저 확인한다.
2. 새 문서나 README를 만들 때는 `docs/99.templates/`의 대응 템플릿을 따른다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.
4. secret 값, token, 인증서 원문은 문서에 쓰지 않는다.

런타임 고정 값은 Compose/Dockerfile 선언이 소유하고 [파생된 Compose 이미지 프로젝션](../../tech-stack.versions.json)으로 드리프트를 검증합니다.
