# Runbook: Keycloak Auth Lockout

> Detailed resolution strategies for recovering from Keycloak administrative lockouts.

## Context

A lockout incident occurs when all administrative access to the Keycloak instance is lost. This can occur due to corrupted password configurations, accidental deletion of the `admin` role, or persistent brute-force lockout triggers.

## Symptoms

- 401/403 Unauthorized errors trying to hit `keycloak.${DEFAULT_URL}/admin`.
- "Invalid credentials" constantly popping up during login despite a known password string.
- Cannot configure OAuth2-Proxy workflows.

## Resolution Steps

### Method 1: Bootstrapping a New Admin

Because Keycloak utilizes a secondary Postgres cache for storing user tables (`keycloak-db` container), simply restarting it won't reset the `admin` account automatically if it has already been bootstrapped. However, you can force the creation of a *new* temporary admin user utilizing Docker execute commands.

1. SSH into the WSL / Host running the Docker daemon.
2. Formulate the add user command via the `kc.sh` utility:

```bash
docker exec -it keycloak /opt/keycloak/bin/add-user-keycloak.sh -r master -u recovery_admin -p Recovery_Pass123
```

1. Restart the container for the new user to be populated in the cache:

```bash
docker restart keycloak
```

1. Login with `recovery_admin` and adjust the permissions of your original account, or regenerate its password via the "Users" panel.

### Method 2: Manual Database Pruning (Destructive)

> [!CAUTION]
> This method will wipe settings and forcefully start the image fresh.

1. Locate the PostgreSQL database storing Keycloak's state.
2. Drop all internal records on the `keycloak` database natively using the Postgres CLI container side, or simply bring the stack down and wipe the bound volume.

```bash
docker compose -f infra/02-auth/keycloak/docker-compose.yml down -v
```

1. Restart the stack using standard `.env.infra` inputs to reconstruct the exact `admin/admin` baseline state.
