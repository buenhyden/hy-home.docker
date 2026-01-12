# MinIO Object Storage

## Overview

MinIO is a high-performance, S3-compatible object storage server. This deployment is configured as a standalone node with initialization automation to ensure required buckets are created on startup.

## Services

### Server (`minio`)

- **Image**: `minio/minio:RELEASE.2025-09-07T16-13-09Z`
- **Role**: S3-compatible Object Storage
- **Console Port**: `${MINIO_CONSOLE_HOST_PORT}`
- **API Port**: `${MINIO_HOST_PORT}`

### Initialization (`minio-create-buckets`)

- **Image**: `minio/mc:RELEASE.2025-08-13T08-35-41Z`
- **Role**: Provisioning buckets on startup
- **Buckets Created**: `tempo-bucket`, `loki-bucket`, `cdn-bucket` (Public)

## Networking

This service is part of the `infra_net` network:

- **Network**: `infra_net`
- **Static IPv4**: `172.19.0.12`

## Persistence

- **`minio-data`** → `/data`: Persistent storage for objects.

## Configuration

Credentials are managed via Docker Secrets (`/run/secrets/`) mapped to environment variables.

| Variable | Description | Default |
| :--- | :--- | :--- |
| `MINIO_ROOT_USER_FILE` | Path to root user secret | `/run/secrets/minio_root_user` |
| `MINIO_ROOT_PASSWORD_FILE` | Path to root password secret | `/run/secrets/minio_root_password` |
| `MINIO_PROMETHEUS_AUTH_TYPE` | Prometheus scraping auth type | `public` |
| `MINIO_API_ROOT_ACCESS` | Enable root access via API | `on` |

## Traefik Integration

Two separate routers are configured:

| Service | Domain | Internal Port | Description |
| :--- | :--- | :--- | :--- |
| **S3 API** | `minio.${DEFAULT_URL}` | `${MINIO_PORT}` (9000) | Endpoint for SDKs/Apps |
| **Console** | `minio-console.${DEFAULT_URL}` | `${MINIO_CONSOLE_PORT}` (9001) | Web Management UI |

## Usage

### Web Console

- **URL**: `https://minio-console.<your-domain>`
- **Login**: Use Root or App credentials defined in your `.env` / secrets.

### S3 Endpoint

- **URL**: `https://minio.<your-domain>`
- **Region**: `us-east-1` (Default)
