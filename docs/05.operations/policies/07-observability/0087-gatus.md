---
title: "Gatus Policy"
version: "0.7.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0087"
parent_ids:
- "AD-0031"
created: "2026-09-19"
next_review_at: "2027-05-13"
---

# Gatus Policy

## Purpose and Scope

### Objective

Gatus는 native OIDC와 지속적인 probe history를 가진 HOME availability monitor다.

#### Authority

- Governing architecture: [AD-0031](../../../02.architecture/descriptions/0031-home-development-host.md)

- 런타임 고정값은 [observability Compose](../../../../infra/06-observability/docker-compose.yml)와 선택된 [Gatus Dockerfile](../../../../infra/06-observability/gatus/Dockerfile)이 소유하며, [derived Compose image projection](../../../../infra/tech-stack.versions.json)이 drift를 검증한다.

### Applies To

로컬 Gatus 이미지, native OIDC 설정, read-only config mount, `gatus-data` SQLite
상태, status UI, metrics 경계, probe를 HOME availability 역량 안에서 유지한다.

#### Exclusions

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0087-R1 | 항상 | 필수: host 포트를 게시하지 않고(`expose`만) non-root identity, read-only root filesystem, read-only config bind, 쓰기 가능한 `gatus-data` mount를 유지한다(현재 `read_only: false`로 미준수) | 정적 소스/catalog 검사 | 미준수 확인 2026-11-06 / owner 예외 또는 Compose 수정 필요 |
| POL-0087-R2 | UI 접근 | 필수: native `home-gatus` OIDC와 `gateway-standard-chain@file`을 쓰고 `sso-auth@file`, local-password fallback, 넓은 subject allowlist를 추가하지 않으며 `/metrics`는 승인된 설계 없이 외부에 노출하지 않는다 | 정적 소스/catalog 검사 | owner 수용 기록(2026-11-07, SPEC-0267) |
| POL-0087-R3 | Task 증거 | 금지: probe URL, response body, credential 자료, 원시 SQLite 데이터를 기록하며 probe 성공을 애플리케이션 수용으로 보지 않는다 | 수동 | none |
| POL-0087-R4 | SQLite 교체/운영 | 필수: SQLite를 stateful로 취급해 조율된 backup과 격리된 restore 증명을 만들고 증상 해결을 위해 volume을 삭제하지 않는다 | 수동 | backup/restore 증명(런타임) |
| POL-0087-R5 | 업그레이드 | 필수: Dockerfile 소스, upstream 릴리스/보안 노트, 라이선스, 로컬 hardening patch를 검토한 후에만 업그레이드하고 승인된 검사가 끝날 때까지 이전 이미지/설정을 유지한다 | 수동 | 로그인/health/probe 검사(런타임) |
| POL-0087-R6 | lifecycle/data | 필수: HOME 유지, `gatus.db`를 live-copy하지 않고 격리 프로젝트에서 리허설하며 업그레이드/제거는 명시적 승인 | 수동 | none |
| POL-0087-R7 | build 수용 | 필수: source commit/checksum/local patch/image digest를 갖추고 zero-fuzz, 정확한 subject, S256 PKCE, Secure/HttpOnly cookie, state/nonce, CA 검증을 유지한다 | 수동 | source commit/checksum/image digest |

- 직접 host 포트는 게시하지 않고(`expose: ${GATUS_PORT}`만), 설정된 non-root identity(`${GATUS_UID:-1000}:${GATUS_GID:-1000}`),
  read-only root filesystem, read-only config bind, 쓰기 가능한 `gatus-data` mount를 유지한다.
- **미준수(2026-11-06 확인):** `template-stateful-low`가 `read_only: false`라 root filesystem이 현재 쓰기
  가능하다. owner가 기한 있는 예외로 수용하거나 Compose를 `read_only: true`와 tmpfs로 고칠 때까지 열린 항목이다.
- UI에는 native `home-gatus` OIDC와 `gateway-standard-chain@file`을 사용한다.
  `sso-auth@file`, local-password fallback, 넓은 subject allowlist를 추가하지 않는다.
  `/metrics`는 브라우저 route 밖에 두고 승인된 모니터링 설계 없이는 외부에 노출하지
  않는다. 내부에서는 main 포트 `8080`의 `/metrics`가 `edge_net`, `mng_data_net`,
  `obs_net`, `keycloak_management_net`의 모든 peer에게 인증 없이 열려 있다. upstream이 OIDC router 밖에서
  제공하고 저장소 patch(`metrics-remains-public-for-internal-scrape`)가 내부 scrape를
  위해 공개로 유지하므로 owner가 2026-11-07 이 노출을 수용했다(SPEC-0267).
  `oidc-hardening.patch`를 건드리는 Gatus 갱신이나 upstream metrics 인증이 생기면
  다시 검토한다.
- probe URL, response body, credential 자료, 원시 SQLite 데이터를 Task 증거에 기록하지
  않는다. probe 성공은 endpoint 증거이지 애플리케이션 수용이 아니다.
- SQLite를 stateful로 취급한다. 교체 전에 조율된 일관된 backup과 격리된 restore 증명을
  만든다. probe나 로그인 증상을 해결하기 위해 volume을 삭제하지 않는다.
- Dockerfile 소스, upstream 릴리스/보안 노트, 라이선스, 로컬 hardening patch를 검토한
  후에만 업그레이드한다. 승인된 로그인, health, probe 검사가 완료될 때까지 이전
  이미지/설정을 유지한다.

#### Lifecycle and data controls

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

### Exceptions

#### Exception Conditions

예외는 owner, scope, risk, expiry, recovery condition이 필요하다.

#### Approval and Review

매월, 그리고 인증, probe inventory, 소스, storage가 변경될 때 검토한다.

## Enforcement

### Mechanisms

정적 소스와 catalog 검사는 선언만 검증한다. 컨테이너 health, native 로그인, 세션 만료,
probe 커버리지, backup, restore는 별도로 승인된 target이 필요한 런타임 증거로 남는다.

### Limits

이 정책은 정적 소스와 catalog 검사가 선언만 검증한다고 명시하며 나머지는 별도 승인된 target의 런타임 증거에 맡긴다.

- 컨테이너 health, native 로그인, 세션 만료, probe 커버리지, backup, restore는 별도 target이 필요한 런타임 증거이며 이 문서에는 없다.
- read-only root filesystem은 `template-stateful-low`가 `read_only: false`라 2026-11-06 기준 미준수이며 owner 예외나 Compose 수정 전까지 열려 있다.
- `/metrics`는 내부 peer에게 인증 없이 열려 있으며 owner 수용(2026-11-07)에 의존하고 `oidc-hardening.patch` 변경이나 upstream 인증 도입 때 재검토한다.
- 소스 문서 검사는 runtime 예외를 부여하지 않는다.
- 증거 기록 금지, 업그레이드 검토, `gatus.db` live-copy 금지는 수동 규율이다.

## Ownership

### Owner

책임 소유자는 **@buenhyden**이다. 예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다. 통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

### Review Triggers

- [Guide](../../guides/07-observability/0087-gatus.md), [Runbook](../../runbooks/07-observability/0087-gatus.md)
- [Gatus upstream security policy](https://github.com/TwiN/gatus/security/policy)
- 이 문서는 SPEC-0267 secondary-listener hardening 결과를 담고 있다. 해당 패키지는 retire되었고 본문은 version history에 있다.
