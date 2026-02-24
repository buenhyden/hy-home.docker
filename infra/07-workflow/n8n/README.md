# n8n

n8n is a low-code workflow automation tool that allows you to connect any app.

## Services

| Service | Image               | Role               | Resources         |
| :------ | :------------------ | :----------------- | :---------------- |
| `n8n`   | `n8nio/n8n:latest` | Workflow Engine    | 0.5 CPU / 1GB RAM |

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
