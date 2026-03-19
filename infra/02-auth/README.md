# Auth (02-auth)

This category manages Identity and Access Management (IAM) and authentication gateways.

## Services

| Service      | Profile | Path             | Purpose                                    |
| ------------ | ------- | ---------------- | ------------------------------------------ |
| Keycloak     | (core)  | `./keycloak`     | IAM provider (SSO, realms, users, clients) |
| OAuth2 Proxy | (core)  | `./oauth2-proxy` | ForwardAuth gateway for protected services |

## Dependencies

- **Database**: Keycloak uses PostgreSQL (via `infra/04-data/mng-db`).
- **Session Store**: OAuth2 Proxy uses Valkey (via `infra/04-data/mng-db`, service `mng-valkey`) for session persistence.
- **Gateway**: Traefik routes `keycloak.${DEFAULT_URL}` and `auth.${DEFAULT_URL}`.
- **Mail**: Applications use `mailhog` (via `infra/10-communication/mail`) for dev SMTP.

## File Map

| Path            | Description                                       |
| --------------- | ------------------------------------------------- |
| `keycloak/`     | Keycloak service and custom image build.          |
| `oauth2-proxy/` | OAuth2 Proxy service and config.                  |
| `README.md`     | Category overview.                                |

## Documentation References

| Guide | Description |
| ----- | ----------- |
| [auth-context.md](../../docs/guides/02-auth/auth-context.md) | System architecture and data flow |
| [auth-procedural.md](../../docs/guides/02-auth/auth-procedural.md) | Bootstrap and configuration procedures |
| [auth-lifecycle.md](../../docs/guides/02-auth/auth-lifecycle.md) | Backup, rotation, and scaling |
| [keycloak-idp-guide.md](../../docs/guides/02-auth/keycloak-idp-guide.md) | Keycloak setup and bootstrapping |
| [keycloak-customization.md](../../docs/guides/02-auth/keycloak-customization.md) | Build-time optimization and custom themes |
| [sso-oauth2-proxy-guide.md](../../docs/guides/02-auth/sso-oauth2-proxy-guide.md) | OAuth2 Proxy integration and SSO flow |
| [ARCHITECTURE.md](../../ARCHITECTURE.md#32-layered-service-map) | System architecture overview |
| [2026-03-15-auth-lockout.md](../../docs/runbooks/2026-03-15-auth-lockout.md) | Admin lockout recovery runbook |
