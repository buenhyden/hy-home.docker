# OAuth2 Proxy

## Overview

A reverse proxy that provides authentication with Google, Azure, OpenID Connect and many more identity providers.

## Services

- **oauth2-proxy**: The main proxy service.
  - URL: `https://auth.${DEFAULT_URL}`
- **oauth2-proxy-valkey**: Valkey (Redis) for session storage.
- **oauth2-proxy-valkey-exporter**: Metrics exporter.

## Configuration

### Environment Variables

- `OAUTH2_PROXY_CLIENT_SECRET`: Client secret for the provider.
- `OAUTH2_PROXY_COOKIE_SECRET`: Secret for cookie encryption.
- `OAUTH2_PROXY_REDIS_CONNECTION_URL`: Redis connection string.

### Volumes

- `./config/oauth2-proxy.cfg`: Configuration file.
- `./certs/rootCA.pem`: CA certificate.

## Networks

- `infra_net`
  - oauth2-proxy: `172.19.0.28`

## Traefik Routing

- **Domain**: `auth.${DEFAULT_URL}`
