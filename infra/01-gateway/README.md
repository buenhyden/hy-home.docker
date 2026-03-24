# 🌐 Gateway Tier (01-gateway)

> Unified entry point for all traffic, orchestrating routing, TLS, and security.

## Overview (KR)

`01-gateway` 티어는 `hy-home.docker` 생태계로 들어오는 모든 트래픽의 통합 진입점입니다. 트래픽 라우팅, TLS 종료(SSL 처리), 보안 미들웨어 체인(SSO, Rate Limit 등)을 관리하며, Traefik과 Nginx를 조합하여 효율적인 트래픽 제어를 수행합니다.

## Overview

The `01-gateway` tier is the unified entry point for all traffic entering the `hy-home.docker` ecosystem. It orchestrates routing, TLS termination (SSL), and security middleware chains (SSO, Rate Limit, etc.). By combining Traefik as the edge router and Nginx as a specialized path proxy, it provide robust and flexible traffic management.

## Structure

```text
01-gateway/
├── nginx/           # Path-based proxy and static asset server
├── traefik/         # Primary edge router with dynamic service discovery
└── README.md        # This file
```

---

## ⚙️ Infrastructure Details

### Tech Stack

| Category   | Technology                        | Notes                     |
| ---------- | --------------------------------- | ------------------------- |
| Router     | Traefik v3.6.8                    | Primary dynamic router    |
| Proxy      | Nginx Alpine                      | Specialized path proxy    |
| Discovery  | Docker Provider                   | Auto-detection of pods    |
| Security   | OAuth2 Proxy / Keycloak           | Integrated SSO provider   |

### Networking (Ports)

| Port (Host) | Port (Int) | Protocol | Purpose |
| :--- | :--- | :--- | :--- |
| `80` | `80` | TCP | HTTP Ingress (Auto-redirect to 443) |
| `443` | `443` | TCP | HTTPS Ingress (Primary Entrypoint) |
| `8080` | `8080` | TCP | Traefik Dashboard (Internal) |
| `7687` | `7687` | TCP | Neo4j Bolt (TCP Passthrough) |

## Usage Instructions

### Maintenance & Monitoring

- **Restarting Gateway**: `docker compose up -d traefik nginx`
- **Log location**: `docker compose logs -f traefik`
- **Health Check**: `docker exec traefik traefik healthcheck --ping`
- **Incident response**: Refer to [Running Books](../../docs/09.runbooks/01-gateway/)

---

## 📚 Documentation Hub

### Navigation Map

| Marker | Entry Point | Use when |
| :--- | :--- | :--- |
| `[LOAD:CONTEXT]` | [CONTEXT.md](../../docs/07.guides/01-gateway/README.md) | Understanding traffic flow and architecture |
| `[LOAD:SETUP]` | [SETUP.md](../../docs/07.guides/01-gateway/01.setup.md) | Initial setup and domain binding |
| `[LOAD:PROC]` | [PROCEDURAL.md](../../docs/08.operations/01-gateway/README.md) | Operational policies and governance |

### Key Resources

- [🤖 Agent Governance](../../AGENTS.md)
- [🏛️ System Architecture](../../docs/02.ard/README.md)
- [🔑 Secret Management](../../secrets/README.md)

---
*Maintained by Infra & Gateway Team*
