# OAuth2 Proxy

OAuth2 Proxy is a reverse proxy and static file server that provides authentication using Providers (Google, GitHub, and others) to validate accounts by email, domain or group.

## Services

| Service        | Image                           | Role               | Resources         | Port       |
| :------------- | :------------------------------ | :----------------- | :---------------- | :--------- |
| `oauth2-proxy` | `quay.io/oauth2-proxy/oauth2-proxy:latest` | Auth Proxy | 0.2 CPU / 128MB | 4180 (Int) |

## Dependencies

- **IdP**: Typically connected to Keycloak (`infra/02-auth/keycloak`).
- **Session Store**: Uses Valkey (`infra/04-data/valkey-cluster`) or Redis for session storage.

## Networking

Exposed via Traefik at `auth.${DEFAULT_URL}`.

## File Map

| Path               | Description                           |
| ------------------ | ------------------------------------- |
| `docker-compose.yml` | Service and session store wiring.    |
| `config/`          | Provider and cookie configuration.    |
| `README.md`        | Service overview and SSO notes.       |
