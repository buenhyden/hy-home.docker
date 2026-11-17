---
title: "Superset Operations Policy"
version: "1.3.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0097"
parent_ids:
- "AD-0012"
created: "2026-09-23"
next_review_at: "2027-05-13"
---

# Superset Operations Policy

## Purpose and Scope

### Objective

Superset는 자체 로그인, 메타데이터 데이터베이스, lakehouse 데이터 접근
권한을 가진 독립 LAB 웹 애플리케이션이며 gateway route가 없다(SPEC-0262). 인증, role 부여, 자격 증명
처리가 통제 대상이다.

#### Authority

- [Application auth integration policy](../03-identity-and-access/0079-application-auth-integration.md)
- SPEC-0262 Analytics labs migration
- [Superset Compose source](../../../../labs/superset/docker-compose.yml) and [derived version projection](../../../../infra/tech-stack.versions.json)

### Applies To

선택, 로그인, role, secret, 메타데이터 데이터베이스, 데이터 연결, 업그레이드.

#### Exclusions

없음: 이 정책 본문에는 명시된 제외 대상이 없다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0097-R1 | 항상 | 필수: 독립 LAB `labs/superset/docker-compose.yml`의 `lab-superset` profile로만 선택한다 | none | none |
| POL-0097-R2 | 항상 | 금지: root include, HOME network 합류, HOME 이름 선택 추가 | none | none |
| POL-0097-R3 | 로그인 시 | 필수: PKCE를 사용하는 native Keycloak OIDC로 로그인한다 | none | none |
| POL-0097-R4 | 항상 | 금지: form 로그인 제공 | none | none |
| POL-0097-R5 | LAB loopback origin용 redirect URI 등록 시 | 필수: 소유자가 승인한 Keycloak client 변경으로만 등록한다 | 수동 | none |
| POL-0097-R6 | self-registration 시 | 필수: `Gamma`만 부여한다 | none | none |
| POL-0097-R7 | Admin/데이터 role 부여 시 | 필수: Admin이 이름이 명시된 Keycloak 사용자에게 부여한다 | 수동 | none |
| POL-0097-R8 | Admin/데이터 role 부여 시 | 필수: 누가 왜 부여했는지를 Task에 기록한다 | 수동 | Task 기록 |
| POL-0097-R9 | 항상 | 필수: signing key, 데이터베이스 비밀번호, client secret은 Docker secret 파일에서 가져온다 | none | none |
| POL-0097-R10 | 항상 | 금지: signing key/데이터베이스 비밀번호/client secret을 환경 변수, 명령줄 인자, 설정 안의 평문 URI로 둠 | 예행연습(컨테이너 환경 변수에 자격 증명이 없음 확인) | none |
| POL-0097-R11 | 항상 | 필수: 메타데이터 데이터베이스는 HOME `mng-pg`에서 feature-owned로 두고 LAB은 `LAB_SUPERSET_DB_HOST`/`LAB_SUPERSET_DB_PORT` 입력으로만 연결한다 | none | none |
| POL-0097-R12 | 소유자가 LAB에서 도달 가능한 endpoint를 승인하기 전 | 금지: `mng-pg`를 LAB network에 임의로 게시 | 수동 | none |
| POL-0097-R13 | 항상 | 필수: Superset app의 host port는 `LAB_HOST_BIND_IP`(기본 `127.0.0.1`)의 `LAB_SUPERSET_HOST_PORT`에만 허용한다 | none | none |
| POL-0097-R14 | loopback 밖 bind 시 | 필수: 별도 보안 검토를 거친다 | 수동 | none |
| POL-0097-R15 | UI에서 데이터 연결 추가 시 | 필수: 범위가 한정된 identity를 사용한다 | none | none |
| POL-0097-R16 | UI에서 추가한 데이터 연결 시 | 금지: 관리자 로그인 사용 | none | none |
| POL-0097-R17 | 항상 | 필수: 문서의 정적 검증과 runtime 운영 승인을 분리한다 | none | none |
| POL-0097-R18 | 항상 | 필수: `@buenhyden`이 named consumer/target/중단 영향/보존 기간/예외를 소유한다 | none | none |
| POL-0097-R19 | service image/profile/port/secret/mount, DDL/init, capacity 또는 backup 범위 변경 시 | 필수: 이 Policy와 linked Guide/Runbook을 함께 검토한다 | 수동 | none |
| POL-0097-R20 | engine secret/certificate 적용 시 | 필수: 이 subject의 credential 계약을 따른다 | none | none |
| POL-0097-R21 | 앱 인증 연동 시 | 필수: 적용되는 `POL-0079` 통제를 따른다 | none | none |
| POL-0097-R22 | source 반영/재기동 시 | 필수: `POL-0006`의 적용 통제를 따른다 | none | none |
| POL-0097-R23 | 보존/삭제 시 | 필수: `POL-0021`의 적용 통제를 따른다 | none | none |
| POL-0097-R24 | exporter/stateless job 적용 시 | 필수: database restore가 없더라도 설정/credential과 그 작업이 변경하는 upstream state를 통제 범위에 포함한다 | none | none |
| POL-0097-R25 | 소유 artifact/복구 지점/expiry가 불명확할 때 | 금지: 삭제/재생성 | none | none |
| POL-0097-R26 | 항상 | 금지: 기존 Exceptions 외의 새 예외를 승인된 것으로 간주 | none | none |

- 독립 LAB `labs/superset/docker-compose.yml`의 `lab-superset` profile로만 선택한다. root include, HOME network
  합류, HOME 이름 선택 추가를 금지한다.
