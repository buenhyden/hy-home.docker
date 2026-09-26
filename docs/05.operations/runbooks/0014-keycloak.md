---
title: "02-Auth Keycloak Runbook"
version: "1.2.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
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

### Checklist

- [ ] `HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh` 성공
- [ ] `bash scripts/hardening/check-all-hardening.sh 02-auth` 결과 확인
- [ ] `docker compose ps`에서 `keycloak`, `mng-pg` 상태 확인

### Steps

1. 설정/로그 확인
   - `docker compose --profile auth logs keycloak --tail=200`
   - `HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh`
   - 로그에 DB 인증 실패, hostname/proxy warning, invalid redirect URI, certificate/JWKS 오류가 있는지 분리한다. 로컬 운영 화면 밖으로 공유하기 전에는 token, authorization code, session id, cookie, email, IP 등 식별자와 credential 후보를 redaction한다.
2. readiness 실패 대응
   - DB 연결 상태 확인(`mng-pg` 로그/상태)
   - Keycloak 재기동: `docker compose --profile auth up -d keycloak`
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

### Verification Steps

- [ ] `bash scripts/hardening/check-all-hardening.sh 02-auth` 통과
- [ ] `docker compose --profile auth exec keycloak sh -c 'exec 3<>/dev/tcp/127.0.0.1/9000; printf "GET /health/ready HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n" >&3; cat <&3'`에서 `"status":"UP"` 확인

### Observability and Evidence Sources

- **Signals**: readiness 상태, Keycloak 로그의 DB/OIDC 오류
- **Evidence to Capture**:
  - `docker compose --profile auth logs keycloak --tail=200`
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

- Capture command output, timestamps, and operator or agent actions for any execution of this runbook.
- Record failed checks, observed symptoms, and the final recovery or escalation state in the related task or incident evidence.

## Rollback or Recovery

Realm export는 database backup을 대신하지 않는다. 공식 절차는 일관성을 위해
모든 Keycloak node를 중지한 export를 권장한다. 업그레이드 rollback에는 이전
image와 migration 전 database 복원이 함께 필요하다. 위 격리 복구 절차는 계획된
절차이며 2026-09-20 문서 교정 중 실행되지 않았다.

## Escalation

Stop and escalate to the owning operator when verification fails, secret exposure risk appears, destructive data changes are required, or observed state diverges from expected procedure results. Include captured evidence, attempted steps, and current rollback/recovery state. Redact credentials, authorization codes, tokens, cookies, session identifiers, private IPs where necessary, and personal account details before evidence leaves the local operator context.

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

- Runtime pins: Compose/Dockerfile declarations are authoritative; the [derived Compose image projection](../../../infra/tech-stack.versions.json) provides drift verification.

- [Operations index](../README.md)
- [Usage guide](../guides/0014-keycloak.md)
- [Operations policy](../policies/0014-keycloak.md)
