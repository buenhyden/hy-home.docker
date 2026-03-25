# Traefik Edge Router

> Primary edge router with dynamic service discovery and TLS orchestration.

## Overview

Traefik acts as the primary ingress controller for the `hy-home.docker` ecosystem. It provides dynamic service discovery via the Docker provider, automatic TLS termination, and a comprehensive dashboard for traffic monitoring.

## Overview (KR)

Traefik은 `hy-home.docker` 생태계의 주 에지 라우터입니다. Docker 프로바이더를 통한 동적 서비스 탐색, 자동 TLS 종료, 그리고 트래픽 모니터링을 위한 대시보드를 제공합니다.

## Audience

- Infrastructure Engineers
- SREs
- AI Agents

## Scope

### In Scope

- Global entrypoint definition (80, 443, 7687).
- Dynamic service discovery and routing labels.
- Middleware orchestration (RateLimit, BasicAuth, SSO).
- TLS Store and Certificate management.

### Out of Scope

- Detailed path-based rewrites (partially delegated to Nginx).
- Application-level business logic.

## Structure

```text
traefik/
├── config/
│   └── traefik.yml     # Static configuration
├── dynamic/
│   ├── middleware.yml  # Shared middlewares
│   └── tls.yaml        # TLS certificate mapping
├── docker-compose.yml  # Service definition
└── README.md           # This file
```

## Configuration

### Key Files

- `config/traefik.yml`: Defines entrypoints, providers, and API settings.
- `dynamic/middleware.yml`: Defines reusable middlewares like `sso-auth` and `req-rate-limit`.
- `dynamic/tls.yaml`: Maps SSL certificates to the TLS store.

## Available Scripts

| Command                               | Description |
| ------------------------------------- | ----------- |
| `docker compose up -d traefik`        | Start Traefik router |
| `docker compose logs -f traefik`      | View Traefik logs |
| `docker exec traefik traefik healthcheck --ping` | Health check |

## Related References

- [01-gateway Root README](../README.md)
- [Traefik Dashboard](https://dashboard.${DEFAULT_URL:-localhost}) (Internal)
