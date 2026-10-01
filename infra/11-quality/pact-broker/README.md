---
title: "Pact Broker"
version: "1.0.1"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
created: "2026-09-23"
---

<!-- [ID:11-quality:pact-broker] -->
# Pact Broker

> 온디맨드 **OPTIONAL** 계약 브로커이며 loopback 전용 포트에 basic auth를 사용하고 데이터는 기능 소유 `mng-pg` 데이터베이스에 저장합니다.

## Overview

Pact Broker는 consumer가 게시한 pact와 provider 검증 결과를 저장하는
**OPTIONAL** 계약 저장소입니다. `contract-testing` profile로만 선택되며
`pact-broker-db-provision`이 `mng-pg`에 전용 role·database를 만든 뒤 broker가
기동합니다. 컨테이너 자체는 디스크 상태가 없습니다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- AI Agents

## Scope

### In Scope

- Pact Broker 서버, 기능 전용 데이터베이스 프로비저닝, basic auth.
- pact 게시 및 검증 클라이언트를 위한 loopback 호스트 게시.

### Out of Scope

- Traefik route, TLS, SSO (구현되어 있지 않음; 호스트 게시는 loopback 전용이며 `mng_data_net` peer 접근은 별도).
- WireMock이 담당하는 HTTP 스터빙.
- consumer나 provider 테스트 실행.

## Structure

```text
pact-broker/
├── README.md             # This file
├── docker-compose.yml    # Provisioning job and broker
└── provisioning/
    └── mng-pg.sql        # Feature-owned role and database
```

## Tech Stack

| Category | Technology | Notes |
| :--- | :--- | :--- |
| **Service** | Pact Broker 2 (`pactfoundation/pact-broker` 3.x image) | 계약 저장소 |
| **Database** | `mng-pg` | `PACT_BROKER_DB_NAME`을 `PACT_BROKER_DB_USER`가 소유 |
| **Port** | `127.0.0.1:${PACT_BROKER_HOST_PORT:-19292}` → `9292` | Loopback 전용 호스트 게시 |
| **Auth** | Basic auth | `/diagnostic/status/heartbeat`만 공개됨 |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `PACT_BROKER_HOST_PORT` | No | Loopback 호스트 포트(기본값: 19292). |
| `PACT_BROKER_DB_USER` | No | 기능 전용 데이터베이스 역할(기본값: `pact_broker`). |
| `PACT_BROKER_DB_NAME` | No | 기능 전용 데이터베이스(기본값: `pact_broker`). |
| `PACT_BROKER_BASIC_AUTH_USERNAME` | No | UI와 API용 basic auth 사용자(기본값: `pact`). |

### Secrets

| Secret | Registry | Consumers |
| :--- | :--- | :--- |
| `pact_broker_db_password` | PG-026 | `pact-broker-db-provision`, `pact-broker` |
| `pact_broker_basic_auth_password` | AUTO-018 | `pact-broker`, 게시 및 검증 클라이언트 |

프로비저닝 작업은 `mng_postgres_password`도 읽습니다. 이미지는 환경 변수에서만
자격 증명을 읽으므로, 서비스 엔트리포인트가 Docker secrets에서 두 비밀번호를
broker 프로세스로 내보냅니다. Compose `environment`에는 어느 것도 선언되어
있지 않습니다.

## Available Scripts

저장소 루트에서 다음 읽기 전용 확인 명령을 실행합니다. 서비스를 시작하려면
런타임 승인이 필요합니다.

| Command | Description |
| :--- | :--- |
| `docker compose --profile contract-testing config --services` | 선택된 root-project 서비스를 확인합니다. |
| `docker compose --profile contract-testing logs --tail=100 pact-broker` | 승인된 실행 중인 서비스를 점검합니다. |

## Validation

- `HYHOME_COMPOSE_PROFILES=contract-testing bash scripts/validation/validate-docker-compose.sh`
- `python3 -m unittest tests.validation.test_compose_baseline_gates`
- `python3 scripts/validation/run-ci-gate.py --profile changed`

## Troubleshooting

- 프로비저닝 종료 코드 `64` 또는 `3`과 broker 종료 코드 `64`는 런북에 설명되어 있습니다.
- 401은 인증이 수락되지 않았다는 신호입니다. 자격 증명 누락·불일치와 전달 경로를 구분하고 비밀 값을 출력하지 않은 채 런북을 따릅니다.

## Related Documents

- **Guide**: Pact Broker Usage Guide (`docs/05.operations/guides/0093-pact-broker.md`)
- **Policy**: Pact Broker Operations Policy (`docs/05.operations/policies/0093-pact-broker.md`)
- **Runbook**: Pact Broker Recovery Runbook (`docs/05.operations/runbooks/0093-pact-broker.md`)
- [Documentation index](../../../docs/README.md)

---

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | `11-quality`의 Pact Broker 서비스 leaf; 서비스: `pact-broker-db-provision`, `pact-broker`; [root docker-compose.yml](../../../docker-compose.yml) -> `infra/11-quality/pact-broker/docker-compose.yml` 경로로 무조건 루트 include되며 프로필로 선택됨 |
| Config files | `docker-compose.yml`, `provisioning/mng-pg.sql` |
| Config values | 프로필: `contract-testing` |
| Compose linkage | [root docker-compose.yml](../../../docker-compose.yml) -> `infra/11-quality/pact-broker/docker-compose.yml` 경로로 무조건 루트 include되며 프로필로 선택됨 |
| Networks | `mng_data_net` |
| Volumes | 프로비저닝 러너와 SQL, 읽기 전용 |
| Ports | `127.0.0.1:${PACT_BROKER_HOST_PORT:-19292}:9292` |
| Labels | `hy-home.tier` |
| Secret refs | `pact_broker_db_password`, `pact_broker_basic_auth_password`, `mng_postgres_password` (프로비저닝) |
| Healthcheck | `pact-broker`에 Compose 헬스체크가 선언되어 있음 (`/diagnostic/status/heartbeat`) |
| Operations | Guide (`docs/05.operations/guides/0093-pact-broker.md`), Policy (`docs/05.operations/policies/0093-pact-broker.md`), Runbook (`docs/05.operations/runbooks/0093-pact-broker.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | heartbeat를 먼저 확인한 뒤 프로비저닝과 broker 로그, 연결된 런북 순서로 확인합니다. |

## How to Work in This Area

1. 상위 tier README와 `docker-compose.yml`을 먼저 확인한다.
2. 권한을 넓히는 SQL 변경은 policy의 거절 조건을 먼저 확인한다.
3. pact에는 합성 예시만 쓴다. 실제 payload·token·개인정보를 게시하지 않는다.

런타임 이미지와 프로필의 권위는 [docker-compose.yml](docker-compose.yml)에 있으며
[파생된 Compose 이미지 프로젝션](../../tech-stack.versions.json)은 드리프트 근거입니다.
