# Runbook: Traefik Ingress & Gateway Recovery

> **Component**: `traefik`
> **Internal Port**: `8080` (API/Dashboard)
> **Alerts**: `TraefikHighHttp4xxErrorRate`, `TraefikTargetDown`

## 1. Issue: 404 Not Found on Service Endpoint

**Given**: A service URL returns 404 while other services are working.
**When**: Routing configuration or label discovery fails.
**Then**: Perform the following checks:

1. **Verify Labels**: Ensure the target container has `traefik.enable=true` and `traefik.http.routers.[name].rule`.
2. **Network Check**: Verify the container is joined to the `infra_net` network.
3. **API Dashboard**: Check `https://traefik.${DEFAULT_URL}/dashboard/` for dynamic configuration errors.

## 2. Issue: 502 Bad Gateway / Connection Refused

**Given**: The browser returns 502 for a specific service.
**When**: The upstream container is down or unhealthy.
**Then**:

1. **Check Upstream**: `docker compose ps [service]` to verify it's running.
2. **Internal DNS**: Test connectivity from Traefik: `docker exec traefik nslookup [service]`.

## 3. Issue: Redirect Loops or SSO Failures

**Given**: Browser shows "Too many redirects" or authentication fails silently.
**When**: Header mismatched or ForwardAuth middleware is misconfigured.
**Then**:

1. **Check Auth Proxy**: `docker compose logs oauth2-proxy` to see if tokens are rejected.
2. **Proxy Headers**: Verify `X-Forwarded-Proto` is sent as `https` from the external load balancer (if any).

## 4. Forced Configuration Reload

If labels are ignored, restart the container to force a full dynamic configuration refresh:

```bash
docker compose -f infra/01-gateway/traefik/docker-compose.yml restart traefik
```
