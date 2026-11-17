---
title: "02-Auth OAuth2 Proxy Operations Policy"
version: "1.3.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
layer: "operations"
artifact_id: "POL-0015"
parent_ids:
- "AD-0002"
created: "2026-05-17"
next_review_at: "2027-05-13"
---

# 02-Auth OAuth2 Proxy Operations Policy

## Purpose and Scope

### Objective

이 문서는 `02-auth` OAuth2 Proxy 운영 정책을 정의한다. 시크릿 주입 경로, 세션/쿠키 표준, fail-closed 및 degraded-mode 운영 통제를 명시한다.

#### Authority

- Declared parent: [02-Auth Architecture Description](../../../02.architecture/descriptions/0002-auth-architecture.md) (`AD-0002`)

### Applies To

- `infra/02-auth/oauth2-proxy/docker-compose.yml`
- `infra/02-auth/oauth2-proxy/docker-entrypoint.sh`
- `infra/02-auth/oauth2-proxy/docker-entrypoint.dev.sh`
- `infra/02-auth/oauth2-proxy/Dockerfile`
- `infra/02-auth/oauth2-proxy/dev.Dockerfile`
- `infra/02-auth/oauth2-proxy/config/oauth2-proxy.cfg`

- **Systems**: OAuth2 Proxy ForwardAuth gateway
- **Environments**: Local, Dev, Stage, Production-like

#### Exclusions

Keycloak realm/client 운영은 [POL-0014](0014-keycloak.md)가 다룬다.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| POL-0015-R1 | 항상 | 필수: `check-all-hardening.sh 02-auth` 실패 0건을 유지한다 | `bash scripts/hardening/check-all-hardening.sh 02-auth` | none |
| POL-0015-R2 | 로그인 루프/콜백 실패 급증/`/ping` 실패 지속 시 | 필수: 런북 절차를 수행한다 | none | none |
| POL-0015-R3 | 서비스 | 필수: `template-infra-readonly-med`를 사용한다 | none | none |
| POL-0015-R4 | 세션 저장소 password | 필수: 엔트리포인트 스크립트가 `/run/secrets` 파일에서 주입한다 | none | none |
| POL-0015-R5 | client/cookie secret | 필수: cfg의 `*_secret_file`로 읽는다 | none | none |
| POL-0015-R6 | client secret | 허용: `OAUTH2_PROXY_CLIENT_SECRET_FILE`로 OpenBao Agent 출력(`/run/openbao/oauth2-proxy`)을 지정한다 | none | none |
| POL-0015-R7 | secret 값 | 금지: 환경 변수 리터럴로 둔다 | none | none |
| POL-0015-R8 | SSO route 통과 | 필수: Keycloak group `/admins`(`allowed_groups`)로 제한한다 | none | none |
| POL-0015-R9 | 신뢰 IP 설정 | 금지: `trusted_ips`를 둔다 | none | none |
| POL-0015-R10 | `trusted_proxy_ips` | 필수: Traefik `edge_net` 주소로 한정한다 | none | none |
| POL-0015-R11 | 세션 저장소 | 필수: 공유 `mng-valkey`를 쓴다 | none | none |
| POL-0015-R12 | 세션 저장소 | 금지: 앱별 전용 Valkey와 exporter를 둔다(ADR-0062 결정 10) | none | none |
| POL-0015-R13 | `OAUTH2_PROXY_VALKEY_HOST` | 필수: `mng-valkey`를 가리킨다 | none | none |
| POL-0015-R14 | 선택한 이미지의 entrypoint가 읽는 세션 시크릿 | 필수: 해당 저장소와 일치한다 | none | none |
| POL-0015-R15 | 이미지 실행 계정 | 필수: non-root다(`dev.Dockerfile`은 `oauth2proxy`/`Dockerfile`은 UID 100·GID 101) | none | none |
| POL-0015-R16 | 세션 정책 | 필수: `cookie_secure=true`/`cookie_httponly=true`/`cookie_samesite=lax`/`cookie_refresh=1h`/`cookie_expire=12h`를 유지한다 | none | none |
| POL-0015-R17 | 기본 운영 모드 | 필수: fail-closed다 | none | none |
| POL-0015-R18 | 운영 승인 하 | 허용: degraded-mode를 제한적으로 수행한다(원복 절차 필수) | 수동 | none |
| POL-0015-R19 | 환경별 도메인 변수 | 허용: `DEFAULT_URL`을 조정한다 | none | none |
| POL-0015-R20 | 상시 운영 | 금지: fail-open | none | none |
| POL-0015-R21 | 시크릿 | 금지: Compose/문서에 평문으로 저장한다 | none | none |
| POL-0015-R22 | Valkey AOF | 금지: 백업 대용으로 사용한다 | none | none |
| POL-0015-R23 | 세션 손실 시 | 필수: 재로그인 영향을 고지한다 | none | none |
| POL-0015-R24 | 공유 `mng-valkey` | 금지: Proxy 복구만을 위해 비우거나 삭제한다 | none | none |
| POL-0015-R25 | credential 노출 경계 | 금지: full `docker inspect`/`docker top`/process `ps`/`/proc/*/cmdline`·`environ`/원문 `.State.Health.Log`를 기록한다 | none | none |
| POL-0015-R26 | credential 노출 경계 | 필수: 서비스명/image identity/health 상태/재시작 횟수·시각처럼 허용된 필드만 사용한다 | none | none |
| POL-0015-R27 | 공통 자원 상한과 mount 적용 | 필수: [POL-0006](../01-common/0006-infrastructure-optimization-governance.md)을 적용한다 | none | none |
| POL-0015-R28 | profile/상호 배제 | 필수: [POL-0078](../01-common/0078-compose-profile-vocabulary.md)을 적용한다 | none | none |
| POL-0015-R29 | image 변경과 검토 | 필수: [POL-0086](../10-platform-and-backup/0086-dependency-version-management.md)을 적용한다 | none | none |
| POL-0015-R30 | 보존할 상태와 private credential | 필수: [POL-0021](../10-platform-and-backup/0021-backup-and-restore.md)의 접근/암호화/retention을 적용한다 | none | none |
| POL-0015-R31 | 제거 전 | 필수: 소비자와 복구 입력을 확인한다 | none | none |
| POL-0015-R32 | volume/인증서/secret 삭제 | 필수: 서비스 중지와 분리된 승인 대상으로 한다 | 수동 | none |
| POL-0015-R33 | Cookie/client/Valkey credential 값 | 필수: 각각의 secret 소유자가 관리한다 | none | none |
| POL-0015-R34 | credential 회전 | 필수: 모든 활성 session이 무효화되는지 명시한다 | 수동 | none |
| POL-0015-R35 | Session-store 내용 | 금지: 영속 business-data backup 대상으로 삼는다 | none | none |
| POL-0015-R36 | store 손실 후 | 필수: fail-closed와 재인증을 우선한다 | none | none |
| POL-0015-R37 | store 손실 후 | 금지: session을 유지하기 위해 cookie 보안을 약화한다 | none | none |
| POL-0015-R38 | upgrade | 필수: 격리된 OIDC/PKCE/ForwardAuth/logout test 후에만 수행한다 | none | none |
| POL-0015-R39 | upgrade | 필수: 이전 image 선언을 보존한다 | none | none |
| POL-0015-R40 | upgrade | 필수: session 무효화 계획을 기록한다 | none | none |

