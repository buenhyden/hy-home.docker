---
title: "Pact Broker Operations Policy"
version: "1.0.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "POL-0093"
parent_ids:
- "AD-0009"
created: "2026-09-23"
---

# Pact Broker Operations Policy

## Overview

브로커의 검증 결과가 어떤 버전을 배포할 수 있는지 정하므로, 누가 publish와
verify를 할 수 있는지, 그리고 어디까지 도달할 수 있는지가 통제 대상이다.

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
- host 포트는 `127.0.0.1`에만 publish한다. loopback 밖으로 나가는 라우트를
  열려면 먼저 TLS와 SSO 또는 토큰 인증을 추가하는 검토된 변경을 거쳐야 한다.
- 자격 증명은 Docker secrets에서 가져오며 Compose `environment`, argv, 로그,
  publish된 pact 어디에도 나타나지 않는다. pact는 캡처된 운영 payload가 아닌
  합성 예시를 담는다.
- analytics ping은 비활성 상태를 유지한다.
- `PACT_BROKER_BASE_URL`은 설정하지 않은 채로 둔다. 생성되는 링크는 요청의
  `Host`를 따른다. 호스트 loopback과 management-data peer 경로가 함께 있으므로 Host 기반 링크가
  안전한 접근 경계를 보장한다고 해석하지 않는다. 새 라우트 전에는 base URL·인증·TLS
  경계를 검토한다.

## Exceptions

없음. 읽기 전용인 두 번째 자격 증명은 consumer가 필요로 할 때만 추가한다.

## Verification

정적 렌더링과 프로비저닝 계약 테스트, 그리고 자격 증명 없이 401이 나오는지,
heartbeat가 공개되는지, 자격 증명으로 publish와 read-back이 되는지, 컨테이너가
non-root이고 읽기 전용인지, Compose 설정·argv·로그에 비밀 값이 노출되지 않는지를 확인하는
격리된 실행.

## Review Cadence

브로커 major 업그레이드, 새 publishing 파이프라인, loopback을 넘어서는 노출이
제안될 때마다 검토한다.

### 책임과 비밀 전달 경계

책임자는 `@buenhyden`이다. wrapper의 프로세스 환경변수 전달은 허용된 입력 방식이나
Compose literal·argv·로그·pact에 비밀 값을 남기는 것은 금지된다. 새 network consumer와
DB 보존·복원·삭제는 영향을 받는 소유자를 확인하고 승인한다. raw 환경 조회를 검증
방법으로 사용하지 않는다.

## Traceability

- [가이드](../guides/0093-pact-broker.md) (`GDE-0093`)
- [런북](../runbooks/0093-pact-broker.md) (`RUN-0093`)
- [Platform Operations·Quality 아키텍처](../../02.architecture/descriptions/0009-tooling-architecture.md)

## Related Documents

- [Pact Broker Compose source](../../../infra/11-quality/pact-broker/docker-compose.yml)
- [Management database policy](0028-management-database.md)
