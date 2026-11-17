---
title: "02-Auth Keycloak Operations Policy"
version: "1.3.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0014"
parent_ids:
- "AD-0002"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# 02-Auth Keycloak Operations Policy

## Purpose and Scope

### Objective

이 문서는 `02-auth` Keycloak 운영 정책을 정의한다. DB/관리자 시크릿 처리, readiness 검증, 변경 통제 기준을 명시한다.

#### Authority

- Declared parent: [02-Auth Architecture Description](../../../02.architecture/descriptions/0002-auth-architecture.md) (`AD-0002`)

### Applies To

- `infra/02-auth/keycloak/docker-compose.yml`
- Keycloak secret injection and healthcheck contract
- Realm/client 운영 변경 승인 정책

- **Systems**: Keycloak (Quarkus)
- **Environments**: Local, Dev, Stage, Production-like

#### Exclusions

OAuth2 Proxy ForwardAuth는 [POL-0015](0015-oauth2-proxy.md)가 다룬다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0014-R1 | 항상 | 필수: `check-all-hardening.sh 02-auth` 실패 0건을 유지한다 | `bash scripts/hardening/check-all-hardening.sh 02-auth` | 점검 출력 |
| POL-0014-R2 | readiness 실패 지속/로그인 실패 급증/realm 설정 오류 | 필수: 런북 절차를 수행한다 | 수동 | RUN-0014 |
| POL-0014-R3 | 항상 | 필수: Keycloak은 `template-infra-high`를 사용한다 | `HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh` | none |
| POL-0014-R4 | 비밀 주입 | 필수: DB 비밀은 `/run/secrets/keycloak_db_password`에서, Admin 비밀은 `KEYCLOAK_ADMIN_PASSWORD_FILE`이 가리키는 파일에서 읽어 환경 변수로 주입한다 | none | none |
| POL-0014-R5 | 항상 | 필수: readiness healthcheck(`/health/ready`)를 유지한다 | `bash scripts/hardening/check-all-hardening.sh 02-auth` | none |
| POL-0014-R6 | 디버그 출력 | 필수: 시크릿 길이/값 등 민감한 디버그 출력을 하지 않는다 | none | none |
| POL-0014-R7 | 기동 안정화 | 허용: healthcheck 타이밍을 조정한다 | none | none |
| POL-0014-R8 | 운영 승인 하 | 허용: realm/client 설정을 변경한다 | 수동 | none |
| POL-0014-R9 | 항상 | 금지: 시크릿 평문 하드코딩 | `bash scripts/hardening/check-all-hardening.sh 02-auth` | none |
| POL-0014-R10 | 항상 | 금지: 인증 우회 목적 설정 변경 | none | none |
| POL-0014-R11 | 백업 시 | 필수: `mng-pg`의 Keycloak database를 권위 백업으로 취급하고 realm export만으로 완전한 복구를 주장하지 않는다 | none | none |
| POL-0014-R12 | 일관된 export 필요 시 | 필수: 공식 offline 절차에 따라 모든 Keycloak node를 중지하며 실행 중 export를 database backup 대체물로 쓰지 않는다 | none | none |
| POL-0014-R13 | 백업 접근/비밀 보관 | 필수: 관리자 password, database password, client secret은 각 secret owner가 보관하고 값을 문서나 증거에 복사하지 않는다 | none | none |
| POL-0014-R14 | upgrade 전 | 필수: 복구 가능한 database backup을 확인하고 격리 복제본에서 migration과 대표 OIDC 흐름을 검증하며 rollback에는 이전 image와 이전 database가 함께 필요하다 | 수동 | none |

- **필수**:
  - `check-all-hardening.sh 02-auth` 실패 0건을 유지해야 한다.
  - readiness 실패 지속, 로그인 실패 급증, realm 설정 오류 시 런북 절차를 수행해야 한다.
  - Keycloak은 `template-infra-high`를 사용한다.
  - DB 비밀은 `/run/secrets/keycloak_db_password`에서, Admin 비밀은 `KEYCLOAK_ADMIN_PASSWORD_FILE`이 가리키는 파일(기본 `/run/secrets/keycloak_admin_password`, OpenBao 소비 시 `/run/openbao/auth` 아래 Agent 출력)에서 읽어 환경 변수로 주입한다.
  - readiness healthcheck(`/health/ready`)를 유지한다.
  - 시크릿 길이/값 등 민감한 디버그 출력은 금지한다.
