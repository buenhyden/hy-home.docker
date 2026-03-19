# Gateway Infrastructure (01-gateway)

The Gateway tier provides the primary ingress point for all external and cross-network traffic. It utilizes **Traefik** as the dynamic edge router and **Nginx** as a high-performance secondary proxy for path-based routing.

## Services Architecture

| Service | Profile | Status | Role | Observability |
| :--- | :--- | :--- | :--- | :--- |
| **Traefik** | `core` | Primary | Edge Router / Reverse Proxy | Metrics, Traces |
| **Nginx** | `nginx` | Optional | Static / Path-based Proxy | Logs |

## Deployment & Profiles

- **Default (Traefik)**: Enabled via `core` profile. Handles standard `Host()` based routing for most services.
- **Optional (Nginx)**: Enabled via `nginx` profile. Used for specialized `location` block requirements or legacy migration.

> [!IMPORTANT]
> Both Traefik and Nginx bind to host ports **80** and **443**. They cannot be active at the same time on the same host interface without port remapping.

## Operational Overview

### Port Mapping

| Host Bind | Internal Port | Protocol | Purpose |
| :--- | :--- | :--- | :--- |
| `80` | `80` | HTTP | Redirect to HTTPS |
| `443` | `443` | HTTPS | Secure Entrypoint |
| `8080/dash` | `8080` | HTTP | Traefik API/Dashboard |

### Certificate Strategy

Both gateways share certificates from the root `secrets/certs` directory, typically generated via `mkcert` for local development.

| Path | Purpose |
| :--- | :--- |
| `secrets/certs/cert.pem` | Server Certificate |
| `secrets/certs/key.pem` | Private Key |
| `secrets/certs/rootCA.pem` | Root Certificate Authority |

## Folder Structure

- [`traefik/`](./traefik/): Main router configuration (Static `traefik.yml`, Dynamic `middleware.yml`).
- [`nginx/`](./nginx/): Standalone Nginx configuration and `nginx.conf`.

## Documentation

- [Gateway Strategy](../../docs/guides/01-gateway/gateway-context.md)
- [Traefik Ingress Guide](../../docs/guides/01-gateway/traefik-ingress-guide.md)
- [Operations Manual](../../docs/guides/01-gateway/gateway-operations.md)
- [Recovery Runbook](../../docs/runbooks/2026-03-15-traefik-proxy-recovery.md)
