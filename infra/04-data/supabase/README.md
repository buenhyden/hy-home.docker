<!-- [ID:04-data:supabase] -->
# Supabase Stack

> Open-source Firebase alternative with PostgreSQL and Auth.

## Overview (KR)

이 서비스는 PostgreSQL, Auth, Realtime, Storage를 포함한 **오픈 소스 Firebase 대안**입니다. 자체 호스팅 가능한 통합 백엔드 솔루션을 제공합니다.

## Overview

The `supabase` stack provides a complete, integrated backend for applications in `hy-home.docker`. It leverages PostgreSQL as the core engine, adding multiple layers for authentication, REST/GraphQL APIs, and file storage.

## Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **db** | PostgreSQL 15 | Core Database Engine (pgvector) |
| **auth** | GoTrue | JWT Authentication & Management |
| **rest** | PostgREST | Automated REST API Generation |
| **studio** | Supabase Studio | Web Management Dashboard |
| **kong** | Kong Gateway | API Gateway & Proxy |
| **realtime** | Realtime | WebSocket Change Propagation |
| **storage** | Storage API | Object Storage Management |

## Networking

| Component | Port | Description |
| :--- | :--- | :--- |
| **Kong HTTP** | `8000` | Unified API entrypoint (`supabase.${DEFAULT_URL}`). |
| **Studio UI** | `3000` | Web management dashboard. |

## Persistence

- **Database**: `${DEFAULT_DATA_DIR}/supabase/db/data`.
- **Storage**: `${DEFAULT_DATA_DIR}/supabase/storage`.
- **Functions**: `${DEFAULT_DATA_DIR}/supabase/functions`.
- **Logs**: `${DEFAULT_DATA_DIR}/supabase/logs`.

## File Map

| Path | Description |
| :--- | :--- |
| `docker-compose.yml` | Comprehensive stack (13+ services). |
| `volumes/` | Mounted database, pooler, and log configs. |

---

## Documentation References

- [Integrated DB Guide](../../../docs/07.guides/04-data/04.integrated-platforms.md)
- [Backup Operations](../../../docs/08.operations/04-data/README.md)
