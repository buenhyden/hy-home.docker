# 🚦 Traefik Edge Router

> Primary dynamic reverse proxy with label-based service discovery.

## Overview

**KR**: Traefik은 프로젝트의 메인 엣지 라우터로, 도커 라벨을 통해 서비스를 자동으로 탐색하고 HTTPS 인증서를 관리합니다.
**EN**: Traefik is the project's primary edge router, providing automatic service discovery via Docker labels and managing HTTPS certificates.

## Navigation / Inventory

| Component | Path | Purpose |
| :--- | :--- | :--- |
| **Static Config** | [`config/traefik.yml`](./config/traefik.yml) | Entrypoints, log levels, and core providers |
| **Dynamic Config** | [`dynamic/`](./dynamic/) | Middleware definitions, TLS options, and manual routers |
| **Deployment** | [`docker-compose.yml`](./docker-compose.yml) | Service definition and volume mounts |

---

## ⚙️ Component Details

### Configuration Highlights

- **Entrypoints**: `web` (80), `websecure` (443), `neo4j-bolt` (7687), `metrics` (8082).
- **Middlewares**:
  - `sso-auth@file`: Forward authentication to OAuth2 Proxy.
  - `dashboard-auth@file`: Basic auth for the Traefik dashboard.
  - `req-rate-limit@file`: Rate limiting for security.

### Operational Commands

```bash
# Check configuration syntax (via logs)
docker compose logs traefik | grep "Configuration loaded"

# Access dashboard (if SSH-tunneled or reachable)
# URL: https://dashboard.hy-home.dev
```

---

## Extensibility & References

- [🌐 Gateway Tier](../README.md)
- [📜 Traefik Official Docs](https://doc.traefik.io/traefik/)
- [🔒 Security Policies](../../../secrets/README.md)

---
*Maintained by Infra Team*
