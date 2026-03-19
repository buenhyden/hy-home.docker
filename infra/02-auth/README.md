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

- **Identity Context**: [auth-context.md](../../docs/guides/02-auth/auth-context.md)
- **Bootstrap Guide**: [auth-procedural.md](../../docs/guides/02-auth/auth-procedural.md)
- **Architecture**: [ARCHITECTURE.md](../../ARCHITECTURE.md#32-layered-service-map)
- **Recovery**: [2026-03-15-auth-lockout.md](../../docs/runbooks/2026-03-15-auth-lockout.md)
