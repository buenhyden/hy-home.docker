# MinIO Object Storage (S3) Guide

> **Component**: `minio`
> **S3 API Port**: `9000`
> **Console Port**: `9001`

## 1. Roles and Endpoints

MinIO is the primary S3-compatible cold storage for the LGTM stack (Tempo/Loki).

### Technical Specifications

| Attribute | Internal DNS | Internal Port | External Port (Proxy) |
| --- | --- | --- | --- |
| **API Endpoint** | `minio` | `9000` | `minio.${DEFAULT_URL}` |
| **Console UI** | `minio` | `9001` | `minio-console.${DEFAULT_URL}` |
| **Hardening** | Standard | `no-new-privileges`, `cap_drop` | [Verified] |

## 2. Bucket Automation & Provisioning

Buckets are automatically provisioned by the `minio-create-buckets` container using the `mc` tool.

### Managed Buckets

- `tempo-bucket`: Cold storage for tracing.
- `loki-bucket`: Log chunk persistence.
- `cdn-bucket`: Publicly accessible assets.
- `doc-intel-assets`: AI processing state.

### Provisioning Verification

```bash
docker logs minio-create-buckets
```

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
