# Gateway Routing Runbook

> **Components**: `traefik`, `nginx`

## Traefik Troubleshooting

### "404 Not Found"

- Check if the target container is running and healthy.
- Verify `traefik.enable=true` label exists on the target container.
- Ensure the target container is on the same Docker network (`infra_net`) as Traefik.

### "Internal Server Error" (SSO/Auth)

- Verify `oauth2-proxy` service is running.
- Check Traefik logs for ForwardAuth integration failures (`docker compose logs traefik`).

## Nginx Troubleshooting

### "Redirect Loop"

- Ensure `proxy_set_header X-Forwarded-Proto https;` is correctly set in the proxy block.
- Verify the upstream target (like Keycloak) and Nginx agree on the scheme (HTTP vs HTTPS).

### "401 Unauthorized" (SSO Path)

- Check if you are correctly logged in via the IdP (Keycloak).
- Verify OAuth2 Proxy is receiving the sub-request and validating the session token correctly.
