# OAuth2 Proxy

**OAuth2 Proxy** is a reverse proxy and static file server that provides authentication using Providers (Google, GitHub, and others) to validate accounts by email, domain or group.

In this infrastructure, it serves as the central **Single Sign-On (SSO)** provider, protecting other services (like MailHog, RedisInsight, etc.) via Traefik middleware.

## Services

| Service | Image | Description |
| :--- | :--- | :--- |
| `oauth2-proxy` | `quay.io/oauth2-proxy/oauth2-proxy:v7.8.1-amd64` | The core authentication proxy. |
| `oauth2-proxy-valkey` | `bitnami/valkey:8.0` | Redis-compatible session store for OAuth2 Proxy. |
| `oauth2-proxy-valkey-exporter` | `bitnami/redis-exporter:latest` | Prometheus exporter for Valkey metrics. |

## Network Configuration

Services are attached to the `infra_net` network with static IPs:

| Service | IP Address |
| :--- | :--- |
| `oauth2-proxy` | `172.19.0.28` |
| `oauth2-proxy-valkey` | `172.19.0.18` |

## Configuration

The service is configured primarily via the configuration file mounted at `/etc/oauth2-proxy.cfg`.

### Environment Variables

| Variable | Description |
| :--- | :--- |
| `OAUTH2_PROXY_CLIENT_ID` | The OAuth2 Client ID (from `.env`). |
| `OAUTH2_PROXY_CLIENT_SECRET` | The OAuth2 Client Secret (from `.env`). |
| `OAUTH2_PROXY_REDIS_CONNECTION_URL` | Connection string for the Valkey session store (e.g., `redis://oauth2-proxy-valkey:6379`). |

### Valkey Configuration

- **Password**: Empty password allowed (`ALLOW_EMPTY_PASSWORD=yes`).
- **Persistence**: Data is stored in the `oauth2-proxy-valkey-data` volume.

## Traefik Integration

The proxy is exposed as `auth.${DEFAULT_URL}` and is used as a middleware by other services.

- **Router**: `oauth2-proxy`
- **Rule**: `Host("auth.${DEFAULT_URL}")`
- **Middleware**: Services use `sso-auth@file` (or similar, defined in dynamic config) which points to this service's `/oauth2/auth` endpoint.

## Usage

Access `https://auth.yourdomain.com` to sign in. Once authenticated, the session is stored in Valkey, and you can access other protected services transparently.
