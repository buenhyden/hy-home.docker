# SSO & OAuth2 Proxy Operational Blueprint

> **Component**: `oauth2-proxy`
> **Dependency**: `keycloak`, `mng-redis`

## 1. Authentication Flow

The infrastructure uses a "Sidecar-less Centralized Gateway" auth pattern. Traefik intercepts requests and forwards authentication headers to `oauth2-proxy`.

- **Internal Callback**: `https://auth.${DEFAULT_URL}/oauth2/callback`
- **Internal API**: `http://oauth2-proxy:4180`

## 2. Protecting Upstream Services

To enable SSO for a service, the `sso-auth@file` middleware must be attached to the Traefik router.

### Middleware Mechanics

The proxy checks for a valid session cookie. If missing, it initiates an OIDC flow with the identity provider (Keycloak).

## 3. Local Cache (Redis)

OAuth2 Proxy utilizes the `mng-redis` (Valkey) instance for session storage to allow for horizontal scaling of the proxy itself.

- **Connection**: `redis://mng-redis:6379`

## 4. Diagnostics

If login loops occur:

1. Verify `COOKIE_DOMAIN` matches the root of `${DEFAULT_URL}`.
2. Check if the backend Keycloak is issuing valid tokens.
3. Inspect proxy logs for `Secret mismatch` or `Redis unreachable`.
