<!-- [ID:04-data:minio] -->
# MinIO Object Storage

> S3-compatible high-performance object storage server.

## Overview (KR)

MinIO는 고성능 S3 호환 객체 스토리지 서버입니다. 고성능 인프라 데이터(Tempo, Loki 등)와 CDN 에셋을 저장하는 데 사용됩니다.

## Overview

MinIO serves as the primary object storage layer for the `hy-home.docker` ecosystem. It is used both for infrastructure persistence (e.g., storing Loki logs and Tempo traces) and as a public CDN for application assets.

## Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **minio** | MinIO RELEASE.2025+ | S3 API Server |
| **minio-init** | MinIO Client (mc) | Bucket & Policy Initialization |

## Networking

- **Internal DNS**: `minio:9000` (API), `minio:9001` (Console)
- **External URL**:
  - API: `https://minio.${DEFAULT_URL}`
  - Console: `https://minio-console.${DEFAULT_URL}`

## Persistence

- **Data**: `minio-data` volume mapped to `${DEFAULT_DATA_DIR}/minio/data-1`.

## Configuration

- **Auto-Buckets**: The system automatically initializes buckets for `tempo`, `loki`, `cdn`, and `doc-intel` on first start.
- **CDN Policy**: The `cdn-bucket` is configured with public anonymous access for static asset hosting.

## File Map

| Path | Description |
| :--- | :--- |
| `docker-compose.yml` | MinIO server and initialization logic. |
| `README.md` | Service overview. |

---

## Documentation References

- [Storage Guide](../../../docs/07.guides/04-data/02.storage.md)
- [Backup Operations](../../../docs/08.operations/04-data/README.md)
