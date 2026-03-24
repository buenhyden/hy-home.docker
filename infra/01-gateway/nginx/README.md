# 🧱 Nginx (Path Proxy)

> Specialized path-based proxy and static asset server for the gateway tier.

## Overview (KR)

Nginx는 `01-gateway` 티어 내에서 특정 경로 기반의 프록싱과 정적 자산 서빙을 담당합니다. 특히 MinIO, Keycloak, OAuth2 Proxy와의 연동을 통해 미세한 트래픽 제어 및 인증 체크 레이어를 제공합니다.

## Overview

Nginx serves as a specialized path-based proxy and static asset server within the `01-gateway` tier. It handles fine-grained traffic control and authentication check layers through integration with MinIO, Keycloak, and OAuth2 Proxy.

## Structure

```text
nginx/
├── config/
│   └── nginx.conf    # Main configuration file
├── docker-compose.yml # Service definition
└── README.md          # This file
```

---

## ⚙️ Configuration

### Upstream Services

- **OAuth2 Proxy**: `oauth2-proxy:4180`
- **MinIO**: `minio:9000` (Server) / `minio:9001` (Console)
- **Keycloak**: `keycloak:8080`

### Integrated Features

- **SSO**: `auth_request` module integrated with `oauth2-proxy`.
- **Rate Limiting**: Configured in `req_rate_limit` zone (100r/s).
- **Caching**: Proxy cache configured for `/var/cache/nginx`.

## Available Scripts

| Command | Description |
| :--- | :--- |
| `docker compose up -d nginx` | Start Nginx service |
| `docker exec -it nginx nginx -t` | Test configuration syntax |
| `docker exec -it nginx nginx -s reload` | Hot-reload configuration |

## Documentation Standards

All documents in this folder MUST maintain traceability back to the [Gateway Architecture](../../../docs/07.guides/01-gateway/).

---
*Layer: Infrastructure / Gateway*
