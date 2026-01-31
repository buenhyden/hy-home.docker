# Gateway (01-gateway)

## Overview

Edge ingress and routing services for the stack. **Traefik** is the default gateway. **Nginx** is an optional standalone proxy for path-based routing, caching, or custom auth flow testing.

## Services

| Service | Profile | Path | Purpose |
| --- | --- | --- | --- |
| Traefik | (core) | `./traefik` | Primary reverse proxy, TLS, routing, SSO middleware |
| Nginx | `nginx` | `./nginx` | Optional standalone proxy (path-based routing) |

## Run

```bash
# Core gateway
docker compose up -d traefik

# Optional standalone gateway
docker compose --profile nginx up -d nginx
```

## Notes

- **Traefik and Nginx both use static IP `172.19.0.13`** on `infra_net`. Do not run them together unless you change one of the IPs.
- TLS assets are shared from `secrets/certs`.

## File Map

| Path | Description |
| --- | --- |
| `traefik/` | Traefik router and dynamic config. |
| `nginx/` | Optional standalone Nginx gateway. |
| `README.md` | Category overview. |
