# Alertmanager

Alertmanager handles alerts sent by client applications such as the Prometheus server.

## Services

| Service        | Image                          | Role           | Resources         |
| :------------- | :----------------------------- | :------------- | :---------------- |
| `alertmanager` | `prom/alertmanager:v0.28.0`    | Alert Router   | 0.1 CPU / 128MB   |

## Networking

| Endpoint                      | Port | Purpose                |
| :---------------------------- | :--- | :--------------------- |
| `alertmanager.${DEFAULT_URL}` | 9093 | Web UI / API           |

## Configuration

- **Config**: Defined in `config/alertmanager.yml`.
- **Routes**: Configured to route alerts to email, Slack, or other receivers.

## File Map

| Path                   | Description                   |
| ---------------------- | ----------------------------- |
| `config/alertmanager.yml` | Alert routing configuration. |
| `README.md`            | Service notes.                |
