# Terrakube

## Overview

Terrakube is an open-source alternative to Terraform Cloud/Enterprise. It allows you to manage Terraform operations, including remote state management and execution. This setup includes the API, UI, and Executor components.

## Service Details

### 1. Terrakube API (`terrakube-api`)

- **Image**: `azbuilder/api-server:2.29.0`
- **Internal Port**: `8080`
- **Dependencies**: `mng-pg` (PostgreSQL), `mng-redis` (Redis), `keycloak`, `minio`.

### 2. Terrakube UI (`terrakube-ui`)

- **Image**: `azbuilder/terrakube-ui:2.29.0`
- **Internal Port**: `${TERRAKUBE_UI_PORT}`

### 3. Terrakube Executor (`terrakube-executor`)

- **Image**: `azbuilder/executor:2.29.0`
- **Internal Port**: `${TERRAKUBE_EXECUTOR_PORT}`
- **Volumes**: `/var/run/docker.sock:/var/run/docker.sock`

## Environment Variables

### Common

- `InternalSecret`: Shared secret for internal communication.
- `TerrakubeRedisHostname`, `TerrakubeRedisPassword`, `TerrakubeRedisPort`: Connection to Valkey/Redis.

### API Specific

- `Datasource*`: PostgreSQL connection details.
- `GroupValidationType`, `UserValidationType`, `AuthenticationValidationType`: set to "DEX" (using Keycloak).
- `PatSecret`: Personal Access Token secret.
- `StorageType`: AWS (MinIO).
- `AwsStorage*`: MinIO credentials and bucket config.

### UI Specific

- `REACT_APP_TERRAKUBE_API_URL`: URL for the API.
- `REACT_APP_AUTHORITY`: Keycloak realm URL.
- `REACT_APP_CLIENT_ID`: OAuth client ID.

## Traefik Configuration

| Service | Host Rule | Port |
| :--- | :--- | :--- |
| **API** | `terrakube-api.${DEFAULT_URL}` | 8080 |
| **UI** | `terrakube-ui.${DEFAULT_URL}` | `${TERRAKUBE_UI_PORT}` |
| **Executor** | `terrakube-executor.${DEFAULT_URL}` | `${TERRAKUBE_EXECUTOR_PORT}` |

All services use the `infra_net` network and have `traefik.enable=true`.
