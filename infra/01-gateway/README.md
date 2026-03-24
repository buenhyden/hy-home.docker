# 🌐 Gateway Tier (01-gateway)

> Unified entry point for all traffic, orchestrating routing, TLS, and security.

## Overview

**KR**: `01-gateway` 티어는 `hy-home.docker` 생태계로 들어오는 모든 트래픽의 통합 진입점입니다. 트래픽 라우팅, TLS 종료(SSL 처리), 보안 미들웨어 체인(SSO, Rate Limit 등)을 관리합니다.
**EN**: The `01-gateway` tier is the unified entry point for all traffic entering the `hy-home.docker` ecosystem. It orchestrates routing, TLS termination (SSL), and security middleware chains (SSO, Rate Limit, etc.).

## Navigation / Inventory

| Component | Path | Purpose |
| :--- | :--- | :--- |
| **Traefik** | [`traefik/`](./traefik/) | Primary edge router with dynamic service discovery |
| **Nginx** | [`nginx/`](./nginx/) | Specialized path-based proxy and static asset server |

---

## ⚙️ Infrastructure Details

### Services & Resources

| Service | Image | Role | Resources |
| :--- | :--- | :--- | :--- |
| `traefik` | `traefik:v3.6.8` | Primary Router | `256MB RAM` / `0.5 CPU` |
| `nginx` | `nginx:alpine` | Path Proxy | `128MB RAM` / `0.2 CPU` |

### Networking (Ports)

| Port (Host) | Port (Int) | Protocol | Purpose |
| :--- | :--- | :--- | :--- |
| `80` | `80` | TCP | HTTP Ingress (Auto-redirect to 443) |
| `443` | `443` | TCP | HTTPS Ingress (Primary Entrypoint) |
| `8080` | `8080` | TCP | Traefik Dashboard (Internal) |
| `7687` | `7687` | TCP | Neo4j Bolt (TCP Passthrough) |

### Operational Commands

```bash
# Start the gateway stack
docker compose up -d traefik

# View routing logs
docker compose logs -f traefik

# Check Traefik internal health
docker exec traefik traefik healthcheck --ping
```

---

## 📚 Documentation Hub

### Navigation Map

| Marker | Entry Point | Use when |
| :--- | :--- | :--- |
| `[LOAD:CONTEXT]` | [CONTEXT.md](../../docs/guides/01-gateway/CONTEXT.md) | Understanding traffic flow and architecture |
| `[LOAD:PROC]` | [PROCEDURAL.md](../../docs/guides/01-gateway/PROCEDURAL.md) | Managing lifecycle and certs |
| `[LOAD:SETUP]` | [SETUP.md](../../docs/guides/01-gateway/SETUP.md) | Initial setup and domain binding |

### Key Resources

- [🤖 Agent Governance](/AGENTS.md)
- [🏛️ System Architecture](/ARCHITECTURE.md)
- [🔑 Secret Management](/secrets/README.md)

---
*Maintained by Infra & Gateway Team*
