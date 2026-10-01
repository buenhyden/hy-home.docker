---
title: "02-Auth Keycloak Runbook"
version: "1.3.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "RUN-0014"
parent_ids:
- "GDE-0014"
created: "2026-05-17"
---

# 02-Auth Keycloak Runbook

## Overview

이 런북은 Keycloak readiness 실패, DB 연결 오류, issuer/redirect 불일치, proxy header 오류, 시크릿 회전 후 인증 장애 상황의 복구 절차를 정의한다. 값이 필요한 점검은 secret 값을 출력하지 않는 방식으로만 수행한다.

> Scope: Keycloak Runtime Recovery and OIDC Issuer Diagnostics

### Purpose

- Keycloak 가용성을 빠르게 복구한다.
- issuer, redirect URI, proxy header, CA trust 불일치를 안전하게 좁힌다.
- 시크릿/설정 회귀 시 안전하게 롤백한다.

## When to Use

- `/health/ready` 실패 지속
- DB 인증 오류 또는 연결 오류
- 관리자/DB 비밀 회전 직후 로그인 실패
- OAuth2 Proxy 또는 native OIDC client의 `invalid_redirect_uri`, issuer mismatch, JWKS fetch 실패
- logout 후 즉시 재로그인되는 세션 경계 문제
- token, session, client secret 노출 후 폐기가 필요할 때

## Procedure

### Target, approval and safe evidence

저장소 루트의 승인된 Docker context에서 아래에 명시한 서비스만 다룬다.
명령이 runtime을 변경하는 단계는 대상, 영향받는 사용자·소비자, 이전 image/config,
중단 조건이 확인된 별도 승인 뒤에만 수행한다. 원문 로그나 전체 환경·inspect는
출력하지 않는다. 필요한 오류 유형과 횟수는 승인된 운영자가 로컬에서 정제해 전달하며
token, code, cookie, session ID, 사용자·비공개 주소를 증거에서 제외한다.
여러 앱 공통 장애는 [RUN-0099](0099-system-operations.md), cold-start는
[RUN-0098](0098-cold-start-and-reboot.md)이 소유한다.

### Checklist

- [ ] `HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh` 성공
- [ ] `bash scripts/hardening/check-all-hardening.sh 02-auth` 결과 확인
- [ ] 승인된 `docker compose ps keycloak mng-pg`에서 `keycloak`, `mng-pg` 상태 확인

### Steps

1. 설정/로그 확인
   - Keycloak의 정제된 DB/OIDC 오류 요약
   - `HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh`
   - 로그에 DB 인증 실패, hostname/proxy warning, invalid redirect URI, certificate/JWKS 오류가 있는지 분리한다. 로컬 운영 화면 밖으로 공유하기 전에는 token, authorization code, session id, cookie, email, IP 등 식별자와 credential 후보를 redaction한다.
2. readiness 실패 대응
   - DB 연결 상태 확인(`mng-pg` 로그/상태)
   - 기동·설정 반영은 아래 Lifecycle and configuration changes의 승인된 대상 절차 사용
   - management port `/health/ready` success를 확인하되, 이것을 user login acceptance로 기록하지 않는다.
3. issuer와 discovery 확인
   - browser 기준 issuer는 `https://keycloak.${DEFAULT_URL}/realms/hy-home.realm`이어야 한다.
   - 현재 HOME 구성에서는 `.well-known/openid-configuration`의 issuer, authorization endpoint, token endpoint, JWKS URI가 `https://keycloak.${DEFAULT_URL}` public hostname을 가리켜야 한다. 이것은 현재 구성의 요구사항이며 모든 OIDC 배포의 일반 규칙은 아니다.
   - discovery URL이 내부 host, wrong scheme, wrong port를 반환하면 `KC_HOSTNAME`, `KC_PROXY_HEADERS`, Traefik forwarded header 처리를 먼저 점검한다.
4. redirect/client 진단
   - OAuth2 Proxy callback은 `https://auth.${DEFAULT_URL}/oauth2/callback`이다.
   - OpenBao native OIDC callback은 OpenBao의 `/ui/vault/auth/{path}/oidc/callback` 형태이며 OAuth2 Proxy callback이 아니다.
   - Keycloak client의 Valid Redirect URI와 Web Origins를 실제 client 목적에 맞게 구분한다.
