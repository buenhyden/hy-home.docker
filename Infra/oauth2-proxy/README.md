# OAuth2 Proxy

## Overview

A reverse proxy that provides authentication with Google, GitHub, or other providers, often used with Traefik `forwardAuth` middleware.

## Service Details

- **Image**: `quay.io/oauth2-proxy/oauth2-proxy:v7.13.0`
- **Session Store**: `oauth2-proxy-valkey` (Redis).
- **Configuration**: `/etc/oauth2-proxy.cfg`

## Environment Variables

- `OAUTH2_PROXY_CLIENT_SECRET`
- `OAUTH2_PROXY_COOKIE_SECRET`
- `OAUTH2_PROXY_REDIS_CONNECTION_URL`

## Traefik Configuration

- **Domain**: `auth.${DEFAULT_URL}`
- **Port**: `${OAUTH2_PROXY_PORT}` (4180)
- **Usage**: Used as an authentication provider for other services via Traefik Middleware (e.g., `sso-auth`).
