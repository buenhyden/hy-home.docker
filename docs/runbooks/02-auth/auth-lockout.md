# Runbook: Keycloak Auth Lockout Recovery

> **Component**: `keycloak`
> **Internal Port**: `8080`
> **State Backend**: `keycloak-db` (Postgres)

## 1. Issue: Administrative User Locked Out

**Given**: All administrative accounts return "Invalid credentials" or are disabled.
**When**: Password loss, role deletion, or brute-force protection trigger.
**Then**: Create a temporary recovery administrator:

1. **Exec Command**:

   ```bash
   docker exec -it keycloak /opt/keycloak/bin/add-user-keycloak.sh \
     -r master -u recovery_admin -p Recovery_Pass123!
   ```

2. **Restart Container**:

   ```bash
   docker restart keycloak
   ```

3. **Recovery**: Login to the Master realm with `recovery_admin`, restore your primary admin, then **DELETE** the temporary user.

## 2. Emergency Reset (Database Purge)

**Given**: The Keycloak configuration is corrupted beyond simple user recovery.
**When**: You need a fresh start (WARNING: SETTINGS LOSS).
**Then**:

1. **Wipe State**:

   ```bash
   docker compose -f infra/02-auth/keycloak/docker-compose.yml down -v
   ```

2. **Restore**: Restart the stack; Keycloak will re-bootstrap from the environment secrets.

## 3. Verification

Navigate to `https://keycloak.${DEFAULT_URL}/admin` and confirm the login screen is responsive and accepts the new credentials.
