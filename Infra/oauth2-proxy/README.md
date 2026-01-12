# OAuth2 Proxy

## Overview

**OAuth2 Proxy** is a reverse proxy and static file server that provides authentication using Providers (Google, GitHub, and others) to validate accounts by email, domain or group.

In this infrastructure, it serves as the central **Single Sign-On (SSO)** provider, protecting other services (like MailHog, RedisInsight, etc.) via Traefik middleware.

## Services

- **Service Name**: `oauth2-proxy`
- **Image**: `quay.io/oauth2-proxy/oauth2-proxy:v7.13.0`
- **Role**: Core Authentication Proxy
- **Restart Policy**: `unless-stopped`

- **Service Name**: `oauth2-proxy-valkey`
- **Image**: `valkey/valkey:9.0.1-alpine`
- **Role**: Redis-compatible session store
- **Restart Policy**: `unless-stopped`

- **Service Name**: `oauth2-proxy-valkey-exporter`
- **Image**: `oliver006/redis_exporter:v1.80.1-alpine`
- **Role**: Prometheus Metrics Exporter
- **Restart Policy**: `unless-stopped`

## Networking

Services are authorized to the `infra_net` network with **Static IPs**:

| Service | Role | Static IPv4 | Port |
| :--- | :--- | :--- | :--- |
| `oauth2-proxy` | Auth Proxy | `172.19.0.28` | `${OAUTH2_PROXY_PORT}` |
| `oauth2-proxy-valkey` | Session Store | `172.19.0.18` | `${VALKEY_PORT}` |
| `oauth2-proxy-valkey-exporter` | Metrics | `172.19.0.19` | `${VALKEY_EXPORTER_PORT}` |

## Persistence

- **Config**: `./config/oauth2-proxy.cfg` → `/etc/oauth2-proxy.cfg` (Read-Only)
- **Certificates**: `./certs/rootCA.pem` → `/etc/ssl/certs/rootCA.pem` (Read-Only)
- **Session Data**: `oauth2-proxy-valkey-data` → `/data` (Valkey Persistence)

## Configuration

The service is configured purely via environment variables and a mounted config file.

### Environment Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `SSL_CERT_FILE` | Trusted Root CA for internal requests | `/etc/ssl/certs/rootCA.pem` |
| `OAUTH2_PROXY_CLIENT_SECRET` | OAuth2 Client Secret | `${OAUTH2_PROXY_CLIENT_SECRET}` |
| `OAUTH2_PROXY_COOKIE_SECRET` | Cookie encryption secret | `${OAUTH2_PROXY_COOKIE_SECRET}` |
| `OAUTH2_PROXY_REDIS_CONNECTION_URL` | Redis session store URL | `redis://...` |

### Valkey Configuration

- **Password**: Managed via Docker Secrets (`valkey_password`).
- **Persistence**: Append-only file enabled.

## Traefik Integration

The proxy is exposed as `auth.${DEFAULT_URL}` and is used as a middleware by other services.

- **Router**: `oauth2-proxy`
- **Url**: `https://auth.${DEFAULT_URL}`
- **Entrypoint**: `websecure` (TLS Enabled)
- **Middleware**: Services use `forward-auth` (or similar) pointing to this service.

## Usage

Access `https://auth.${DEFAULT_URL}` to sign in. Once authenticated, the session is stored in Valkey, and you can access other protected services transparently.
