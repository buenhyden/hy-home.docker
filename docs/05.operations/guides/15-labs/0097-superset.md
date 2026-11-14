---
title: "Superset Usage Guide"
version: "1.2.3"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-11-14"
layer: "operations"
artifact_id: "GDE-0097"
parent_ids:
- "POL-0097"
implementation_services:
  labs/superset/docker-compose.yml:
  - superset-db-provision
  - superset-init
  - superset
created: "2026-09-23"
next_review_at: "2027-05-13"
---

# Superset Usage Guide

## Purpose

### Outcome

Superset은 root Compose에서 분리된 독립 LAB `labs/superset/docker-compose.yml`의 BI 웹 애플리케이션이며 LAB
profile `lab-superset`으로 선택된다(SPEC-0262). Trino를 통해 레이크하우스 테이블을 탐색하고 차트로 만드는
용도다. Grafana는 운영 관측 도구로 남고, Superset은 데이터 분석용이다. root `bi` profile은
이제 HOME mng-pg 기반만 선택하고 Superset을 선택하지 않는다.

Superset으로 레이크하우스 데이터를 탐색하는 분석가와 운영자를 위한 문서다. 접근 방식과 명령의 부작용을 이해하고 정상 사용·점검 방법을 찾는 것이 목표다.

### Boundaries

#### Traceability

- [Policy](../../policies/15-labs/0097-superset.md) (`POL-0097`)
- [Runbook](../../runbooks/15-labs/0097-superset.md) (`RUN-0097`)
- [Application auth integration guide](../03-identity-and-access/0079-application-auth-integration.md)
- [Lakehouse guide](0094-lakehouse.md)
- SPEC-0262 Analytics labs migration

#### Related Documents

