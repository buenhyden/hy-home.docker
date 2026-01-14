# Deployment Guide

## Prerequisites

### Required Tools

- **Docker Engine**: 24.0+
- **Docker Compose**: v2.20+
- **NVIDIA GPU** (optional): For Ollama LLM inference

### System Requirements

**Minimum:**

- CPU: 8 cores
- RAM: 16GB
- Disk: 100GB SSD

**Recommended:**

- CPU: 16 cores
- RAM: 32GB
- Disk: 500GB NVMe SSD
- GPU: NVIDIA GPU with CUDA support

## Setup

### 1. Create Secrets Directory

```bash
mkdir -p secrets

# Generate password files
echo "your_postgres_password" > secrets/postgres_password.txt
echo "your_redis_password" > secrets/redis_password.txt
echo "your_valkey_password" > secrets/valkey_password.txt
echo "minio_admin" > secrets/minio_root_user.txt
echo "minio_password" > secrets/minio_root_password.txt
echo "minio_app_user" > secrets/minio_app_user.txt
echo "minio_app_password" > secrets/minio_app_user_password.txt
```

> **Security**: The `secrets/` directory is excluded from git via `.gitignore`.

### 2. Environment Configuration

The `infra/.env` file contains all configuration variables. Key variables:

```bash
DEFAULT_URL=127.0.0.1.nip.io
HTTP_PORT=80
HTTPS_PORT=443
POSTGRES_PORT=5432
REDIS_PORT=6379
```

> **Note**: No modification needed for local development with defaults.

## Automation & Tools

We provide helper scripts to simplify common operational tasks.

### Create New Service

Scaffold a new infrastructure service complete with README, Dockerfile, and Compose config.

```bash
./scripts/new_infra_service.sh <service_name>
```

### Validate Configuration

Check your `docker compose.yml` files for syntax errors before deploying.

```bash
./scripts/validate_compose_change.sh
```

## Deployment Options

### Option 1: Full Infrastructure Deployment

Deploy all active services:

```bash
cd infra
docker compose up -d
```

**Wait Time**: 2-5 minutes for all services to start and become healthy.

**Verification**:

```bash
docker compose ps
```

All services should show status `Up` or `Up (healthy)`.

### Option 2: Individual Service Deployment

Deploy specific services:

```bash
# PostgreSQL cluster only
cd infra/postgresql-cluster
docker compose up -d

# Observability stack only
cd infra/observability
docker compose up -d

# Kafka cluster only
cd infra/kafka
docker compose up -d
```

### Option 3: Selective Services via Include

Edit `infra/docker compose.yml` to comment/uncomment services in the `include` section:

```yaml
include:
  - traefik/docker compose.yml
  - mng-db/docker compose.yml
  # - mail/docker compose.yml  # Commented = disabled
```

## Post-Deployment Verification

### 1. Check Service Health

```bash
cd infra
docker compose ps
docker compose logs -f --tail=50
```

### 2. Access Web UIs

Open in browser:

- **Traefik Dashboard**: <https://dashboard.127.0.0.1.nip.io>
- **Grafana**: <https://grafana.127.0.0.1.nip.io>
- **Keycloak**: <https://keycloak.127.0.0.1.nip.io/admin>

### 3. Test Database Connectivity

**PostgreSQL (Write):**

```bash
psql -h localhost -p 5000 -U postgres
```

**Redis:**

```bash
redis-cli -h localhost -p 6379 -a $(cat ../secrets/redis_password.txt)
```

## Common Deployment Scenarios

### Scenario 1: Development Environment

**Services needed:**

- PostgreSQL cluster
- Redis cluster
- Traefik
- Observability (optional)

```bash
cd infra
docker compose up -d postgresql-haproxy redis-cluster traefik
```

### Scenario 2: Data Engineering Platform

**Services needed:**

- Kafka
- PostgreSQL
- n8n
- Observability

```bash
cd infra
docker compose up -d kafka postgresql-cluster n8n observability
```

### Scenario 3: AI/LLM Development

**Services needed:**

- Ollama
- Qdrant
- MinIO
- PostgreSQL

```bash
cd infra
docker compose up -d ollama qdrant minio postgresql-cluster
```

## Updating Services

### Update All Services

```bash
cd infra
docker compose pull
docker compose up -d
```

Docker Compose will automatically recreate containers with updated images.

### Update Specific Service

```bash
cd infra/kafka
docker compose pull
docker compose up -d
```

### Cleanup Old Images

```bash
docker image prune -f
```

## Stopping Services

### Stop All

```bash
cd infra
docker compose down
```

### Stop Specific Service

```bash
cd infra/observability
docker compose down
```

### Stop and Remove Volumes (DESTRUCTIVE)

```bash
cd infra
docker compose down -v
```

> **Warning**: This deletes **all data**. Backup first!

## Next Steps

- [Troubleshooting Guide](./troubleshooting.md)
- [Security Configuration](./security.md)
- [Maintenance Procedures](./maintenance.md)
