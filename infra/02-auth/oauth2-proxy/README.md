---
title: "OAuth2 Proxy"
version: "1.1.0"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-19"
created: "2025-11-29"
---

# OAuth2 Proxy

> OIDC ForwardAuth gateway for services that do not use approved application-native OIDC.

## Overview

OAuth2 Proxy provides gateway authentication for services without suitable
built-in OIDC support. It uses Keycloak for OIDC and Valkey for session state.

OAuth2 Proxy is **not** a mandatory hop for every protected subdomain.
Airflow and Kafbat UI use application-native OIDC and are not protected by
OAuth2 Proxy ForwardAuth.

## Audience

- Developers
- Operators
- AI Agents

## Scope

### In Scope

- OAuth2 Proxy config
- Traefik ForwardAuth
- Valkey session
- secret injection
- cookie/issuer/redirect contract

### Out of Scope

- Keycloak identity management
- Native OIDC application RBAC
- TLS certificate issuance

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
| Session | shared `mng-valkey` by default |
| Dedicated session | `oauth2-proxy-valkey` under `dedicated-valkey` |
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
| Session | Valkey | Redis-compatible |
| Protocol | OIDC | Keycloak |
| Gateway | Traefik | ForwardAuth caller |

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
- [OAuth2 Proxy Guide](../../../docs/README.md)
- [Application Authentication Integration Guide](../../../docs/README.md)
- [Documentation index](../../../docs/README.md)

Runtime pins are owned by the Compose/Dockerfile declarations; the [curated version projection](../../tech-stack.versions.json) provides drift verification.

Build source authority: [Dockerfile](Dockerfile), [dev.Dockerfile](dev.Dockerfile).
