<!-- [ID:04-data:minio] -->
# MinIO Object Storage

> S3-compatible high-performance object storage server.

## 1. Context (SSoT)

MinIO serves as the primary object storage layer. It is used for infrastructure persistence (Loki logs, Tempo traces) and as a public CDN for application assets.

- **Status**: Production / Storage
- **Protocol**: S3 Compatible
- **SSoT Documentation**: [docs/07.guides/04-data/02.storage.md](../../../docs/07.guides/04-data/02.storage.md)

## 2. Structure

```text
minio/
├── docker-compose.yml   # Server & MC initialization
└── README.md            # Service overview
```

## 3. Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **minio** | MinIO RELEASE.2025+ | S3 API Server |
| **minio-init** | MinIO Client (mc) | Bucket & Policy Init |

## 4. Configuration (Secrets & Env)

- **Secrets**: `MINIO_ROOT_USER_FILE`, `MINIO_ROOT_PASSWORD_FILE`.
- **Auto-Buckets**: Initializes `tempo`, `loki`, `cdn`, and `doc-intel` on startup.
- **CDN Policy**: `cdn-bucket` has public anonymous access.

## 5. Persistence

- **Data**: `minio-data` volume mapped to `${DEFAULT_DATA_DIR}/minio/data-1`.

## 6. Operational Status

- **API**: `minio:9000` / `https://minio.${DEFAULT_URL}`
- **Console**: `minio:9001` / `https://minio-console.${DEFAULT_URL}`

---
Copyright (c) 2026. Licensed under the MIT License.
