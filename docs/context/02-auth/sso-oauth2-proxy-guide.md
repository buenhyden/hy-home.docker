# SSO & OAuth2 Proxy Operational Blueprint

> **Component**: `oauth2-proxy`
> **Dependency**: `keycloak`, `mng-redis`
> **Port**: `4180`

## 1. Centralized Authentication Gateway

The infrastructure uses a "Sidecar-less" pattern. Traefik intercepts requests and verifies identity via this proxy.

- **Internal API**: `http://oauth2-proxy:4180`
- **Internal Callback**: `https://auth.${DEFAULT_URL}/oauth2/callback`

## 2. Initial Setup Requirements

Before the proxy can serve requests, the following must be configured in Keycloak:

1. **Client ID**: Must match `OAUTH2_PROXY_CLIENT_ID` (default: `oauth2-proxy`).
2. **Client Secret**: Generated in Keycloak and stored in Docker Secrets (`@oauth2_proxy_client_secret`).
3. **Cookie Secret**: A random 32-byte string for signing session cookies.

## 3. Protecting Services

Attach the `sso-auth@file` middleware to any Traefik router to enforce SSO.

### Flow Mechanics

1. Traefik sends auth request to `oauth2-proxy`.
2. Proxy checks for a valid session cookie.
3. If missing, proxy redirects user to Keycloak for OIDC login.
4. Upon success, Keycloak redirects back to proxy callback, which sets the session cookie.

## 4. Session Persistence

Sessions are stored dynamically in `mng-redis` (Valkey) to support multi-node scaling of the proxy layer.

- **Connection**: `redis://mng-redis:6379`

## 5. Diagnostics

- **Login Loops**: Verify `COOKIE_DOMAIN` is correctly set to your root domain.
- **Header Issues**: Ensure Traefik correctly passes the `X-Auth-Request-User` and `X-Auth-Request-Email` headers to upstream apps.
