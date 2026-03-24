---
layer: infra
---

# Gateway Tier Guides

The `01-gateway` tier provides the primary entrance to the `hy-home.docker` cluster, handling SSL/TLS termination, dynamic service discovery, and centralized authentication middleware.

## Navigation Map

| View | Command | Focus |
| :--- | :--- | :--- |
| **Architecture** | `[LOAD:CONTEXT]` | Traffic flow and component roles |
| **Installation** | `[LOAD:SETUP]` | Initial bootstrap and verification |
| **Operations** | `[LOAD:USAGE]` | Daily tasks and connection strings |
| **Maintenance** | `[LOAD:PROCEDURAL]` | Lifecycle and recovery |

## Categorized Service Index

### Edge Routing & Proxy

- **[CONTEXT.md](./CONTEXT.md)**: Architectural overview of Traefik and Nginx.
- **[SETUP.md](./SETUP.md)**: Bootstrapping the gateway with certificates.
- **[mkcert.md](./mkcert.md)**: Local TLS certificate generation guide.

### Operations & Troubleshooting

- **[USAGE.md](./USAGE.md)**: Traefik Dashboard access and common routing scenarios.
- **[PROCEDURAL.md](./PROCEDURAL.md)**: Scaling and service health verification.

For technical configuration details (Docker Compose, Config files), see [infra/01-gateway/](file:///home/hy/projects/hy-home.docker/infra/01-gateway/README.md).
