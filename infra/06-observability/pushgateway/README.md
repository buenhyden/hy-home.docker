# Pushgateway

Pushgateway allows ephemeral and batch jobs to expose metrics to Prometheus.

## Services

| Service       | Image                      | Role           | Resources      |
| :------------ | :------------------------- | :------------- | :------------- |
| `pushgateway` | `prom/pushgateway:v1.11.2` | Metrics buffer | 0.1 CPU / 64MB |

## Networking

| Endpoint                        | Port | Purpose               |
| :------------------------------ | :--- | :-------------------- |
| `pushgateway.${DEFAULT_URL}`    | 9091 | Metrics ingestion API |

> Port is exposed via Traefik (not published directly to the host). Prometheus scrapes it over `infra_net`.

## Notes

- **Use case**: Short-lived batch jobs or CI pipelines that cannot be scraped by Prometheus directly.
- **Caution**: Pushgateway is not a general-purpose metrics proxy. For long-running services, use the standard Prometheus pull model.
- **Retention**: Metrics remain in Pushgateway until deleted explicitly or the container restarts. There is no automatic expiry.

## File Map

| Path        | Description                       |
| ----------- | --------------------------------- |
| `README.md` | Service overview and usage notes. |
