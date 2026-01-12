# MinIO

## Overview

High Performance Object Storage compatible with Amazon S3 API.

## Services

- **minio**: MinIO Server.
  - S3 API: `https://minio.${DEFAULT_URL}`
  - Console: `https://console.minio.${DEFAULT_URL}`
- **minio-create-buckets**: Initialization container to create buckets and users.

## Configuration

### Environment Variables

- `MINIO_ROOT_USER_FILE`: Root username file location.
- `MINIO_ROOT_PASSWORD_FILE`: Root password file location.
- `MINIO_PROMETHEUS_AUTH_TYPE`: `public` (for metrics).

### Volumes

- `minio-data`: `/data`

## Networks

- `infra_net`
  - IP: `172.19.0.12`

## Traefik Routing

- **API Domain**: `minio.${DEFAULT_URL}` (Port 9000)
- **Console Domain**: `minio-console.${DEFAULT_URL}` (Port 9001)