- [Superset package README](../../../../labs/superset/README.md)
- [Superset Compose source](../../../../labs/superset/docker-compose.yml) and [derived version projection](../../../../infra/tech-stack.versions.json)
- [Superset configuration](https://superset.apache.org/docs/configuration/configuring-superset)

## Prerequisites

### Environment

#### Current implementation

- **Image.** [Superset Compose](../../../../labs/superset/docker-compose.yml)는
  `apache/superset`에 PostgreSQL 드라이버, Authlib, `requirements.txt`에
  고정된 Trino 다이얼렉트를 더해 빌드한다.
- **LAB boundary.** `hy-home-lab-superset` project의 `lab_superset_net` 하나만 사용하고 HOME
  network에 합류하지 않는다. 서비스는 `hy-home.tier: lab`, `traefik.enable: 'false'` label을
  가지며 gateway route가 없다. HOME 의존성은 [`labs/.env.example`](../../../../labs/.env.example)의
  필수 입력으로만 지정한다: `LAB_SUPERSET_DB_HOST`/`LAB_SUPERSET_DB_PORT`(HOME mng-pg),
  `LAB_SUPERSET_DEFAULT_URL`(Keycloak을 gateway 이름 `keycloak.<domain>`으로 찾는 domain),
  `LAB_SUPERSET_CA_FILE`(루트 CA 파일). HOME은 기본적으로 mng-pg를 LAB network에 게시하지
  않으므로 소유자가 도달 가능한 endpoint를 승인하기 전까지 이 LAB은 렌더링 전용이다
  (SPEC-0262 Task의 미결정 항목, 별도 승인).
- **Metadata.** `superset-db-provision`은 공유 기능 러너를 통해 설정된 mng-pg에
  `superset` 역할과 데이터베이스를 생성한다. `superset-init`은
  `superset db upgrade`, `superset init`을 실행하고 `lakehouse`
  데이터베이스를 `trino://superset@trino:8080/lakehouse`로 등록한다. 셋
  모두 멱등적이다. `trino`는 별도 lakehouse LAB network에 있으므로 이 등록은 `trino` host에
  도달할 수 있는 곳에서만 해석되며, 현재 선언으로는 Superset LAB에서 Trino 질의가 되지 않는다
  (미결정 항목).
- **Login.** Flask-AppBuilder를 통한 네이티브 Keycloak OIDC(클라이언트
  `home-superset`, PKCE S256)다. 처음 로그인하면 데이터를 보지 못하는
  `Gamma` 사용자가 생성되고 역할은 Admin이 부여한다. 등록된 redirect URI는 이전 gateway host
  `https://superset.${DEFAULT_URL}`을 가리키므로, LAB loopback origin에서 로그인하려면 소유자가
  승인한 redirect 등록이 따로 필요하다(미결정 항목). 그 전까지 LAB 로그인 성공을 주장하지 않는다.
- **Secrets.** 서명 키, 데이터베이스 비밀번호, 클라이언트 시크릿은
  `superset_config.py`가 `/run/secrets`에서 읽는 Docker secret 파일이다. secret은 LAB 전용이며
  이름은 `lab_superset_<purpose>`, 파일은 `${LAB_SECRET_DIR:-../../secrets/labs}/superset/` 아래이고
  원래 `/run/secrets/<name>` target에 mount된다. 값은 복사되지 않았으므로 운영자가 mng-pg 관리자·
  Superset DB 비밀번호, signing key, OIDC client secret의 LAB 사본을 별도 승인 아래 준비해야 한다
  (미결정 항목). OpenBao Agent 출력 bind(`/run/openbao/superset`)는 제거되었다. 비밀번호가 든
  데이터베이스 URI는 메모리에서 조립하며 자격 증명은 하나도 환경 변수나
  명령줄에 두지 않는다. Keycloak을 호출할 수 있도록 `LAB_SUPERSET_CA_FILE`의 루트 CA를 공개
  번들에 추가한다.
- **Runtime.** gunicorn을 사용하는 application/container 인스턴스 하나이며 worker/thread 설정이 OS 프로세스 하나를 보장하지 않는다. 1 CPU, 1 GiB, `SUPERSET_HOME`용
  tmpfs를 둔 읽기 전용 루트다. UI는 `${LAB_HOST_BIND_IP:-127.0.0.1}:${LAB_SUPERSET_HOST_PORT:-18092}`에만
  게시된다.

### Permissions

secret은 LAB 전용 `lab_superset_<purpose>`이며 mng-pg 관리자·Superset DB 비밀번호, signing key, OIDC client secret의 LAB 사본은 별도 승인 아래 준비한다. 렌더링 외 명령은 활성 lease와 승인된 mng-pg endpoint가 필요하다.

## Procedure

### Actions

#### Identity-specific behavior

`superset-init`과 `superset` app은 같은 build와 config를 쓰지만, app은 upstream gunicorn command를 실행하고 init은 db upgrade, init, Trino URI 등록을 실행한다. provision은 PostgreSQL runner로 별도 metadata DB와 role을 만든다. 공유 PostgreSQL을 복원하면 다른 consumer에도 영향이 간다. Keycloak OIDC, PKCE S256, Gamma 등록은 유지하고 Admin identity 매칭은 별도로 검증한다. Secret signing key는 encrypted metadata 연결을 복원할 때도 필요하다. Trino URI의 superset user는 인증 없는 SQL의 표시값이며 DB 권한 경계가 아니다. 직접 package pin은 transitive lock이 아니며 `/health`는 OIDC나 SQL query의 증거가 아니다. 실행 버전은 [Dockerfile](../../../../labs/superset/Dockerfile)이 소유한다.

| 정확한 식별자 | 목적·상태·기동 차이 | 준비 상태 판단의 한계 | 구현 소유자 |
| --- | --- | --- | --- |
| `superset-db-provision` | metadata role/database provisioning job | HTTP health 없음; 종료 코드와 변경된 대상의 실제 상태 확인 | [선택·의존·접속·입력·mount](../../../../labs/superset/docker-compose.yml) |
| `superset-init` | migration/role init/Trino URI 등록 job | HTTP health 없음; 종료 코드와 변경된 대상의 실제 상태 확인 | [선택·의존·접속·입력·mount](../../../../labs/superset/docker-compose.yml) |
| `superset` | OIDC BI app; metadata는 공유 PG | 선언된 역할별 health; 사용자 기능 별도 | [선택·의존·접속·입력·mount](../../../../labs/superset/docker-compose.yml) |

선택 profile, version, port, 환경 입력, secret identifier와 mount의 정확한 값은 각 행의 구현이 소유한다. [공통 template](../../../../infra/common-optimizations.yml)의 resource·security 상속과 서비스 override를 함께 읽는다. 값의 2026-10-01 source snapshot과 official version/build 검토는 W4 Task에 보존했다. 반복 OOM, disk/WAL/checkpoint 증가와 metrics 누락은 capacity 검토 trigger이며 health는 사용자 기능이나 복원을 증명하지 않는다.

#### Commands and side effects

표의 `LAB`은 `docker compose --env-file labs/.env -f labs/superset/docker-compose.yml --profile lab-superset`다. `LAB config`
렌더링만 승인 없이 안전하며, 그 외 명령은 `python3 scripts/operations/lab.py check|up|down superset`의
목적·lease·충돌·예산 규칙을 따르는 활성 lease 안에서, 승인된 mng-pg endpoint가 있을 때만 쓴다.

| Command | Effect |
| --- | --- |
| `LAB config --quiet` | 렌더링만; 필수 입력이 비어 있으면 거부 |
| `LAB up -d superset` | 데이터베이스를 프로비저닝하고 마이그레이션한 다음 웹 서버 시작 |
| `LAB run --rm superset-init` | 마이그레이션과 역할 동기화 재실행(업그레이드 후) |
| `LAB exec superset superset fab create-admin --username <keycloak username> …` | 해당 사용자의 첫 OIDC 로그인 전에 Admin 생성 |

### Exceptions

이 가이드는 Troubleshooting에 적은 내용 외의 예외를 따로 기록하지 않는다.

## Verification

### Expected Result

- `docker compose --env-file labs/.env -f labs/superset/docker-compose.yml --profile lab-superset config --quiet`
- `python3 -m unittest tests.validation.test_lab_isolation`
- `HYHOME_PG_REHEARSAL=1 python3 -m unittest tests.validation.test_compose_baseline_gates.FeatureProvisioningRehearsalTests.test_6_superset_migrates_and_serves_on_its_own_database`

### Troubleshooting

#### Runbook Handoff

최초 설정, 로그인 실패, 업그레이드는 [runbook](../../runbooks/15-labs/0097-superset.md)을 따른다.
