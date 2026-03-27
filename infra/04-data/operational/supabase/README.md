<!-- [ID:04-data:supabase] -->
# Supabase Stack

> Open-source Firebase alternative with PostgreSQL, Auth, Realtime, and Storage.

## Overview

The `supabase` stack provides a complete, integrated backend for applications in `hy-home.docker`. It leverages PostgreSQL as the core engine, adding multiple layers for authentication, REST/GraphQL APIs, and file storage. It is designed to be a self-hosted alternative to Firebase, offering the full Supabase experience within a Docker environment.

## Audience

이 README의 주요 독자:

- Developers
- Operators
- AI Agents

## Scope

### In Scope

- Infrastructure configuration (`docker-compose.yml`, `.env.example`).
- Service mapping and internal networking.
- Persistence and volume management.
- Documentation references for internal services.

### Out of Scope

- Specific application logic using Supabase.
- External database migrations (managed via Studio or CLI).
- Global backup policies (refer to `docs/08.operations/04-data/`).

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

## Structure

```text
supabase/
├── volumes/            # Mounted database, pooler, and log configs
├── .env.example        # Environment variable template
├── docker-compose.yml  # Comprehensive stack configuration
└── README.md           # This file
```

## How to Work in This Area

1. Ensure the `.env` file is correctly configured based on `.env.example`.
2. Start the stack using `docker compose up -d`.
3. Access Supabase Studio at `http://localhost:3000`.
4. Refer to [Supabase Guide](../../../docs/07.guides/04-data/operational/supabase.md) for detailed architecture and usage.

## Related References

- **Guide**: [Supabase Guide](../../../docs/07.guides/04-data/operational/supabase.md)
- **Operations**: [Supabase Operations](../../../docs/08.operations/04-data/operational/supabase.md)
- **Runbook**: [Supabase Runbook](../../../docs/09.runbooks/04-data/operational/supabase.md)

---

## AI Agent Guidance

이 영역을 수정하기 전에 Agent는 다음을 먼저 수행해야 한다.

1. `docker-compose.yml`의 서비스 의존성을 확인한다.
2. `volumes/` 내의 설정 파일이 컨테이너 내부 경로와 일치하는지 확인한다.
3. 공유 최적화 파일(`../../../common-optimizations.yml`)의 영향을 고려한다.

