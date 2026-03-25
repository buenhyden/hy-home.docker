# OAuth2 Proxy

> OIDC ForwardAuth gateway for protecting backend services.

## Overview

OAuth2 Proxy provides a generic authentication layer for services that do not have built-in OIDC support. It interacts with Keycloak to verify user sessions and passes a `Set-Cookie` header to the browser. It is integrated into the Traefik ecosystem as a ForwardAuth provider.

## Audience

이 README의 주요 독자:

- Developers (Integrating new backends with SSO)
- Operators (Session troubleshooting)
- AI Agents (Label configuration & cookie secret rotation)

## Scope

### In Scope

- OAuth2 Proxy configuration (`oauth2-proxy.cfg`)
- ForwardAuth flow with Traefik
- Valkey session storage integration
- Custom Docker build for Alpine stability

### Out of Scope

- User identity management (handled by Keycloak)
- SSL Certificate issuance (handled by Traefik)
- Deep backend authorization logic (restricted to basic group checks)

## Structure

```text
oauth2-proxy/
├── config/             # Proxy configuration (cfg)
├── Dockerfile          # Custom build for stability
├── docker-compose.yml  # Container orchestration
└── README.md           # This file
```

## How to Work in This Area

1. Read the [Auth Setup Guide](../../../docs/07.guides/02-auth/01.setup.md) for OIDC client configuration.
2. Check `config/oauth2-proxy.cfg` for runtime settings.
3. Use the [Auth Runbook](../../../docs/09.runbooks/02-auth/README.md) for cookie secret rotation.

## Tech Stack

| Category   | Technology                     | Notes                     |
| ---------- | ------------------------------ | ------------------------- |
| Proxy      | OAuth2 Proxy (Go)              | v7.14.2                   |
| Session    | Valkey                         | Redis-compatible storage  |
| Protocol   | OIDC                           | Keycloak integration      |

## Configuration

### Environment Variables

| Variable | Required | Description |
| --------- | -------: | ----------- |
| `OAUTH2_PROXY_CLIENT_ID` | Yes | OIDC Client ID from Keycloak |
| `OAUTH2_PROXY_COOKIE_SECRET` | Yes | Cookie encryption key (32-byte string) |
| `OAUTH2_PROXY_CLIENT_SECRET` | Yes | Client secret from Keycloak |

## Testing

```bash
# Verify health readiness
docker exec oauth2-proxy wget -qO- http://localhost:4180/ping

# Verify OIDC reachability via logs
docker logs oauth2-proxy | grep "OIDC"
```

## Change Impact

- Modifying `cookie_domains` will affect which subdomains can participate in SSO.
- Rotating `OAUTH2_PROXY_COOKIE_SECRET` will invalidate all current user sessions.
- Traefik labels on backend services must point to the OAuth2 Proxy `auth` endpoint.

## Related References

- [Keycloak](../keycloak/README.md) - The Identity Provider.
- [01-gateway](../../01-gateway/README.md) - Traefik route configuration.
- [docs/08.operations/02-auth](../../../docs/08.operations/02-auth/README.md) - Session policies.

## AI Agent Guidance

1. When adding a new service, ensure Traefik labels include the ForwardAuth middleware pointing to `auth.${DEFAULT_URL}`.
2. Use `pass_authorization_header = true` in the `.cfg` if backends need the Bearer token.
3. Do not modify `redirect_url` in the `.cfg` without matching the same in Keycloak client settings.
