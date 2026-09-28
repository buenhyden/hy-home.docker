---
title: "WireMock Usage Guide"
version: "1.0.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "GDE-0092"
parent_ids:
- "POL-0092"
implementation_services:
  infra/09-tooling/wiremock/docker-compose.yml:
  - wiremock
created: "2026-09-23"
---

# WireMock Usage Guide

## Usage

### Purpose and classification

WireMock은 `api-mock`으로만 선택되는 OPTIONAL HTTP 스텁 서버다. 개발과
테스트 중 외부 HTTP 의존성을 대신해 실제 서비스를 호출하지 않고도
소비자를 테스트할 수 있게 한다. 주 데이터를 보유하지 않고 웹 UI도 없어
라우트나 OIDC 클라이언트는 없고 필요하지도 않다.

### Current implementation

- [WireMock Compose](../../../infra/09-tooling/wiremock/docker-compose.yml)는
  프로젝트 기본 네트워크에 하나의 서비스를 정의한다. 호스트는
  `http://127.0.0.1:${WIREMOCK_HOST_PORT:-18088}`로 접근하고 해당
  네트워크의 컨테이너는 `http://wiremock:8080`으로 접근하며 전체 관리
  권한을 가진다.
- 스텁은 `infra/09-tooling/wiremock/mappings/`의 JSON 파일이며 읽기
  전용으로 마운트된다. 추적되는 `hyhome-ping.json`은 `GET /hyhome/ping`에
  응답하며 매핑이 로드됨을 증명하는 용도다.
- `/__admin` 아래의 관리자 API는 인증이 없다. 스텁을 추가, 재설정, 목록
  조회하고 요청 저널을 읽을 수 있다. 호스트 포트는 루프백에만
  바인딩되며, 컨테이너 쪽에서는 프로젝트 기본 네트워크가 신뢰 경계다.
  관리자 API로 추가한 스텁은 메모리에만 존재하며 재시작하면 사라진다.
- 요청 저널은 1000개 항목으로 제한되어 있으므로, 테스트를 오래 실행해도
  JVM이 템플릿 메모리 한도를 넘어 커질 수 없다.

### Adding a stub

`mappings/` 아래에 매핑 파일을 추가한 다음 서비스를 재시작하거나
`POST /__admin/mappings/reset`을 호출하면 파일이 다시 로드된다. 스텁
본문은 합성 데이터로 유지한다. 매핑은 추적되는 파일이므로 운영 시스템에서
캡처한 실제 응답, 토큰, 개인정보를 포함해서는 안 된다.

| Command | Effect |
| --- | --- |
| `docker compose --profile api-mock up -d wiremock` | 스텁 서버 시작 |
| `curl -s http://127.0.0.1:${WIREMOCK_HOST_PORT:-18088}/__admin/health` | 상태, 버전, 가동 시간 |
| `curl -s http://127.0.0.1:${WIREMOCK_HOST_PORT:-18088}/__admin/requests` | 시작 이후 수신한 요청 |
| `curl -s -X POST http://127.0.0.1:${WIREMOCK_HOST_PORT:-18088}/__admin/mappings/reset` | 추적된 매핑을 다시 로드하고 메모리상 매핑은 삭제 |

## Common Checks

- `HYHOME_COMPOSE_PROFILES=api-mock bash scripts/validation/validate-docker-compose.sh`
- `python3 scripts/validation/check-operations-catalog.py`

## Runbook Handoff

서비스가 비정상이거나 스텁이 일치하지 않거나 메모리 한도에 도달하면
[runbook](../runbooks/0092-wiremock.md)을 사용한다.

## Traceability

- [Policy](../policies/0092-wiremock.md) (`POL-0092`)
- [Runbook](../runbooks/0092-wiremock.md) (`RUN-0092`)
- [Tooling architecture](../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [WireMock package README](../../../infra/09-tooling/wiremock/README.md) and [derived version projection](../../../infra/tech-stack.versions.json)
- [WireMock stubbing reference](https://wiremock.org/docs/stubbing/)
- [WireMock standalone Docker](https://wiremock.org/docs/standalone/docker/)
