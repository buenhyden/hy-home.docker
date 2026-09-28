---
title: "WireMock Operations Policy"
version: "1.0.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "POL-0092"
parent_ids:
- "AD-0009"
created: "2026-09-23"
---

# WireMock Operations Policy

## Overview

WireMock은 추적되는 stub으로 HTTP 요청에 응답하고 받은 요청을 기록한다. admin
API에는 인증이 없으므로 노출과 stub 내용이 곧 control이다.

## Policy Scope

선택, 네트워크 노출, stub 내용, request journal, 제거.

## Controls

- `api-mock`을 통해서만 선택한다. HOME이나 도메인 프로필에 절대 추가하지 않는다.
- host 포트는 `127.0.0.1`에만 게시하고 Traefik route를 추가하지 않는다. admin API를
  노출하려면 먼저 인증을 추가하는 검토된 변경이 필요하다.
- 프로젝트 기본 네트워크가 컨테이너 측 신뢰 경계다. 그 안의 어떤 컨테이너든 완전한
  admin 권한을 가진다. named consumer가 추가되면 범위가 제한된 네트워크를 받는다.
- 추적되는 mapping만이 지속적인 stub이다. stub body는 합성 데이터다. 캡처된 운영
  response, credential, 토큰, 개인 데이터는 사용하지 않는다.
- 실제 upstream을 대상으로 한 recording이나 proxying은 정책으로 금지한다. read-only
  mount는 recording 저장만 막는다. admin API로 recording을 시작하거나
  `proxyBaseUrl`을 가진 stub을 만드는 일은 기술적으로 막혀 있지 않다.
- request journal은 제한된 상태로 유지한다. stub에 보낸 요청에는 테스트 credential이
  들어 있을 수 있고 실행 중에는 admin API로 읽을 수 있다.

## Exceptions

없음. 다른 네트워크에서 도달 가능한 stub이 필요한 consumer는 host binding을 넓히는
대신 프로젝트 기본 네트워크에 합류한다.

## Verification

Compose 렌더링, 운영 catalog 검사, health, 추적되는 stub, non-root user, read-only
root filesystem을 증명하는 격리된 실행.

## Review Cadence

WireMock major 업그레이드, 신규 consumer, loopback을 넘는 노출이 제안될 때마다
검토한다.

## Traceability

- [Guide](../guides/0092-wiremock.md) (`GDE-0092`)
- [Runbook](../runbooks/0092-wiremock.md) (`RUN-0092`)
- [Tooling architecture](../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [WireMock Compose source](../../../infra/09-tooling/wiremock/docker-compose.yml)
- [Compose profile vocabulary](0078-compose-profile-vocabulary.md)
