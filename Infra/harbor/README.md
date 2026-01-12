# Harbor Registry

## Overview

Harbor is an open source trusted cloud native registry project that stores, signs, and scans content.

## Services

- **harbor-registry**: Stores and distributes Docker images.
- **harbor-registryctl**: Controls the registry.
- **harbor-core**: Core services (API, UI, webhook, token service).
  - URL: `https://harbor.${DEFAULT_URL}`
- **harbor-portal**: Frontend UI.
- **harbor-jobservice**: Asynchronous job execution framework.

## Configuration

### Environment Variables

- `HARBOR_ADMIN_PASSWORD`: Admin password.
- `REGISTRY_HTTP_SECRET`: Secret for registry security.
- `CORE_SECRET`: Secret for core service security.
- `JOBSERVICE_SECRET`: Secret for job service security.
- `EXT_ENDPOINT`: External URL (`https://harbor.${DEFAULT_URL}`).
- `DATABASE_TYPE`: `postgresql`
- `CHART_CACHE_DRIVER`: `redis`

### Volumes

- `harbor-registry-data-volume`: `/storage`
- `harbor-registry-conf-volume`: `/etc/registry`
- `harbor-registryctl-conf-volume`: `/etc/registryctl`
- `harbor-core-data-volume`: `/data`
- `harbor-core-conf-volume`: `/etc/core`
- `harbor-jobservice-logs-volume`: `/var/log/jobs`
- `harbor-jobservice-conf-volume`: `/etc/jobservice`

## Networks

- `infra_net`

## Traefik Routing

- **Domain**: `harbor.${DEFAULT_URL}`
- **Internally**: Traefik routes to `harbor-portal` (UI) and `harbor-core` (API) via specific path rules defined in `services.yml` or default behavior (here pointing to core/portal integration).
