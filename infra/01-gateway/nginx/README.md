# Nginx Proxy

> Profile-only specialized path-based proxy and SSO client for the hy-home.docker ecosystem.

## Overview

The Nginx component in the `01-gateway` tier is a profile-only specialized proxy for complex path-based routing (for example, MinIO and Keycloak) and SSO checks through OAuth2 Proxy. It is not included in the current root compose stack by default; validation and runtime use require an explicit root network and dependency context.

## Overview (KR)

Nginx 컴포넌트는 복잡한 경로 기반 라우팅과 SSO(OAuth2 Proxy) 인증 클라이언트 역할을 수행하는 profile-only leaf입니다. 현재 root compose에는 기본 include되어 있지 않으므로, 실행은 명시적인 root network/dependency context와 승인된 runtime 절차가 있을 때만 다룹니다.

## Audience

이 README의 주요 독자:

- Infrastructure Engineers
- Backend Developers
- AI Agents

## Scope

### In Scope

- Path-based routing rules (e.g., `/minio/`, `/keycloak/`, `/oauth2/`).
- SSO authentication integration via `auth_request`.
- Custom header management and proxy optimizations.
- Secondary SSL/TLS termination for internal services.

### Out of Scope

- Core edge routing and global TLS orchestration (handled by Traefik).
- Global load balancing across multiple clusters.
- Permanent storage management.

## Structure

```text
nginx/
├── config/
│   └── nginx.conf    # Main configuration file (upstreams, servers, locations)
├── docker-compose.yml # Service definition and volumes
└── README.md          # This file
```

## Service Readiness

| Field | Evidence |
| --- | --- |
| Purpose | Nginx Proxy service leaf in `01-gateway`; services: `nginx`; profile-only local compose with root network/dependency requirements |
| Config files | `docker-compose.yml`, `config`, `config/nginx.conf` |
| Config values | profiles: `nginx` |
| Compose linkage | not root-included by default; local compose requires an explicit validation/runtime context for `infra_net` and backend dependencies |
| Networks | `infra_net` |
| Volumes | `./config/nginx.conf:/etc/nginx/nginx.conf:ro`, `../../../secrets/certs:/etc/nginx/certs:ro` |
| Ports | `${HTTP_HOST_PORT:-80}:${HTTP_PORT:-80}`, `${HTTPS_HOST_PORT:-443}:${HTTPS_PORT:-443}` |
| Labels | Not declared |
| Secret refs | Not declared |
| Healthcheck | Compose healthcheck declared for `nginx` |
| Operations | [Guide](../../../docs/05.operations/guides/01-gateway/nginx.md), [Policy](../../../docs/05.operations/policies/01-gateway/nginx.md), [Runbook](../../../docs/05.operations/runbooks/01-gateway/nginx.md) |
| Validation | [validate-docker-compose.sh](../../../scripts/validation/validate-docker-compose.sh); [check-repo-contracts.sh](../../../scripts/validation/check-repo-contracts.sh) |
| Troubleshooting | Start with static hardening checks; inspect service logs only when an approved Nginx runtime context is already running. |

## How to Work in This Area

1. Review `config/nginx.conf` to understand current `location` blocks and `upstream` definitions.
2. When adding a new path-based route, ensure it is added to the main `server` block in `nginx.conf`.
3. If the route requires SSO, include the `auth_request /_oauth2_auth_check;` directive.
4. After any configuration change, run `bash scripts/hardening/check-all-hardening.sh 01-gateway`; run `nginx -t` or reload only against an approved running Nginx context.

## Validation Commands

| Command | Description |
| --- | --- |
| `bash scripts/hardening/check-all-hardening.sh 01-gateway` | Verify the tracked Nginx compose/config hardening contract |
| `docker compose exec nginx nginx -t` | Runtime config lint only after an approved Nginx compose context is running |
| `docker compose exec nginx nginx -s reload` | Runtime reload only after `nginx -t` passes in the approved running context |

## Configuration

### Core Files

- `config/nginx.conf`: Defines routing logic, SSO integration, and buffer optimizations.
- `docker-compose.yml`: Mounts certificates and configuration files into the container.

### Docker Healthcheck

Nginx includes a healthcheck that verifies the availability of the `/ping` endpoint on port 80:

```yaml
healthcheck:
  test: ['CMD-SHELL', 'wget -q --spider http://localhost:${HTTP_PORT:-80}/ping || exit 1']
```

## Validation

- Run `bash scripts/hardening/check-all-hardening.sh 01-gateway` after README, compose, or config changes that affect this service.
- Run `bash scripts/validation/check-repo-contracts.sh` before marking the service documentation ready.
- Treat service-local standalone compose rendering as insufficient evidence because `nginx` depends on the root `infra_net` and backend services.

## Troubleshooting

- Start with the gateway hardening check to confirm the tracked Nginx contract still matches implementation.
- Check `nginx` container logs only when the approved runtime context is in scope, then compare routing errors with the linked operations guide.

## Related Documents

- [01-gateway Root README](../README.md)
- [Nginx Guide](../../../docs/05.operations/guides/01-gateway/nginx.md)
- [Gateway Operations Policy](../../../docs/05.operations/policies/01-gateway/nginx.md)
- [Nginx Runbook](../../../docs/05.operations/runbooks/01-gateway/nginx.md)
- [SSO Setup Guide](../../../docs/05.operations/guides/02-auth/README.md)

## AI Agent Guidance

1. Always run `nginx -t` in the approved running context before reloading configuration.
2. Ensure `X-Forwarded-Proto https` is set for upstreams to avoid redirect loops.
3. Update specific path guides in `docs/05.operations/guides/01-gateway/nginx.md` when adding new routing logic.
