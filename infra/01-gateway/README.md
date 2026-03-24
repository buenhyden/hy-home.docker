---
layer: infra
---

# Gateway Infrastructure (01-gateway)

The `01-gateway` tier is the unified entry point for all traffic entering the `hy-home.docker` ecosystem. It orchestrates routing, TLS termination, and security middlewares.

## Services Architecture

The stack consists of a primary dynamic router (Traefik) and an optional path-based proxy (Nginx).

| Service | Profile | Status | Role | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Traefik** | `core`, `dev` | **Primary** | Edge Router | Dynamic routing via Docker labels, TLS termination. |
| **Nginx** | `nginx` | Optional | Path Proxy | Specialized path-based routing and legacy proxying. |

## Port Inventory

The gateway manages host-level ports to route traffic to internal services.

| Port | Protocol | Service | Purpose |
| :--- | :--- | :--- | :--- |
| `80` | TCP | Gateway | HTTP Ingress (Redirects to 443) |
| `443` | TCP | Gateway | HTTPS Ingress (Primary Entrypoint) |
| `8080` | TCP | Traefik | Admin Dashboard (Host: `dashboard.${DEFAULT_URL}`) |
| `8082` | TCP | Traefik | Health Check / Metrics (Internal) |
| `7687` | TCP | Traefik | Neo4j Bolt Protocol (TCP Passthrough) |

## Configuration Mapping

| Component | Path | Role |
| :--- | :--- | :--- |
| **Traefik Static** | [`./traefik/config/traefik.yml`](./traefik/config/traefik.yml) | Entrypoints, Providers, Log Level. |
| **Traefik Dynamic** | [`./traefik/dynamic/`](./traefik/dynamic/) | Middlewares, TLS options, hot-reloaded. |
| **Nginx Config** | [`./nginx/config/nginx.conf`](./nginx/config/nginx.conf) | Path-based routing and SSO integration. |

## Documentation Hierarchy

- **Technical Reference**: Detailed configuration and operation guides.
  - [Traefik Technical Guide](./traefik/README.md)
  - [Nginx Technical Guide](./nginx/README.md)
- **Conceptual Guides**: High-level architecture and operational procedures.
  - [System Context](../../docs/guides/01-gateway/CONTEXT.md)
  - [Procedural & Lifecycle Guides](../../docs/guides/01-gateway/PROCEDURAL.md)
