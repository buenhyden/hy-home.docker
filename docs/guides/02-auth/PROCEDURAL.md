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
# Restart for clean config application (run from service directory)
cd infra/02-auth/oauth2-proxy
docker compose restart oauth2-proxy
```

## Keycloak Customization

### Build-time Optimizations

Keycloak 26.x (Quarkus) uses build-time configurations to reduce startup time.

- **Dockerfile**: Located in `infra/02-auth/keycloak/Dockerfile`.
- **Custom Themes**: Place in `themes/` and rebuild.
- **Providers**: Place JARs in `providers/` and rebuild.

```bash
docker compose build --no-cache keycloak
docker compose up -d keycloak
```

## Maintenance Procedures

### Database Migrations

Keycloak handles internal schema migrations automatically upon startup. However, before a major version upgrade:

1. **Snapshot**: Create a manual backup of the `mng-pg` database.
2. **Dry Run**: Test the container upgrade in a staging environment.

### Certificate Rotation

When the local RootCA expires or a new one is generated:

1. **Update Secrets**: Place the new `rootCA.pem` in `secrets/certs/`.
2. **Rebuild/Restart**:

   ```bash
   cd infra/02-auth/keycloak
   docker compose build --no-cache
   docker compose up -d
   ```

## Log Analysis

Monitoring logs is critical for identifying authentication failures or OIDC misconfigurations.

### Keycloak Logs

```bash
docker logs -f keycloak
```

- Look for: `WARN  [org.keycloak.events]` (Failed logins, invalid client attempts).
- Look for: `ERROR [org.keycloak.services]` (System errors, DB connection issues).

### OAuth2 Proxy Logs

```bash
docker logs -f oauth2-proxy
```

- Look for: `[error] Error retrieving session` (Redis connection or password issues).
- Look for: `[error] Error validating token` (OIDC provider/certificate mismatch).
