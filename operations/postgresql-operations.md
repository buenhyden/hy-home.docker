# PostgreSQL Router Operations

> **Component**: `postgresql-cluster`, `mng-db`

## Usage

### Connecting to the HA Cluster

Always connect via the **Router** to respect Leader/Replica roles in the `postgresql-cluster` patoni setup.

**Write Operations (Leader):**

```bash
psql -h localhost -p ${POSTGRES_WRITE_HOST_PORT} -U postgres
```

**Read Operations (Replica):**

```bash
psql -h localhost -p ${POSTGRES_READ_HOST_PORT} -U postgres
```

### Checking Cluster Health

You can check the Patroni API on any node:

```bash
curl http://localhost:8008/cluster
```

### Connecting to Management DB (`mng-pg`)

From container:

```bash
docker exec -it mng-pg psql -U postgres
```

### Initialization Failed (`mng-db`)

If database creation fails on fresh boots:

1. Ensure `/docker-entrypoint-initdb.d/init_users_dbs.sql` syntax is correct.
2. Verify `POSTGRES_PASSWORD` secret maps correctly.
