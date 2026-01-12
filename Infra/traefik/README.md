# Traefik Edge Router

## Overview

The main entry point (Reverse Proxy & Load Balancer) for the entire infrastructure. It handles automatic SSL (via external tools/certs), routing, and middlewares.

## Services

- **traefik**: Traefik v3 Server.
  - HTTP Port: `${HTTP_PORT}` (80)
  - HTTPS Port: `${HTTPS_PORT}` (443)
  - Dashboard Port: `${TRAEFIK_DASHBOARD_PORT}` (8080)
  - Metrics Port: `${TRAEFIK_METRICS_PORT}` (8082)
  - URL: `https://dashboard.${DEFAULT_URL}`

## Configuration

### Volumes

- `/var/run/docker.sock`: For Docker provider auto-discovery.
- `./certs`: SSL Certificates location.
- `./dynamic`: Dynamic configuration files (middlewares, routers).
- `./config/traefik.yml`: Static configuration.

## Networks

- `infra_net`
  - Fixed IP: `172.19.0.13`
  - Aliases: `auth`, `keycloak`, `whoami` domain placeholders.

## Traefik Routing

- **Dashboard**: `dashboard.${DEFAULT_URL}` (Protected by Basic Auth).
