# Traefik Edge Router

> Primary edge router with dynamic service discovery and TLS orchestration for the hy-home.docker ecosystem.

## Overview (KR)

Traefik은 `hy-home.docker` 생태계의 주 에지 라우터입니다. Docker 프로바이더를 통한 동적 서비스 탐색, 자동 TLS 종료, 그리고 트래픽 모니터링 및 관리를 위한 대시보드를 제공합니다.

---

## Audience

이 README의 주요 독자:

- Infrastructure Engineers
- SREs
- AI Agents

## Scope

### In Scope

- Global entrypoint definition (`web` 80, `websecure` 443, `metrics` 8082).
- Dynamic service discovery and routing labels via Docker Provider.
- Middleware orchestration (RateLimit, BasicAuth, SSO).
- TLS Store and Certificate management.
- Observability integration (Prometheus metrics, OTLP tracing).

### Out of Scope

- Application-level business logic.
- Detailed path-based rewrites (partially delegated to Nginx).
- Individual service container definitions (managed in their respective infra folders).

## Structure

```text
traefik/
├── config/
│   └── traefik.yml     # Static configuration (entrypoints, providers, API)
├── dynamic/
│   ├── middleware.yml  # Shared middlewares (SSO, RateLimit, BasicAuth)
│   └── tls.yaml        # TLS certificate mapping and stores
├── docker-compose.yml  # Service definition and deployment
└── README.md           # This file
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Traefik Edge Router service leaf in `01-gateway`; services: `traefik`; root include active via [root docker-compose.yml](../../../docker-compose.yml) -> `infra/01-gateway/traefik/docker-compose.yml` |
| Config files | `docker-compose.yml`, `config`, `config/README.md`, `config/traefik.yml` |
| Config values | profiles: `core`, `dev` |
| Compose linkage | root include active via [root docker-compose.yml](../../../docker-compose.yml) -> `infra/01-gateway/traefik/docker-compose.yml` |
| Networks | `k3d-hyhome`, `infra_net` |
| Volumes | `/var/run/docker.sock:/var/run/docker.sock:ro`, `../../../secrets/certs:/certs:ro`, `./dynamic:/dynamic:ro`, `./config/traefik.yml:/etc/traefik/traefik.yml:ro` |
| Ports | `${HTTP_HOST_PORT:-80}:${HTTP_PORT:-80}`, `${HTTPS_HOST_PORT:-443}:${HTTPS_PORT:-443}` |
| Labels | `hy-home.tier`, `traefik.enable`, `traefik.http.routers.dashboard.rule`, `traefik.http.routers.dashboard.entrypoints`, `traefik.http.routers.dashboard.tls`, `traefik.http.routers.dashboard.service`, `traefik.http.routers.dashboard.middlewares` |
| Secret refs | names: `traefik_basicauth_password`, `traefik_opensearch_basicauth_password`; mounts: `/run/secrets/traefik_basicauth_password`, `/run/secrets/traefik_opensearch_basicauth_password` |
| Healthcheck | Compose healthcheck declared for `traefik` |
| Operations | [Guide](../../../docs/05.operations/guides/01-gateway/traefik.md), [Policy](../../../docs/05.operations/policies/01-gateway/traefik.md), [Runbook](../../../docs/05.operations/runbooks/01-gateway/traefik.md) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with root profile validation and gateway hardening checks, then inspect service logs only when the Traefik runtime is already approved and running. |

## How to Work in This Area

1. Start by reviewing `config/traefik.yml` to understand the core routing entrypoints.
2. Check `dynamic/middleware.yml` when adding authentication or rate-limiting to a new service.
3. Use labels in your service's `docker-compose.yml` to register routes with Traefik.
4. After any configuration change, run the root profile validator and the gateway hardening check before using runtime dashboard evidence.

## Configuration

### Core Files

- `config/traefik.yml`: Static configuration (entrypoints, providers, API).
- `dynamic/middleware.yml`: Shared middlewares (SSO/ForwardAuth, RateLimit, BasicAuth).
- `dynamic/tls.yaml`: TLS certificate mapping and stores.

### Docker Healthcheck

Traefik is configured with a built-in healthcheck using its internal ping endpoint:

```yaml
healthcheck:
  test: ['CMD', 'traefik', 'healthcheck', '--ping']
  interval: 15s
  timeout: 30s
  retries: 5
```

### Keycloak & OAuth2 Proxy Integration

Traefik uses the `ForwardAuth` middleware (`sso-auth@file`) to delegate authentication to OAuth2 Proxy:

1. Entrypoint: `websecure` (Port 443).
2. Middleware: `sso-auth@file` -> `http://oauth2-proxy:4180/oauth2/auth`.
3. Error Redirect: `sso-errors@file` handles 401/403 redirects to `/oauth2/sign_in`.

## AI Agent Operation Policy

- **Required**: Any dynamic routing change must be verified via the Traefik Dashboard.
- **Caution**: Do not modify `traefik.yml` entrypoints without a full cluster impact analysis.
- **Validation**: Use static validation first; inspect Traefik logs only for an approved running stack.

### Environment Variables

| Variable          | Required | Description |
| ----------------- | -------: | ----------- |
| `DEFAULT_URL`     |      Yes | Primary domain (e.g., localhost or your-domain.com) |
| `HTTP_HOST_PORT`  |       No | Host port for HTTP (default: 80) |
| `HTTPS_HOST_PORT` |       No | Host port for HTTPS (default: 443) |

## Validation

| Command | Description |
| --- | --- |
| `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh` | Validate the root-included Traefik compose context |
| `bash scripts/hardening/check-all-hardening.sh 01-gateway` | Verify gateway hardening contracts |
| `docker compose ps traefik` | Runtime state check only after an approved root stack is running |
| `docker compose exec traefik traefik healthcheck --ping` | Runtime health check only after an approved root stack is running |

- Run `HYHOME_COMPOSE_PROFILES=core bash scripts/validation/validate-docker-compose.sh` after Traefik compose or config reference changes.
- Run `bash scripts/hardening/check-all-hardening.sh 01-gateway` before marking documentation ready.
- Verify routing configuration in the Traefik dashboard only after the approved root runtime is running.
- Confirm TLS and middleware behavior from sanitized Traefik logs only after runtime approval.

## Troubleshooting

- Start with the root `core` profile validator to confirm routers, networks, secrets, and mounted dynamic config paths render.
- Check `traefik` container logs only when runtime evidence is in scope, then compare router or middleware failures with the linked gateway operations guide.

## Related Documents

- [01-gateway Root README](../README.md)
- [Traefik Guide](../../../docs/05.operations/guides/01-gateway/traefik.md)
- [Gateway Operations Policy](../../../docs/05.operations/policies/01-gateway/traefik.md)
- [Traefik Runbook](../../../docs/05.operations/runbooks/01-gateway/traefik.md)
- [Traefik Dashboard](https://dashboard.${DEFAULT_URL:-localhost}) (Internal)
