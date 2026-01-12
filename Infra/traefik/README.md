# Traefik (Edge Router)

## Overview

The main **Reverse Proxy** and **Load Balancer** for the infrastructure. It manages routing, SSL termination (Let's Encrypt), and Authentication middlewares.

## Services

| Service | Image | Role |
| :--- | :--- | :--- |
| `traefik` | `traefik:v3.6.6` | Edge Router / Ingress Controller |

## Networking

Service runs on `infra_net` with a static IP and critical network aliases.

| Service | Static IP | Ports | Host Aliases |
| :--- | :--- | :--- | :--- |
| `traefik` | `172.19.0.13` | `80`, `443`, `8080` (Dash), `8082` (Metrics) | `keycloak.*`, `auth.*`, `whoami.*` |

## Persistence

Configuration and certificates are mounted from the host:

- **Config**: `./config/traefik.yml` → `/etc/traefik/traefik.yml`
- **Dynamic**: `./dynamic/` → `/dynamic/` (Routers, Middlewares)
- **Certs**: `./certs/` → `/certs/` (Self-signed or custom CA)

## Configuration

This service primarily uses **Static Configuration** (`traefik.yml`) and **Dynamic Configuration** (File provider in `./dynamic`).

Environment variables in `docker-compose.yml` are mainly for Port mapping.

## Traefik Integration

Traefik manages its own Dashboard routing.

- **Dashboard**: `dashboard.${DEFAULT_URL}`
- **Auth**: Protected by `dashboard-auth@file` (Basic Auth defined in dynamic config).

## Usage

1. **Dashboard**: Navigate to `https://dashboard.${DEFAULT_URL}`.
2. **Metrics**: Available at `http://172.19.0.13:8082/metrics`.
3. **Routing**: All other services in `infra/` route *through* this service via `infra_net`.
