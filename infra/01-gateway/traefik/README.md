# Traefik Edge Router

Traefik is the primary reverse proxy and load balancer for the Hy-Home infrastructure. It handles TLS termination, dynamic routing based on Docker labels, and authentication middleware integration.

## Services

| Service   | Image                    | Role                       | Resources         | Port       |
| :-------- | :----------------------- | :------------------------- | :---------------- | :--------- |
| `traefik` | `traefik:v3.6.8`         | Edge Router / Reverse Proxy| 1.0 CPU / 1GB RAM | 80, 443    |

## Networking

Traefik binds to the host's ports (configurable via `.env`) and routes traffic via `infra_net`.

| Host Bind | Host Port                         | Protocol | Purpose                  |
| :-------- | :-------------------------------- | :------- | :----------------------- |
| `0.0.0.0` | `${HTTP_HOST_PORT}` (80)          | HTTP     | Redirect to HTTPS        |
| `0.0.0.0` | `${HTTPS_HOST_PORT}` (443)        | HTTPS    | Main Edge Entrypoint     |
| `0.0.0.0` | `${TRAEFIK_DASHBOARD_PORT}`       | Dash     | Traefik UI (Basic-Auth)  |
| `0.0.0.0` | `${TRAEFIK_METRICS_PORT}`         | Metrics  | Prom scraping /ping      |

## Persistence

Traefik maintains state for certificates and dynamic configurations.

- **Certs**: `${DEFAULT_DOCKER_PROJECT_PATH}/secrets/certs` mapped to `/certs`.
- **Config**: `./config/traefik.yml` (Static) and `./dynamic` (Dynamic).

## Configuration

### Key Environment Variables

| Variable                       | Description                      | Default/Example     |
| :----------------------------- | :------------------------------- | :------------------ |
| `DEFAULT_URL`                  | Parent domain                    | `hy-home.com`       |
| `DEFAULT_DOCKER_PROJECT_PATH`          | Root host path                   | `/opt/hy-home`      |
| `HTTP_HOST_PORT`               | Host HTTP Port                   | `80`                |
| `HTTPS_HOST_PORT`              | Host HTTPS Port                  | `443`               |
| `TRAEFIK_DASHBOARD_HOST_PORT`  | Dashboard Port                   | `8080`              |

### Dashboard Security

The Traefik dashboard is protected by **basic auth** (Docker secret file mounted at `/run/secrets/traefik_basicauth_password`).

- **Endpoint**: `https://dashboard.${DEFAULT_URL}`
- **Auth**: `dashboard-auth@file` middleware (see `dynamic/middleware.yml`).

## Integration Guides

### Adding a New Service to Traefik

To expose a new service via Traefik, add the following labels to its `docker-compose.yml`:

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.myservice.rule=Host(`myservice.${DEFAULT_URL}`)"
  - "traefik.http.routers.myservice.entrypoints=websecure"
  - "traefik.http.routers.myservice.tls=true"
  - "traefik.http.services.myservice.loadbalancer.server.port=8080"
```

### SSO (OAuth2 Proxy) Integration

To protect a service with Keycloak SSO, add the `sso-auth@file` middleware to your router labels:

```yaml
labels:
  - "traefik.http.routers.myservice.middlewares=sso-auth@file"
```

## File Map

| Path                       | Description                                |
| -------------------------- | ------------------------------------------ |
| `docker-compose.yml`       | Service definition and host port bindings. |
| `config/traefik.yml`       | Static configuration (entrypoints, logs).  |
| `dynamic/middleware.yml`   | Dynamic config (SSO + basic auth middleware). |
| `dynamic/tls.yaml`         | Local TLS configuration. |
| `README.md`                | Overview and routing guides.               |

## Documentation References

- **Edge Spec**: [traefik-ingress-guide.md](../../../docs/guides/01-gateway/traefik-ingress-guide.md)
- **Operations**: [gateway-operations.md](../../../docs/guides/01-gateway/gateway-operations.md)
- **Local SSL**: [mkcert.md](../../../docs/guides/01-gateway/mkcert.md)
- **Recovery**: [2026-03-15-traefik-proxy-recovery.md](../../../docs/runbooks/2026-03-15-traefik-proxy-recovery.md)
