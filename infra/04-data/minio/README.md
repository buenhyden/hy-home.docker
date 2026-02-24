# MinIO Object Storage

MinIO is an S3-compatible high-performance object storage server.

## Services

| Service | Image | Role | Resources |
| :--- | :--- | :--- | :--- |
| `minio` | `minio/minio:RELEASE.2025-09-07...` | Object Storage | 1.0 CPU / 1GB RAM |
| `minio-init` | `minio/mc:RELEASE.2025-08-13...` | Bucket Init | 128MB RAM |

## Networking

- **Static IP**: `172.19.0.12`
- **S3 API**: `minio.${DEFAULT_URL}` (Port 9000)
- **Web Console**: `minio-console.${DEFAULT_URL}` (Port 9001)

## Persistence

- **Data**: `minio-data` volume mapped to `${DEFAULT_DATA_DIR}/minio/data-1`.

## Configuration

- **Auto-Buckets**: Creates `tempo-bucket`, `loki-bucket`, `cdn-bucket`, `doc-intel-assets`.
- **Public CDN**: `cdn-bucket` is set to anonymous public access by default.
| Variable             | Description        | Value                  |
| :------------------- | :----------------- | :--------------------- |
| `MINIO_ROOT_USER`    | Admin Username     | `${MINIO_ROOT_USER}`   |
| `MINIO_ROOT_PASSWORD`| Admin Password     | `${MINIO_ROOT_PASSWORD}`|

## File Map

| Path        | Description                         |
| ----------- | ----------------------------------- |
| `README.md` | Service overview and access notes.  |
