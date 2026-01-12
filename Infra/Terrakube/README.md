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

## Network

All Terrakube components are configured with **Dynamic IP** assignment on the `infra_net` network.

| Service | IP Address |
| :--- | :--- |
| `terrakube-api` | Dynamic (DHCP) |
| `terrakube-ui` | Dynamic (DHCP) |
| `terrakube-executor` | Dynamic (DHCP) |

## Environment Variables

### Common Configuration

| Variable | Description | Default |
| :--- | :--- | :--- |
| `InternalSecret` | Shared Secret | `${TERRAKUBE_INTERNAL_SECRET}` |
| `TerrakubeRedisHostname` | Redis Host | `${MNG_VALKEY_HOST}` |
| `TerrakubeRedisPassword` | Redis Password | `${VALKEY_PASSWORD}` |
| `TerrakubeRedisPort` | Redis Port | `${VALKEY_PORT}` |

### API Specific

| Variable | Description | Default |
| :--- | :--- | :--- |
| `ApiDataSourceType` | DB Type | `POSTGRESQL` |
| `DatasourceHostname` | DB Host | `${POSTGRES_HOSTNAME}` |
| `DatasourceUser` | DB User | `${TERRAKUBE_DB_USERNAME}` |
| `DatasourcePassword` | DB Password | `${TERRAKUBE_DB_PASSWORD}` |
| `GroupValidationType` | Auth Provider | `DEX` |
| `StorageType` | Storage Provider | `AWS` |
| `AwsStorageAccessKey` | S3 Access Key | `${MINIO_APP_USERNAME}` |
| `AwsStorageSecretKey` | S3 Secret Key | `${MINIO_APP_USER_PASSWORD}` |
| `AwsEndpoint` | S3 Endpoint | `http://minio:9000` |

### UI Specific

| Variable | Description | Default |
| :--- | :--- | :--- |
| `REACT_APP_TERRAKUBE_API_URL` | API URL | `https://terrakube-api...` |
| `REACT_APP_AUTHORITY` | Auth Authority | `https://keycloak...` |
| `REACT_APP_CLIENT_ID` | OAuth Client ID | `proxy-client` |

## Traefik Configuration

| Service | Host Rule | Port |
| :--- | :--- | :--- |
| **API** | `terrakube-api.${DEFAULT_URL}` | 8080 |
| **UI** | `terrakube-ui.${DEFAULT_URL}` | `${TERRAKUBE_UI_PORT}` |
| **Executor** | `terrakube-executor.${DEFAULT_URL}` | `${TERRAKUBE_EXECUTOR_PORT}` |

All services use the `infra_net` network and have `traefik.enable=true`.
