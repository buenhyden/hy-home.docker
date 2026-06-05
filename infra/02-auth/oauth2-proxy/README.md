# OAuth2 Proxy

> OIDC ForwardAuth gateway for protecting backend services within the `hy-home.docker` ecosystem.

## Overview

OAuth2 Proxy provides a generic authentication layer for services that do not have built-in OIDC support. It interacts with Keycloak to verify user sessions and manages session state using Valkey. It is integrated into the Traefik ecosystem as a ForwardAuth provider, ensuring centralized SSO across all protected subdomains.

## Audience

이 README의 주요 독자:

- Developers (Integrating new backends with SSO)
- Operators (Session troubleshooting & secret rotation)
- AI Agents (Label configuration & label-based middleware setup)

## Scope

### In Scope

- OAuth2 Proxy configuration (`oauth2-proxy.cfg`)
- ForwardAuth workflow integration with Traefik
- Valkey session storage connectivity and persistence
- Custom Docker build based on Alpine for security and stability

### Out of Scope

- User identity management (handled by Keycloak)
- SSL Certificate issuance (handled by Traefik/Cert-manager)
- Granular application-level RBAC (handled by backends)

## Structure

```text
oauth2-proxy/
├── config/             # Proxy configuration (oauth2-proxy.cfg)
├── Dockerfile          # Custom Alpine-based build
├── dev.Dockerfile      # Root-active build using mng-valkey sessions
├── docker-entrypoint.sh # Secret/Env injection script
├── docker-entrypoint.dev.sh # Root-active secret/Env injection script
├── docker-compose.dev.yml # Root include active compose leaf
├── docker-compose.yml  # Container orchestration
└── README.md           # This file
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | OAuth2 Proxy service leaf in `02-auth`; root include active via [root docker-compose.yml](../../../docker-compose.yml) -> `infra/02-auth/oauth2-proxy/docker-compose.dev.yml`; local/full leaf: `docker-compose.yml` |
| Config files | `docker-compose.dev.yml`, `docker-compose.yml`, `Dockerfile`, `dev.Dockerfile`, `docker-entrypoint.sh`, `docker-entrypoint.dev.sh`, `config/oauth2-proxy.cfg` |
| Config values | env keys: `SSL_CERT_FILE`, `OAUTH2_PROXY_SESSION_STORE_TYPE`, `OAUTH2_PROXY_REDIS_CONNECTION_URL`, `OAUTH2_PROXY_CLIENT_ID`, `OAUTH2_PROXY_OIDC_ISSUER_URL`, `OAUTH2_PROXY_REDIRECT_URL`, `OAUTH2_PROXY_COOKIE_DOMAINS`, `OAUTH2_PROXY_WHITELIST_DOMAINS`; profiles: `core`, `auth`, `dev` |
| Compose linkage | root-active dev leaf uses `mng-valkey`; local/full leaf includes `oauth2-proxy-valkey` and `oauth2-proxy-valkey-exporter` |
| Networks | `infra_net` |
| Volumes | `./config/oauth2-proxy.cfg:/etc/oauth2-proxy.cfg:ro`, `../../../secrets/certs/rootCA.pem:/etc/ssl/certs/rootCA.pem:ro`, `oauth2-proxy-valkey-data`, `oauth2-proxy-valkey-data:/data` |
| Ports | `${VALKEY_PORT:-6379}`, `${VALKEY_EXPORTER_PORT:-9121}` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.oauth2-proxy.rule`, `traefik.docker.network`, `traefik.http.routers.oauth2-proxy.entrypoints`, `traefik.http.routers.oauth2-proxy.service`, `traefik.http.routers.oauth2-proxy.tls`, `traefik.http.routers.oauth2-proxy.middlewares`, plus 1 more |
| Secret refs | names: `mng_valkey_password`, `oauth2_proxy_client_secret`, `oauth2_proxy_cookie_secret`, `oauth2_valkey_password`; mounts: `/run/secrets/mng_valkey_password`, `/run/secrets/oauth2_proxy_client_secret`, `/run/secrets/oauth2_proxy_cookie_secret`, `/run/secrets/oauth2_valkey_password` |
| Healthcheck | Compose healthcheck declared for `oauth2-proxy`, `oauth2-proxy`, `oauth2-proxy-valkey`; not declared for `oauth2-proxy-valkey-exporter` |
| Operations | [Guide](../../../docs/05.operations/guides/02-auth/oauth2-proxy.md), [Policy](../../../docs/05.operations/policies/02-auth/oauth2-proxy.md), [Runbook](../../../docs/05.operations/runbooks/02-auth/oauth2-proxy.md) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with `docker compose config`, then inspect service logs and linked operations/runbook evidence. |

