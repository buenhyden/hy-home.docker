# Authentication Lifecycle & Procedures

This guide covers the recurring operational tasks and lifecycle management for the `02-auth` tier.

## Backup & Recovery

### Keycloak Database

Keycloak stores all configuration, realms, and users in the `mng-pg` database.

- **Backup**: Use the PostgreSQL cluster backup procedures.
- **Export Realm**:

  ```bash
  docker compose exec keycloak /opt/keycloak/bin/kc.sh export --realm <realm-name> --file /tmp/realm-export.json
  ```


### OAuth2 Proxy Sessions

Sessions are ephemeral and stored in `mng-valkey`. No backup is required, but clearing Redis will force all users to re-authenticate.

## Certificate Rotation

The auth tier relies on `rootCA.pem` for TLS trust between containers.

1. **Update CA**: Place the new `rootCA.pem` in `secrets/certs/`.

2. **Reload OAuth2 Proxy**:

   ```bash
   docker compose -f infra/02-auth/oauth2-proxy/docker-compose.yml restart
   ```

3. **Update Keycloak Truststore**: (If custom truststore is used) Update files in `infra/02-auth/keycloak/conf`.

## Scaling Services

### OAuth2 Proxy
The proxy is stateless (session in Redis) and can be scaled horizontally:

```bash
docker compose -f infra/02-auth/oauth2-proxy/docker-compose.yml up -d --scale oauth2-proxy=3
```

### Keycloak
Requires Infinispan clustering configuration for horizontal scaling. Currently configured for single-node with persistence.
