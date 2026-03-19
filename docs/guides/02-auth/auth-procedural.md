# Authentication Procedural Guide (02-auth)

This guide provides step-by-step procedures for initializing, configuring, and maintaining the authentication tier.

## Keycloak Bootstrapping

When starting from a fresh environment:

1. **Database Readiness**: Ensure `mng-pg` is running and the database specified in `KEYCLOAK_DATABASE` exists.
2. **First Run**:
   ```bash
   cd infra/02-auth/keycloak
   docker compose up -d
   ```
3. **Admin Access**:
   - Access the console at `https://keycloak.${DEFAULT_URL}/admin`.
   - Use credentials from the `keycloak_admin_password` secret.

## OAuth2 Proxy Integration

To protect a new service with SSO:

1. **Client Provisioning**: Create an OIDC client in Keycloak (e.g., `hy-home-proxy`).
2. **Secret Setup**: Add the client secret to `secrets/oauth2_proxy_client_secret`.
3. **Traefik Configuration**: Apply the `chain-oauth-proxy` middleware to the target service's route.

## Configuration Reloading

- **Keycloak**: Requires a restart for sensitive environment variable changes (DB, Port).
- **OAuth2 Proxy**: Automatically picks up changes to `config/oauth2-proxy.cfg` on file save (if mounted as a volume), but a restart is recommended for core OIDC settings.

```bash
# Restart for clean config application
docker compose -f infra/02-auth/oauth2-proxy/docker-compose.yml restart
```
