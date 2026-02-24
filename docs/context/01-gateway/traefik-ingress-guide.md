# Traefik Ingress Controller Guide

> **Component**: `traefik`
> **Internal DNS**: `traefik`
> **Administrative Node**: `infra-gateway`

## 1. Role and Architecture

Traefik serves as the primary Ingress Controller for the entire `infra_net`. It handles TLS termination, dynamic routing based on Docker labels, and security middleware orchestration.

- **Frontend Port**: `80`, `443` (HTTP/HTTPS)
- **Dashboard**: `https://traefik.${DEFAULT_URL}` (Protected by SSO)

## 2. Standard Routing Pattern

New services should implement these labels for automatic exposure:

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.<name>.rule=Host('<subdomain>.${DEFAULT_URL}')"
  - "traefik.http.routers.<name>.tls=true"
  - "traefik.http.services.<name>.loadbalancer.server.port=<internal_port>"
```

## 3. Dynamic Configuration Hub

All non-label based configs (Middlewares, Transport settings) reside in the `./dynamic/` directory within the Traefik service folder.

- **Middlewares**: `sso-auth@file`, `compression@file`
- **ServersTransports**: `insecureTransport@file` (Used for internal self-signed backend SSL)

## 4. Operational Maintenance

### Reloading Configs

Traefik watches files in `/dynamic` for changes. Restarts are only necessary for core static flag modifications.

```bash
# Graceful restart of the gateway
docker compose -f infra/01-gateway/traefik/docker-compose.yml restart
```
