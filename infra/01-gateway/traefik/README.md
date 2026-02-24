# Traefik Edge Router

Traefik is the primary reverse proxy and load balancer for the Hy-Home infrastructure. It handles TLS termination, dynamic routing based on Docker labels, and authentication middleware integration.

## Services

| Service   | Image                    | Role                       | Resources         | Port       |
| :-------- | :----------------------- | :------------------------- | :---------------- | :--------- |
| `traefik` | `traefik:v3.6.8`         | Edge Router / Reverse Proxy| 1.0 CPU / 1GB RAM | 80, 443    |

## Networking

Traefik binds to the host's ports (configurable via `.env`) and routes traffic via `infra_net`.

| Local IP      | Host Port                        | Protocol | Purpose                  |
| :------------ | :------------------------------- | :------- | :----------------------- |
| `172.19.0.13` | `${HTTP_HOST_PORT}` (80)         | HTTP     | Forced redirect to HTTPS |
| `172.19.0.13` | `${HTTPS_HOST_PORT}` (443)       | HTTPS    | Primary entrypoint       |
| `172.19.0.13` | `${TRAEFIK_DASHBOARD_HOST_PORT}`| Dashboard| Traefik monitoring UI    |
| `172.19.0.13` | `${TRAEFIK_METRICS_HOST_PORT}`  | Metrics  | Prometheus scraping      |

## Persistence

Traefik maintains state for certificates and dynamic configurations.

- **Certs**: `${DEFAULT_DOCKER_PATH}/secrets/certs` mapped to `/certs`.
- **Config**: `./config/traefik.yml` (Static) and `./dynamic` (Dynamic).

## Configuration

### Key Environment Variables

| Variable                       | Description                      | Default/Example     |
| :----------------------------- | :------------------------------- | :------------------ |
| `DEFAULT_URL`                  | Parent domain                    | `hy-home.com`       |
| `DEFAULT_DOCKER_PATH`          | Root host path                   | `/opt/hy-home`      |
| `HTTP_HOST_PORT`               | Host HTTP Port                   | `80`                |
| `HTTPS_HOST_PORT`              | Host HTTPS Port                  | `443`               |
| `TRAEFIK_DASHBOARD_HOST_PORT`  | Dashboard Port                   | `8080`              |

### Dashboard Security

The Traefik dashboard is protected by **basic auth** (credentials in `secrets/traefik_auth.txt`).

- **Endpoint**: `https://traefik.${DEFAULT_URL}`
- **Auth**: `traefik-auth` middleware (applied via labels).

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
| `config/dynamic_conf.yml`  | Dynamic config (SSO middleware, manual TLS)|
| `config/acme.json`         | Auto-generated Let's Encrypt certificates. |
| `README.md`                | Overview and routing guides.               |

> **Note**: This component's local documentation has been migrated to the global repository standards to enforce Spec-Driven Development boundaries.

Please refer to the following global documentation directories for information regarding this service:

- **Architecture & Topology**: [docs/architecture](../../../docs/architecture)
- **Configuration & Setup Guides**: [docs/guides](../../../docs/guides)
- **Routine Operations**: [operations/](../../../operations)
- **Troubleshooting & Recovery**: [runbooks/](../../../runbooks)
