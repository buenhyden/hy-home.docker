# Alertmanager

Alertmanager handles alerts sent by Prometheus and routes them to configured notification channels.

## Services

| Service        | Image                       | Role         | Resources       |
| :------------- | :-------------------------- | :----------- | :-------------- |
| `alertmanager` | `prom/alertmanager:v0.30.0` | Alert router | 0.1 CPU / 128MB |

## Networking

| Endpoint                      | Port | Purpose        |
| :---------------------------- | :--- | :------------- |
| `alertmanager.${DEFAULT_URL}` | 9093 | Web UI / API   |

## Configuration

- **Config**: Defined in `config/config.yml`. The file uses `__SMTP_USERNAME__`, `__SMTP_PASSWORD__`, and `__SLACK_WEBHOOK_URL__` placeholders that are substituted at container startup from Docker Secrets.
- **Routes**: Configured to route all alerts to the `team-notifications` receiver (Slack + Email).

## Secrets

| Secret name       | Purpose                               |
| :---------------- | :------------------------------------ |
| `smtp_username`   | Gmail SMTP account for email alerts.  |
| `smtp_password`   | Gmail app password (16-character).    |
| `slack_webhook`   | Slack Incoming Webhook URL.           |

## File Map

| Path               | Description                       |
| ------------------ | --------------------------------- |
| `config/config.yml`| Alert routing configuration.      |
| `README.md`        | Service notes.                    |
