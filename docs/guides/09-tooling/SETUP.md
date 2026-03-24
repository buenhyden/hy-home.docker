---
layer: infra
---

# Tooling Tier: Setup & Initialization

This guide covers the initial bootstrap and configuration for the Tooling stack.

## 1. Prerequisites

Before starting any tooling service, ensure these external services are healthy:

```bash
# Verify management database is ready
docker inspect --format='{{.State.Health.Status}}' mng-pg

# Verify MinIO is ready (required by Terrakube)
docker inspect --format='{{.State.Health.Status}}' minio

# Verify Keycloak is ready (required by Terrakube)
docker inspect --format='{{.State.Health.Status}}' keycloak

# Verify InfluxDB is ready (required by Locust)
docker inspect --format='{{.State.Health.Status}}' influxdb
```

## 2. Bootstrapping Services

### Initial Startup
```bash
# Start all tooling services
docker compose --profile tooling up -d
```

### SonarQube Initialization
1. Navigate to `https://sonarqube.${DEFAULT_URL}`.
2. Log in with `admin` / `admin`.
3. Change password immediately.
4. Set `vm.max_map_count >= 524288` on the host.

### Terrakube Setup
1. Create `TERRAKUBE_ADMIN` group in Keycloak.
2. Create `tfstate` bucket in MinIO.

## 3. Post-Setup Verification
Ensure all services are reachable via their respective subdomains.
