# Harbor

## Overview

Harbor is an open-source trusted cloud native registry project that stores, signs, and scans content.

## Service Details

- **Image**: `bitnami/harbor-*:2`
- **Components**:
  - `harbor-registry`: Docker registry.
  - `harbor-registryctl`: Registry controller.
  - `harbor-core`: Core services and API.
  - `harbor-portal`: Web UI.
  - `harbor-jobservice`: Async job worker.

### Volumes

- `harbor-registry-data-volume`
- `harbor-registry-conf-volume`
- `harbor-registryctl-conf-volume`
- `harbor-core-data-volume`
- `harbor-core-conf-volume`
- `harbor-jobservice-logs-volume`
- `harbor-jobservice-conf-volume`

These volumes are bind-mounted to host directories defined in `${DEFAULT_CICD_DIR}/harbor/*`.

## Environment Variables

- `HARBOR_ADMIN_PASSWORD`: Admin password.
- `REGISTRY_HTTP_SECRET`, `CORE_SECRET`, `JOBSERVICE_SECRET`: Internal secrets.
- `POSTGRESQL_*`: External PostgreSQL connection.
- `_REDIS_URL_*`: External Redis (Valkey) connection.
- `EXT_ENDPOINT`: External URL (`https://harbor.${DEFAULT_URL}`).

## Network & Access

- All services attach to `infra_net`.
- Exposed Port: `${HARBOR_PORT}`.

> **Note**: Traefik labels are NOT explicitly defined in the provided `docker-compose.yml`. Ensure there is an external configuration or a separate routing setup handling `harbor.${DEFAULT_URL}`.
