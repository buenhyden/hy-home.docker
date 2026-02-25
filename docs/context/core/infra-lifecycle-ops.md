# Infrastructure Lifecycle & Core Operations

> **Component**: Global `infra` stack
> **Orchestrator**: Docker Compose V2

## 1. Stack Startup Order

The infrastructure is designed with a "Bottom-Up" dependency model.

1. **Security (02/03)**: Keycloak & Vault.
2. **Data (04)**: MinIO & PostgreSQL (Must be healthy for observability logs).
3. **Gateway (01)**: Traefik (Enables external routing).
4. **Services (05-10)**: Application workloads.

## 2. Global Management Commands

To launch or update the entire standard stack:

- Bootstrap prerequisites (secrets/certs/env/dirs): `runbooks/core/infra-bootstrap-runbook.md`

```bash
# Standard boot (without specific profiles)
docker compose up -d

# Targeted update of one service
docker compose up -d --no-deps --build [service_name]
```

## 3. Network Health

The `infra_net` bridge is the backbone of internal communication.

- **Subnet**: `172.19.0.0/16`
- **DNS**: Docker's internal resolver handles service-to-service discovery via container names.

## 4. Graceful Teardown

To ensure database flush and log commit:

```bash
docker compose stop
# Wait for 30s
docker compose down
```
