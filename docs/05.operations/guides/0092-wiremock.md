---
title: "WireMock Usage Guide"
version: "1.0.1"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "GDE-0092"
parent_ids:
- "POL-0092"
implementation_services:
  infra/11-quality/wiremock/docker-compose.yml:
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

- [WireMock Compose](../../../infra/11-quality/wiremock/docker-compose.yml)는
  프로젝트 기본 네트워크에 하나의 서비스를 정의한다. 호스트는
  `http://127.0.0.1:${WIREMOCK_HOST_PORT:-18088}`로 접근하고 해당
  네트워크의 컨테이너는 `http://wiremock:8080`으로 접근하며 전체 관리
  권한을 가진다.
- 스텁은 `infra/11-quality/wiremock/mappings/`의 JSON 파일이며 읽기
  전용으로 마운트된다. 추적되는 `hyhome-ping.json`은 `GET /hyhome/ping`에
  응답하며 매핑이 로드됨을 증명하는 용도다.
- `/__admin` 아래의 관리자 API는 인증이 없다. 스텁을 추가, 재설정, 목록
  조회하고 요청 저널을 읽을 수 있다. 호스트 포트는 루프백에만
  바인딩되며, 컨테이너 쪽에서는 프로젝트 기본 네트워크가 신뢰 경계다.
  관리자 API로 추가한 스텁은 메모리에만 존재하며 재시작하면 사라진다.
- 요청 저널 항목 수는 Compose에서 제한한다. 항목 수 제한이 JVM 전체 메모리나
  요청·본문 크기까지 제한하지는 않으므로 자원 한도와 실제 사용량을 함께 확인한다.

### Adding a stub

실행 순서와 실패·복구 판단은 [런북](../runbooks/0092-wiremock.md)의 `매핑 변경·기동·재적용` 절차를 따른다. 데이터와 권한 경계는 해당 정책을 유지한다.

## Common Checks

- `HYHOME_COMPOSE_PROFILES=api-mock bash scripts/validation/validate-docker-compose.sh`
- `python3 scripts/validation/check-operations-catalog.py`

## Runbook Handoff

서비스가 비정상이거나 스텁이 일치하지 않거나 메모리 한도에 도달하면
[runbook](../runbooks/0092-wiremock.md)을 사용한다.

### 정상 사용과 보존

승인된 테스트는 추적된 합성 stub을 호출하고 예상 status·응답 계약을 비교한다.
WireMock은 외부 대상과의 실제 계약 검증을 대신하지 않는다. 선언된 의존성 대기는
없으며 health와 `GET /hyhome/ping`은 프로세스·매핑 로드 신호다. 장기 상태는
추적된 mapping 파일이 소유하고 메모리 journal·추가 stub은 재시작 때 사라진다.
HTTP 인증서·DB 복원은 적용되지 않지만 노출·요청 데이터 보존 통제는 유지한다.

## Traceability

- [Policy](../policies/0092-wiremock.md) (`POL-0092`)
- [Runbook](../runbooks/0092-wiremock.md) (`RUN-0092`)
- [Platform Operations·Quality 아키텍처](../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [WireMock package README](../../../infra/11-quality/wiremock/README.md) and [derived version projection](../../../infra/tech-stack.versions.json)
- [WireMock stubbing reference](https://wiremock.org/docs/stubbing/)
- [WireMock standalone Docker](https://wiremock.org/docs/standalone/docker/)
