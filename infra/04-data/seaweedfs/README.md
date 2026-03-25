<!-- [ID:04-data:seaweedfs] -->
# SeaweedFS

> High-performance distributed file system and object storage.

## Overview (KR)

이 서비스는 대용량 파일 저장과 빠른 제공을 위해 설계된 **고성능 분산 파일 시스템**입니다. S3 호환 API를 지원하며, CDN 백엔드 및 로그 저장소로 활용됩니다.

## Overview

The `seaweedfs` stack provides a resilient and scalable storage layer for unstructured data. It utilizes a master-volume-filer architecture to achieve high throughput and low metadata overhead, serving as a primary storage backend for media and logs.

## Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **master** | SeaweedFS Master | Metadata Management |
| **volume** | SeaweedFS Volume | Data Storage |
| **filer** | SeaweedFS Filer | File System Interface |
| **s3** | SeaweedFS S3 | S3 Compatible API |
| **mount** | SeaweedFS Mount | FUSE Mount Utility |

## Networking

| Component | Port | Description |
| :--- | :--- | :--- |
| **Master** | `9333` | Manager Interface (`seaweedfs.${DEFAULT_URL}`). |
| **Filer** | `8888` | HTTP File Access (`cdn.${DEFAULT_URL}`). |
| **S3** | `8333` | S3 API endpoint (`s3.${DEFAULT_URL}`). |

## Persistence

- **Volumes**: `seaweedfs-master-data` and `seaweedfs-volume-data`.
- **Mount**: `/mnt/seaweedfs` on the host via FUSE.
- **Path**: `${DEFAULT_DATA_DIR}/seaweedfs` on the host for configuration.

## Operations

### Checking Cluster Status

```bash
curl http://localhost:9333/cluster/status
```

## File Map

| Path | Description |
| :--- | :--- |
| `docker-compose.yml` | Distributed stack definition. |
| `config/` | Security and network configurations. |

---

## Documentation References

- [Storage Guide](../../../docs/07.guides/04-data/02.storage.md)
- [Backup Operations](../../../docs/08.operations/04-data/README.md)
