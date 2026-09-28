---
title: "OAuth2 Proxy"
version: "1.1.1"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-27"
created: "2025-11-29"
---

# OAuth2 Proxy

> 승인된 애플리케이션 native OIDC를 사용하지 않는 서비스를 위한 OIDC ForwardAuth 게이트웨이입니다.

## Overview

OAuth2 Proxy는 적절한 내장 OIDC 지원이 없는 서비스에 게이트웨이 인증을 제공합니다.
OIDC에는 Keycloak을, 세션 상태에는 Valkey를 사용합니다.

OAuth2 Proxy는 모든 보호 대상 서브도메인의 필수 hop이 **아닙니다**.
Airflow와 Kafbat UI는 애플리케이션 native OIDC를 사용하며 OAuth2 Proxy
ForwardAuth로 보호되지 않습니다.

## Audience

- Developers
- Operators
- AI Agents

## Scope

### In Scope

- OAuth2 Proxy 설정
- Traefik ForwardAuth
- Valkey 세션
- secret 주입
- cookie/issuer/redirect 계약

### Out of Scope

- Keycloak identity 관리
- Native OIDC 애플리케이션 RBAC
- TLS 인증서 발급

## Structure

```text
oauth2-proxy/
├── config/
├── Dockerfile
├── dev.Dockerfile
├── docker-entrypoint.sh
├── docker-entrypoint.dev.sh
├── docker-compose.yml
└── README.md
```

## Authentication Applicability

ForwardAuth 대상:

- Flower
- n8n
- 자체 OIDC가 없는 서비스

Native OIDC 대상:

- Airflow
- Kafbat UI

Native OIDC app에는 `sso-auth@file`/`sso-errors@file`을 중복 적용하지 않는다.

## Service Readiness

| Field | Evidence |
| --- | --- |
| Service | `oauth2-proxy` |
| Session | 기본값은 공유 `mng-valkey` |
| Dedicated session | `dedicated-valkey` 아래의 `oauth2-proxy-valkey` |
| Health | `/ping` |
| OIDC client | `home-proxy-client` |
| Issuer | `https://keycloak.${DEFAULT_URL}/realms/hy-home.realm` |

## How to Work in This Area

1. Auth Operations와 integration guide를 먼저 확인.
2. new service onboarding 시 ForwardAuth vs Native OIDC를 먼저 분류.
3. ForwardAuth 대상에만 OAuth2 Proxy middleware 적용.
4. cookie/client/session secret 변경 영향 확인.
5. `Authorization` header forwarding은 upstream JWT scheme과 충돌 여부 검증.
6. callback URL을 재사용하지 않는다.

## Tech Stack

| Category | Technology | Notes |
| --- | --- | --- |
| Proxy | OAuth2 Proxy | ForwardAuth |
| Session | Valkey | Redis 호환 |
| Protocol | OIDC | Keycloak |
| Gateway | Traefik | ForwardAuth 호출자 |

## Secrets

- `oauth2_proxy_cookie_secret`
- `oauth2_proxy_client_secret`
- shared/dedicated Valkey secret

## Testing

```bash
HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh 02-auth
docker compose --profile auth exec oauth2-proxy   wget -qO- http://127.0.0.1:4180/ping
```

## Troubleshooting

- issuer/redirect/cookie domain
- Valkey connectivity
- ForwardAuth middleware route
- Native OIDC app에 중복 적용 여부
- upstream `Authorization` collision

## Related Documents

- [Keycloak](../keycloak/README.md)
- [Gateway](../../01-gateway/README.md)
- OAuth2 Proxy 운영 문서: `docs/05.operations/guides/0015-oauth2-proxy.md`, `docs/05.operations/policies/0015-oauth2-proxy.md`, `docs/05.operations/runbooks/0015-oauth2-proxy.md`
- 애플리케이션 인증 통합 가이드: `docs/05.operations/guides/0079-application-auth-integration.md`
- [문서 인덱스](../../../docs/README.md)

런타임 고정 값은 Compose/Dockerfile 선언이 소유하며 [curated 버전 투영](../../tech-stack.versions.json)은 drift 검증을 제공합니다.

빌드 소스 권한: [Dockerfile](Dockerfile), [dev.Dockerfile](dev.Dockerfile).
