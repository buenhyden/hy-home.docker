# Auth Tier (02-auth)

> Identity and Access Management (IAM) & Authentication ForwardAuth Gateway.

## Overview

The `02-auth` tier provides the security foundation for the `hy-home.docker` ecosystem. It centralizes user identity, single sign-on (SSO), and access control through Keycloak and OAuth2 Proxy. This tier is responsible for issuing OIDC tokens and protecting internal services via ForwardAuth verification.

## Audience

이 README의 주요 독자:

- Developers (Service Integration)
- Operators (User Management & Security)
- AI Agents (Provisioning & Auditing)

## Scope

### In Scope

- Keycloak: IAM Provider (OIDC/SAML)
- OAuth2 Proxy: SSO ForwardAuth Gateway
- Authentication flow configuration and service discovery labels
- Dependency management for PostgreSQL (Identity DB) and Valkey (Session Cache)

### Out of Scope

- SSL/TLS termination (handled by `01-gateway`)
- Network-level firewall rules
- Individual application-level RBAC (managed within Keycloak or Apps)

## Structure

```text
02-auth/
├── keycloak/           # IAM Provider configuration
├── oauth2-proxy/       # ForwardAuth Gateway configuration
└── README.md           # This file
```

## How to Work in This Area

1. Read the [Auth Guides](../../docs/05.operations/guides/02-auth/README.md) for bootstrap and integration steps.
2. Review the `docker-compose.yml` in subdirectories for specific service configurations.
3. Follow the [Operations Policy](../../docs/05.operations/policies/02-auth/README.md) for user and realm management.
4. Use the [Auth Runbook](../../docs/05.operations/runbooks/02-auth/README.md) for maintenance and recovery tasks.

## Tech Stack

| Category   | Technology                     | Notes                     |
| ---------- | ------------------------------ | ------------------------- |
| IAM        | Keycloak (Quarkus)             | OIDC/SAML Provider        |
| Proxy      | OAuth2 Proxy                   | ForwardAuth Implementation |
| Database   | PostgreSQL                     | Identity Persistence      |
| Cache      | Valkey                         | Session Store             |
| Discovery  | Traefik labels                 | Dynamic Service Routing   |

## Configuration

### Environment Variables

| Variable | Required | Description |
| --------- | -------: | ----------- |
| `DEFAULT_URL` | Yes | Root domain for services (e.g., `127.0.0.1.nip.io`) |
| `KEYCLOAK_ADMIN_USER` | Yes | Initial admin username for Keycloak |
| `OAUTH2_PROXY_CLIENT_ID` | Yes | Client ID registered in Keycloak for the proxy |

## Testing

Static validation is the primary local/CI boundary. Runtime checks require the
root compose context so shared networks, secrets, and included dependencies are
available.

```bash
# Validate the root auth profile and 02-auth hardening contract
HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh 02-auth

# Runtime-only checks after the auth profile is already running
docker compose --profile auth exec keycloak sh -c 'exec 3<>/dev/tcp/127.0.0.1/9000; printf "GET /health/ready HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n" >&3; cat <&3'
docker compose --profile auth exec oauth2-proxy wget -qO- http://127.0.0.1:4180/ping
```

## Change Impact

- Changes in Keycloak realms or clients will affect all SSO-integrated services.
- OAuth2 Proxy configuration updates may require a redirect URI update in Keycloak.
- Secret rotations (Cookie Secret, Client Secret) must be synchronized across both services.

## Related Documents

- [01-gateway](../01-gateway/README.md) - Handles ingress and ForwardAuth routing.
- [04-data](../04-data/README.md) - Provides persistence and caching layers.
- [docs/05.operations/02-auth](../../docs/05.operations/guides/02-auth/README.md) - Conceptual and setup guides.

## AI Agent Guidance

1. Always read this README to understand the relationship between Keycloak and OAuth2 Proxy.
2. Refer to `docs/03.specs/002-auth` (if exists) for detailed protocol flows.
3. Do not modify secrets directly; use `scripts/operations/gen-secrets.sh` if available.
4. Ensure all new services are integrated using the standard ForwardAuth pattern via Traefik labels.
