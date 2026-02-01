# Auth (02-auth)

## Overview

Authentication and SSO layer for the platform. **Keycloak** provides IAM, while **OAuth2 Proxy** fronts internal services with ForwardAuth for Traefik/Nginx.

## Services

| Service      | Profile | Path             | Purpose                                    |
| ------------ | ------- | ---------------- | ------------------------------------------ |
| Keycloak     | (core)  | `./keycloak`     | IAM provider (SSO, realms, users, clients) |
| OAuth2 Proxy | (core)  | `./oauth2-proxy` | ForwardAuth gateway for protected services |

## Run

```bash
docker compose up -d keycloak oauth2-proxy
```

## Dependencies

- **Database**: Keycloak uses PostgreSQL (via `infra/04-data/postgresql-cluster` or `infra/04-data/mng-db`).
- **Gateway**: Traefik routes `keycloak.${DEFAULT_URL}` and `auth.${DEFAULT_URL}`.

## File Map

| Path            | Description                                       |
| --------------- | ------------------------------------------------- |
| `keycloak/`     | Keycloak service and optional custom image build. |
| `oauth2-proxy/` | OAuth2 Proxy service and config.                  |
| `README.md`     | Category overview.                                |
