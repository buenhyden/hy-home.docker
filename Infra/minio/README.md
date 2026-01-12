# MinIO Object Storage

## Overview

MinIO is a high-performance, S3-compatible object storage server. This deployment is configured as a standalone node with initialization automation to ensure required buckets are created on startup.

## Architecture

- **Mode**: Standalone (Single Node)
- **Initialization**: Dedicated `minio-create-buckets` container runs at startup to provision buckets and users using the `mc` (MinIO Client) tool.
- **Security**: Root and App credentials are managed securely via **Docker Secrets**.

## Service Details

### 1. Server (`minio`)

- **Image**: `minio/minio:RELEASE.2025-09-07T16-13-09Z`
- **Console Port**: `${MINIO_CONSOLE_HOST_PORT}`
- **API Port**: `${MINIO_HOST_PORT}`
- **Volume**: `minio-data` (Mapped to `/data`)

### 2. Initialization Job (`minio-create-buckets`)

- **Image**: `minio/mc:RELEASE.2025-08-13T08-35-41Z`
- **Behavior**: Waits for MinIO to be healthy, then executes a script to:
    1. Authenticate as Root.
    2. Create App User (`$$APP_USER`).
    3. Grant `readwrite` policy.
    4. Create Buckets: `tempo-bucket`, `loki-bucket`, `cdn-bucket`.
    5. Set `cdn-bucket` to Public (Anonymous Read).
- **Lifecycle**: Exits after completion (`restart: "no"`).

## Networking

- **Network**: `infra_net`
- **Static IPv4**: `172.19.0.12`

## Secrets & Environment

Credentials are strictly managed via Docker Secrets located in `/run/secrets/`:

- `minio_root_user`
- `minio_root_password`
- `minio_app_user`
- `minio_app_user_password`

Environment variables map these secrets to the MinIO configuration:

- `MINIO_ROOT_USER_FILE`
- `MINIO_ROOT_PASSWORD_FILE`
- `MINIO_PROMETHEUS_AUTH_TYPE`: `public` (For monitoring)

## Traefik Configuration

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
