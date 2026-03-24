# Authentication Lifecycle & Procedures

This guide covers the recurring operational tasks and lifecycle management for the `02-auth` tier.

## Backup & Recovery

### Keycloak Database

Keycloak stores all configuration, realms, and users in the `mng-pg` database.

- **Backup**: Use the PostgreSQL cluster backup procedures.
- **Export Realm**:

  ```bash
  docker exec keycloak /opt/keycloak/bin/kc.sh export \
    --realm <realm-name> --file /tmp/realm-export.json
  ```

- **Import Realm**:

  ```bash
  docker exec keycloak /opt/keycloak/bin/kc.sh import \
    --file /tmp/realm-export.json
  ```

### OAuth2 Proxy Sessions

Sessions are ephemeral and stored in `mng-valkey`. No backup is required. Clearing Redis (e.g., `FLUSHDB`) forces all users to re-authenticate via Keycloak.

## Certificate Rotation

The auth tier relies on `rootCA.pem` for TLS trust between containers.

1. **Update CA**: Place the new `rootCA.pem` in `secrets/certs/`.

2. **Reload OAuth2 Proxy** (run from service directory):

   ```bash
   cd infra/02-auth/oauth2-proxy
   docker compose restart oauth2-proxy
   ```

3. **Rebuild Keycloak** (if the CA is baked into the custom image):

   ```bash
   cd infra/02-auth/keycloak
   docker compose build --no-cache
   docker compose up -d
   ```

## Major Version Upgrades

Before upgrading Keycloak to a new major version:

1. **Snapshot**: Create a manual backup of the `mng-pg` Keycloak database.
2. **Export Realms**: Export all realms to JSON files (see Backup section).
3. **Update image version** in `keycloak/docker-compose.yml` and `keycloak/Dockerfile`.
4. **Rebuild**: `docker compose build --no-cache` in `infra/02-auth/keycloak`.
5. **Validate**: Start and check `docker exec keycloak curl -f http://localhost:9000/health/ready`.
6. **Rollback**: If migration fails, restore the database snapshot and revert the image version.

## Scaling Services

### OAuth2 Proxy

The proxy is stateless — sessions live in `mng-valkey`. Scale horizontally:

```bash
cd infra/02-auth/oauth2-proxy
docker compose up -d --scale oauth2-proxy=3
```

All replicas share the same Valkey session store, so users stay logged in across restarts or rolling updates.

### Keycloak

Requires Infinispan clustering for horizontal scaling. Currently configured for single-node with PostgreSQL persistence. For HA, enable Keycloak's built-in infinispan cache coordination (`KC_CACHE=ispn`) and point replicas to the same `mng-pg` instance.
