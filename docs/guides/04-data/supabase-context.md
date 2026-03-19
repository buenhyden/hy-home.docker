---
layer: infra
---
# Supabase Self-Hosted Stack Context

**Overview (KR):** 자체 호스팅 Supabase 스택의 서비스 구성, 인증 흐름, 그리고 외부 서비스 연동을 위한 컨텍스트 가이드입니다.

> **Component**: `supabase`
> **Profile**: `standalone` (Complex multi-service stack)
> **Gateway**: `kong` (API Gateway, ports `SUPABASE_KONG_HTTP_PORT` / `SUPABASE_KONG_HTTPS_PORT`)

## 1. System Role

Supabase provides an open-source Firebase-alternative platform, bundling PostgreSQL, Auth (GoTrue), Realtime, Storage, and a management Studio UI. It operates as a standalone, self-contained stack, **not** integrated into the main `infra_net` network by default.

- **Studio UI**: `http://localhost:${SUPABASE_KONG_HTTP_PORT}` → internally on port `3000`
- **API Access**: All calls route through Kong at `localhost:${SUPABASE_KONG_HTTP_PORT}`

## 2. Service Architecture

```text
[Client]
   |
[Kong :KONG_PORT]    ← API Gateway (auth, routing)
   ├── [PostgREST]   ← Auto-generated REST API
   ├── [GoTrue]      ← Auth service (JWT, OAuth)
   ├── [Realtime]    ← WebSocket subscriptions
   ├── [Storage]     ← S3-compatible file storage
   └── [Studio]      ← Management UI
          |
       [PostgreSQL]  ← Supabase-patched Postgres 15
```

## 3. Key Secrets

| Secret | Description |
| :--- | :--- |
| `supabase_db_password` | Supabase Postgres password |
| `supabase_jwt_secret` | JWT signing secret (must be 32+ chars) |
| `supabase_anon_key` | Public (anon) API key |
| `supabase_service_key` | Private service-role API key |

> [!IMPORTANT]
> The `supabase_anon_key` and `supabase_service_key` are JWT tokens pre-signed with `supabase_jwt_secret`. If the JWT secret changes, both keys must be regenerated.

## 4. Configuration Variables

| Variable | Description |
| :--- | :--- |
| `SUPABASE_KONG_HTTP_PORT` | External HTTP port for Kong |
| `SUPABASE_KONG_HTTPS_PORT` | External HTTPS port for Kong |
| `SUPABASE_JWT_SECRET` | JWT signing key |
| `SUPABASE_ANON_KEY` | Public client API key |
| `SUPABASE_SERVICE_ROLE_KEY` | Admin API key |

## 5. Persistence

| Path | Content |
| :--- | :--- |
| `${DEFAULT_DATA_DIR}/supabase/db/data` | PostgreSQL data directory |
| `${DEFAULT_DATA_DIR}/supabase/storage` | File storage objects |
| `${DEFAULT_DATA_DIR}/supabase/functions` | Edge function code |

## 6. Integration Notes

- Supabase runs its own embedded Postgres. Do **not** use the `mng-pg` or `postgresql-cluster` instances for Supabase data.
- The stack does not use Traefik by default; Kong manages routing and TLS termination internally.
- Edge functions run in a Deno runtime (`supabase-edge-functions`).
