# Traefik Edge Router

> Primary edge router with dynamic service discovery and TLS orchestration for the hy-home.docker ecosystem.

## Overview

Traefik acts as the primary ingress controller for the `hy-home.docker` cluster. It provides dynamic service discovery via the Docker provider, automatic TLS termination, and a comprehensive dashboard for traffic monitoring and management.

## Overview (KR)

Traefik은 `hy-home.docker` 생태계의 주 에지 라우터입니다. Docker 프로바이더를 통한 동적 서비스 탐색, 자동 TLS 종료, 그리고 트래픽 모니터링 및 관리를 위한 대시보드를 제공합니다.

## Audience

이 README의 주요 독자:

- Infrastructure Engineers
- SREs
- AI Agents

## Scope

### In Scope

- Global entrypoint definition (Port 80, 443, 7687, 8082).
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

## How to Work in This Area

1. Start by reviewing `config/traefik.yml` to understand the core routing entrypoints.
2. Check `dynamic/middleware.yml` when adding authentication or rate-limiting to a new service.
3. Use labels in your service's `docker-compose.yml` to register routes with Traefik.
4. After any configuration change, verify the status via the Traefik Dashboard.

## Available Scripts

| Command                               | Description |
| ------------------------------------- | ----------- |
| `docker compose up -d`                | Start Traefik router |
| `docker compose down`                 | Stop Traefik router |
| `docker compose logs -f`              | View Traefik logs |
| `docker exec traefik traefik healthcheck --ping` | Health check |

## Configuration

### Environment Variables

| Variable          | Required | Description |
| ----------------- | -------: | ----------- |
| `DEFAULT_URL`     |      Yes | Primary domain (e.g., localhost or your-domain.com) |
| `HTTP_HOST_PORT`  |       No | Host port for HTTP (default: 80) |
| `HTTPS_HOST_PORT` |       No | Host port for HTTPS (default: 443) |

## Related References

- [01-gateway Root README](../README.md)
- [Traefik Guide](../../../docs/07.guides/01-gateway/traefik.md)
- [Gateway Operations Policy](../../../docs/08.operations/01-gateway/traefik.md)
- [Traefik Runbook](../../../docs/09.runbooks/01-gateway/traefik.md)
- [Traefik Dashboard](https://dashboard.${DEFAULT_URL:-localhost}) (Internal)