- **허용**:
  - 기동 안정화를 위한 healthcheck 타이밍 조정
  - 운영 승인 하의 realm/client 설정 변경
- **금지**:
  - 시크릿 평문 하드코딩
  - 인증 우회 목적 설정 변경

#### Shared controls and accountability

공통 자원 상한과
mount 적용은 [POL-0006](../01-common/0006-infrastructure-optimization-governance.md), profile·
상호 배제는 [POL-0078](../01-common/0078-compose-profile-vocabulary.md), image 변경과 검토는
[POL-0086](../10-platform-and-backup/0086-dependency-version-management.md)을 적용한다. 보존할 상태와 private credential은 [POL-0021](../10-platform-and-backup/0021-backup-and-restore.md)의
접근·암호화·retention을 적용한다. 제거 전에 소비자와 복구 입력을 확인하고,
volume·인증서·secret 삭제는 서비스 중지와 분리된 승인 대상으로 한다.

#### Backup and Upgrade Controls

- `mng-pg`의 Keycloak database를 권위 백업으로 취급한다. realm export만으로
  사용자, 세션, 자격 증명, 실행 중 변경의 완전한 복구를 주장하지 않는다.
- 일관된 export가 필요하면 공식 offline 절차에 따라 모든 Keycloak node를
  중지한다. 실행 중 export를 database backup 대체물로 쓰지 않는다.
- 백업 접근, 관리자 password, database password, client secret은 각 secret
  owner가 보관하며 문서나 증거에 값을 복사하지 않는다.
- upgrade 전에 복구 가능한 database backup을 확인하고 격리 복제본에서 migration과
  대표 OIDC 흐름을 검증한다. rollback에는 이전 image와 이전 database가 함께 필요하다.

### Exceptions

#### Exception Conditions

- 긴급 장애 대응 시 임시 설정 변경은 가능하나, 동일 작업 윈도우 내 원복 계획과 변경 기록을 남겨야 한다.

#### Approval and Review

- 월 1회 정기 점검
- Keycloak 버전/realm 정책 변경 시 수시 점검

- OOM·반복 재시작·인증 실패 증가 또는 이미지·노출·mount 변경 시 정기 주기를 기다리지 않고 검토한다.

## Enforcement

### Mechanisms

- `bash scripts/hardening/check-all-hardening.sh 02-auth`
- `HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh`
- `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh`

### Limits

정책이 명명한 검사는 hardening 점검과 `auth`/`core` profile 정적 렌더링뿐이며 다음은 기계적으로 강제되지 않는다.

- readiness 실패, 로그인 실패 급증, realm 설정 오류 시의 런북 수행과 realm/client 변경 승인은 수동 판단이다.
- 시크릿 주입 경로, 민감 디버그 출력 금지, 평문 하드코딩 금지, 인증 우회 설정 금지에는 명명된 전용 검사가 없다.
- 백업/업그레이드 통제(DB 백업 확인, 격리 복제본 migration 검증, offline export, rollback 입력)는 검사 없이 수동 절차에 의존한다.
- 긴급 장애 시 임시 설정 변경의 원복 계획과 변경 기록은 수동이다.
- 월 1회 정기 점검과 수시 점검에는 명명된 자동 검사가 없다.

## Ownership

### Owner

운영 책임자는 @buenhyden이다. 변경·재시작·credential 작업의 대상과 영향, 승인,
종료 조건을 기록하며 예외는 위험·만료·원복 책임까지 명시한다.

### Review Triggers

- Subject peers: [Guide](../../guides/03-identity-and-access/0014-keycloak.md) (`GDE-0014`), [Runbook](../../runbooks/03-identity-and-access/0014-keycloak.md) (`RUN-0014`)

- [Official upstream operational documentation](https://www.keycloak.org/server/containers)

- 런타임 버전은 Compose/Dockerfile 선언이 소유하며, [파생 Compose 이미지 목록](../../../../infra/tech-stack.versions.json)은 drift 검증에 사용한다.

- [Operations index](../../README.md)
