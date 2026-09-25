---
title: "Pact Broker"
version: "1.0.0"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
created: "2026-09-23"
---

<!-- [ID:09-tooling:pact-broker] -->
# Pact Broker

> On-demand OPTIONAL contract broker; basic auth on a loopback-only port, data in a feature-owned `mng-pg` database.

## Overview

Pact Broker는 consumer가 게시한 pact와 provider 검증 결과를 저장하는
**OPTIONAL** 계약 저장소입니다. `contract-testing` profile로만 선택되며,
`pact-broker-db-provision`이 `mng-pg`에 전용 role·database를 만든 뒤 broker가
기동합니다. 컨테이너 자체는 디스크 상태가 없습니다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- AI Agents

## Scope

### In Scope

- Pact Broker server, its feature-owned database provisioning and basic auth.
- Loopback host publication for pact publishing and verification clients.

### Out of Scope

- Traefik route, TLS and single sign-on (not implemented; exposure is loopback-only).
- HTTP stubbing, which belongs to WireMock.
- Running consumer or provider tests.

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
| **Service** | Pact Broker 2 (`pactfoundation/pact-broker` 3.x image) | Contract store |
| **Database** | `mng-pg` | `PACT_BROKER_DB_NAME` owned by `PACT_BROKER_DB_USER` |
| **Port** | `127.0.0.1:${PACT_BROKER_HOST_PORT:-19292}` → `9292` | Loopback-only host publication |
| **Auth** | Basic auth | Only `/diagnostic/status/heartbeat` is public |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `PACT_BROKER_HOST_PORT` | No | Loopback host port (default: 19292). |
| `PACT_BROKER_DB_USER` | No | Feature-owned database role (default: `pact_broker`). |
| `PACT_BROKER_DB_NAME` | No | Feature-owned database (default: `pact_broker`). |
| `PACT_BROKER_BASIC_AUTH_USERNAME` | No | Basic auth user for the UI and API (default: `pact`). |

### Secrets

| Secret | Registry | Consumers |
| :--- | :--- | :--- |
| `pact_broker_db_password` | PG-026 | `pact-broker-db-provision`, `pact-broker` |
| `pact_broker_basic_auth_password` | AUTO-018 | `pact-broker`, publishing and verifying clients |

The provisioning job also reads `mng_postgres_password`. The image reads
credentials only from the environment, so the service entrypoint exports both
passwords from Docker secrets into the broker process; none is declared in
Compose `environment`.

## Available Scripts

Run these read-only checks from the repository root. Starting the service
requires runtime approval.

| Command | Description |
| :--- | :--- |
| `docker compose --profile contract-testing config --services` | Confirm the selected root-project services. |
| `docker compose --profile contract-testing logs --tail=100 pact-broker` | Inspect an approved running service. |

## Validation

- `HYHOME_COMPOSE_PROFILES=contract-testing bash scripts/validation/validate-docker-compose.sh`
- `python3 -m unittest tests.validation.test_compose_baseline_gates`
- `python3 scripts/validation/run-ci-gate.py --profile changed`

## Troubleshooting

- Provisioning exit `64` or `3` and broker exit `64` are explained in the runbook.
- A 401 means the client's username or password differs from the configured pair.

## Related Documents

- **Guide**: Pact Broker Usage Guide (`docs/05.operations/guides/0093-pact-broker.md`)
- **Policy**: Pact Broker Operations Policy (`docs/05.operations/policies/0093-pact-broker.md`)
- **Runbook**: Pact Broker Recovery Runbook (`docs/05.operations/runbooks/0093-pact-broker.md`)
- [Documentation index](../../../docs/README.md)

---

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Pact Broker service leaf in `09-tooling`; services: `pact-broker-db-provision`, `pact-broker`; unconditional root include, profile-selected, in [root docker-compose.yml](../../../docker-compose.yml) -> `infra/09-tooling/pact-broker/docker-compose.yml` |
| Config files | `docker-compose.yml`, `provisioning/mng-pg.sql` |
| Config values | profiles: `contract-testing` |
| Compose linkage | unconditional root include, profile-selected, in [root docker-compose.yml](../../../docker-compose.yml) -> `infra/09-tooling/pact-broker/docker-compose.yml` |
| Networks | `mng_data_net` |
| Volumes | provisioning runner and SQL, read-only |
| Ports | `127.0.0.1:${PACT_BROKER_HOST_PORT:-19292}:9292` |
| Labels | `hy-home.tier` |
| Secret refs | `pact_broker_db_password`, `pact_broker_basic_auth_password`, `mng_postgres_password` (provisioning) |
| Healthcheck | Compose healthcheck declared for `pact-broker` (`/diagnostic/status/heartbeat`) |
| Operations | Guide (`docs/05.operations/guides/0093-pact-broker.md`), Policy (`docs/05.operations/policies/0093-pact-broker.md`), Runbook (`docs/05.operations/runbooks/0093-pact-broker.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | Inspect the heartbeat, then provisioning and broker logs, then the linked runbook. |

## How to Work in This Area

1. 상위 tier README와 `docker-compose.yml`을 먼저 확인한다.
2. 권한을 넓히는 SQL 변경은 policy의 거절 조건을 먼저 확인한다.
3. pact에는 합성 예시만 쓴다. 실제 payload·token·개인정보를 게시하지 않는다.

Runtime image and profile authority is [docker-compose.yml](docker-compose.yml);
the [derived Compose image projection](../../tech-stack.versions.json) is drift evidence.