- **필수**:
  - `check-all-hardening.sh 02-auth` 실패 0건을 유지해야 한다.
  - 로그인 루프, 콜백 실패 급증, `/ping` 실패 지속 시 런북 절차를 수행해야 한다.
  - 서비스는 `template-infra-readonly-med`를 사용해야 한다.
  - 세션 저장소 password는 엔트리포인트 스크립트가 `/run/secrets` 파일에서 주입한다.
    client/cookie secret은 cfg의 `*_secret_file`로 읽고, client secret은
    `OAUTH2_PROXY_CLIENT_SECRET_FILE`로 OpenBao Agent 출력(`/run/openbao/oauth2-proxy`)을
    지정할 수 있다. 값을 환경 변수 리터럴로 두지 않는다.
  - SSO route 통과는 Keycloak group `/admins`(`allowed_groups`)로 제한하고,
    `trusted_ips`는 두지 않으며 `trusted_proxy_ips`는 Traefik `edge_net` 주소로 한정한다.
  - 세션 저장소는 공유 `mng-valkey`다. 앱별 전용 Valkey와 exporter는 ADR-0062 결정 10으로
    제거되었고, `OAUTH2_PROXY_VALKEY_HOST`는 `mng-valkey`를 가리켜야 한다. 선택한
    이미지의 entrypoint가 읽는 세션 시크릿도 해당 저장소와 일치해야 한다.
  - 이미지 실행 계정은 non-root여야 한다(`dev.Dockerfile`은 `oauth2proxy`, `Dockerfile`은 UID 100/GID 101).
  - 세션 정책은 `cookie_secure=true`, `cookie_httponly=true`, `cookie_samesite=lax`, `cookie_refresh=1h`, `cookie_expire=12h`를 유지한다.
  - 기본 운영 모드는 fail-closed다.
- **허용**:
  - 운영 승인 하에 degraded-mode를 제한적으로 수행(원복 절차 필수)
  - 환경별 도메인 변수(`DEFAULT_URL`) 조정
- **금지**:
  - fail-open 상시 운영
  - 시크릿을 Compose/문서에 평문으로 저장

#### Session boundaries

