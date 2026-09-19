---
title: "02-Auth OAuth2 Proxy Usage Guide"
version: "1.1.0"
type: "operation/guide"
status: "active"
owner: "@buenhyden"
updated: "2026-09-19"
layer: "operations"
artifact_id: "GDE-0015"
parent_ids:
- "POL-0015"
implementation_services:
  infra/02-auth/oauth2-proxy/docker-compose.yml:
  - oauth2-proxy
  - oauth2-proxy-valkey
  - oauth2-proxy-valkey-exporter
created: "2026-05-10"
---

# 02-Auth OAuth2 Proxy Usage Guide

## Usage

### Implementation Sources

- [infra/02-auth/oauth2-proxy/docker-compose.yml](../../../../../infra/02-auth/oauth2-proxy/docker-compose.yml)

`oauth2-proxy-valkey-exporter` exposes the OAuth2 session-store metrics; its activation follows the authored Compose profiles.

### Overview

이 문서는 OAuth2 Proxy를 Traefik `ForwardAuth` 표준으로 운영하는 방법을 설명한다. `oauth2-proxy`의 lifecycle class는 **HOME**이고, `oauth2-proxy-valkey`와 `oauth2-proxy-valkey-exporter` helper의 class는 **OPTIONAL**이다. Keycloak OIDC provider, redis/Valkey session storage, cookie와 token의 차이, callback/logout 경계를 함께 다룬다. 이 문서의 구성값은 tracked source 기준이며, 현재 실측으로 완료된 OIDC 로그인은 OpenBao native OIDC뿐이다. OAuth2 Proxy 전체 login/logout acceptance는 별도 런북 증거가 필요하다.

### Usage Type

`system-guide | how-to`

### Target Audience

- Infra/DevOps Engineers
- Operators
- Contributors

### Purpose

- 인증 프록시를 표준 하드닝 상태로 유지한다.
- 신규 서비스의 gateway SSO 연동 시 issuer, callback, cookie, session 회귀를 줄인다.
- OAuth2 Proxy session logout과 Keycloak SSO logout을 구분한다.

### Prerequisites

- `infra/02-auth/keycloak` 정상 동작
- `infra/02-auth/oauth2-proxy` 구성 파일 접근
- 공유 `mng-valkey` 또는 `dedicated-valkey` profile의 `oauth2-proxy-valkey` 세션 저장소 준비
- 사용할 저장소에 맞는 `OAUTH2_PROXY_VALKEY_HOST` 및 이미지/entrypoint의 세션 시크릿
  경로 확인. Profile은 서비스를 추가할 뿐 Proxy의 기본 호스트나 이미지를 전환하지 않는다.
  공유 경로는 `dev.Dockerfile`/`docker-entrypoint.dev.sh`의 `mng_valkey_password`,
  전용 경로는 `Dockerfile`/`docker-entrypoint.sh`의 `oauth2_valkey_password`를 사용한다.
  이미지 선택은 기존 `OAUTH2_PROXY_DOCKERFILE` 구성에 따른다.

### Tracked Configuration Snapshot

| Item | Tracked value | Source |
| --- | --- | --- |
| Provider | `keycloak-oidc` | `config/oauth2-proxy.cfg` |
| Client ID | `home-proxy-client` from `OAUTH2_PROXY_CLIENT_ID` | `.env.example`, compose env |
| Issuer | `https://keycloak.${DEFAULT_URL}/realms/hy-home.realm` | compose env |
| Redirect URL | `https://auth.${DEFAULT_URL}/oauth2/callback` | compose env |
| Cookie domain | `.${DEFAULT_URL}`; public default domain is `hy.home.arpa` | compose env |
| Cookie name | `__Secure-sso-cookie` | config file |
| Cookie lifetime | refresh `1h`, expire `12h` | config file |
| Session store | `redis` protocol against Valkey | compose env and official session-storage docs |
| Session backend | `mng-valkey` by default; `dedicated-valkey` only adds `oauth2-proxy-valkey` and its exporter | compose env/profile |
| Provider CA | `/etc/ssl/certs/rootCA.pem`, `ssl_insecure_skip_verify=false` | compose env/config file |
| Callback route | `Host(auth.${DEFAULT_URL}) && PathPrefix(/oauth2)` | Traefik labels |

### Cookie, Token, and Session Distinctions

OAuth2 Proxy uses a browser cookie to track the user. With `session_store_type=redis`, the browser cookie is a short ticket while encrypted session data is stored in Redis/Valkey. Access, ID and refresh tokens may live in the backend session data; they are not the same as the browser cookie. Rotating `oauth2_proxy_cookie_secret` invalidates existing proxy cookies. Rotating the Keycloak client secret affects token redemption. Rotating Valkey credentials affects session lookup. Treat these as separate incidents.

The tracked config requests `openid email profile offline_access groups`, uses PKCE `S256`, passes authorization/access-token headers, and enables `set_xauthrequest`. That means downstream services may receive identity/token headers when routed through ForwardAuth. A downstream service must still define what it trusts; gateway SSO alone is not native application RBAC.

### Logout Boundary