## How to Work in This Area

1. Read the [Auth Guides](../../../docs/05.operations/guides/02-auth/README.md) for OIDC/ForwardAuth configuration.
2. Refer to the [OAuth2 Proxy Guide](../../../docs/05.operations/guides/02-auth/oauth2-proxy.md) for detailed configuration steps.
3. Check `config/oauth2-proxy.cfg` for runtime provider and cookie settings.
4. Use the [Auth Runbook](../../../docs/05.operations/runbooks/02-auth/README.md) for cookie secret rotation procedures.

## Tech Stack

| Category | Technology         | Notes                    |
| -------- | ------------------ | ------------------------ |
| Proxy    | OAuth2 Proxy (Go)  | `quay.io/oauth2-proxy/oauth2-proxy:v7.15.2` copied into Alpine |
| Session  | Valkey             | Redis-compatible storage |
| Protocol | OIDC / ForwardAuth | Keycloak & Traefik       |
| Runtime  | Alpine Linux       | Minimal footprint        |

## Configuration

### Environment Variables

| Variable                     | Required | Description                            |
| ---------------------------- | -------: | -------------------------------------- |
| `OAUTH2_PROXY_CLIENT_ID`     |      Yes | OIDC Client ID from Keycloak           |
| `OAUTH2_PROXY_COOKIE_SECRET` |      Yes | Cookie encryption key (32-byte string) |
| `OAUTH2_PROXY_CLIENT_SECRET` |      Yes | Client secret from Keycloak            |

### Secrets Injection

Secrets are injected via `docker-entrypoint.sh` from `/run/secrets/`:

- `oauth2_proxy_cookie_secret`
- `oauth2_proxy_client_secret`
- `mng_valkey_password` in the root-active dev leaf
- `oauth2_valkey_password` in the local/full leaf

## Testing

### Healthcheck Configuration

The service uses `wget` to perform a health check against the `/ping` endpoint:

```yaml
healthcheck:
  test: ['CMD-SHELL', 'wget -qO- http://127.0.0.1:4180/ping >/dev/null 2>&1 || exit 1']
  interval: 30s
  timeout: 10s
  retries: 3
```

### Manual Verification

```bash
# Validate the root auth profile and 02-auth hardening contract
HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh 02-auth

# Runtime-only checks after the auth profile is already running
docker compose --profile auth exec oauth2-proxy wget -qO- http://127.0.0.1:4180/ping
docker compose --profile auth logs oauth2-proxy --tail=200 | grep "OIDC"
```

## Validation

- Run `HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh` after any Compose or config reference changes.
- Run `bash scripts/hardening/check-all-hardening.sh 02-auth` before marking documentation ready.
- Verify OIDC ForwardAuth forwarding by checking `docker compose --profile auth logs oauth2-proxy --tail=200 | grep "OIDC"` after config changes.
- Confirm cookie and session connectivity by verifying the `/ping` runtime endpoint from the root compose context.

## Troubleshooting

- Start with `HYHOME_COMPOSE_PROFILES=auth bash scripts/validation/validate-docker-compose.sh` to confirm root-context network, volume, secret, and label references render correctly.
- Check container logs and the linked runbook before changing configuration or secret references.
- For OIDC errors: verify `OAUTH2_PROXY_CLIENT_ID` matches the Keycloak client and `redirect_url` is synchronized.
- For session errors: confirm `mng_valkey_password` is injected in the root-active dev leaf, or `oauth2_valkey_password` is injected in the local/full leaf.
- For ForwardAuth failures: check Traefik middleware labels reference `auth.${DEFAULT_URL}` and the upstream config is correct.

## Related Documents

- [Keycloak](../keycloak/README.md) - The Identity Provider.
- [01-gateway](../../01-gateway/README.md) - Traefik route configuration.
- [docs/05.operations/02-auth/oauth2-proxy.md](../../../docs/05.operations/guides/02-auth/oauth2-proxy.md) - Session policies.

## AI Agent Guidance

1. 이 README를 먼저 읽고 Traefik 레이블 설정을 확인한다.
2. 새로운 서비스 추가 시 `forwardauth` 미들웨어를 `auth.${DEFAULT_URL}` 경로로 설정한다.
3. `OAUTH2_PROXY_COOKIE_SECRET` 변경 시 모든 세션이 초기화됨을 인지한다.
4. `config/oauth2-proxy.cfg`의 `redirect_url`과 Keycloak 클라이언트 설정을 동기화한다.
