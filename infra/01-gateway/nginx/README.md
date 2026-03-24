# 🛡️ Nginx Path Proxy

> Specialized high-performance proxy for path-based routing and static asset serving.

## Overview

**KR**: Nginx는 경로 기반의 복잡한 라우팅과 정적 자원 서빙, 그리고 `auth_request`를 이용한 세밀한 SSO 통합을 위해 사용됩니다.
**EN**: Nginx is used for complex path-based routing, static asset serving, and fine-grained SSO integration using `auth_request`.

## Navigation / Inventory

| Component | Path | Purpose |
| :--- | :--- | :--- |
| **Nginx Config** | [`config/nginx.conf`](./config/nginx.conf) | Server blocks, upstream definitions, and auth logic |
| **Deployment** | [`docker-compose.yml`](./docker-compose.yml) | Service definition and network mapping |

---

## ⚙️ Component Details

### Key Features

- **Dual Support**: Binds to 80/443 (same as Traefik, use profiles to switch).
- **Auth Integration**: Built-in logic to check authentication against the IAM tier.
- **Upstream Mapping**: Defined for MinIO (S3/Console), Keycloak, and OpenSearch.

### Operational Commands

```bash
# Test configuration syntax
docker exec nginx nginx -t

# Reload configuration without restart
docker exec nginx nginx -s reload

# Start with Nginx profile
docker compose --profile nginx up -d nginx
```

---

## Extensibility & References

- [🌐 Gateway Tier](../README.md)
- [📜 Nginx Official Docs](https://nginx.org/en/docs/)

---
*Maintained by Infra Team*
