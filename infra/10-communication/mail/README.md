# Mail (MailHog)

A developer-focused email testing tool with a built-in SMTP server and web UI.

## Services

| Service | Image | Role | Resources | Portal |
| :--- | :--- | :--- | :--- | :--- |
| `mailhog` | `mailhog:v1.0.1` | SMTP Test | 0.5 CPU / 512M | `mail.${DEFAULT_URL}` |

## Networking

- **SMTP**: `mailhog:1025`.
- **Web UI**: `mail.${DEFAULT_URL}` (via Traefik).

## Note

Check the `docker-compose.yml` comments for an alternative production-ready **Stalwart** configuration.

## File Map

| Path                 | Description                                  |
| -------------------- | -------------------------------------------- |
| `docker-compose.yml` | MailHog service definition.                  |
| `README.md`          | Service overview and SMTP settings.          |