5. CA/issuer/token 진단
   - OAuth2 Proxy는 tracked config에서 `SSL_CERT_FILE=/etc/ssl/certs/rootCA.pem`, `ssl_insecure_skip_verify=false`를 사용한다.
   - CA trust 오류가 있으면 root CA mount와 certificate chain을 확인한다. `ssl_insecure_skip_verify=true`로 우회하지 않는다.
   - Token, authorization code, client secret, admin password 값은 출력하지 않는다.
6. 시크릿 회전 장애 대응
   - `/run/secrets/keycloak_admin_password`, `/run/secrets/keycloak_db_password` 파일 존재와 mount 상태 확인
   - secret 값은 출력하지 않고 환경 변수/secret 파일 매핑 오타, rotation timestamp, 관련 서비스 재시작 여부 점검
7. 로그아웃 경계 확인
   - Keycloak은 OIDC logout endpoint를 제공하지만, OAuth2 Proxy `/oauth2/sign_out`만 호출하면 provider session은 남을 수 있다.
   - Keycloak SSO까지 끝내야 하는 UX라면 OAuth2 Proxy runbook의 provider end-session redirect 조건과 whitelist를 함께 확인한다.
8. 노출된 token/session 폐기
   - 무엇이 노출됐는지 먼저 나눈다. Keycloak SSO session과 그에 묶인
     refresh token, 이미 발급된 access token, client secret은 여기서 다룬다.
     Airflow 자체 JWT는 [RUN-0050](0050-airflow.md#시나리오-4-노출된-airflow-tokensession-폐기),
     OAuth2 Proxy cookie와 session store는
     [GDE-0015](../guides/0015-oauth2-proxy.md)가 다룬다.
   - 한 사용자의 session: Admin Console `Users` → 사용자 → `Sessions`에서
     sign out하거나 `POST /admin/realms/hy-home.realm/users/{user-id}/logout`을
     호출한다. session 하나만 끝내려면
     `DELETE /admin/realms/hy-home.realm/sessions/{session}`을 쓰고, offline
     session이면 `?isOffline=true`를 붙인다.
   - realm 전체: Admin Console `Sessions`의 `Sign out all active sessions` 또는
     `POST /admin/realms/hy-home.realm/logout-all`. 모든 사용자가 다시
     로그인해야 한다.
   - refresh token 하나: 그 token을 가진 client가
     `POST /realms/hy-home.realm/protocol/openid-connect/revoke`(RFC 7009)를
     호출한다.
   - session이 끝나면 거기에 묶인 refresh token으로는 갱신할 수 없다. 이미
     발급된 access token은 서명만 검증하는 쪽에서 realm의 access token
     수명이 끝날 때까지 유효할 수 있다. client `Advanced` 탭 `Revocation`의
     `Set to now`로 not-before를 올리고 `Push`
     (`POST /admin/realms/hy-home.realm/clients/{client-uuid}/push-revocation`)
     하면 admin URL이 설정된 client만 통보받는다. admin URL이 없는 client는
     만료를 기다리거나 앱 쪽 session을 따로 폐기한다.
   - client secret 노출: client `Credentials` 탭의 `Regenerate` 또는
     `POST /admin/realms/hy-home.realm/clients/{client-uuid}/client-secret`으로
     새 secret을 만든다. 새 값은 출력하지 않고 해당 secret 파일(예:
     `secrets/auth/airflow_client_secret.txt`)을 기존 소유자와 mode로
     교체한 뒤, 그 secret을 읽는 서비스만 재생성한다. 파일을 교체하기 전까지
     서비스는 로그인 code를 token으로 교환하지 못한다.
   - Admin REST 호출에 쓰는 admin token도 출력하거나 기록하지 않는다.
     증거는 HTTP 상태 코드, 시각, 남은 session 수만 남긴다.
9. 사후 검증
   - readiness 재확인
   - OAuth2 Proxy login/logout 플로우와 해당 native OIDC client login을 각각 별도 증거로 기록한다.

### Lifecycle and configuration changes

`keycloak`의 DB인 `mng-pg`가 먼저 준비되어야 하지만 Compose startup edge는 없다.
기존 로컬 image, DB schema 호환성, conf/providers/themes mount와 두 Secret 참조를
확인한다. 첫 기동은 bootstrap admin을 설정할 수 있으나 기존 realm/client를
자동 provision하거나 기존 관리자 password를 바꾸지 않는다.

```bash
# 승인된 기존 이미지의 대상 기동; DB를 자동 기동하지 않는다.
docker compose --profile auth up -d --no-deps --no-build --pull never keycloak
# 승인된 유지보수 중지; 전체 realm 로그인에 영향을 준다.
docker compose stop keycloak
```

설정·Secret 파일 교체는 [POL-0006](../policies/0006-infrastructure-optimization-governance.md#source-and-lifecycle-boundary)의
재생성·hash 점검을 따른다. 대상 명령은
`docker compose --profile auth up -d --no-deps --no-build --pull never --force-recreate keycloak`이다.
일상적인 process restart와 DB restore는 다르다. startup/readiness 실패이면 추가
migration/재시작을 반복하지 말고 DB/host/config 문제를 먼저 분류한다.

이미지 upgrade는 [RUN-0086](0086-dependency-version-management.md)에서 시작하며
[POL-0021](../policies/0021-backup-and-restore.md)의 DB와 private theme/provider/conf
backup 쌍을 요구한다. 지원되는 격리 DB 복구 입력·custody·검증 계획이 없으면
stateful recovery는 BLOCKED다. 여기에는 검증된 자동 realm provisioning이나 DB
restore 명령이 없으며 @buenhyden과 DB owner가 별도 복구 계약을 준비한다.

### Application authorization provisioning

Airflow Keycloak Auth Manager bootstrap은 Keycloak client와 realm role
`Viewer`, `User`, `Op`, `Admin`, `SuperAdmin`을 먼저 준비하고, 승인된
`airflow-apiserver`와 관리자 인증의 숨겨진 password prompt를 사용한다.
Keycloak Authorization Services 변경과 Airflow 영향을 함께 승인받는다.
명령의 `keycloak_admin`은 예시 계정명이므로 승인된 실제 관리자 이름으로 바꾼다.
실제 설치 provider를 [Airflow build](../../../infra/07-workflow/airflow/Dockerfile)와
실행 증거로 대조한 뒤 다음을 사용한다.

```bash
docker compose exec airflow-apiserver airflow keycloak-auth-manager create-all --username keycloak_admin --user-realm master --password
```

기대 결과는 HTTP method/menu/list scope, Dag/Asset/Pool/View resource, role policy와
permission 생성이다. `invalid_scope` 또는 realm-role404이면 중단하고 선행 입력을
확인한다. provider0.9.0 경계에서는 기존 non-team permission 재생성이 필요하다. <!-- runtime-version-exception: compatibility — preserves the existing Airflow provider migration boundary, not a current installed-version claim -->

```bash
docker compose exec airflow-apiserver airflow keycloak-auth-manager create-permissions --username keycloak_admin --user-realm master --password
```

provider 설치만으로 저장된 permission이 바뀌지 않는다. 실패 시 임의 realm 전체
초기화는 금지하며 변경 전 client/권한 복구 자료로 owner가 복원 범위를 정한다.
CLI는 사용자에게 realm role을 배정하지 않으므로 의도한 사용자에게 역할을 별도로
부여하고 최소 권한을 검증한다. 근거는 선언 provider의
[권한 관리 문서](https://raw.githubusercontent.com/apache/airflow/providers-keycloak/0.9.0/providers/keycloak/docs/auth-manager/manage/permissions.rst)와 <!-- runtime-version-exception: compatibility — official evidence pinned to the declared release; not an installed runtime observation -->
[CLI 정의](https://raw.githubusercontent.com/apache/airflow/providers-keycloak/0.9.0/providers/keycloak/src/airflow/providers/keycloak/cli/definition.py)다. <!-- runtime-version-exception: compatibility — official evidence pinned to the declared release; not an installed runtime observation -->
Compose의 명시적 build args가 Dockerfile 기본값보다 우선하며 현재 source 조합의
설치 성공은 관찰하지 않았다. 로그인 성공 외에 Pool/DAG/Asset별 허용·거부를 확인하고
[Airflow Runbook](0050-airflow.md)으로 후속 앱 검증을 전달한다.

### Verification Steps

- [ ] `bash scripts/hardening/check-all-hardening.sh 02-auth` 통과
- [ ] `docker compose --profile auth exec keycloak bash -ec 'exec 3<>/dev/tcp/127.0.0.1/9000; printf "GET /health/ready HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n" >&3; cat <&3'`에서 공백과 무관하게 status가 UP인지 확인(기본9000 기준; listener 변경 시 승인된 관리 포트와 함께 조정)

### Observability and Evidence Sources

- **Signals**: readiness 상태, Keycloak 로그의 DB/OIDC 오류
- **Evidence to Capture**:
  - Keycloak의 정제된 DB/OIDC 오류 요약
  - `check-all-hardening.sh 02-auth` 실행 결과

### Safe Rollback or Recovery Procedure

- [ ] 쓰기 중단 시점을 기록하고 Keycloak을 중지한 뒤 database owner가 검증한
      `mng-pg` Keycloak database 백업을 새 격리 database로 복원한다.
- [ ] 복구 시점과 일치하는 image/config declaration 및 secret references로
      격리 Keycloak을 연결한다. 운영 database 위에 import하지 않는다.
- [ ] realm/client/user 수, 관리자 로그인, issuer/discovery, OAuth2 Proxy,
      대표 native OIDC client를 확인하고 기존 token/session을 재사용하지 않는다.
- [ ] 승인 후에만 운영 endpoint를 전환한다. 실패하면 격리 복구본을 보존하고
      기존 환경을 변경하지 않은 채 database owner에게 인계한다.

## Evidence

- 원문을 제외한 명령 종료 상태·시각·승인 대상·조치와 미검증 항목만 기록한다.
- 실패한 점검, 관찰된 증상과 최종 복구 또는 에스컬레이션 상태를 관련 Task나 incident evidence에 기록한다.

## Rollback or Recovery

Realm export는 database backup을 대신하지 않는다. 공식 절차는 일관성을 위해
모든 Keycloak node를 중지한 export를 권장한다. 업그레이드 rollback에는 이전
image와 migration 전 database 복원이 함께 필요하다. 위 격리 복구 절차는 계획된
절차이며 2026-09-20 문서 교정 중 실행되지 않았다.

## Escalation

검증 실패, secret 노출 위험, 파괴적인 data 변경 필요, 또는 예상한 절차 결과와 관찰 상태의 불일치가 나타나면 중단하고 @buenhyden에게 에스컬레이션한다. 수집한 evidence, 시도한 단계와 현재 rollback/recovery 상태를 포함한다. evidence가 local 운영자 환경을 벗어나기 전에 credential, authorization code, token, cookie, session identifier, 필요한 경우 private IP, 개인 account 정보를 가린다.

## Traceability

- Declared parent: [02-Auth Keycloak Usage Guide](../guides/0014-keycloak.md) (`GDE-0014`)
- Governing authority: [02-Auth Architecture Description](../../02.architecture/descriptions/0002-auth-architecture.md) (`AD-0002`)
- Subject peers: [Guide](../guides/0014-keycloak.md) (`GDE-0014`), [Policy](../policies/0014-keycloak.md) (`POL-0014`)

## Related Documents

- [Official Keycloak container guide](https://www.keycloak.org/server/containers)
- [Official Keycloak hostname guide](https://www.keycloak.org/server/hostname)
- [Official Keycloak reverse proxy guide](https://www.keycloak.org/server/reverseproxy)
- [Official Keycloak health checks](https://www.keycloak.org/observability/health)
- [Official Keycloak OIDC application guide](https://www.keycloak.org/securing-apps/oidc-layers)
- [Official Keycloak import and export](https://www.keycloak.org/server/importExport)
- [Official Keycloak upgrading guide](https://www.keycloak.org/docs/latest/upgrading/index.html)
- [Official Keycloak server administration guide](https://www.keycloak.org/docs/latest/server_admin/index.html)
- [Official Keycloak Admin REST API](https://www.keycloak.org/docs-api/latest/rest-api/index.html)

- 런타임 버전은 Compose/Dockerfile 선언이 소유하며, [파생 Compose 이미지 목록](../../../infra/tech-stack.versions.json)은 drift 검증에 사용한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0014-keycloak.md)
- [Operations policy](../policies/0014-keycloak.md)
