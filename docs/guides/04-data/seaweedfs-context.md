---
layer: infra
---
# SeaweedFS Distributed Object Storage Context

**Overview (KR):** SeaweedFS 분산 파일 시스템의 마스터-볼륨-파일러 아키텍처와 S3 호환 API 연동 가이드입니다.

> **Component**: `seaweedfs`
> **Profile**: `standalone` (Optional)
> **S3 API Port**: `8333`

## 1. System Role

SeaweedFS is a high-performance distributed object storage system with an S3-compatible API, capable of storing billions of files. It serves as an alternative to MinIO for large-scale deployments, CDN static asset serving, and long-term log/trace archival.

| URL | Purpose |
| :--- | :--- |
| `https://seaweedfs.${DEFAULT_URL}` | Master UI |
| `https://cdn.${DEFAULT_URL}` | Filer (CDN endpoint) |
| `https://s3.${DEFAULT_URL}` | S3-compatible API |

## 2. Architecture

SeaweedFS uses a four-component model:

```text
Client (S3/HTTP)
      |
[S3 Gateway :8333]  ← S3 API entry point
      |
[Filer :8888]       ← File system interface / CDN
      |
[Master :9333]      ← Metadata & volume allocation
      |
[Volume :8080]      ← Actual file data storage
```

- **Master**: Manages volume allocation and cluster topology.
- **Volume**: Stores the actual file data (up to 10,000 files/volume by default).
- **Filer**: Provides a file-system view and CDN capability.
- **S3 Gateway**: Translates S3 API calls to SeaweedFS operations.

## 3. Security Configuration

Authentication is managed via `security.toml` (mounted as a config file):

- **Internal JWT**: Signs all inter-component communication.
- **S3 Accounts**: Access/secret key pairs defined in `[aws.access.*]` blocks.

> [!WARNING]
> Change the JWT signing keys and S3 credentials from defaults before using in any non-local environment.

## 4. Key Ports

| Component | HTTP Port | gRPC Port |
| :--- | :--- | :--- |
| Master | `SEAWEEDFS_MASTER_HTTP_PORT` (9333) | `SEAWEEDFS_MASTER_GRPC_PORT` (19333) |
| Volume | `SEAWEEDFS_VOLUME_HTTP_PORT` (8080) | `SEAWEEDFS_VOLUME_GRPC_PORT` (18080) |
| Filer | `SEAWEEDFS_FILER_HTTP_PORT` (8888) | `SEAWEEDFS_FILER_GRPC_PORT` (18888) |
| S3 | `SEAWEEDFS_S3_HTTP_PORT` (8333) | — |

## 5. Persistence

| Volume | Purpose |
| :--- | :--- |
| `seaweedfs-master-data` | Cluster metadata (critical — back up regularly) |
| `seaweedfs-volume-data` | File content data |

## 6. Relationship to MinIO

Both SeaweedFS and MinIO provide S3-compatible object storage. SeaweedFS is preferred for very large file counts and CDN scenarios; MinIO is the default choice for LGTM observability backend (Loki/Tempo) due to its simpler configuration.
