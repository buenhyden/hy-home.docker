# MinIO Object Storage (S3) Guide

> **Component**: `minio`
> **S3 API Port**: `9000`
> **Console Port**: `9001`

## 1. Roles and Endpoints

MinIO provides a high-performance S3 alternative for local and staging assets (Loki chunks, Postgres backups, etc.).

- **S3 Endpoint**: `https://minio.${DEFAULT_URL}`
- **Web Console**: `https://minio-console.${DEFAULT_URL}`

## 2. Initialization & Provisioning

MinIO is critical for the observability stack (Loki/Tempo backends).

### Mandatory Buckets

Required buckets (e.g., `loki-data`, `tempo-data`) must be automatically provisioned on startup (via init containers) or created manually via the UI before dependent services launch.

## 3. CLI Automation (mc)

The `mc` tool is the preferred way to manage buckets and policies.

```bash
# Setup local alias
mc alias set myminio https://minio.${DEFAULT_URL} admin ${MINIO_ROOT_PASSWORD}

# Create a private bucket for logs
mc mb myminio/system-logs
mc versioning enable myminio/system-logs
```

## 4. Data Resilience

MinIO is configured with a single-drive node by default for local dev, but mounts `${DEFAULT_DATA_DIR}/minio` for persistence.

- **Storage Class**: Standard S3-compatibility API logic applies.
- **Diagnostics**: Check `/run/secrets/` within the container to ensure root credentials are being correctly injected via Docker Secrets.
