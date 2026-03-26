# Keycloak IAM

> Identity and Access Management (IAM) provider based on Quarkus.

## Overview

Keycloak is the central identity provider for the `hy-home.docker` ecosystem. It handles user authentication, session management, and OIDC/SAML token issuance for protected applications. It supports multi-tenancy through realms and provides a robust admin console for user management.

## Audience

이 README의 주요 독자:

- Developers (OIDC Client configuration)
- Operators (Realms & User Management)
- AI Agents (Service provisioning & Realm exports)

## Scope

### In Scope

- Keycloak service configuration (Standard Quarkus distribution)
- Realm and Client provisioning via GUI or CLI
- Volume mounts for themes, providers, and static configurations
- Database connectivity to PostgreSQL

### Out of Scope

- Forwarding and SSO session handling (delegated to OAuth2 Proxy)
- SMTP/Email provider configuration (managed externally in `10-communication`)
- Deep custom Java SPI development (only basic provider management included)

## Structure

```text
keycloak/
├── conf/               # Quarkus static configuration
├── providers/          # Custom JARs/SPIs for extensions
├── themes/             # Custom UI/UX themes
├── docker-compose.yml  # Container orchestration
└── README.md           # This file
```

## How to Work in This Area

1. Refer to the [Auth Setup Guide](../../../docs/07.guides/02-auth/01.setup.md) for initial realm creation.
2. Check the [Keycloak Configuration Guide](../../../docs/07.guides/02-auth/keycloak-config.md) for specific realm/client settings.
3. Check `opt/keycloak/conf` for static settings.
4. Use the [Auth Operation Policy](../../../docs/08.operations/02-auth/README.md) for user management procedures.

## Tech Stack

| Category   | Technology                     | Notes                     |
| ---------- | ------------------------------ | ------------------------- |
| Platform   | Keycloak (Quarkus)             | V26.5.4                   |
| Database   | PostgreSQL                     | Identity Persistence      |
| Logging    | Console (Structured)           | JSON format via Quarkus   |

## Configuration

### Environment Variables

| Variable | Required | Description |
| --------- | -------: | ----------- |
| `KC_HOSTNAME` | Yes | Public access URL (keycloak.${DEFAULT_URL}) |
| `KC_DB` | Yes | Database vendor (postgres) |
| `KEYCLOAK_ADMIN_USER` | Yes | Admin username for bootstrap |

## Testing

```bash
# Verify health readiness
docker exec keycloak curl -f http://localhost:9000/health/ready

# Verify metrics endpoint
docker exec keycloak curl -f http://localhost:9000/metrics
```

## Related References

- [02-auth](../README.md) - Parent tier overview.
- [OAuth2 Proxy](../oauth2-proxy/README.md) - Client of Keycloak.
- [docs/09.runbooks/02-auth](../../../docs/09.runbooks/02-auth/README.md) - Recovery procedures.

## AI Agent Guidance

1. Do not modify `KC_DB_URL` manually in `docker-compose.yml`; check environment variables first.
2. Use `KC_BOOTSTRAP_ADMIN_PASSWORD` from secrets for initial setup only.
3. Ensure all new realms follow the `hy-home.{realm-name}` naming convention.
