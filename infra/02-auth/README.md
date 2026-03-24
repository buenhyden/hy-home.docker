# Auth Tier (02-auth)

<!-- [ID:02-auth:root] -->
: Identity and Access Management (IAM) & Authentication ForwardAuth Gateway.

---

## Overview

The `02-auth` tier provides the security foundation for the `hy-home.docker` ecosystem. It centralizes user identity, single sign-on (SSO), and access control through Keycloak and OAuth2 Proxy.

### Service Roles

| Component | Role | Details |
| :--- | :--- | :--- |
| **Keycloak** | IAM Provider | OIDC/SAML Provider, User Management, SSO. |
| **OAuth2 Proxy** | ForwardAuth | Protects internal services via OIDC verification. |

## Navigation Map


> [!NOTE]
> This tier is documented across multiple levels. Use the following map for quick access.

### 1. Infrastructure (This Branch)

- **[Keycloak](./keycloak/README.md)**: IAM service configuration and build.
- **[OAuth2 Proxy](./oauth2-proxy/README.md)**: SSO gateway configuration.

### 2. Documentation Suite (Golden 5)

- **[Setup Guide](../../docs/07.guides/02-auth/01.setup.md)**: Initialization and bootstrapping.
- **[Operations Policy](../../docs/08.operations/02-auth/README.md)**: Security and maintenance rules.
- **[Auth Runbook](../../docs/09.runbooks/02-auth/README.md)**: Recovery and troubleshooting.

## Dependencies

- **Database**: Keycloak requires **PostgreSQL** (via `infra/04-data/mng-db`).
- **Session Cache**: OAuth2 Proxy requires **Valkey** (via `infra/04-data/mng-db`).
- **Gateway**: Traefik (via `infra/01-gateway`) handles TLS and forward-auth routing.

## Environmental Requirements

| Variable | Description | Source |
| :--- | :--- | :--- |
| `DEFAULT_URL` | Root domain for services. | `.env` |
| `KEYCLOAK_ADMIN_USER` | Initial admin username. | `.env` |
| `OAUTH2_PROXY_CLIENT_ID` | Client ID for SSO. | `.env` |

---

## Operational Brief

### Monitoring

- **Traefik Dashboard**: Monitor routing status for `keycloak.${DEFAULT_URL}` and `auth.${DEFAULT_URL}`.
- **Prometheus**: Metrics are exposed at `/metrics` (Keycloak) and `/metrics` (OAuth2 Proxy).

### Maintenance
Refer to the **[Auth Runbook](../../docs/09.runbooks/02-auth/README.md)** for account recovery and certificate rotation procedures.
