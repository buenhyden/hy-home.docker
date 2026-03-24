# 🚦 Traefik (Edge Router)

> Primary edge router with dynamic service discovery and automatic TLS management.

## Overview (KR)

Traefik은 `01-gateway` 티어의 핵심 에지 라우터입니다. Docker 레이블을 통한 서비스 자동 발견, Let's Encrypt 또는 사용자 인증서를 이용한 자동 TLS 관리, 그리고 유연한 미들웨어 체인을 통해 전체 인프라의 트래픽을 오케스트레이션합니다.

## Overview

Traefik is the core edge router of the `01-gateway` tier. It orchestrates traffic for the entire infrastructure using automatic service discovery via Docker labels, automated TLS management (certificates), and a flexible middleware chain.

## Structure

```text
traefik/
├── config/
│   └── traefik.yml    # Static configuration
├── dynamic/
│   ├── middleware.yml # Dynamic middlewares
│   └── tls.yaml      # Dynamic TLS/Cert configuration
├── docker-compose.yml # Service definition
└── README.md          # This file
```

---

## ⚙️ Configuration

### EntryPoints

| Name | Address | Purpose |
| :--- | :--- | :--- |
| `web` | `:80` | HTTP (Redirects to 443) |
| `websecure` | `:443` | HTTPS (TLS termination) |
| `neo4j-bolt` | `:7687` | Neo4j TCP Passthrough |
| `metrics` | `:8082` | Prometheus Metrics |

### Observability

- **Logs**: INFO level by default.
- **Tracing**: OTLP/gRPC enabled, pointing to `tempo:4317`.
- **Metrics**: Prometheus exporter enabled on port 8082.

## Available Scripts

| Command | Description |
| :--- | :--- |
| `docker compose up -d traefik` | Start Traefik service |
| `docker exec traefik traefik healthcheck --ping` | Check internal health |
| `docker compose logs -f traefik` | Tail access and system logs |

## Documentation Standards

Refer to [Gateway Setup Guide](../../../docs/07.guides/01-gateway/01.setup.md) for domain and certificate setup instructions.

---
*Layer: Infrastructure / Gateway*
