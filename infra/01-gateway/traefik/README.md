---
layer: infra
---

# Traefik Edge Router

Traefik is the primary ingress controller for `hy-home.docker`. It handles routing, TLS termination, and middleware orchestration.

## Configuration Structure

Traefik uses a two-tier configuration model:

1. **Static Configuration** ([`./config/traefik.yml`](./config/traefik.yml)):
   - Defines entrypoints: `web` (80), `websecure` (443), `bolt` (7687).
   - Configures providers: Docker (dynamic labels) and File (dynamic config directory).
   - Sets log levels and observability (Prometheus/Metrics).

2. **Dynamic Configuration** ([`./dynamic/`](./dynamic/)):
   - **Middlewares** ([`middleware.yml`](./dynamic/middleware.yml)): SSO auth, headers, rate limiting.
   - **TLS Options** ([`tls.yaml`](./dynamic/tls.yaml)): Local certificate management and cipher suites.
   - **Hot-reloaded**: Changes in this folder are applied instantly without restarting Traefik.

## Routing Pattern

Services are exposed by adding labels to their `docker-compose.yml` service definition:

```yaml
labels:
  traefik.enable: "true"
  traefik.http.routers.<name>.rule: Host(`<subdomain>.${DEFAULT_URL}`)
  traefik.http.routers.<name>.entrypoints: websecure
  traefik.http.routers.<name>.tls: "true"
  traefik.http.services.<name>.loadbalancer.server.port: "<port>"
```

### Identity & SSO Protection

To protect a service with SSO, apply the `sso-auth@file` middleware:

```yaml
labels:
  traefik.http.routers.<name>.middlewares: sso-auth@file
```

## Operations

### Lifecycle Commands

- **Start**: `docker compose up -d`
- **Restart**: `docker compose restart` (Required for `traefik.yml` or `docker-compose.yml` changes)
- **Check Logs**: `docker compose logs -f traefik`

### Verification

| Method | Command / Action |
| :--- | :--- |
| **Dashboard** | Visit `https://dashboard.${DEFAULT_URL}` |
| **Health Check** | `docker exec traefik traefik healthcheck --ping` |
| **Metrics** | `curl http://localhost:8082/metrics` |

## Dependencies

- **Docker Socket**: Used for dynamic service discovery.
- **Certificates**: Mounted from `secrets/certs/`.
- **Auth Tier**: Depends on `02-auth` (OAuth2 Proxy) for the `sso-auth` middleware.
