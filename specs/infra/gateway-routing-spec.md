# Gateway Routing Specification & Operations

> **Component**: `traefik`, `nginx`

## Overview

Edge ingress and routing services for the stack. **Traefik** is the default gateway. **Nginx** is an optional standalone proxy for path-based routing, caching, or custom auth flow testing.

## Startup

```bash
# Core gateway
docker compose up -d traefik

# Optional standalone gateway
docker compose --profile nginx up -d nginx
```

## Traefik Usage

### 1. Adding a New Service

To expose a Docker container via Traefik, add labels to its `docker-compose.yml`:

```yaml
labels:
  - 'traefik.enable=true'
  - 'traefik.http.routers.my-service.rule=Host(`service.${DEFAULT_URL}`)'
  - 'traefik.http.routers.my-service.entrypoints=websecure'
  - 'traefik.http.routers.my-service.tls=true'
  - 'traefik.http.services.my-service.loadbalancer.server.port=3000'
```

### 2. Enabling SSO

To protect a service with Keycloak SSO (via OAuth2 Proxy), add the middleware:

```yaml
labels:
  - 'traefik.http.routers.my-service.middlewares=sso-auth@file'
```

## Nginx Usage

### 1. Direct Access

Access services via the host machine's IP or DNS mapping using path-based URLs:

- `https://localhost:${HTTPS_HOST_PORT}/keycloak/`
- `https://localhost:${HTTPS_HOST_PORT}/minio-console/`

### 2. Monitoring Logs

```bash
# Monitor access/error logs
docker logs -f nginx
```
