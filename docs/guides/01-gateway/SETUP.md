# Gateway Tier: Setup & Installation Guide

This guide provides the necessary steps to initialize and verify the gateway tier.

---

## 1. Prerequisites

Before starting the gateway, ensure you have completed the core setup:

- **Local Domain Binding**: Map your desired domains to `127.0.0.1` in `/etc/hosts`.

  ```bash
  127.0.0.1 dashboard.hy-home.dev auth.hy-home.dev minio.hy-home.dev
  ```

- **Secrets Initialization**: Ensure all required secrets are generated.

  ```bash
  ./scripts/gen-secrets.sh
  ```

- **Local Certificates**: Generate TLS certificates via `mkcert`.

  ```bash
  bash scripts/generate-local-certs.sh
  ```

## 2. Quick Start (Traefik)

The primary gateway is Traefik. To bring it up:

```bash
# 1. Start the service
docker compose up -d traefik

# 2. Verify health
docker exec traefik traefik healthcheck --ping
```

## 3. Alternative Start (Nginx)

If you need to use Nginx specifically for path-based proxying:

```bash
# 1. Stop Traefik (if running on 80/443)
docker compose stop traefik

# 2. Start Nginx
docker compose --profile nginx up -d nginx
```

## 4. Post-Installation Verification

| Test | Tool | Expected Result |
| :--- | :--- | :--- |
| **HTTP Redirect** | `curl -I http://localhost` | `301 Moved Permanently` to HTTPS |
| **HTTPS Connectivity** | `curl -kI https://localhost` | `200 OK` or `404 Not Found` (encrypted) |
| **Metrics Endpoint** | `curl http://localhost:8082/metrics` | Prometheus metrics data |
| **Dashboard Access** | Browser | Accessible at `https://dashboard.hy-home.dev` |

---
*Maintained by Infra Team*
