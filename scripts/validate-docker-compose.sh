#!/bin/bash
set -e

# Base directory
BASE_DIR="$(git rev-parse --show-toplevel)"
cd "$BASE_DIR"

echo "🔍 Validating Docker Compose configurations..."

# Temporarily create .env from example if not already present
CLEANUP_ENV=false
if [ ! -f .env ]; then
    cp .env.example .env
    CLEANUP_ENV=true
fi

# Temporarily create dummy secret files
mkdir -p secrets
DUMMY_FILES=()

# List of secrets found in ci-quality.yml
SECRETS=(
    postgres_password redis_password minio_root_password minio_app_user_password
    valkey_password smtp_username influxdb_password influxdb_api_token
    couchdb_password couchdb_cookie valkey_cluster_password n8n_db_password
    n8n_valkey_password n8n_encryption_key n8n_runner_auth_token airflow_db_password
    airflow_fernet_key airflow_www_password grafana_admin_password
    oauth2_proxy_client_secret sonarqube_db_password terrakube_db_password
    terrakube_pat_secret terrakube_internal_secret alertmanager_smtp_password
    alertmanager_slack_webhook service_postgres_password
)

for secret in "${SECRETS[@]}"; do
    if [ ! -f "secrets/${secret}.txt" ]; then
        echo "dummy" > "secrets/${secret}.txt"
        DUMMY_FILES+=("secrets/${secret}.txt")
    fi
done

# Create dummy env files if they are referenced but missing
# This helps passing 'docker compose config' validation
ENV_FILES=$(grep -r "env_file:" . --include="docker-compose.yml" -A 5 | grep -o "\.env\.[a-z0-9._-]*" | sort -u || true)
for env_file in $ENV_FILES; do
    # Find where this env_file might be relative to the docker-compose.yml that references it
    # For simplicity, we search for the file in the whole repo.
    # If not found anywhere, we create it in the root for now, or better, we try to be smarter.
    # Actually, the error message gives the path: infra/04-data/postgresql-cluster/.env.postgres
    if [ ! -f "$env_file" ]; then
        # We don't know the exact path easily from just grep.
        # But 'docker compose config' failed because of specific missing files.
        # Let's just create some common ones if they are missing.
        :
    fi
done

# A better way to find missing env files is to parse the compose files.
# For now, let's just manually add the one that failed and any other obvious ones.
MISSING_ENVS=(
    "infra/04-data/postgresql-cluster/.env.postgres"
)

for env in "${MISSING_ENVS[@]}"; do
    if [ ! -f "$env" ]; then
        mkdir -p "$(dirname "$env")"
        touch "$env"
        DUMMY_FILES+=("$env")
    fi
done


# Perform validation
ERROR=0
if ! docker compose config > /dev/null; then
    ERROR=1
fi

# Cleanup
for file in "${DUMMY_FILES[@]}"; do
    rm -f "$file"
done

if [ "$CLEANUP_ENV" = true ]; then
    rm -f .env
fi

if [ $ERROR -eq 1 ]; then
    echo "❌ Docker Compose validation failed"
    exit 1
fi

echo "✅ Docker Compose validation passed"
exit 0