Valkey AOF는 세션 persistence이며 백업을 대신하지 않는다. 세션 손실 시 재로그인
영향을 고지하고 공유 `mng-valkey`를 Proxy 복구만을 위해 비우거나 삭제하지 않는다.

#### Credential exposure boundary

Proxy는 entrypoint가 Secret 파일에서 읽어 `OAUTH2_PROXY_REDIS_PASSWORD` 환경 변수로
password를 소비한다. Docker daemon/host process 접근도 credential 신뢰 경계다. full
`docker inspect`, `docker top`/process `ps`, `/proc/*/cmdline`·`environ`, 원문
`.State.Health.Log`는 기록하지 않는다. 서비스명·image identity·health 상태·재시작
횟수·시각처럼 허용된 필드만 사용한다. 실제 유출은 관찰하지 않았다.

#### Shared controls and accountability

공통 자원 상한과
mount 적용은 [POL-0006](../01-common/0006-infrastructure-optimization-governance.md), profile·
상호 배제는 [POL-0078](../01-common/0078-compose-profile-vocabulary.md), image 변경과 검토는
[POL-0086](../10-platform-and-backup/0086-dependency-version-management.md)을 적용한다. 보존할 상태와 private credential은 [POL-0021](../10-platform-and-backup/0021-backup-and-restore.md)의
접근·암호화·retention을 적용한다. 제거 전에 소비자와 복구 입력을 확인하고,
volume·인증서·secret 삭제는 서비스 중지와 분리된 승인 대상으로 한다.

#### Session and Upgrade Controls

- Cookie, client, Valkey credential 값은 각각의 secret 소유자가 관리한다.
  회전할 때는 모든 활성 session이 무효화되는지 명시해야 한다.
- Session-store 내용은 단기 인증 상태이며 영속 business-data backup 대상이 아니다.
  store 손실 후에는 fail-closed와 재인증을 우선하며, session을 유지하기 위해
  cookie 보안을 약화하지 않는다.
- 격리된 OIDC/PKCE/ForwardAuth/logout test 후에만 upgrade한다.
  이전 image 선언을 보존하고 session 무효화 계획을 기록한다.

### Exceptions

#### Exception Conditions

- OIDC 공급자 장애가 장기화될 때 한시적 degraded-mode 허용 가능.
- 단, 승인자 기록과 종료 조건(원복 기준)을 사전에 명시해야 한다.

#### Approval and Review

- 월 1회 정기 점검
- OAuth2 Proxy/Keycloak 버전 변경 시 수시 점검

- OOM·반복 재시작·인증 실패 증가 또는 이미지·노출·mount 변경 시 정기 주기를 기다리지 않고 검토한다.

## Enforcement

### Mechanisms

- `bash scripts/hardening/check-all-hardening.sh 02-auth`
- `HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh`
- `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh`
- Runtime-only: `docker compose --profile auth exec oauth2-proxy wget -qO- http://127.0.0.1:4180/ping`(기본 `OAUTH2_PROXY_PORT` 기준)

### Limits

이 정책은 아래 규칙에 대해 명명된 자동 검사를 연결하지 않거나 수동 검토에 맡긴다.

- hardening/대응: 명명된 검사 없음 R2 (`POL-0015-` 접두)
- 서비스 구성: 명명된 검사 없음 R3~R17 (`POL-0015-` 접두)
- 허용/금지: 명명된 검사 없음 R19~R21; 수동 검토 R18 (`POL-0015-` 접두)
- 세션/credential 경계: 명명된 검사 없음 R22~R26 (`POL-0015-` 접두)
- 공통 통제: 명명된 검사 없음 R27~R31; 수동 검토 R32 (`POL-0015-` 접두)
- 세션/업그레이드: 명명된 검사 없음 R33, R35~R40; 수동 검토 R34 (`POL-0015-` 접두)
- `/ping` runtime 점검(`docker compose --profile auth exec oauth2-proxy wget -qO- http://127.0.0.1:4180/ping`)은 runtime-only이며 어느 규칙을 검증하는지 본문이 연결하지 않는다(144행).

## Ownership

### Owner

운영 책임자는 @buenhyden이다. 변경·재시작·credential 작업의 대상과 영향, 승인,
종료 조건을 기록하며 예외는 위험·만료·원복 책임까지 명시한다.

### Review Triggers

- Subject peers: [Guide](../../guides/03-identity-and-access/0015-oauth2-proxy.md) (`GDE-0015`), [Runbook](../../runbooks/03-identity-and-access/0015-oauth2-proxy.md) (`RUN-0015`)

- 런타임 버전은 Compose/Dockerfile 선언이 소유하며, [파생 Compose 이미지 목록](../../../../infra/tech-stack.versions.json)은 drift 검증에 사용한다.

- [Operations index](../../README.md)
