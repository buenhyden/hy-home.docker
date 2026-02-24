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

> **Note**: This component's local documentation has been migrated to the global repository standards to enforce Spec-Driven Development boundaries.

Please refer to the following global documentation directories for information regarding this service:

- **Architecture & Topology**: [docs/architecture](../../docs/architecture)
- **Configuration & Setup Guides**: [docs/guides](../../docs/guides)
- **Routine Operations**: [operations/](../../operations)
- **Troubleshooting & Recovery**: [runbooks/](../../runbooks)
