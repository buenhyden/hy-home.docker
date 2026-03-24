---
layer: infra
---

# Gateway Tier: Procedural & Lifecycle Guides

This guide covers the operational lifecycle of the edge routing and proxy stack.

## Service Management

All gateways are managed via Docker Compose. Use the appropriate profile to start the desired service.

```bash
# Start Traefik (Primary - core profile)
docker compose up -d traefik

# Start Nginx (Secondary - nginx profile)
docker compose up -d nginx
```

## Configuration Updates

### Dynamic Updates (No Restart)
Traefik automatically reloads any changes made to `infra/01-gateway/traefik/dynamic/*.yml`. This includes:
- Middleware definitions.
- TLS options and certificate locations.
- Manual router/service overrides.

### Static Updates (Restart Required)
Changes to the following require a service restart:
- `infra/01-gateway/traefik/config/traefik.yml` (Static config).
- `infra/01-gateway/*/docker-compose.yml` (Service structure/ports).

```bash
docker compose restart traefik
```

## Certificate Management

The system uses `mkcert` for local TLS development.

1. **Generation**: Generate certificates using the `generate-local-certs.sh` script or manually in `secrets/certs/`.
2. **Detection**: Traefik monitor the `secrets/certs/` directory and hot-reloads when files change.
3. **Nginx Integration**: If using Nginx, certificates must be reloaded manually if the container is already running:
   ```bash
   docker exec nginx nginx -s reload
   ```

## Verification & Health

Always verify the gateway status after any significant change.

### Connectivity Checks

```bash
# Verify HTTP to HTTPS redirect
curl -I http://localhost

# Verify HTTPS access
curl -kI https://localhost
```

### Health Diagnostics
| Component | Action | Purpose |
| :--- | :--- | :--- |
| **Traefik** | `docker exec traefik traefik healthcheck --ping` | Verify internal health state. |
| **Traefik** | `curl http://localhost:8082/metrics` | Inspect Prometheus metrics. |
| **Nginx** | `docker exec nginx nginx -t` | Validate configuration syntax. |
| **Logs** | `docker compose logs -f traefik` | Monitor real-time routing events. |

## Failover Procedures

Since both Traefik and Nginx bind to host ports 80 and 443, only one can be active at a time for these ports.

1. **Stop Active**: `docker compose stop traefik` (or `nginx`).
2. **Start Target**: `docker compose up -d nginx` (or `traefik`).
3. **Validate**: Perform the connectivity checks listed above.
