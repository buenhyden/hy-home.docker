---
layer: infra
---

# Traefik Dynamic Configuration

Configurations in this directory are hot-reloaded by Traefik without requiring a restart.

- **middleware.yml**: Defines reusable middlewares like `sso-auth` (ForwardAuth) and `dashboard-auth` (BasicAuth).
- **tls.yaml**: Defines the default TLS store and certificate locations.
