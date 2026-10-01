---
title: "Gatus Policy"
version: "0.2.1"
type: "operation/policy"
status: "draft"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "POL-0087"
parent_ids:
- "AD-0031"
created: "2026-09-19"
---

# Gatus Policy

## Overview

Gatus는 native OIDC와 지속적인 probe history를 가진 HOME availability monitor다.

## Policy Scope

로컬 Gatus 이미지, native OIDC 설정, read-only config mount, `gatus-data` SQLite
상태, status UI, metrics 경계, probe를 HOME availability 역량 안에서 유지한다.

## Controls

- 직접 host 포트는 게시하지 않고, 설정된 non-root identity, read-only root filesystem,
  쓰기 가능한 data mount를 Compose 소스가 선언한 그대로 유지한다.
- UI에는 native `home-gatus` OIDC와 `gateway-standard-chain@file`을 사용한다.
  `sso-auth@file`, local-password fallback, 넓은 subject allowlist를 추가하지 않는다.
  `/metrics`는 브라우저 route 밖에 두고 승인된 모니터링 설계 없이는 외부에 노출하지
  않는다.
- probe URL, response body, credential 자료, 원시 SQLite 데이터를 Task 증거에 기록하지
  않는다. probe 성공은 endpoint 증거이지 애플리케이션 수용이 아니다.
- SQLite를 stateful로 취급한다. 교체 전에 조율된 일관된 backup과 격리된 restore 증명을
  만든다. probe나 로그인 증상을 해결하기 위해 volume을 삭제하지 않는다.
- Dockerfile 소스, upstream 릴리스/보안 노트, 라이선스, 로컬 hardening patch를 검토한
  후에만 업그레이드한다. 승인된 로그인, health, probe 검사가 완료될 때까지 이전
  이미지/설정을 유지한다.

### Lifecycle and data controls

- Gatus는 `HOME`으로 유지한다. native Keycloak OIDC, root-CA 검증, 세션 제어, 최소
  권한 endpoint credential이 필요하다.
- SQLite/data, endpoint 설정, 로컬 patch/이미지 identity, 대응하는 OIDC secret이 recovery
  set을 구성한다. 쓰기를 멈추거나 SQLite-native backup을 사용한다. `gatus.db`를 절대
  live-copy하지 않는다.
- 테스트 route/credential을 사용하는 격리된 프로젝트에서 리허설하고, private response
  데이터를 노출하지 않고 schema, history, endpoint, OIDC, 세션 동작, metrics를 검증한다.
- 업그레이드/제거는 patch 호환성, endpoint-owner 조율, 보존된 history 결정, client/route
  폐기, 명시적 데이터 삭제 승인이 필요하다.

Build 수용에는 source commit·checksum·local patch·생성 image digest가 필요하며 local tag만으로 패치를 증명하지 않는다. Zero-fuzz, 대소문자를 구분하는 정확한 subject, S256 PKCE, Secure/HttpOnly 임시 cookie, state/nonce 검사와 CA 검증을 유지한다. Public health/bootstrap/metrics와 보호 status API를 구분한다. Source/auth/storage 예외와 종료 시점은 @buenhyden이 승인하며 소스 문서 검사는 runtime 예외를 부여하지 않는다.

## Exceptions

예외는 owner, scope, risk, expiry, recovery condition이 필요하다.

## Verification

정적 소스와 catalog 검사는 선언만 검증한다. 컨테이너 health, native 로그인, 세션 만료,
probe 커버리지, backup, restore는 별도로 승인된 target이 필요한 런타임 증거로 남는다.

책임 소유자는 **@buenhyden**이다. 예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다. 통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

## Review Cadence

매월, 그리고 인증, probe inventory, 소스, storage가 변경될 때 검토한다.

## Traceability

- Governing architecture: [AD-0031](../../02.architecture/descriptions/0031-home-development-host.md)
- Subject peers: [Guide](../guides/0087-gatus.md) and [Runbook](../runbooks/0087-gatus.md)

## Related Documents

- [Guide](../guides/0087-gatus.md), [Runbook](../runbooks/0087-gatus.md)
- 런타임 고정값은 [observability Compose](../../../infra/06-observability/docker-compose.yml)와 선택된 [Gatus Dockerfile](../../../infra/06-observability/gatus/Dockerfile)이 소유하며, [derived Compose image projection](../../../infra/tech-stack.versions.json)이 drift를 검증한다.
- [Gatus upstream security policy](https://github.com/TwiN/gatus/security/policy)
