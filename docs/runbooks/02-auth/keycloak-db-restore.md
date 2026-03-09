# Keycloak DB Restore Procedure

> **Service**: `keycloak`, `mng-pg`
> **Scenario**: The PostgreSQL database hosting the Keycloak `iam` schema becomes corrupted, or Keycloak fails to boot due to missing schemas. Data restoration is required.

## 1. Prerequisites

- Target Environment: Local Docker Compose/WSL
- Required Tools: `docker`, `psql` (or `docker exec`)
- A valid PostgreSQL dump file (e.g., `keycloak_backup.sql` or `.dump`).

## 2. Assessment Steps

1. Verify the `mng-pg` database is running and accepting connections.

   ```bash
   docker exec -it mng-pg pg_isready -U postgres
   ```

2. Check Keycloak logs for FATAL errors regarding database connections.

   ```bash
   docker logs keycloak
   ```

## 3. Remediation (Restoration)

### Step 1: Halt Keycloak

Stop the Keycloak container so it stops actively writing/reading from the DB.

```bash
docker stop keycloak
```

### Step 2: Drop and Recreate the Database

```bash
# Enter the DB
docker exec -it mng-pg psql -U postgres

# In the PSQL prompt:
DROP DATABASE keycloak;
CREATE DATABASE keycloak OWNER keycloak;
\q
```

### Step 3: Import the Dump

Assuming the backup file `keycloak_backup.sql` is copied into the container or mounted:

```bash
docker exec -i mng-pg psql -U keycloak -d keycloak < ./keycloak_backup.sql
```

### Step 4: Restart Keycloak

```bash
docker start keycloak
```

Monitor logs to ensure the database migration schema syncs successfully.

```bash
docker logs -f keycloak
```

## 4. Rollback

If the backup file is corrupted, you must perform a clean wipe and allow the `mng-pg-init` (if present) or manual scripts to recreate the empty tables.

```bash
docker rm -f keycloak mng-pg
# Wipe the volume (WARNING: LOSES ALL mng-pg DATA)
# docker volume rm hy-home-docker_mng-pg-data
```
