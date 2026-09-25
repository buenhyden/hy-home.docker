---
title: "02-Auth OAuth2 Proxy Runbook"
version: "1.1.0"
type: "operation/runbook"
status: "active"
owner: "@buenhyden"
updated: "2026-09-22"
layer: "operations"
artifact_id: "RUN-0015"
parent_ids:
- "GDE-0015"
created: "2026-05-17"
---

# 02-Auth OAuth2 Proxy Runbook

## Overview

이 런북은 OAuth2 Proxy 인증 루프, OIDC 장애, CA/issuer/callback 불일치, Redis/Valkey session 장애, logout 경계 혼동, readonly/tmpfs 관련 오류, 설정 검증 실패 상황에 대한 복구 절차를 정의한다.

> Scope: OAuth2 Proxy ForwardAuth Recovery

### Purpose

- 인증 경로 장애를 신속히 복구한다.
- degraded-mode 수행/종료를 통제한다.
- config lint 실패 시 안전하게 롤백한다.

## When to Use

- 로그인 루프(무한 redirect)
- OIDC issuer 접근 실패
- callback `https://auth.${DEFAULT_URL}/oauth2/callback` 거부 또는 state/CSRF 오류
- Keycloak login 후 OAuth2 Proxy cookie/session 생성 실패
- logout 후 Keycloak SSO가 남아 즉시 재로그인되는 현상
- `/ping` healthcheck 실패
- readonly/tmpfs 관련 쓰기 오류
- compose/config 변경 후 런타임 부팅 실패

## Procedure

### Checklist

- [ ] `HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh` 성공
- [ ] `bash scripts/hardening/check-all-hardening.sh 02-auth` 실행
- [ ] `docker compose --profile auth logs oauth2-proxy --tail=200` 오류 패턴 확인

### Steps

1. 기본 진단
   - `/ping` 확인: `docker compose --profile auth exec oauth2-proxy wget -qO- http://127.0.0.1:4180/ping`
   - `/ready` 확인: `docker compose --profile auth exec oauth2-proxy wget -qO- http://127.0.0.1:4180/ready`
   - OIDC issuer 확인: `https://keycloak.${DEFAULT_URL}/realms/hy-home.realm`
   - 로그 확인: `docker compose --profile auth logs oauth2-proxy --tail=200`; 로컬 운영 화면 밖으로 공유하기 전에는 token, authorization code, session id, cookie, email, IP 등 식별자와 credential 후보를 redaction한다.
2. issuer/CA/JWKS 대응
   - tracked issuer는 `https://keycloak.${DEFAULT_URL}/realms/hy-home.realm`이다.
   - root CA mount는 `/etc/ssl/certs/rootCA.pem`, `SSL_CERT_FILE`과 `ssl_insecure_skip_verify=false`를 확인한다.
   - CA 오류를 `ssl_insecure_skip_verify=true`로 우회하지 않는다.
3. callback/state/PKCE 대응
   - Keycloak client `home-proxy-client`의 Valid Redirect URI가 `https://auth.${DEFAULT_URL}/oauth2/callback`인지 확인한다.
   - OAuth2 Proxy config의 `code_challenge_method = "S256"`와 Keycloak client flow가 호환되는지 확인한다.
   - state/CSRF 오류가 있으면 `cookie_domains=.${DEFAULT_URL}`, `cookie_secure=true`, HTTPS 진입, browser stale cookie를 함께 확인한다.
4. session store 대응
   - tracked default는 `OAUTH2_PROXY_SESSION_STORE_TYPE=redis`, `OAUTH2_PROXY_REDIS_CONNECTION_URL=redis://${OAUTH2_PROXY_VALKEY_HOST:-mng-valkey}:6379`이다.
   - shared path는 `mng-valkey`; `dedicated-valkey` profile은 `oauth2-proxy-valkey`를 추가할 뿐이다. 실제 proxy backend 전환은 `OAUTH2_PROXY_VALKEY_HOST`, selected image, entrypoint secret path가 함께 맞을 때만 성립한다.
   - `/ping`은 process health이고 `/ready`는 Redis/Valkey 연결까지 확인한다.
   - Valkey credential rotation 후 기존 sessions는 무효화될 수 있으며 secret 값은 출력하지 않는다.
5. logout 진단
   - `/oauth2/sign_out`만 호출하면 OAuth2 Proxy cookie만 제거된다.
   - Keycloak SSO까지 종료하려면 provider `end_session_endpoint`로 redirect해야 하며, `rd` 대상 domain이 `OAUTH2_PROXY_WHITELIST_DOMAINS=.${DEFAULT_URL}`에 맞아야 한다.
   - 현재 tracked config만으로 모든 app logout이 Keycloak SSO를 끝낸다고 기록하지 않는다.
6. 로그인 루프 대응
   - `OAUTH2_PROXY_COOKIE_DOMAINS`, `OAUTH2_PROXY_WHITELIST_DOMAINS`, `OAUTH2_PROXY_REDIRECT_URL` 정합성 확인
   - `reverse_proxy=true`, trusted proxy/header 설정을 검토한다. Forwarded header spoofing을 허용하는 네트워크 경로가 있으면 중단하고 gateway boundary를 먼저 고친다.
7. readonly/tmpfs 장애 복구
   - 쓰기 대상 경로가 `/tmp`, `/run` 내인지 점검
   - 엔트리포인트/인증서 마운트 경로 권한 확인
