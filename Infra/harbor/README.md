# Harbor Container Registry

## Overview

Harbor is an open-source trusted cloud native registry project that stores, signs, and scans content. This deployment uses external databases (PostgreSQL, Redis) and binds to host directories for persistence.

## Architecture & Services

| Service | Description | Port (Internal) |
| :--- | :--- | :--- |
| `harbor-core` | Core API and management service | `${HARBOR_PORT}` |
| `harbor-registry` | Docker registry (distribution) | `${HARBOR_PORT}` |
| `harbor-registryctl` | Registry controller | `${HARBOR_PORT}` |
| `harbor-portal` | Web UI frontend | `${HARBOR_PORT}` |
| `harbor-jobservice` | Asynchronous job execution | `${HARBOR_PORT}` |

### External Dependencies

This setup relies on the following external services within the `infra_net` network:

- **PostgreSQL**: Used for metadata storage (`harbor_db` database).
- **Redis (Valkey)**: Used for caching and job queues (Indices 0 and 1).

## Environment Variables

Key configuration variables defined in `docker-compose.yml`:

### General

- `HARBOR_ADMIN_PASSWORD`: Admin password.
- `EXT_ENDPOINT`: External access URL (`https://harbor.${DEFAULT_URL}`).
- `HARBOR_PORT`: Internal service port.

### Secrets (Internal)

- `CORE_SECRET`, `JOBSERVICE_SECRET`, `REGISTRY_HTTP_SECRET`: Keys for inter-service communication.

### Database Connection

- `POSTGRESQL_HOST`: `${POSTGRES_HOSTNAME}`
- `POSTGRESQL_PORT`: `${POSTGRES_PORT}`
- `POSTGRESQL_DATABASE`: `${HARBOR_POSTGRE_DBNAME}`
- `POSTGRESQL_USERNAME`: `${DEFAULT_USERNAME}`
- `POSTGRESQL_PASSWORD`: `${POSTGRES_PASSWORD}`

### Redis Connection

- `_REDIS_URL_CORE`: Core cache (`db 0`).
- `_REDIS_URL_REG`: Registry cache (`db 1`).

## Volumes

Persistence is handled via bind mounts to the host file system:

| Volume Name | Host Path | Container Path | Description |
| :--- | :--- | :--- | :--- |
| `harbor-registry-data-volume` | `${DEFAULT_CICD_DIR}/harbor/registry/data` | `/storage` | Docker images/layers |
| `harbor-registry-conf-volume` | `${DEFAULT_CICD_DIR}/harbor/registry/conf` | `/etc/registry` | Registry config |
| `harbor-registryctl-conf-volume`| `${DEFAULT_CICD_DIR}/harbor/registryctl/conf`| `/etc/registryctl` | Controller config |
| `harbor-core-data-volume` | `${DEFAULT_CICD_DIR}/harbor/core/data` | `/data` | Core data |
| `harbor-core-conf-volume` | `${DEFAULT_CICD_DIR}/harbor/core/conf` | `/etc/core` | Core config |
| `harbor-jobservice-logs-volume` | `${DEFAULT_CICD_DIR}/harbor/jobservice/logs` | `/var/log/jobs` | Job logs |
| `harbor-jobservice-conf-volume` | `${DEFAULT_CICD_DIR}/harbor/jobservice/conf` | `/etc/jobservice` | JobService config |

## Network

All services are connected to the **`infra_net`** network.

## Traefik & Access

> **Note**: This `docker-compose.yml` does **not** include explicit Traefik labels.
> Routing must be handled by an external Traefik configuration or an override file that adds the necessary labels to the `harbor-portal` (for UI) and `harbor-core` (for API) services.

Typical routing requirements:

- **Host**: `harbor.${DEFAULT_URL}`
- **Entrypoints**: `websecure` (UDP may be required for some features, though standard Harbor usage is HTTP/HTTPS).

## Usage

### Prerequisites

Ensure the external **PostgreSQL** and **Redis** services are running and accessible on `infra_net` before starting Harbor.

### Start Harbor

```bash
docker-compose up -d
```

### Access

Once configured with a reverse proxy:

- **URL**: `https://harbor.<your-domain>`
- **Default Admin**: `admin` / `${HARBOR_ADMIN_PASSWORD}`
