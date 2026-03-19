---
layer: infra
---

# Gateway Lifecycle and Procedural Guide

Standard procedures for managing the infrastructure gateways (Traefik/Nginx).

## 1. Service Control

All gateways are managed via Docker Compose.

```bash
# Start Traefik (Primary)
docker compose -f infra/01-gateway/traefik/docker-compose.yml up -d

# Start Nginx (Secondary/Path-based)
docker compose -f infra/01-gateway/nginx/docker-compose.yml up -d
```

## 2. Configuration Reloading

### Dynamic Config (No Restart)

Traefik automatically reloads any changes made to `infra/01-gateway/traefik/dynamic/*.yml`.

### Static Config (Restart Required)

Changes to `traefik.yml` or `docker-compose.yml` require a service restart.

## 3. Certificate Management

The system uses `mkcert` for local TLS.

### Initial Creation/Renewal

Reference the [mkcert guide](./mkcert.md) for generation commands.

### Rotation Procedure

1. Generate new certs in `secrets/certs/`.
2. Traefik will detect changes to mounted files and hot-reload.
3. If Nginx is used, it must be reloaded: `docker exec nginx nginx -s reload`.

## 4. Verification

Check Traefik health:

```bash
docker exec traefik traefik healthcheck --ping
```

### Observability Verification

Verify metrics endpoint is active:

```bash
# From within infra_net
curl http://traefik:8082/metrics
```

### Gateway Switching

Since both Traefik and Nginx bind to host ports 80/443 by default:

1. Stop the active gateway: `docker compose -f infra/01-gateway/<current>/docker-compose.yml stop`
2. Start the target gateway: `docker compose -f infra/01-gateway/<target>/docker-compose.yml up -d`
