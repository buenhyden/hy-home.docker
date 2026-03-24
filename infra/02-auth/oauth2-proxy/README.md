# OAuth2 Proxy

<!-- [ID:02-auth:oauth2-proxy] -->
: OIDC ForwardAuth gateway for protecting backend services.

---

## Overview

OAuth2 Proxy provides a generic authentication layer for services that do not have built-in OIDC support. It interacts with Keycloak to verify user sessions and passes a `Set-Cookie` header to the browser.

### Service Details

| Service | Image / Build | Role | Port |
| :--- | :--- | :--- | :--- |
| **oauth2-proxy** | Custom build (Alpine) | ForwardAuth Gateway | 4180 (HTTP) |

## Dependencies

- **Identity Provider**: Keycloak (`keycloak:8080`).
- **Session Store**: Valkey (`mng-valkey:6379`) for distributed session persistence.

## Networking

Exposed via Traefik at `auth.${DEFAULT_URL}`.

- **ForwardAuth Path**: Services use `auth.${DEFAULT_URL}/oauth2/auth` for verification.
- **Callback URL**: `https://auth.${DEFAULT_URL}/oauth2/callback`.

---

## Operations

### Health Verification

```bash
# Verify status through local ping endpoint
docker exec oauth2-proxy wget -qO- http://localhost:4180/ping
```

### Key Configuration

| Variable | Description | Source |
| :--- | :--- | :--- |
| `OAUTH2_PROXY_CLIENT_ID` | OIDC Client ID | `.env` |
| `OAUTH2_PROXY_COOKIE_SECRET` | Cookie encryption key | Docker Secret |

## Related Documents

- **[Setup Guide](../../../docs/07.guides/02-auth/01.setup.md)**
- **[Operations Policy](../../../docs/08.operations/02-auth/README.md)**
- **[Auth Runbook](../../../docs/09.runbooks/02-auth/README.md)**
