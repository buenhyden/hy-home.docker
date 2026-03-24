---
layer: infra
---

# Workflow Tier: Setup & Initialization

This guide covers the initial bootstrapping of Airflow and n8n.

## 1. Prerequisites

- **Tiers Required**: `04-data` (PostgreSQL) must be healthy.
- **Resources**: At least 4GB RAM recommended for the full stack.
- **Environment**: Ensure `DEFAULT_WORKFLOW_DIR` is defined in `.env`.

## 2. Secrets Bootstrap

Generate required secrets before starting:

```bash
# Generate Airflow Fernet Key
echo $(python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())") > ./secrets/airflow_fernet_key

# Generate n8n Encryption Key
openssl rand -hex 24 > ./secrets/n8n_encryption_key
```

## 3. Profile Activation

The workflow tier is **opt-in**.

```bash
# Enable in root docker-compose.yml (uncomment)
# include:
#   - infra/07-workflow/docker-compose.yml

# Or specify at runtime:
COMPOSE_PROFILES=workflow docker compose up -d
```

## 4. Airflow Initialization

The `airflow-init` container handles DB migrations and admin user creation:

1. Start the init job:
   ```bash
   docker compose --profile workflow up airflow-init
   ```
2. Verify exit code 0:
   ```bash
   docker wait airflow-init
   ```

## 5. n8n Initialization

n8n auto-migrates its database on first start. Ensure the database `n8n` is created in PostgreSQL.

```bash
# Create database (via mng-pg)
docker exec mng-pg psql -U postgres -c "CREATE DATABASE n8n;"
```
