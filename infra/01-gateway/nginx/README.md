# Nginx Proxy

> Specialized path-based proxy and SSO client for the hy-home.docker ecosystem.

## Overview

The Nginx component in the `01-gateway` tier acts as a specialized proxy for complex path-based routing (e.g., MinIO, Keycloak) and serves as a client for SSO (OAuth2 Proxy) authentication using the `auth_request` module. It handles specific header transformations and redirects that are more efficiently managed by Nginx.

## Overview (KR)

Nginx 컴포넌트는 복잡한 경로 기반 라우팅과 SSO(OAuth2 Proxy) 인증 클라이언트 역할을 수행합니다. 특정 헤더 변환 및 리다이렉트 처리를 담당하며, Traefik 뒷단에서 정적 자산 서빙 또는 특수 프록시 규칙을 처리합니다.

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

## How to Work in This Area

1. Review `config/nginx.conf` to understand current `location` blocks and `upstream` definitions.
2. When adding a new path-based route, ensure it is added to the main `server` block in `nginx.conf`.
3. If the route requires SSO, include the `auth_request /_oauth2_auth_check;` directive.
4. After any configuration change, reload Nginx:

   ```bash
   docker exec nginx nginx -s reload
   ```

## Available Scripts

| Command                               | Description |
| ------------------------------------- | ----------- |
| `docker compose up -d`                | Start Nginx proxy |
| `docker compose down`                 | Stop Nginx proxy |
| `docker compose logs -f`              | View Nginx logs |
| `docker exec nginx nginx -t`          | Test configuration syntax |
| `docker exec nginx nginx -s reload`   | Hot-reload configuration |

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

## Related References

- [01-gateway Root README](../README.md)
- [Nginx Guide](../../../docs/07.guides/01-gateway/nginx.md)
- [Gateway Operations Policy](../../../docs/08.operations/01-gateway/nginx.md)
- [Nginx Runbook](../../../docs/09.runbooks/01-gateway/nginx.md)
- [SSO Setup Guide](../../../docs/07.guides/02-auth/README.md)

## AI Agent Guidance

1. Always run `nginx -t` before reloading configuration.
2. Ensure `X-Forwarded-Proto https` is set for upstreams to avoid redirect loops.
3. Update specific path guides in `docs/07.guides/01-gateway/nginx.md` when adding new routing logic.
