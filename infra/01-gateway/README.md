# Gateway Tier (01-gateway)

> Unified entry point for all traffic, orchestrating routing, TLS, and security.

## Overview

The `01-gateway` tier is the unified entry point for traffic entering the `hy-home.docker` ecosystem. The current root stack actively includes Traefik as the edge router. Nginx remains a profile-only specialized path proxy leaf and must be validated or run only with an explicit root network/dependency context.

## Audience

이 README의 주요 독자:

- Infrastructure Engineers
- Backend Developers
- Security Auditors
- AI Agents

## Scope

### In Scope

- Traefik (Edge Router) configuration and root-stack deployment.
- Nginx (Path Proxy) configuration and profile-only validation boundary.
- TLS termination and certificate management.
- Dynamic service discovery via Docker provider.

### Out of Scope

- Application-level business logic.
- Long-term log storage or analysis (handled by Observability tier).
- Identity provider management (handled by Auth tier).

## Structure

```text
01-gateway/
├── nginx/           # Path-based proxy and static asset server
├── traefik/         # Primary edge router with dynamic service discovery
└── README.md        # This file
```

## Tech Stack

| Category   | Technology                        | Notes                     |
| ---------- | --------------------------------- | ------------------------- |
| Router     | Traefik v3.7.1                    | Primary dynamic router    |
| Proxy      | Nginx Alpine                      | Specialized path proxy    |
| Discovery  | Docker Provider                   | Auto-detection of containers |
| Security   | OAuth2 Proxy / Keycloak           | Integrated SSO provider   |

## Networking (Ports)

| Port (Host) | Port (Int) | Protocol | Purpose |
| :--- | :--- | :--- | :--- |
| `80` | `80` | TCP | HTTP Ingress (Auto-redirect to 443) |
| `443` | `443` | TCP | HTTPS Ingress (Primary Entrypoint) |
| `8082` | `8082` | TCP | Traefik metrics and ping entrypoint, container-internal unless separately exposed |

## How to Work in This Area

1. Review the [Gateway operations guides](../../docs/05.operations/guides/01-gateway/README.md) to understand traffic flow.
2. Ensure secrets are generated via `scripts/operations/gen-secrets.sh` before deployment.
3. Follow the [Gateway setup guide](../../docs/05.operations/guides/01-gateway/01.setup.md) for initial deployment boundaries.
4. Verify static readiness with `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh` and `bash scripts/hardening/check-all-hardening.sh 01-gateway`; use runtime health commands only against an approved running stack.

## Related Documents

- [Agent Governance](../../AGENTS.md)
- [System Architecture](../../docs/02.architecture/requirements/README.md)
- [Secret Management](../../secrets/README.md)
- [Gateway Guides](../../docs/05.operations/guides/01-gateway/README.md)
- [Operations Policy](../../docs/05.operations/policies/01-gateway/README.md)
- [Emergency Runbooks](../../docs/05.operations/runbooks/01-gateway/README.md)