8. degraded-mode 절차(승인 필요)
   - OIDC 장기 장애 시 운영 승인 후 제한적 degraded-mode 적용
   - 적용 시간/범위/종료 조건을 티켓에 기록
   - Keycloak 정상화 즉시 기본 fail-closed로 복귀
9. config lint 실패 롤백
   - 직전 정상 커밋으로 compose/config 복원
   - 재기동 후 `/ping`, `/ready`, 인증 플로우 재검증

### Verification Steps

- [ ] `bash scripts/hardening/check-all-hardening.sh 02-auth` 통과
- [ ] `docker compose --profile auth exec oauth2-proxy wget -qO- http://127.0.0.1:4180/ping` 성공
- [ ] 인증 콜백(`/oauth2/callback`) 정상 동작
- [ ] `/ready`가 session store 연결까지 성공
- [ ] `/oauth2/sign_out`과 Keycloak end-session redirect의 효과를 구분해서 기록

### Observability and Evidence Sources

- **Signals**: `/ping`, oauth2-proxy 로그, Keycloak 연결 오류율
- **Evidence to Capture**:
  - `docker compose --profile auth logs oauth2-proxy --tail=200`
  - `docker compose --profile auth logs keycloak --tail=200`
  - check-all-hardening.sh 02-auth 출력

### Safe Rollback or Recovery Procedure

- [ ] 아래 파일을 직전 정상 커밋으로 복원
  - `infra/02-auth/oauth2-proxy/docker-compose.yml`
  - `infra/02-auth/oauth2-proxy/docker-entrypoint.sh`
  - `infra/02-auth/oauth2-proxy/docker-entrypoint.dev.sh`
  - `infra/02-auth/oauth2-proxy/Dockerfile`
  - `infra/02-auth/oauth2-proxy/dev.Dockerfile`
  - `infra/02-auth/oauth2-proxy/config/oauth2-proxy.cfg`
- [ ] `docker compose --profile auth up -d oauth2-proxy`
- [ ] `/ping` + 로그인 시나리오 재검증

### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: N/A
- **Eval Re-run**: `bash scripts/hardening/check-all-hardening.sh 02-auth`
- **Trace Capture**: oauth2-proxy/keycloak 로그 + CI job 로그

## Evidence

- Capture command output, timestamps, and operator or agent actions for any execution of this runbook.
- Record failed checks, observed symptoms, and the final recovery or escalation state in the related task or incident evidence.

### Shared Valkey outage rehearsal (2026-09-22, owner-approved)

`mng-valkey` was stopped for 68 seconds and recreated. Probes every five seconds:
unauthenticated SSO route 401, `/oauth2/start` 302 and `/ping` OK throughout;
oauth2-proxy logged no errors and did not restart. The Airflow Celery worker
logged connection errors and reconnected four seconds after Valkey returned
without a restart; n8n and its worker restarted twice and were healthy 37 seconds
after Valkey returned. Not measured: an existing authenticated session during
the outage, because oauth2-proxy rejects an unsigned cookie before it reaches
Valkey and no test credentials were used.

## Rollback or Recovery

If Valkey session state is lost or incompatible, keep ForwardAuth fail-closed,
restore the reviewed endpoint and credential references, then require users to
authenticate again. Do not restore stale sessions from an unknown point or expose
cookie/client secrets to preserve logins. If the cookie secret changed, explicitly
invalidate old cookies and test a fresh Keycloak login. The session-loss recovery
and upgrade rollback paths are planned and were not executed during the 2026-09-20
documentation correction.

## Escalation

Stop and escalate to the owning operator when verification fails, secret exposure risk appears, destructive data changes are required, or observed state diverges from expected procedure results. Include captured evidence, attempted steps, and current rollback/recovery state. Redact credentials, authorization codes, tokens, cookies, session identifiers, private IPs where necessary, and personal account details before evidence leaves the local operator context.

## Traceability

- Declared parent: [02-Auth OAuth2 Proxy Usage Guide](../guides/0015-oauth2-proxy.md) (`GDE-0015`)
- Governing authority: [02-Auth Architecture Description](../../02.architecture/descriptions/0002-auth-architecture.md) (`AD-0002`)
- Subject peers: [Guide](../guides/0015-oauth2-proxy.md) (`GDE-0015`), [Policy](../policies/0015-oauth2-proxy.md) (`POL-0015`)

## Related Documents

- [Official OAuth2 Proxy Keycloak OIDC provider](https://oauth2-proxy.github.io/oauth2-proxy/configuration/providers/keycloak_oidc/)
- [Official OAuth2 Proxy configuration overview](https://oauth2-proxy.github.io/oauth2-proxy/configuration/overview/)
- [Official OAuth2 Proxy session storage](https://oauth2-proxy.github.io/oauth2-proxy/configuration/session_storage/)
- [Official OAuth2 Proxy endpoints](https://oauth2-proxy.github.io/oauth2-proxy/features/endpoints/)

- Runtime pins: Compose/Dockerfile declarations are authoritative; the [derived Compose image projection](../../../infra/tech-stack.versions.json) provides drift verification.

- [Operations index](../README.md)
- [Usage guide](../guides/0015-oauth2-proxy.md)
- [Operations policy](../policies/0015-oauth2-proxy.md)
