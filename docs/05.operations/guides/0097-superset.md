---
title: "Superset Usage Guide"
version: "1.0.3"
type: "operation/guide"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "GDE-0097"
parent_ids:
- "POL-0097"
implementation_services:
  infra/12-analytics/superset/docker-compose.yml:
  - superset-db-provision
  - superset-init
  - superset
created: "2026-09-23"
---

# Superset Usage Guide

## Usage

### Purpose and classification

Superset은 `bi`로 선택되는 OPTIONAL BI 웹 애플리케이션이다. Trino를
통해 레이크하우스 테이블을 탐색하고 차트로 만든다. Grafana는 운영
관측 도구로 남고, Superset은 데이터 분석용이다.

### Current implementation

- **Image.** [Superset Compose](../../../infra/12-analytics/superset/docker-compose.yml)는
  `apache/superset`에 PostgreSQL 드라이버, Authlib, `requirements.txt`에
  고정된 Trino 다이얼렉트를 더해 빌드한다.
- **Metadata.** `superset-db-provision`은 공유 기능 러너를 통해 `mng-pg`에
  `superset` 역할과 데이터베이스를 생성한다. `superset-init`은
  `superset db upgrade`, `superset init`을 실행하고 `lakehouse`
  데이터베이스를 `trino://superset@trino:8080/lakehouse`로 등록한다. 셋
  모두 멱등적이다.
- **Login.** Flask-AppBuilder를 통한 네이티브 Keycloak OIDC(클라이언트
  `home-superset`, PKCE S256)다. 처음 로그인하면 데이터를 보지 못하는
  `Gamma` 사용자가 생성되고 역할은 Admin이 부여한다. 다른 네이티브
  OIDC 서비스와 마찬가지로 라우트는 `gateway-standard-chain@file`만
  사용한다.
- **Secrets.** 서명 키, 데이터베이스 비밀번호, 클라이언트 시크릿은
  `superset_config.py`가 읽는 Docker secret 파일이다. 비밀번호가 든
  데이터베이스 URI는 메모리에서 조립하며 자격 증명은 하나도 환경 변수나
  명령줄에 두지 않는다. Keycloak을 호출할 수 있도록 로컬 루트 CA를 공개
  번들에 추가한다.
- **Runtime.** gunicorn을 사용하는 application/container 인스턴스 하나이며 worker/thread 설정이 OS 프로세스 하나를 보장하지 않는다. 1 CPU, 1 GiB, `SUPERSET_HOME`용
  tmpfs를 둔 읽기 전용 루트; 네트워크는 `edge_net`(Traefik, Keycloak
  별칭), `mng_data_net`(`mng-pg`), `object_net`(Trino)이다.

### Identity-specific behavior

Superset6.1.0 app/init 는동일 build/config 지만 app 은 upstreamgunicorn command,init 는 db upgrade/init/Trino URI 등록을실행한다. provision 은 PG18.6 runner 로별도 metadataDB/role 을만든다. sharedPG 의복원은다른 consumer 에도영향을준다. KeycloakOIDC/PKCES256/Gamma 등록은유지하고 Admin identity 매칭은별도검증한다. Secret signing key 는 encrypted metadata 연결복원에도필요하다. Trino URI 의 superset user 는무인증 SQL 의표시값이며 DB 권한경계가아니다. 직접 packagepin 은 transitivelock 이아니며/health 는 OIDC/SQLquery 증거가아니다.

| 정확한 식별자 | 목적·상태·기동 차이 | 준비 상태 판단의 한계 | 구현 소유자 |
| --- | --- | --- | --- |
| `superset-db-provision` | metadata role/database provisioning job | HTTP health 없음; 종료 코드와 변경된 대상의 실제 상태 확인 | [선택·의존·접속·입력·mount](../../../infra/12-analytics/superset/docker-compose.yml) |
| `superset-init` | migration/role init/Trino URI 등록 job | HTTP health 없음; 종료 코드와 변경된 대상의 실제 상태 확인 | [선택·의존·접속·입력·mount](../../../infra/12-analytics/superset/docker-compose.yml) |
| `superset` | OIDC BI app; metadata는 공유 PG | 선언된 역할별 health; 사용자 기능 별도 | [선택·의존·접속·입력·mount](../../../infra/12-analytics/superset/docker-compose.yml) |

선택 profile, version, port, 환경 입력, secret identifier와 mount의 정확한 값은 각 행의 구현이 소유한다. [공통 template](../../../infra/common-optimizations.yml)의 resource·security 상속과 서비스 override를 함께 읽는다. 값의2026-10-01 source snapshot과 official version/build 검토는 [W4 Task](../../03.specs/0198-operations-documentation-system/tasks/tsk-0004-data-messaging-analytics.md)에 보존했다. 반복OOM, disk/WAL/checkpoint 증가와 metrics 누락은 capacity 검토 trigger이며 health는 사용자 기능이나 복원을 증명하지 않는다.

### Commands and side effects

| Command | Effect |
| --- | --- |
| `docker compose --profile bi up -d superset` | 데이터베이스를 프로비저닝하고 마이그레이션한 다음 웹 서버 시작 |
| `docker compose --profile bi --profile lakehouse up -d superset trino` | 동일하되 레이크하우스 엔진도 쿼리에 쓸 수 있게 함 |
| `docker compose --profile bi run --rm superset-init` | 마이그레이션과 역할 동기화 재실행(업그레이드 후) |
| `docker compose --profile bi exec superset superset fab create-admin --username <keycloak username> …` | 해당 사용자의 첫 OIDC 로그인 전에 Admin 생성 |

## Common Checks

- `HYHOME_COMPOSE_PROFILES=bi bash scripts/validation/validate-docker-compose.sh`
- `HYHOME_PG_REHEARSAL=1 python3 -m unittest tests.validation.test_compose_baseline_gates.FeatureProvisioningRehearsalTests.test_6_superset_migrates_and_serves_on_its_own_database`

## Runbook Handoff

최초 설정, 로그인 실패, 업그레이드는 [runbook](../runbooks/0097-superset.md)을 따른다.

## Traceability

- [Policy](../policies/0097-superset.md) (`POL-0097`)
- [Runbook](../runbooks/0097-superset.md) (`RUN-0097`)
- [Application auth integration guide](0079-application-auth-integration.md)
- [Lakehouse guide](0094-lakehouse.md)

## Related Documents

- [Superset package README](../../../infra/12-analytics/superset/README.md)
- [Superset Compose source](../../../infra/12-analytics/superset/docker-compose.yml) and [derived version projection](../../../infra/tech-stack.versions.json)
- [Superset configuration](https://superset.apache.org/docs/configuration/configuring-superset)
