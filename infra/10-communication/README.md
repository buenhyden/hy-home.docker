# Communication (10-communication)

This category manages external communication services: a dev SMTP trap (MailHog) and a production-capable mail server (Stalwart).

## Services

| Service | Profile | Path | Purpose |
| :--- | :--- | :--- | :--- |
| MailHog | `communication` | `./mail` | Dev SMTP relay — captures mail in memory, no external delivery |
| Stalwart | `communication` | `./mail` | Production SMTP/IMAP mail server with TLS and web admin |

> Both services share the `communication` profile and live in the same `mail/docker-compose.yml`.

## File Map

| Path | Description |
| :--- | :--- |
| `mail/` | MailHog and Stalwart service definitions. |
| `mail/docker-compose.yml` | Compose file with both MailHog and Stalwart services. |
| `README.md` | Category overview (this file). |
