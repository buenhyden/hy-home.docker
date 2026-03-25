# Nginx Proxy

> Specialized path-based proxy and SSO client.

## Overview

The Nginx component in the `01-gateway` tier acts as a specialized proxy for complex path-based routing and serves as a client for SSO (OAuth2 Proxy) authentication. It handles specific header transformations and redirects that are more efficiently managed by Nginx.

## Overview (KR)

Nginx 컴포넌트는 복잡한 경로 기반 라우팅과 SSO(OAuth2 Proxy) 인증 클라이언트 역할을 수행합니다. 특정 헤더 변환 및 리다이렉트 처리를 담당하며, Traefik 뒷단에서 정적 자산 서빙 또는 특수 프록시 규칙을 처리합니다.

## Audience

- Infrastructure Engineers
- Backend Developers
- AI Agents

## Scope

### In Scope

- Path-based routing rules (e.g., `/minio/`, `/keycloak/`).
- SSO authentication integration (auth_request).
- Static asset serving (if configured).
- SSL/TLS certificate mapping for secondary termination.

### Out of Scope

- Core edge routing (handled by Traefik).
- Global Load balancing.

## Structure

```text
nginx/
├── config/
│   └── nginx.conf    # Main configuration file
├── docker-compose.yml # Service definition
└── README.md          # This file
```

## Configuration

### Core Files

- `config/nginx.conf`: Defines upstreams, server blocks, and SSO logic.
- `docker-compose.yml`: Mounts config and certificates, defines networks.

## Available Scripts

| Command                               | Description |
| ------------------------------------- | ----------- |
| `docker compose up -d nginx`          | Start Nginx proxy |
| `docker compose logs -f nginx`        | View Nginx logs |
| `docker exec nginx nginx -s reload`   | Reload configuration |

## Related References

- [01-gateway Root README](../README.md)
- [SSO Setup Guide](../../../docs/07.guides/02-auth/README.md)
