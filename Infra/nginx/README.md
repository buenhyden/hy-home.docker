# Nginx (Standalone Proxy)

## Overview

This is a standalone **Nginx** instance configured to serve as an entry point or static asset server. Unlike most services in this infrastructure which are routed via Traefik, this Nginx instance **bypasses Traefik** and exposes ports directly to the host.

## Services

- **Service Name**: `nginx`
- **Image**: `nginx:alpine`
- **Role**: Standalone Web Server / Reverse Proxy
- **Restart Policy**: `(implied default)` (Configured with deploy limits)
- **Dependency**: Waits for `minio` (likely for static bucket serving).

## Networking

This service runs on the `infra_net` network and exposes ports directly to the host:

- **Network**: `infra_net`
- **Static IPv4**: `172.19.0.13`
- **Traefik**: **Not Configured**. This service handles its own ingress/routing via standard Nginx configuration.

| Port Type | Internal | Host Port |
| :--- | :--- | :--- |
| **HTTP** | `80` | `${HTTP_HOST_PORT}` |
| **HTTPS** | `443` | `${HTTPS_HOST_PORT}` |

## Persistence

- **Config**: `./config/nginx.conf` → `/etc/nginx/nginx.conf` (Read-Only)
- **Certificates**: `./certs` → `/etc/nginx/certs` (Read-Only)

## Configuration

This service relies primarily on mounted configuration files. However, ports are configured via environment variables.

### Environment Variables

| Variable | Description |
| :--- | :--- |
| `HTTP_HOST_PORT` | Host port mapped to container port 80 |
| `HTTPS_HOST_PORT`| Host port mapped to container port 443 |
| `HTTP_PORT` | Container internal port usually 80 |
| `HTTPS_PORT` | Container internal port usually 443 |

## Usage

Access directly via the host's IP or DNS mapped to the exposed ports.

```bash
# Check logs
docker logs nginx
```
