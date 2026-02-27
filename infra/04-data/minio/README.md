# MinIO Object Storage

MinIO is an S3-compatible high-performance object storage server.

## Services

| Service | Image | Role | Resources |
| :--- | :--- | :--- | :--- |
| `minio` | `minio/minio:RELEASE.2025-09-07...` | Object Storage | 1.0 CPU / 1GB RAM |
| `minio-init` | `minio/mc:RELEASE.2025-08-13...` | Bucket Init | 128MB RAM |

## Networking

- **Internal DNS**: `minio:${MINIO_PORT:-9000}` (S3 API, within `infra_net`)
- **External (S3 API)**: `https://minio.${DEFAULT_URL}` (via Traefik)
- **External (Console)**: `https://minio-console.${DEFAULT_URL}` (via Traefik)

## Persistence

- **Data**: `minio-data` volume mapped to `${DEFAULT_DATA_DIR}/minio/data-1`.

## Configuration

- **Auto-Buckets**: Creates `tempo-bucket`, `loki-bucket`, `cdn-bucket`, `doc-intel-assets`.
- **Public CDN**: `cdn-bucket` is set to anonymous public access by default.
- **Credentials**: Injected via Docker secrets (`minio_root_username`, `minio_root_password`, `minio_app_username`, `minio_app_user_password`).

## File Map

| Path        | Description                         |
| ----------- | ----------------------------------- |
| `README.md` | Service overview and access notes.  |
