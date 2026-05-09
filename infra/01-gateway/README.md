# Gateway Tier (01-gateway)

> Unified entry point for all traffic, orchestrating routing, TLS, and security.

The `01-gateway` tier is the unified entry point for all traffic entering the `hy-home.docker` ecosystem. It orchestrates routing, TLS termination (SSL), and security middleware chains (SSO, Rate Limit, etc.). By combining Traefik as the edge router and Nginx as a specialized path proxy, it provides robust and flexible traffic management.

## Audience

이 README의 주요 독자:

- Infrastructure Engineers
- Backend Developers
- Security Auditors
- AI Agents

## Scope

### In Scope

- Traefik (Edge Router) configuration and deployment.
- Nginx (Path Proxy) configuration and deployment.
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
| Router     | Traefik v3.6.12                   | Primary dynamic router    |
| Proxy      | Nginx Alpine                      | Specialized path proxy    |
| Discovery  | Docker Provider                   | Auto-detection of pods    |
| Security   | OAuth2 Proxy / Keycloak           | Integrated SSO provider   |

## Networking (Ports)

| Port (Host) | Port (Int) | Protocol | Purpose |
| :--- | :--- | :--- | :--- |
| `80` | `80` | TCP | HTTP Ingress (Auto-redirect to 443) |
| `443` | `443` | TCP | HTTPS Ingress (Primary Entrypoint) |
| `8080` | `8080` | TCP | Traefik Dashboard (Internal) |
| `7687` | `7687` | TCP | Neo4j Bolt (TCP Passthrough) |

## How to Work in This Area

1. Review [CONTEXT.md](../../docs/07.guides/01-gateway/README.md) to understand traffic flow.
2. Ensure secrets are generated via `scripts/gen-secrets.sh` before deployment.
3. Follow [SETUP.md](../../docs/07.guides/01-gateway/01.setup.md) for initial deployment.
4. Verify changes using `docker exec traefik traefik healthcheck --ping`.

## Related References

- [🤖 Agent Governance](../../AGENTS.md)
- [🏛️ System Architecture](../../docs/02.ard/README.md)
- [🔑 Secret Management](../../secrets/README.md)
- [📘 Gateway Guides](../../docs/07.guides/01-gateway/README.md)
- [⚙️ Operations Policy](../../docs/08.operations/01-gateway/README.md)
- [🚑 Emergency Runbooks](../../docs/09.runbooks/01-gateway/README.md)

---
*Maintained by Infra & Gateway Team*

---

## Overview

`infra/01-gateway`는 Docker Compose 서비스, 설정, 운영 문서의 구현 위치다. 이 README는 하위 파일을 찾는 진입점이며, 기존 본문과 실제 디렉터리 구조를 함께 기준으로 사용한다.
