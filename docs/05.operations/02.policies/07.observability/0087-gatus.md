---
title: "Gatus Policy"
version: "1.0.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
document_scope:
  subject: hy-home.docker
  layer: workspace
updated: "2026-11-20"
layer: "operations"
artifact_id: "POL-0087"
parent_ids:
- "AD-0031"
created: "2026-09-19"
next_review_at: "2027-05-13"
---

# Gatus Policy

<!-- document-core: WORKSPACE-DOCUMENT-CORE/1.0.0 -->

## 문서 개요

### 목적과 독자

Readers use the policy payload below for this document's information and judgments.

### 책임과 적용 범위

The frontmatter and role payload own the maintained subject, owner and applicability.

## 내용 계약

### 입력과 전제

Actual inputs and preconditions are those declared by the role payload below.

### 본문과 규칙

#### Purpose and Scope

##### Objective

Gatus는 native OIDC와 지속적인 probe history를 가진 HOME availability monitor다.

###### Authority
<!-- core-payload-level:4 -->

- Governing architecture: [AD-0031](../../../02.architecture/01.descriptions/0031-home-development-host.md)

- 런타임 고정값은 [observability Compose](../../../../infra/06-observability/docker-compose.yml)와 선택된 [Gatus Dockerfile](../../../../infra/06-observability/gatus/Dockerfile)이 소유하며, [derived Compose image projection](../../../../infra/tech-stack.versions.json)이 drift를 검증한다.

##### Applies To

로컬 Gatus 이미지, native OIDC 설정, read-only config mount, `gatus-data` SQLite
상태, status UI, metrics 경계, probe를 HOME availability 역량 안에서 유지한다.

###### Exclusions
<!-- core-payload-level:4 -->

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

#### Rules

##### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0087-R1 | 항상 | 금지: 직접 host 포트 게시(`expose: ${GATUS_PORT}`만 사용) | none | none |
| POL-0087-R2 | 항상 | 필수: 설정된 non-root identity(`${GATUS_UID:-1000}:${GATUS_GID:-1000}`)/read-only root filesystem/read-only config bind/쓰기 가능한 `gatus-data` mount 유지(2026-11-06 확인: `read_only: false`로 미준수) | none | 미준수 확인 2026-11-06 |
| POL-0087-R3 | read-only root filesystem 미준수 상태 | 필수: owner가 기한 있는 예외로 수용하거나 Compose를 `read_only: true`와 tmpfs로 고칠 때까지 열린 항목으로 유지 | 수동 | none |
| POL-0087-R4 | UI 접근 | 필수: native `home-gatus` OIDC와 `gateway-standard-chain@file` 사용 | none | none |
| POL-0087-R5 | UI 접근 | 금지: `sso-auth@file`/local-password fallback/넓은 subject allowlist 추가 | none | none |
| POL-0087-R6 | 항상 | 필수: `/metrics`는 브라우저 route 밖에 둠 | none | none |
| POL-0087-R7 | 승인된 모니터링 설계가 없을 때 | 금지: `/metrics` 외부 노출 | 수동 | none |
| POL-0087-R8 | `oidc-hardening.patch`를 건드리는 Gatus 갱신 또는 upstream metrics 인증 도입 시 | 필수: `/metrics` 내부 무인증 노출 수용(owner 2026-11-07, SPEC-0267)을 다시 검토 | none | owner 수용 기록(2026-11-07, SPEC-0267) |
| POL-0087-R9 | Task 증거 작성 시 | 금지: probe URL/response body/credential 자료/원시 SQLite 데이터 기록 | 수동 | none |
| POL-0087-R10 | 항상 | 금지: probe 성공을 애플리케이션 수용으로 간주 | none | none |
| POL-0087-R11 | SQLite 교체 전 | 필수: SQLite를 stateful로 취급해 조율된 일관된 backup과 격리된 restore 증명 확보 | none | backup/restore 증명(런타임) |
| POL-0087-R12 | 항상 | 금지: probe나 로그인 증상 해결을 위해 volume 삭제 | none | none |
| POL-0087-R13 | 업그레이드 전 | 필수: Dockerfile 소스/upstream 릴리스·보안 노트/라이선스/로컬 hardening patch 검토 | 수동 | none |
| POL-0087-R14 | 업그레이드 시 | 필수: 승인된 로그인/health/probe 검사가 완료될 때까지 이전 이미지/설정 유지 | none | 로그인/health/probe 검사(런타임) |
| POL-0087-R15 | 항상 | 필수: Gatus를 HOME으로 유지하고 native Keycloak OIDC/root-CA 검증/세션 제어/최소 권한 endpoint credential 요구 | none | none |
| POL-0087-R16 | 항상 | 필수: SQLite/data/endpoint 설정/로컬 patch·이미지 identity/대응 OIDC secret을 recovery set으로 구성하고 쓰기 중단 또는 SQLite-native backup 사용 | none | none |
| POL-0087-R17 | 항상 | 금지: `gatus.db` live-copy | 수동 | none |
| POL-0087-R18 | 항상 | 필수: 테스트 route/credential을 쓰는 격리된 프로젝트에서 리허설하고 private response 데이터 노출 없이 schema/history/endpoint/OIDC/세션 동작/metrics 검증 | none | none |
| POL-0087-R19 | 업그레이드/제거 시 | 필수: patch 호환성/endpoint-owner 조율/보존된 history 결정/client·route 폐기/명시적 데이터 삭제 승인 | 수동 | none |
| POL-0087-R20 | build 수용 시 | 필수: source commit/checksum/local patch/생성 image digest 확보 | none | source commit/checksum/image digest |
| POL-0087-R21 | 항상 | 금지: local tag만으로 패치 증명 | none | none |
| POL-0087-R22 | 항상 | 필수: Zero-fuzz/대소문자를 구분하는 정확한 subject/S256 PKCE/Secure·HttpOnly 임시 cookie/state·nonce 검사/CA 검증 유지 | none | none |
| POL-0087-R23 | 항상 | 필수: Public health/bootstrap/metrics와 보호 status API 구분 | none | none |
| POL-0087-R24 | Source/auth/storage 예외와 종료 시점 | 필수: @buenhyden이 승인 | 수동 | none |
| POL-0087-R25 | 항상 | 금지: 소스 문서 검사를 runtime 예외 부여로 간주 | none | none |

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