- 로그인은 PKCE를 사용하는 native Keycloak OIDC다. gateway route가 없으므로 OAuth2 Proxy
  ForwardAuth도 적용되지 않으며 form 로그인은 제공하지 않는다. LAB loopback origin용 redirect
  URI는 소유자가 승인한 Keycloak client 변경으로만 등록한다(미결정, 별도 승인).
- self-registration은 `Gamma`만 부여한다. Admin과 데이터 role은 Admin이
  이름이 명시된 Keycloak 사용자에게 부여하며, 누가 왜 부여했는지를 Task에
  기록한다.
- signing key, 데이터베이스 비밀번호, client secret은 Docker secret 파일에서
  가져온다. 어느 것도 환경 변수, 명령줄 인자, 설정 안의 평문 URI로 두지
  않는다.
- 메타데이터 데이터베이스는 HOME `mng-pg`에서 feature-owned로 존재하며 LAB은
  `LAB_SUPERSET_DB_HOST`/`LAB_SUPERSET_DB_PORT` 입력으로만 연결한다. 소유자가 LAB에서 도달 가능한
  endpoint를 승인하기 전까지 mng-pg를 LAB network에 임의로 게시하지 않는다(미결정, 별도 승인).
  Superset app의 host port는 `LAB_HOST_BIND_IP`(기본 `127.0.0.1`)의 `LAB_SUPERSET_HOST_PORT`에만
  허용하며 loopback 밖 bind는 별도 보안 검토가 필요하다.
- UI에서 추가한 데이터 연결은 범위가 한정된 identity를 사용한다. 어떤
  것도 관리자 로그인을 쓰지 않는다.

#### Accountable lifecycle boundary

적용 identity: `superset-db-provision`, `superset-init`, `superset`. 문서의 정적 검증과 runtime 운영 승인을 분리한다. @buenhyden이 named consumer·target·중단 영향·보존 기간과 예외를 소유한다. service image/profile/port/secret/mount, DDL·init, capacity 또는 backup 범위 변경 시 이 Policy와 linked Guide/Runbook을 함께 검토한다. engine secret/certificate는 이 subject의 credential 계약을, 앱 인증 연동은 적용되는 [POL-0079](../03-identity-and-access/0079-application-auth-integration.md)를, source 반영·재기동은 [POL-0006](../01-common/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary), 보존·삭제는 [POL-0021](../10-platform-and-backup/0021-backup-and-restore.md)의 적용 통제를 따른다. exporter와 stateless job 자체에는 database restore가 없지만 설정·credential와 그 작업이 변경하는 upstream state는 제외되지 않는다. 소유 artifact·복구 지점·expiry가 불명확하면 삭제/재생성을 중단한다. 기존 Exceptions 외의 새 예외는 승인된 것으로 간주하지 않는다.

### Exceptions

#### Exception Conditions

없음. Superset는 native OIDC를 사용하므로 OAuth2 Proxy `/admins` allowlist는
적용되지 않는다. 어떤 realm 사용자든 `Gamma`(데이터 접근 없음)로 로그인할
수 있고 Admin이 role을 부여한다. 소유자는 realm이 사용자 한 명뿐인
2026-09-24 시점에 이를 유지하기로 했다.

#### Approval and Review

Superset 또는 Flask-AppBuilder 업그레이드, Keycloak client 변경, 새 데이터
연결이 생길 때마다 검토한다.

## Enforcement

### Mechanisms

LAB Compose 렌더링과 `tests.validation.test_lab_isolation`, hardening 고정값, 그리고 예행연습: 프로비저닝, idempotent
마이그레이션, 등록된 `lakehouse` 데이터베이스, `/health`, 익명 API `401`,
Keycloak 로그인 옵션, 컨테이너 환경 변수에 자격 증명이 없음.

### Limits

정책은 LAB Compose 렌더링, `tests.validation.test_lab_isolation`, hardening 고정값, 예행연습 중 환경 변수 자격 증명 점검만 규칙(`POL-0097-R10`)과 연결하며, 아래 규칙은 승인/검토에 의존하거나 강제 수단이 없다.

- 격리: 강제 수단 없음 `POL-0097-R1`~`R2`
- 인증/role: 수동 검토 `POL-0097-R5`, `POL-0097-R7`~`R8`; 강제 수단 없음 `POL-0097-R3`~`R4`, `POL-0097-R6`
- secret: 강제 수단 없음 `POL-0097-R9`
- DB/노출: 수동 검토 `POL-0097-R12`, `POL-0097-R14`; 강제 수단 없음 `POL-0097-R11`, `POL-0097-R13`
- 데이터 연결: 강제 수단 없음 `POL-0097-R15`~`R16`
- 책임/수명주기 경계: 수동 검토 `POL-0097-R19`; 강제 수단 없음 `POL-0097-R17`~`R18`, `POL-0097-R20`~`R26`
- Keycloak client redirect URI 등록과 `mng-pg` endpoint 승인은 미결정이다.
- Admin/데이터 role 부여 기록은 Task에 의존하는 수동 항목이다.
- UI에서 추가한 데이터 연결의 범위 한정 identity 사용은 이름 붙은 검사가 없다.
- 어떤 realm 사용자든 `Gamma`로 로그인할 수 있는 것은 owner가 유지하기로 한 예외다.

## Ownership

### Owner

이 정책의 소유자는 frontmatter의 `owner`인 `@buenhyden`이다.

### Review Triggers

- [가이드](../../guides/15-labs/0097-superset.md) (`GDE-0097`)
- [런북](../../runbooks/15-labs/0097-superset.md) (`RUN-0097`)
- [Compose profile vocabulary](../01-common/0078-compose-profile-vocabulary.md)
