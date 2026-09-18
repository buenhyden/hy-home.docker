---
title: "Auth Tier (02-auth)"
version: "1.1.0"
type: "common/package-readme"
status: "active"
owner: "@buenhyden"
updated: "2026-09-18"
created: "2025-11-12"
---

# Auth Tier (02-auth)

> Identity and Access Management, Gateway ForwardAuth, and application-native OIDC integration.

## Overview

The `02-auth` tier provides the security foundation for the `hy-home.docker`
ecosystem. Keycloak is the central Identity Provider. OAuth2 Proxy provides
Gateway ForwardAuth for services without suitable built-in OIDC, while approved
applications such as Airflow and Kafbat UI authenticate directly against
Keycloak using application-native OIDC.

## Audience

- Developers
- Operators
- AI Agents

## Scope

### In Scope

- Keycloak: IAM Provider
- OAuth2 Proxy: ForwardAuth Gateway
- ForwardAuth vs Native OIDC selection
- OIDC client integration
- PostgreSQL identity persistence
- Valkey session storage for OAuth2 Proxy

### Out of Scope

- TLS termination (`01-gateway`)
- network firewall
- application business logic
- application-internal RBAC implementation details

## Structure

```text
02-auth/
├── keycloak/
├── oauth2-proxy/
└── README.md
```

## Authentication Patterns

### Gateway ForwardAuth

```text
Browser -> Traefik -> OAuth2 Proxy -> Keycloak -> Service
```

현재 예:
- Flower
- n8n
- 자체 OIDC가 없는 내부 UI

### Application-native OIDC

```text
Browser -> Traefik -> Application -> Keycloak
```

현재:
- Airflow
- Kafbat UI

Native OIDC 서비스 앞에 OAuth2 Proxy ForwardAuth를 기본적으로 중복 적용하지 않는다.

## How to Work in This Area

1. [Auth Operations](../../docs/05.operations/catalog/02-auth/README.md)를 먼저 확인한다.
2. Keycloak/OAuth2 Proxy compose/config를 변경하기 전에 guide/policy/runbook을 확인한다.
3. 신규 서비스를 `Gateway ForwardAuth` 또는 `Application-native OIDC`로 분류한다.
4. 승인된 Native OIDC 서비스 앞에 OAuth2 Proxy ForwardAuth를 중복 적용하지 않는다.
5. secret은 `scripts/operations/gen-secrets.sh`와 Docker Secret 경계를 사용한다.
6. root profile validation/hardening을 실행한다.

## Tech Stack

| Category | Technology | Notes |
| --- | --- | --- |
| IAM | Keycloak | Central OIDC/SAML IdP |
| ForwardAuth | OAuth2 Proxy | Gateway authentication |
| Native OIDC | Airflow, Kafbat UI | Direct Keycloak clients |
| Database | PostgreSQL | Identity persistence |
| Session | Valkey | OAuth2 Proxy session |
| Gateway | Traefik | TLS/routing/middleware |

## Configuration

| Variable | Required | Description |
| --- | ---: | --- |
| `DEFAULT_URL` | Yes | root domain |
| `KEYCLOAK_REALM` | Yes | `hy-home.realm` |
| `KEYCLOAK_URL` | Yes | public Keycloak URL |
| `OAUTH2_PROXY_CLIENT_ID` | Yes | ForwardAuth client |
| `KAFBAT_OAUTH_CLIENT_ID` | Yes | Kafbat Native OIDC client |
| `AIRFLOW_KEYCLOAK_CLIENT_ID` | Yes | Airflow Native OIDC client |

## Testing

```bash
HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh 02-auth
```

Runtime:

```bash
docker compose --profile auth exec keycloak sh -c   'exec 3<>/dev/tcp/127.0.0.1/9000; printf "GET /health/ready HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n" >&3; cat <&3'
docker compose --profile auth exec oauth2-proxy   wget -qO- http://127.0.0.1:4180/ping
```

## Change Impact

- Keycloak realm/client 변경은 여러 application에 영향.
- OAuth2 Proxy 변경은 ForwardAuth target에 영향.
- Native OIDC client 변경은 해당 application login/RBAC에 영향.
- secret rotation은 session/client 재로그인을 요구할 수 있다.

## Related Documents

- [Gateway](../01-gateway/README.md)
- [Data](../04-data/README.md)
- [Auth Operations](../../docs/05.operations/catalog/02-auth/README.md)
- [Application Authentication Integration Guide](../../docs/05.operations/catalog/02-auth/0079-application-auth-integration/guide.md)
- [Documentation index](../../docs/README.md)