OAuth2 Proxy official endpoint docs say `/oauth2/sign_out` clears OAuth2 Proxy cookies only. The user can still be logged in at Keycloak and may immediately re-login. Keycloak SSO logout requires redirecting to the provider end-session endpoint with an allowed `rd` destination and matching whitelist settings. The current tracked config sets `OAUTH2_PROXY_WHITELIST_DOMAINS=.${DEFAULT_URL}`, but it does not prove that every service's logout button calls a Keycloak end-session redirect. Do not blanket-claim that current logout ends Keycloak SSO.

### Step-by-step Instructions

1. Compose 런타임 계약 확인
   - `template-infra-readonly-med` 사용
   - 기본 경로는 `docker-compose.yml`, `dev.Dockerfile`, `docker-entrypoint.dev.sh`, 공유 `mng-valkey`를 사용
   - `dedicated-valkey` profile은 같은 `docker-compose.yml`에서 `oauth2-proxy-valkey`와 그 exporter를 추가로 선택
   - command가 `--config /etc/oauth2-proxy.cfg`인지 확인
   - `OAUTH2_PROXY_OIDC_ISSUER_URL`, `OAUTH2_PROXY_REDIRECT_URL`, `OAUTH2_PROXY_COOKIE_DOMAINS`, `OAUTH2_PROXY_WHITELIST_DOMAINS` 확인
2. 엔트리포인트 시크릿 주입 확인
   - root-active `docker-entrypoint.dev.sh`에서 `mng_valkey_password`를 읽어 환경 변수에 export하는지 확인
   - local/full `docker-entrypoint.sh`에서 `oauth2_valkey_password`를 읽어 환경 변수에 export하는지 확인
3. 이미지 권한 모델 확인
   - local/full `Dockerfile`에서 UID 100/GID 101을 명시적으로 생성하고 `USER 100:101`을 적용하는지 확인
   - root-active `dev.Dockerfile`에서 `USER oauth2proxy:oauth2proxy`를 적용하는지 확인
4. 정적 검증
   - `HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh`
   - `bash scripts/hardening/check-all-hardening.sh 02-auth`

### Common Pitfalls

- `DEFAULT_URL`, Keycloak realm issuer, OAuth2 Proxy callback 도메인 불일치
- `ssl_insecure_skip_verify=false` 상태에서 root CA mount가 깨져 discovery/JWKS fetch가 실패하는 경우
- 세션 비밀 변경 후 기존 쿠키 재사용으로 인한 인증 실패
- `/ping`은 process health이고 `/ready`는 Redis 등 backend 연결까지 본다는 차이를 놓치는 경우
- `/oauth2/sign_out`을 Keycloak SSO 종료로 오해하는 경우
- `trusted_ips` 또는 `trusted_proxy_ips`를 넓게 두고 forwarded header spoofing 위험을 검토하지 않는 경우

## Common Checks

- `HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh`
- `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh`
- `bash scripts/hardening/check-all-hardening.sh 02-auth`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](runbook.md)을 따른다.

### Session Recovery and Upgrade

Redis/Valkey에는 ticket 형태의 server-side session이 있고 browser에는 이를 찾는
cookie가 있다. `oauth2_proxy_cookie_secret`을 잃거나 바꾸거나 session store를
비우면 활성 로그인이 무효화될 수 있다. 세션은 업무 데이터가 아니므로 database
restore보다 명시적인 재로그인을 기본 복구로 사용한다. secret owner가 cookie,
client 및 Valkey 자격 증명을 별도 보관하며 값은 백업 증거에 넣지 않는다.

업그레이드는 공식 release notes와 configuration changes를 검토하고, 격리 환경에서
Keycloak discovery, PKCE callback, `/ready`, ForwardAuth headers, logout, session
expiry를 검증한다. 이전 image로 rollback할 때도 cookie secret과 session-store
endpoint를 동일하게 유지하거나 모든 사용자 재로그인을 선언한다.

## Traceability

- Declared parent: [02-Auth OAuth2 Proxy Operations Policy](policy.md) (`POL-0015`)
- Governing authority: [02-Auth Architecture Description](../../../../02.architecture/descriptions/0002-auth-architecture.md) (`AD-0002`)
- Subject peers: [Policy](policy.md) (`POL-0015`), [Runbook](runbook.md) (`RUN-0015`)

## Related Documents

- [Official OAuth2 Proxy Keycloak OIDC provider](https://oauth2-proxy.github.io/oauth2-proxy/configuration/providers/keycloak_oidc/)
- [Official OAuth2 Proxy configuration overview](https://oauth2-proxy.github.io/oauth2-proxy/configuration/overview/)
- [Official OAuth2 Proxy session storage](https://oauth2-proxy.github.io/oauth2-proxy/configuration/session_storage/)
- [Official OAuth2 Proxy endpoints](https://oauth2-proxy.github.io/oauth2-proxy/features/endpoints/)

- Runtime pins: Compose/Dockerfile declarations are authoritative; the [derived Compose image projection](../../../../../infra/tech-stack.versions.json) provides drift verification.

- [Operations index](../../../README.md)
- [Operations policy](policy.md)
- [Recovery runbook](runbook.md)