###### Lifecycle and data controls
<!-- core-payload-level:4 -->

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

##### Exceptions

###### Exception Conditions
<!-- core-payload-level:4 -->

예외는 owner, scope, risk, expiry, recovery condition이 필요하다.

###### Approval and Review
<!-- core-payload-level:4 -->

매월, 그리고 인증, probe inventory, 소스, storage가 변경될 때 검토한다.

#### Enforcement

##### Mechanisms

정적 소스와 catalog 검사는 선언만 검증한다. 컨테이너 health, native 로그인, 세션 만료,
probe 커버리지, backup, restore는 별도로 승인된 target이 필요한 런타임 증거로 남는다.

##### Limits

정책 본문이 이름 붙인 검사로 강제하는 규칙은 일부이며 아래 항목은 기계적으로 강제되지 않는다.

- Compose/보안 경계: `POL-0087-R1`, `POL-0087-R2`는 이름 붙은 검사가 지정되지 않았다.
- Compose/보안 경계: `POL-0087-R3`는 승인/검토 등 수동 절차에 의존한다.
- OIDC/metrics 경계: `POL-0087-R4`, `POL-0087-R5`, `POL-0087-R6`, `POL-0087-R8`는 이름 붙은 검사가 지정되지 않았다.
- OIDC/metrics 경계: `POL-0087-R7`는 승인/검토 등 수동 절차에 의존한다.
- 증거/수용: `POL-0087-R9`는 승인/검토 등 수동 절차에 의존한다.
- 증거/수용: `POL-0087-R10`는 이름 붙은 검사가 지정되지 않았다.
- 수명주기/데이터: `POL-0087-R11`, `POL-0087-R12`, `POL-0087-R15`, `POL-0087-R16`, `POL-0087-R18`는 이름 붙은 검사가 지정되지 않았다.
- 업그레이드: `POL-0087-R13`는 승인/검토 등 수동 절차에 의존한다.
- 업그레이드: `POL-0087-R14`는 이름 붙은 검사가 지정되지 않았다.
- 수명주기/데이터: `POL-0087-R17`, `POL-0087-R19`는 승인/검토 등 수동 절차에 의존한다.
- build 수용: `POL-0087-R20`, `POL-0087-R21`, `POL-0087-R22`, `POL-0087-R23`, `POL-0087-R25`는 이름 붙은 검사가 지정되지 않았다.
- build 수용: `POL-0087-R24`는 승인/검토 등 수동 절차에 의존한다.
- 정적 소스와 catalog 검사는 선언만 검증한다고 정책이 명시하며 컨테이너 health, native 로그인, 세션 만료, probe 커버리지, backup, restore는 별도 승인된 target의 런타임 증거가 필요하고 이 문서에는 없다.
- read-only root filesystem은 `read_only: false`라 2026-11-06 기준 미준수이며 owner 예외나 Compose 수정 전까지 열려 있다.
- `/metrics`는 내부 peer에게 인증 없이 열려 있으며 owner 수용(2026-11-07)에 의존한다.

#### Ownership

##### Owner

책임 소유자는 **@buenhyden**이다. 예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다. 통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

##### Review Triggers

- [Guide](../../01.guides/07.observability/0087-gatus.md), [Runbook](../../03.runbooks/07.observability/0087-gatus.md)
- [Gatus upstream security policy](https://github.com/TwiN/gatus/security/policy)
- 이 문서는 SPEC-0267 secondary-listener hardening 결과를 담고 있다. 해당 패키지는 retire되었고 본문은 version history에 있다.

## 적용과 확인

### 적용 방법

Use the procedures or reading order stated in the role payload.

### 확인 기준

Apply only this document's stated checks and limits; execution, verification and acceptance remain separate.

## 관계와 출처

### 관련 문서

The role payload retains the current owner and dependency references.

### 외부 근거

External basis and its limits remain those stated in the role payload; a citation grants no authority.
