# Pushgateway

Pushgateway allows ephemeral and batch jobs to expose their metrics to Prometheus.

## Services

| Service       | Image                      | Role           | Resources         |
| :------------ | :------------------------- | :------------- | :---------------- |
| `pushgateway` | `prom/pushgateway:v1.11.0` | Metrics Buffer | 0.1 CPU / 64MB    |

## Networking

| Port | Purpose                |
| :--- | :--------------------- |
| 9091 | Metrics ingestion API  |

## Notes

- **Caution**: Pushgateway should only be used for batch/short-lived jobs. For long-running services, use the standard Prometheus pull model.

## File Map

| Path        | Description                         |
| ----------- | ----------------------------------- |
| `README.md` | Service overview and usage notes.   |
