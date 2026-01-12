# Traefik (Edge Router)

## Overview

The main Reverse Proxy and Load Balancer for the infrastructure. It manages routing, SSL termination (Let's Encrypt), and Authentication middlewares.

## Service Details

- **Image**: `traefik:v3.6.6`
- **Configuration**: `/etc/traefik/traefik.yml` (Static) and `/dynamic` (Dynamic).
- **Ports**:
  - `80` (HTTP) redirect to HTTPS
  - `443` (HTTPS)
  - `8080` (Dashboard)
  - `8082` (Metrics)

## Dashboard

- **Domain**: `dashboard.${DEFAULT_URL}`
- **Auth**: Protected by `dashboard-auth@file` (Basic Auth).

## Network

- **IP**: `172.19.0.13` (Static) on `infra_net`.
- **Aliases**: `keycloak.${DEFAULT_URL}`, `auth.${DEFAULT_URL}`, `whoami.${DEFAULT_URL}`.
