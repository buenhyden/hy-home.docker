# Harbor Container Registry

## Overview

Harbor is an open-source trusted cloud native registry project that stores, signs, and scans content. This deployment uses external databases (PostgreSQL, Redis) and binds to host directories for persistence.

## Services

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

## Networking

All services are connected to the **`infra_net`** network.

## Configuration

### General Configuration

| Variable | Description | Default |
| :--- | :--- | :--- |
| `EXT_ENDPOINT` | External URL | `https://harbor.${DEFAULT_URL}` |
| `HARBOR_ADMIN_PASSWORD` | Admin Password | `${HARBOR_PASSWORD}` |
| `HARBOR_PORT` | Internal Port | `${HARBOR_PORT}` |

### Database & Redis

| Variable | Description | Default |
| :--- | :--- | :--- |
| `POSTGRESQL_HOST` | DB Host | `${POSTGRES_HOSTNAME}` |
| `POSTGRESQL_DATABASE` | DB Name | `${HARBOR_POSTGRE_DBNAME}` |
| `_REDIS_URL_CORE` | Core Cache URL | `redis://.../0` |
| `_REDIS_URL_REG` | Registry Cache URL | `redis://.../1` |

### Internal Secrets

| Variable | Description | Default |
| :--- | :--- | :--- |
| `CORE_SECRET` | Core Service Secret | `${HARBOR_CORE_SECRET}` |
| `JOBSERVICE_SECRET` | Job Service Secret | `${HARBOR_JOBSERVICE_SECRET}` |
| `REGISTRY_HTTP_SECRET` | Registry Secret | `${HARBOR_REGISTRY_HTTP_SECRET}` |

## Persistence

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

## Traefik Integration

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
