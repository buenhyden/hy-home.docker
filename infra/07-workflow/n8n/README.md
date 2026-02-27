# n8n

n8n is a low-code workflow automation tool that allows you to connect any app.

## Services

| Service | Image | Role | Resources |
| :--- | :--- | :--- | :--- |
| `n8n` | `n8nio/n8n:2.6.2` | Main engine | 1.0 CPU / 2G |
| `worker`| `n8nio/n8n:2.6.2` | Job worker | 1.0 CPU / 2G |
| `runner`| `n8nio/runners:2.6.2` | Task runner | 0.5 CPU / 1G |
| `valkey`| `valkey:9.0.2` | Queue DB | 2.0 CPU / 1G |

## Networking

Exposed via Traefik at `n8n.${DEFAULT_URL}`.

> [!NOTE]
> `n8n` is currently not enabled in the root `docker-compose.yml` by default. Enable it by uncommenting the `infra/07-workflow/n8n/docker-compose.yml` include entry.

## Persistence

- **Database**: PostgreSQL (via `infra/04-data/mng-db`).
- **Data**: `/home/node/.n8n` (mounted to `n8n-data` volume).

## File Map

| Path                 | Description                          |
| -------------------- | ------------------------------------ |
| `docker-compose.yml` | n8n service and env configuration.   |
| `README.md`          | Service overview and usage notes.    |
