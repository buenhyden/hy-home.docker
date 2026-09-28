---
title: "WireMock"
version: "1.0.1"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
created: "2026-09-23"
---

<!-- [ID:09-tooling:wiremock] -->
# WireMock

> 온디맨드 **OPTIONAL** HTTP 스텁 서버이며 호스트 엔드포인트와 인증되지 않은 admin API는 loopback 전용입니다.

## Overview

WireMock은 개발·테스트 중 외부 HTTP 의존성을 대신하는 **OPTIONAL** stub
서버입니다. `api-mock` profile로만 선택되며 tracked `mappings/`의 stub만 영속
권한이 있습니다. 영속 데이터·web UI·OIDC client가 없습니다.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- AI Agents

## Scope

### In Scope

- 읽기 전용 추적 mapping을 사용하는 WireMock standalone 서버.
- Loopback 호스트 게시와 project-default-network 접근.

### Out of Scope

- 관리 API 인증 (구현되어 있지 않음; 노출은 loopback 전용).
- 실제 upstream에 대한 record-and-playback.
- Pact Broker가 담당하는 consumer 계약 검증.

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
| **Service** | WireMock 3 (Alpine 이미지) | HTTP stub 서버 |
| **Port** | `127.0.0.1:${WIREMOCK_HOST_PORT:-18088}` → `8080` | Loopback 전용 호스트 게시 |
| **Storage** | 없음 | mapping은 이 디렉터리를 읽기 전용으로 바인드함 |

## Configuration

### Environment Variables

| Variable | Required | Description |
| :--- | :---: | :--- |
| `WIREMOCK_HOST_PORT` | No | Loopback 호스트 포트(기본값: 18088); 컨테이너는 항상 8080에서 수신합니다. |

## Available Scripts

저장소 루트에서 다음 읽기 전용 확인 명령을 실행합니다. 서비스를 시작하려면
런타임 승인이 필요합니다.

| Command | Description |
| :--- | :--- |
| `docker compose --profile api-mock config --services` | 선택된 root-project 서비스를 확인합니다. |
| `docker compose --profile api-mock logs --tail=100 wiremock` | 승인된 실행 중인 서비스를 점검합니다. |

## Validation

- `HYHOME_COMPOSE_PROFILES=api-mock bash scripts/validation/validate-docker-compose.sh`
- `python3 scripts/validation/run-ci-gate.py --profile changed`

## Troubleshooting

- 예상한 stub이 404를 반환하면 `__admin/requests/unmatched`를 조회하고 런북을 따릅니다.
- 로드되지 않은 mapping은 시작 시 컨테이너 로그에 이름이 남습니다.

## Related Documents

- **Guide**: WireMock Usage Guide (`docs/05.operations/guides/0092-wiremock.md`)
- **Policy**: WireMock Operations Policy (`docs/05.operations/policies/0092-wiremock.md`)
- **Runbook**: WireMock Recovery Runbook (`docs/05.operations/runbooks/0092-wiremock.md`)
- [Documentation index](../../../docs/README.md)

---

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | `09-tooling`의 WireMock 서비스 leaf; 서비스: `wiremock`; [root docker-compose.yml](../../../docker-compose.yml) -> `infra/09-tooling/wiremock/docker-compose.yml` 경로로 무조건 루트 include되며 프로필로 선택됨 |
| Config files | `docker-compose.yml`, `mappings/*.json` |
| Config values | 프로필: `api-mock` |
| Compose linkage | [root docker-compose.yml](../../../docker-compose.yml) -> `infra/09-tooling/wiremock/docker-compose.yml` 경로로 무조건 루트 include되며 프로필로 선택됨 |
| Networks | project default |
| Volumes | `./mappings:/home/wiremock/mappings:ro` |
| Ports | `127.0.0.1:${WIREMOCK_HOST_PORT:-18088}:8080` |
| Labels | `hy-home.tier` |
| Secret refs | 선언되지 않음 |
| Healthcheck | `wiremock`에 Compose 헬스체크가 선언되어 있음 (`/__admin/health`) |
| Operations | Guide (`docs/05.operations/guides/0092-wiremock.md`), Policy (`docs/05.operations/policies/0092-wiremock.md`), Runbook (`docs/05.operations/runbooks/0092-wiremock.md`) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [run-ci-gate.py](../../../scripts/validation/run-ci-gate.py) (`python3 scripts/validation/run-ci-gate.py --profile changed`) |
| Troubleshooting | 헬스 엔드포인트와 unmatched-request 목록을 확인한 뒤 연결된 런북을 확인합니다. |

## How to Work in This Area

1. 상위 tier README와 `docker-compose.yml`을 먼저 확인한다.
2. stub을 추가할 때는 `mappings/`에 합성 데이터만 쓴다. 실제 응답·token·개인정보를 커밋하지 않는다.
3. 변경 후 상위 README와 관련 stage 문서의 링크를 함께 확인한다.

런타임 이미지와 프로필의 권위는 [docker-compose.yml](docker-compose.yml)에 있으며
[파생된 Compose 이미지 프로젝션](../../tech-stack.versions.json)은 드리프트 근거입니다.
