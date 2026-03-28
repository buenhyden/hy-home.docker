# OAuth2 Proxy

> OIDC ForwardAuth gateway for protecting backend services within the `hy-home.docker` ecosystem.

## Overview

OAuth2 Proxy provides a generic authentication layer for services that do not have built-in OIDC support. It interacts with Keycloak to verify user sessions and manages session state using Valkey. It is integrated into the Traefik ecosystem as a ForwardAuth provider, ensuring centralized SSO across all protected subdomains.

## Audience

이 README의 주요 독자:

- Developers (Integrating new backends with SSO)
- Operators (Session troubleshooting & secret rotation)
- AI Agents (Label configuration & label-based middleware setup)

## Scope

### In Scope

- OAuth2 Proxy configuration (`oauth2-proxy.cfg`)
- ForwardAuth workflow integration with Traefik
- Valkey session storage connectivity and persistence
- Custom Docker build based on Alpine for security and stability

### Out of Scope

- User identity management (handled by Keycloak)
- SSL Certificate issuance (handled by Traefik/Cert-manager)
- Granular application-level RBAC (handled by backends)

## Structure

```text
oauth2-proxy/
├── config/             # Proxy configuration (oauth2-proxy.cfg)
├── Dockerfile          # Custom Alpine-based build
├── docker-entrypoint.sh # Secret/Env injection script
├── docker-compose.yml  # Container orchestration
└── README.md           # This file
```

## How to Work in This Area

1. Read the [Auth Guides](../../../docs/07.guides/02-auth/README.md) for OIDC/ForwardAuth configuration.
2. Refer to the [OAuth2 Proxy Guide](../../../docs/07.guides/02-auth/oauth2-proxy.md) for detailed configuration steps.
3. Check `config/oauth2-proxy.cfg` for runtime provider and cookie settings.
4. Use the [Auth Runbook](../../../docs/09.runbooks/02-auth/README.md) for cookie secret rotation procedures.

## Tech Stack

| Category   | Technology                     | Notes                     |
| ---------- | ------------------------------ | ------------------------- |
| Proxy      | OAuth2 Proxy (Go)              | v7.14.2                   |
| Session    | Valkey                         | Redis-compatible storage  |
| Protocol   | OIDC / ForwardAuth             | Keycloak & Traefik        |
| Runtime    | Alpine Linux                   | Minimal footprint         |

## Configuration

### Environment Variables

| Variable | Required | Description |
| --------- | -------: | ----------- |
| `OAUTH2_PROXY_CLIENT_ID` | Yes | OIDC Client ID from Keycloak |
| `OAUTH2_PROXY_COOKIE_SECRET` | Yes | Cookie encryption key (32-byte string) |
| `OAUTH2_PROXY_CLIENT_SECRET` | Yes | Client secret from Keycloak |

### Secrets Injection

Secrets are injected via `docker-entrypoint.sh` from `/run/secrets/`:

- `oauth2_proxy_cookie_secret`
- `oauth2_proxy_client_secret`
- `mng_valkey_password`

## Testing

### Healthcheck Configuration

The service uses `wget` to perform a health check against the `/ping` endpoint:

```yaml
healthcheck:
  test: ["CMD-SHELL", "wget -qO- http://127.0.0.1:4180/ping >/dev/null 2>&1 || exit 1"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### Manual Verification

```bash
# Verify health readiness
docker exec oauth2-proxy wget -qO- http://localhost:4180/ping

# Verify OIDC reachability via logs
docker logs oauth2-proxy | grep "OIDC"
```

## Related References

- [Keycloak](../keycloak/README.md) - The Identity Provider.
- [01-gateway](../../01-gateway/README.md) - Traefik route configuration.
- [docs/08.operations/02-auth/oauth2-proxy.md](../../../docs/08.operations/02-auth/oauth2-proxy.md) - Session policies.

## AI Agent Guidance

1. 이 README를 먼저 읽고 Traefik 레이블 설정을 확인한다.
2. 새로운 서비스 추가 시 `forwardauth` 미들웨어를 `auth.${DEFAULT_URL}` 경로로 설정한다.
3. `OAUTH2_PROXY_COOKIE_SECRET` 변경 시 모든 세션이 초기화됨을 인지한다.
4. `config/oauth2-proxy.cfg`의 `redirect_url`과 Keycloak 클라이언트 설정을 동기화한다.
