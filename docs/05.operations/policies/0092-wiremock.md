---
title: "WireMock Operations Policy"
version: "1.0.2"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-03"
layer: "operations"
artifact_id: "POL-0092"
parent_ids:
- "AD-0009"
created: "2026-09-23"
---

# WireMock Operations Policy

## Overview

### Overview

WireMock은 추적되는 stub으로 HTTP 요청에 응답한다. 기능 모드는 bounded request
journal을 기록하고, load override 모드는 journal을 기록하지 않는다. admin API에는
인증이 없으므로 노출과 stub 내용이 곧 control이다.

## Scope

### Policy Scope

기능·부하 모드 선택, 네트워크 노출, stub 내용, request journal, 제거.

### Traceability

- [Guide](../guides/0092-wiremock.md) (`GDE-0092`)
- [Runbook](../runbooks/0092-wiremock.md) (`RUN-0092`)
- [Platform Operations·Quality 아키텍처](../../02.architecture/descriptions/0009-tooling-architecture.md)

## Rules

### Controls

- 기능 모드는 `api-mock`만 선택한다. 부하 모드는 root Compose와
  `wiremock.load.yml` override를 함께 사용해 같은 `api-mock`을 선택한다.
  두 모드는 같은 service state를 공유하므로 동시에 선택하거나 HOME·도메인 profile에
  추가하지 않는다.
- 기능 모드 host 포트는 `127.0.0.1`에만 게시하고 Traefik route를 추가하지 않는다.
  부하 모드는 host port를 게시하지 않고 `--admin-api-require-https`로 HTTP admin을
  거부한다. HTTPS listener를 추가하려면 인증·노출을 검토한 별도 변경이 필요하다.
- 기능 모드에서는 프로젝트 기본 네트워크의 컨테이너가 admin 권한을 가진다.
  부하 모드의 HTTP admin은 거부되지만 named consumer가 추가되면 별도 제한
  네트워크와 HTTPS listener 부재를 확인한다.
- 추적되는 mapping만이 지속적인 stub이다. stub body는 합성 데이터다. 캡처된 운영
  response, credential, 토큰, 개인 데이터는 사용하지 않는다.
- 실제 upstream을 대상으로 한 recording이나 proxying은 정책으로 금지한다. read-only
  mount는 recording 저장만 막는다. admin API로 recording을 시작하거나
  `proxyBaseUrl`을 가진 stub을 만드는 일은 기술적으로 막혀 있지 않다.
- 기능 모드 request journal은 제한된 상태로 유지하고 각 승인된 실행 전에 reset한다.
  stub에 보낸 요청에는 테스트 credential이 들어 있을 수 있고 실행 중에는 admin API로
  읽을 수 있다. 부하 모드는 `--no-request-journal`을 유지하며 journal reset이나
  조회를 성능 증거로 사용하지 않는다.

### Verification

각 모드의 Compose 렌더링, 운영 catalog 검사, 추적되는 stub, non-root user,
read-only root filesystem을 확인한다. 기능 모드는 bounded journal/reset, load 모드는
host port 없음과 `--no-request-journal`을 격리된 실행에서 별도로 확인한다.

### Review Cadence

WireMock major 업그레이드, 신규 consumer, loopback을 넘는 노출이 제안될 때마다
검토한다.

### 소유권과 자원

책임자는 `@buenhyden`이다. 기능 모드의 journal 개수 한도와 컨테이너 자원 제한을
유지한다. 삭제·재시작으로 사라지는 메모리 자료는 복구 약속 대상이 아니며 민감한
요청을 보존 근거로 복제해서는 안 된다. mapping·이미지 변경은 합성 canary와 검토된
rollback 원본을 확보하고 적용한다.

## Exceptions

### Exceptions

현재 승인된 예외는 없다. 새로운 consumer의 네트워크 연결은 범위와 admin API
권한을 검토한 변경이어야 한다. host binding이나 기본 네트워크 참여를 자동으로 넓히지 않는다.

## Related Documents

- [WireMock Compose source](../../../infra/11-quality/wiremock/docker-compose.yml)
- [Compose profile vocabulary](0078-compose-profile-vocabulary.md)
