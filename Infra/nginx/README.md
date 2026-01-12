# Nginx (Standalone Proxy)

## Overview

This is a standalone **Nginx** instance configured to serve as an entry point or static asset server. Unlike most services in this infrastructure which are routed via Traefik, this Nginx instance **bypasses Traefik** and exposes ports directly to the host.

## Architecture

- **Role**: Standalone Web Server / Reverse Proxy.
- **Dependency**: Waits for `minio` to be healthy before starting. This suggests it is configured to proxy requests to MinIO (e.g., serving static buckets) or serve content that depends on object storage.

## Service Details

- **Service Name**: `nginx`
- **Image**: `nginx:alpine`
- **Host Ports**:
  - **HTTP**: `${HTTP_HOST_PORT}` -> `80` (Internal)
  - **HTTPS**: `${HTTPS_HOST_PORT}` -> `443` (Internal)

  - **HTTPS**: `${HTTPS_HOST_PORT}` -> `443` (Internal)

## Environment Variables

This service relies on mounted configuration files (`nginx.conf`) rather than environment variables.

## Networking

- **Network**: `infra_net`
- **Static IPv4**: `172.19.0.13`
- **Traefik**: **Not Configured**. This service handles its own ingress/routing via standard Nginx configuration.

## Configuration & Persistence

- **Config**: `./config/nginx.conf` is mounted to `/etc/nginx/nginx.conf` (Read-Only).
- **Certificates**: `./certs` is mounted to `/etc/nginx/certs` (Read-Only).

## Usage

Access directly via the host's IP or DNS mapped to the exposed ports (defined in `.env`).

```bash
# Check logs
docker logs nginx
```
