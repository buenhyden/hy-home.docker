# Gateway Tier: Usage & Troubleshooting Guide

High-level operational guide for daily maintenance and common scenarios.

---

## 🚀 Use Cases & Scenarios

### A. Routing to a New Service

1. **Container Labels**: Add the following labels to your new service in `docker-compose.yml`:

   ```yaml
   labels:
     traefik.enable: "true"
     traefik.http.routers.my-app.rule: Host(`my-app.${DEFAULT_URL}`)
     traefik.http.routers.my-app.entrypoints: websecure
     traefik.http.routers.my-app.tls: "true"
   ```

2. **Network**: Ensure the service is joined to the `infra_net` network.

### B. Adding SSO Protection

Simply add the `sso-auth@file` middleware to your service labels:

```yaml
labels:
  traefik.http.routers.my-app.middlewares: sso-auth@file
```

### C. Custom Middleware (Rate Limiting)

Available middlewares in `dynamic/middleware.yml`:
- `req-rate-limit@file`: Prevents brute force or excessive requests.

---

## ❓ FAQ (Frequently Asked Questions)

**Q: Traefik is running but my domains are not resolving.**
A: Ensure your `/etc/hosts` file maps the domains to `127.0.0.1`.

**Q: I get a browser warning for "Insecure Connection".**
A: Since we use local CA (mkcert), you must install the root CA in your browser/OS:
   ```bash
   mkcert -install
   ```

**Q: Can I use both Traefik and Nginx simultaneously?**
A: Not on the same ports (80/443). You must choose one or change the host port mappings in `docker-compose.yml`.

---

## 🛠️ Troubleshooting

| Issue | Potential Cause | Fix |
| :--- | :--- | :--- |
| **502 Bad Gateway** | Backend service is down or not on the same network. | Check `docker ps` and ensure `infra_net` is used. |
| **403 Forbidden** | Middleware (SSO) rejected the request. | Check OAuth2 Proxy session or Basic Auth credentials. |
| **404 Not Found** | Router rule (Host header) doesn't match the URL. | Verify `traefik.http.routers.<name>.rule` in labels. |
| **Empty Response** | TLS handshake failure. | Check if certs exist in `secrets/certs/` and are valid. |

### Diagnostic Toolbox
```bash
# Watch real-time logs for routing errors
docker compose logs -f traefik

# Inspect dynamic configuration loaded by Traefik
# 1. Tunnel to dashboard (if restricted)
# 2. View "HTTP Routers" and "Middlewares" tabs.
```

---
*Maintained by Infra Team*
