# Auth (02-auth)

This category manages Identity and Access Management (IAM) and authentication gateways.

## Services

| Service      | Profile | Path             | Purpose                                    |
| ------------ | ------- | ---------------- | ------------------------------------------ |
| Keycloak     | (core)  | `./keycloak`     | IAM provider (SSO, realms, users, clients) |
| OAuth2 Proxy | (core)  | `./oauth2-proxy` | ForwardAuth gateway for protected services |

## Dependencies

- **Database**: Keycloak uses PostgreSQL (via `infra/04-data/postgresql-cluster` or `infra/04-data/mng-db`).
- **Gateway**: Traefik routes `keycloak.${DEFAULT_URL}` and `auth.${DEFAULT_URL}`.

## File Map

| Path            | Description                                       |
| --------------- | ------------------------------------------------- |
| `keycloak/`     | Keycloak service and optional custom image build. |
| `oauth2-proxy/` | OAuth2 Proxy service and config.                  |
| `README.md`     | Category overview.                                |

## Documentation References

- **Architecture Principles**: [ARCHITECTURE.md](../../ARCHITECTURE.md)
- **Auth Blueprints**: [docs/context/02-auth](../../docs/context/02-auth)
- **Platform Guides**: [docs/guides/README.md](../../docs/guides/README.md)
- **Runbooks (Auth)**: [runbooks/02-auth](../../runbooks/02-auth)
- **Operations History**: [operations/README.md](../../operations/README.md)
