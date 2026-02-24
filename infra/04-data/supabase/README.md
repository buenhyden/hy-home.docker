# Supabase

Self-hosted Supabase stack provides an open-source Firebase alternative with PostgreSQL, Auth, Realtime, and Storage.

## Stack Overview (Standalone)

Supabase runs as a complex set of integrated services, typically managed as a standalone stack.

| Service       | Role                     | Endpoint                     |
| :------------ | :----------------------- | :--------------------------- |
| `kong`        | API Gateway              | `supabase.${DEFAULT_URL}`    |
| `studio`      | Dashboard UI             | `dashboard.${DEFAULT_URL}`   |
| `auth`        | GoTrue Auth server       |                              |
| `db`          | PostgreSQL + PostgREST   |                              |
| `storage`     | S3-compatible storage    |                              |
| `realtime`    | Websocket sync server    |                              |

## Networking

| Endpoint                   | Port | Purpose                 |
| :------------------------- | :--- | :---------------------- |
| `supabase.${DEFAULT_URL}`  | 8000 | Kong API Gateway        |
| `dashboard.${DEFAULT_URL}` | 3000 | Supabase Studio Console |

## Persistence

- **Database**: Uses local PostgreSQL volume or external cluster.
- **Storage**: Files are persisted in the `storage` volume.

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
