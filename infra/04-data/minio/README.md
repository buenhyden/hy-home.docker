# MinIO Object Storage

MinIO is an S3-compatible high-performance object storage server.

## Services

| Service | Image                                | Role           | Resources         | Port       |
| :------ | :----------------------------------- | :------------- | :---------------- | :--------- |
| `minio` | `quay.io/minio/minio:RELEASE.2025-01-20T14-44-24Z` | Object Store   | 0.5 CPU / 1GB RAM | 9000, 9001 |

## Networking

| Endpoint             | Port | Purpose             |
| :------------------- | :--- | :------------------ |
| `s3.${DEFAULT_URL}`  | 9000 | API (S3 compatible) |
| `oss.${DEFAULT_URL}` | 9001 | Web Console         |

## Persistence

- **Data**: `/data` (mounted to `minio-data` volume).

## Configuration

| Variable             | Description        | Value                  |
| :------------------- | :----------------- | :--------------------- |
| `MINIO_ROOT_USER`    | Admin Username     | `${MINIO_ROOT_USER}`   |
| `MINIO_ROOT_PASSWORD`| Admin Password     | `${MINIO_ROOT_PASSWORD}`|

## File Map

| Path        | Description                         |
| ----------- | ----------------------------------- |
| `README.md` | Service overview and access notes.  |
