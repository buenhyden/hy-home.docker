# Traefik Edge Router

Traefik is the primary reverse proxy and load balancer for the Hy-Home infrastructure. It handles TLS termination, dynamic routing based on Docker labels, and authentication middleware integration.

## Services

| Service   | Image                    | Role                       | Resources         | Port       |
| :-------- | :----------------------- | :------------------------- | :---------------- | :--------- |
| `traefik` | `traefik:v3.3.3`         | Edge Router / Reverse Proxy| 0.5 CPU / 256MB   | 80, 443    |
| `whoami`  | `traefik/whoami:latest`  | Connection testing utility | 0.1 CPU / 64MB    | 80 (Int)   |

## Networking

Traefik binds to the host's ports 80 and 443 and routes traffic to internal services on `infra_net`.

| Local IP      | Host Port | Protocol | Purpose                  |
| :------------ | :-------- | :------- | :----------------------- |
| `172.19.0.13` | `80`      | HTTP     | Forced redirect to HTTPS |
| `172.19.0.13` | `443`     | HTTPS    | Primary entrypoint       |
| `172.19.0.13` | `8080`    | Dashboard| Traefik monitoring UI    |

## Persistence

Traefik maintains a small amount of state for ACME (SSL) certificates and logs.

- **Storage**: `acme-data` volume (tracks Let's Encrypt certificates).
- **Certificates**: Shared from `secrets/certs` for internal/manual TLS.

## Configuration

### Key Environment Variables

| Variable       | Description                       | Value                        |
| :------------- | :-------------------------------- | :--------------------------- |
| `DEFAULT_URL`  | Parent domain for all services    | e.g., `hy-home.com`          |
| `TRAEFIK_PORT` | Host port mapping for dashboard   | `${TRAEFIK_PORT}`            |

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
