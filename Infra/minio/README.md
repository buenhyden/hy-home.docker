# MinIO

## Overview

MinIO is a high-performance, S3 compatible object storage. This setup includes the MinIO server and a helper container for automatic bucket creation.

## Service Details

### Server (`minio`)

- **Image**: `minio/minio:RELEASE.2025-09-07T16-13-09Z`
- **Console Address**: `:${MINIO_CONSOLE_HOST_PORT}`
- **Network**: `infra_net` (Static IP: `172.19.0.12`)
- **Volume**: `minio-data` (Mapped to `/data`)

### Bucket Creator (`minio-create-buckets`)

- **Purpose**: Automatically creates buckets (`tempo-bucket`, `loki-bucket`, `cdn-bucket`) and sets policies on startup.
- **Image**: `minio/mc:RELEASE.2025-08-13T08-35-41Z`
- **Exits**: After completion (`restart: "no"`)

## Environment Variables & Secrets

- **Secrets**: `minio_root_user`, `minio_root_password`, `minio_app_user`, `minio_app_user_password`.
- **Environment**:
  - `MINIO_ROOT_USER_FILE`, `MINIO_ROOT_PASSWORD_FILE`: Paths to secrets.
  - `MINIO_PROMETHEUS_AUTH_TYPE`: `public`.

## Traefik Configuration

| Service | Host Rule | Internal Port | Description |
| :--- | :--- | :--- | :--- |
| **API** (S3) | `minio.${DEFAULT_URL}` | `${MINIO_PORT}` (9000) | S3 API Endpoint |
| **Console** | `minio-console.${DEFAULT_URL}` | `${MINIO_CONSOLE_PORT}` (9001) | Web Admin UI |
