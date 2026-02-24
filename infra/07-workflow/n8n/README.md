# n8n

n8n is a low-code workflow automation tool that allows you to connect any app.

## Services

| Service | Image | Role | IP | Resources |
| :--- | :--- | :--- | :--- | :--- |
| `n8n` | `n8nio/n8n:2.6.2` | Main Engine | `172.19.0.14` | 1.0 CPU / 2G |
| `worker`| `n8nio/n8n:2.6.2` | Job Worker | `172.19.0.17` | 1.0 CPU / 2G |
| `runner`| `n8nio/runners:2.6.2` | Task Runner | `172.19.0.74` | 0.5 CPU / 1G |
| `valkey`| `valkey:9.0.2` | Queue DB | `172.19.0.15` | 2.0 CPU / 1G |

## Networking

Exposed via Traefik at `n8n.${DEFAULT_URL}`.

## Persistence

- **Database**: PostgreSQL (via `infra/04-data/mng-db`).
- **Data**: `/home/node/.n8n` (mounted to `n8n-data` volume).

## File Map

| Path                 | Description                          |
| -------------------- | ------------------------------------ |
| `docker-compose.yml` | n8n service and env configuration.   |
| `README.md`          | Service overview and usage notes.    |
