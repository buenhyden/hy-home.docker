---
title: "WireMock"
version: "1.0.0"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-23"
created: "2026-09-23"
---

<!-- [ID:09-tooling:wiremock] -->
# WireMock

> On-demand OPTIONAL HTTP stub server; the host endpoint and its unauthenticated admin API are loopback-only.

## Overview

WireMock은 개발·테스트 중 외부 HTTP 의존성을 대신하는 **OPTIONAL** stub
서버입니다. `api-mock` profile로만 선택되며, tracked `mappings/`의 stub만 영속
권한을 가집니다. 영속 데이터·web UI·OIDC client가 없습니다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- AI Agents

## Scope

### In Scope

- WireMock standalone server with read-only tracked mappings.
- Loopback host publication and project-default-network access.

### Out of Scope

- Authentication on the admin API (not implemented; exposure is loopback-only).
- Record-and-playback against real upstreams.
- Consumer contract verification, which belongs to the Pact Broker.

## Structure

```text
wiremock/
├── README.md          # This file
├── docker-compose.yml # Service definition
└── mappings/          # Tracked stub mappings (read-only mount)
```

## Tech Stack

| Category | Technology | Notes |
| :--- | :--- | :--- |
| **Service** | WireMock 3 (Alpine image) | HTTP stub server |
| **Port** | `127.0.0.1:${WIREMOCK_HOST_PORT:-18088}` → `8080` | Loopback-only host publication |
| **Storage** | None | Mappings are a read-only bind of this directory |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `WIREMOCK_HOST_PORT` | No | Loopback host port (default: 18088); the container always listens on 8080. |

## Available Scripts

Run these read-only checks from the repository root. Starting the service
requires runtime approval.

| Command | Description |
| :--- | :--- |
| `docker compose --profile api-mock config --services` | Confirm the selected root-project services. |
| `docker compose --profile api-mock logs --tail=100 wiremock` | Inspect an approved running service. |

## Validation

- `HYHOME_COMPOSE_PROFILES=api-mock bash scripts/validation/validate-docker-compose.sh`
- `python3 scripts/validation/run-ci-gate.py --profile changed`

## Troubleshooting

- A 404 for an expected stub: list `__admin/requests/unmatched` and follow the runbook.
- A mapping that does not load is named in the container log at start.

## Related Documents

- **Guide**: WireMock Usage Guide (`docs/05.operations/catalog/09-tooling/0092-wiremock/guide.md`)
- **Policy**: WireMock Operations Policy (`docs/05.operations/catalog/09-tooling/0092-wiremock/policy.md`)
- **Runbook**: WireMock Recovery Runbook (`docs/05.operations/catalog/09-tooling/0092-wiremock/runbook.md`)
- [Documentation index](../../../docs/README.md)

---

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | WireMock service leaf in `09-tooling`; services: `wiremock`; unconditional root include, profile-selected, in [root docker-compose.yml](../../../docker-compose.yml) -> `infra/09-tooling/wiremock/docker-compose.yml` |
| Config files | `docker-compose.yml`, `mappings/*.json` |
| Config values | profiles: `api-mock` |
| Compose linkage | unconditional root include, profile-selected, in [root docker-compose.yml](../../../docker-compose.yml) -> `infra/09-tooling/wiremock/docker-compose.yml` |
| Networks | project default |
| Volumes | `./mappings:/home/wiremock/mappings:ro` |
| Ports | `127.0.0.1:${WIREMOCK_HOST_PORT:-18088}:8080` |
| Labels | `hy-home.tier` |
| Secret refs | Not declared |
| Healthcheck | Compose healthcheck declared for `wiremock` (`/__admin/health`) |
| Operations | Guide (`docs/05.operations/catalog/09-tooling/0092-wiremock/guide.md`), Policy (`docs/05.operations/catalog/09-tooling/0092-wiremock/policy.md`), Runbook (`docs/05.operations/catalog/09-tooling/0092-wiremock/runbook.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | Inspect the health endpoint and the unmatched-request list, then the linked runbook. |

## How to Work in This Area

1. 상위 tier README와 `docker-compose.yml`을 먼저 확인한다.
2. stub을 추가할 때는 `mappings/`에 합성 데이터만 쓴다. 실제 응답·token·개인정보를 커밋하지 않는다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.

Runtime image and profile authority is [docker-compose.yml](docker-compose.yml);
the [derived Compose image projection](../../tech-stack.versions.json) is drift evidence.
