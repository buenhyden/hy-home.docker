---
layer: infra
---

# Gateway Tier: System & Service Context

The `01-gateway` tier is the unified entry point for all traffic entering the `hy-home.docker` ecosystem. It serves as both a secure perimeter and a dynamic traffic orchestrator.

## Architectural Overview

The gateway tier uses a "Dual-Proxy" approach to balance dynamic flexibility with specialized routing requirements.

### Component Roles

- **Traefik (Primary Entrypoint)**:
  - **Dynamic Routing**: Discovers services via Docker labels.
  - **TLS Termination**: Manages local HTTPS certificates via File/Docker providers.
  - **Middleware Engine**: Orchestrates SSO (via OAuth2 Proxy), rate limiting, and header manipulation.
  - **TCP Routing**: Handles non-HTTP traffic, such as Neo4j Bolt protocol (port 7687).

- **Nginx (Specialized Proxy)**:
  - **Path-based Logic**: Handles complex location blocks and URI rewrites.
  - **Static Assets**: Serves files directly from mapped volumes for performance.
  - **Auth Integration**: Uses `auth_request` to interface with the identity tier.

## Network & Traffic Flow

### External Ingress
- **HTTP (80)**: Automatically redirected to HTTPS (443) by Traefik.
- **HTTPS (443)**: Primary encrypted entrypoint for all web services.
- **Bolt (7687)**: Direct TCP passthrough for Neo4j database connections.

### Traffic Lifecycle

1. **Ingress**: Traffic hits the host machine on port 443.
2. **TLS Handshake**: Traefik terminates the SSL connection using certificates from `secrets/certs/`.
3. **Middleware Chain**:
   - Headers are sanitized and optimized.
   - If a route is protected, the `sso-auth` middleware verifies the session against `02-auth`.
4. **Service Discovery**: Traefik identifies the healthy backend container based on Host headers (e.g., `traefik.http.routers.<name>.rule`).
5. **Egress**: Traffic is forwarded over the `infra_net` internal bridge network to the target container.

## Core Dependencies

| Dependency | Purpose | Integration Point |
| :--- | :--- | :--- |
| **`02-auth`** | SSO / Identity Verification | OAuth2 Proxy endpoint (`auth.hy-home.dev`) |
| **`04-data`** | Database Access | Neo4j Bolt & OpenSearch HTTPS routes |
| **`secrets/`** | Security Assets | Mounted TLS certificates and basic auth files |
| **Docker Engine** | Dynamic Discovery | `/var/run/docker.sock` read access |
