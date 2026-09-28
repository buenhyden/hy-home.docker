---
title: "Pact Broker Operations Policy"
version: "1.0.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-29"
layer: "operations"
artifact_id: "POL-0093"
parent_ids:
- "AD-0009"
created: "2026-09-23"
---

# Pact Broker Operations Policy

## Overview

브로커의 검증 결과가 어떤 버전을 배포할 수 있는지를 결정하므로, 누가 publish와
verify를 할 수 있는지, 그리고 어디까지 도달 가능한지가 통제 대상이다.

## Policy Scope

프로비저닝, 인증, 노출, 자격 증명, 데이터 보존 및 제거.

## Controls

- `contract-testing`를 통해서만 선택한다. HOME에는 절대 추가하지 않는다.
- 프로비저닝은 `mng-pg-init`이 아니라 feature SQL에 둔다. 역할(role)은
  `NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS`이며 자신의
  데이터베이스만 소유한다. job은 관리자 권한, 자신이 생성하지 않은 role, 다른
  소유자의 데이터베이스를 거부한다.
- Basic auth는 계속 활성화하고 `PACT_BROKER_ALLOW_PUBLIC_READ`는 `false`를
  유지한다. heartbeat만 공개한다.
- host 포트는 `127.0.0.1`에만 publish한다. loopback을 넘어서는 라우트는 TLS와
  SSO 또는 토큰 인증을 먼저 추가하는 검토된 변경이 필요하다.
- 자격 증명은 Docker secrets에서 가져오며 Compose `environment`, argv, 로그,
  publish된 pact 어디에도 나타나지 않는다. pact는 캡처된 운영 payload가 아닌
  합성 예시를 담는다.
- analytics ping은 비활성 상태를 유지한다.
- `PACT_BROKER_BASE_URL`은 설정하지 않은 채로 둔다. 생성되는 링크는 요청의
  `Host`를 따르며, 이는 유일한 리스너가 loopback인 동안에는 안전하고
  네트워크 내 클라이언트가 동작하게 해 준다. 라우트가 추가되면 설정한다.

## Exceptions

없음. 두 번째, 읽기 전용 자격 증명은 consumer가 필요로 할 때만 추가한다.

## Verification

정적 렌더링과 프로비저닝 계약 테스트, 그리고 자격 증명 없이 401이 나오는지,
heartbeat가 공개되는지, 자격 증명으로 publish와 read-back이 되는지, 컨테이너가
non-root이고 읽기 전용인지, 환경 변수나 로그에 secret이 없는지를 증명하는
격리된 실행.

## Review Cadence

브로커 major 업그레이드, 새 publishing 파이프라인, loopback을 넘어서는 노출이
제안될 때마다 검토한다.

## Traceability

- [가이드](../guides/0093-pact-broker.md) (`GDE-0093`)
- [런북](../runbooks/0093-pact-broker.md) (`RUN-0093`)
- [Tooling architecture](../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [Pact Broker Compose source](../../../infra/09-tooling/pact-broker/docker-compose.yml)
- [Management database policy](0028-management-database.md)
