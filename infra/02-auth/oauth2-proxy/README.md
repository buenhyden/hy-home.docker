# OAuth2 Proxy

OAuth2 Proxy is a reverse proxy and static file server that provides authentication using Providers (Google, GitHub, and others) to validate accounts by email, domain or group.

## Services

| Service        | Image                           | Role               | Resources         | Port       |
| :------------- | :------------------------------ | :----------------- | :---------------- | :--------- |
| `oauth2-proxy` | `build: ./Dockerfile`           | Auth Proxy         | 0.5 CPU / 256MB   | 4180 (Int) |

## Dependencies

- **IdP**: Typically connected to Keycloak (`infra/02-auth/keycloak`).
- **Session Store**: Uses Valkey (`mng-valkey:6379`) located in `infra/04-data/mng-db`.

## Networking

Exposed via Traefik at `auth.${DEFAULT_URL}`. Traefik uses this service as a **ForwardAuth** provider.

- **Port Mapping**: Uses `${OAUTH2_PROXY_PORT}` (usually 4180).
- **Callback**: `https://auth.${DEFAULT_URL}/oauth2/callback`.

## File Map

| Path               | Description                                                                      |
| ------------------ | -------------------------------------------------------------------------------- |
| `docker-compose.yml` | Service wiring and secrets injection (overrides entrypoint via `command:`).   |
| `config/oauth2-proxy.cfg` | Core OIDC and cookie configuration. Hardcoded to local `nip.io` dev URLs. |
| `Dockerfile`       | Multi-stage build: copies `oauth2-proxy` binary into a `valkey:alpine` base image to leverage its existing CA certificates and `sh` shell for secret injection. |
| `docker-entrypoint.sh` | Reads `mng_valkey_password` from Docker Secrets and builds the Redis connection URL before starting the proxy. |

## Documentation References

- **Integration**: [auth-procedural.md](../../../docs/guides/02-auth/auth-procedural.md)
- **Identity Flow**: [auth-context.md](../../../docs/guides/02-auth/auth-context.md)
- **SSO Guide**: [sso-oauth2-proxy-guide.md](../../../docs/guides/02-auth/sso-oauth2-proxy-guide.md)
