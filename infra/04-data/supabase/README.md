# Supabase

Self-hosted Supabase stack provides an open-source Firebase alternative with PostgreSQL, Auth, Realtime, and Storage.

## Stack Overview (Standalone)

Supabase runs as a complex set of integrated services, typically managed as a standalone stack.

## Services (Partial List)

| Service | Image | Role |
| :--- | :--- | :--- |
| `db` | `supabase/postgres:15.14.1...`| Core Database |
| `auth` | `supabase/gotrue:v2.182.1` | GoTrue Auth |
| `rest` | `postgrest/postgrest:v13.0.8` | PostgREST API |
| `studio` | `supabase/studio:2025.11.10...`| Management GUI |
| `kong` | `kong:3.9.1` | API Gateway |

## Networking

Accessed via **Kong** bridge:

- **HTTP**: `http://localhost:${SUPABASE_KONG_HTTP_PORT}` (External)
- **HTTPS**: `https://localhost:${SUPABASE_KONG_HTTPS_PORT}` (External)
- **Studio**: Port 3000 (Internal)

## Persistence

- **Database**: `./volumes/db/data`
- **Storage**: `./volumes/storage`
- **Functions**: `./volumes/functions`

## Configuration

- **Auth**: Uses `supabase_db_password`, `supabase_jwt_secret`, `supabase_anon_key`, and `supabase_service_key` secrets.
- **Edge Runtime**: `supabase-edge-functions` runs custom Deno tasks.

## Configuration

### Core Variables

| Variable                | Description              | Value                           |
| :---------------------- | :----------------------- | :------------------------------ |
| `POSTGRES_PASSWORD`     | DB Password              | `${POSTGRES_PASSWORD}`          |
| `JWT_SECRET`            | Auth Token Secret        | `${SUPABASE_JWT_SECRET}`        |
| `SERVICE_ROLE_KEY`      | Admin API Key            | `${SUPABASE_SERVICE_ROLE_KEY}`  |
| `ANON_KEY`              | Public API Key           | `${SUPABASE_ANON_KEY}`          |

## File Map

| Path                 | Description                                      |
| -------------------- | ------------------------------------------------ |
| `docker-compose.yml` | Full Supabase stack (20+ services).              |
| `volumes/`           | Default volume mount points for DB and logs.     |
| `README.md`          | Service overview and self-hosting notes.         |
