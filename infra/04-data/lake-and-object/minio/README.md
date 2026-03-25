# MinIO Object Storage

> S3-compatible high-performance object storage server.

## 1. Context & Objective

MinIO serves as the primary object storage layer for the `hy-home.docker` ecosystem. It provides persistence for infrastructure workloads (Loki logs, Tempo traces) and serves as a public asset repository for applications.

### Role
- **Infrastructure Persistence**: Backend for observability stacks.
- **Public CDN**: Distributed asset delivery.

## 2. Requirements & Constraints

- **Protocol**: S3 Compatible API.
- **Secrets**: ROOT credentials MUST be managed via `MINIO_ROOT_USER_FILE` and `MINIO_ROOT_PASSWORD_FILE`.
- **Persistence**: Data is mapped to `${DEFAULT_DATA_DIR}/minio`.

## 3. Setup & Installation

### Deployment
```bash
# Start the MinIO stack
docker compose up -d
```

### Automatic Initialization
The `minio-init` service automatically creates the following buckets:
- `tempo`, `loki`: Observability.
- `cdn`: Public assets (Public/Anonymous access enabled).
- `doc-intel`: Document processing.

## 4. Usage & Integration

### Operational Endpoints
- **API (S3)**: `minio:9000` / `https://minio.${DEFAULT_URL}`
- **Console (UI)**: `minio:9001` / `https://minio-console.${DEFAULT_URL}`

### Integration Pointers
- Consult the [Object Storage Guide](../../../docs/07.guides/04-data/03.storage.md) for SDK examples.
- Use `mc` (MinIO Client) for administrative tasks.

## 5. Maintenance & Safety

### Health & Safety
1. Monitor volume usage for `minio-data` to prevent storage exhaustion.
2. Bucket policies should follow the Principle of Least Privilege (except for `cdn`).
3. Always rotate root credentials via the defined secret management process.

---

Copyright (c) 2026. Licensed under the MIT License.
