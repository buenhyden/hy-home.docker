# OAuth2 Proxy

OAuth2 Proxy is a reverse proxy and static file server that provides authentication using Providers (Google, GitHub, and others) to validate accounts by email, domain or group.

## Services

| Service        | Image                           | Role               | Resources         | Port       |
| :------------- | :------------------------------ | :----------------- | :---------------- | :--------- |
| `oauth2-proxy` | `build: ./Dockerfile`           | Auth Proxy         | 0.5 CPU / 256MB   | 4180 (Int) |

## Dependencies

- **IdP**: Typically connected to Keycloak (`infra/02-auth/keycloak`).
- **Session Store**: Uses Valkey (`mng-valkey:6379`) located in `infra/04-data/mng-db`.

## Networking

Exposed via Traefik at `auth.${DEFAULT_URL}`.

- **Port Mapping**: Uses `${OAUTH2_PROXY_PORT}` (usually 4180).

## File Map

| Path               | Description                           |
| ------------------ | ------------------------------------- |
| `docker-compose.yml` | Service and session store wiring.    |
| `config/`          | Provider and cookie configuration.    |
| `README.md`        | Service overview and SSO notes.       |
