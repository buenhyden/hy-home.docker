# Observability Stack (06-observability)

This category manages the LGTM (Loki, Grafana, Tempo, Mimir/Prometheus) stack for monitoring, logging, and tracing.

## Stack Overview

| Service      | Purpose                   | Endpoint                      |
| ------------ | ------------------------- | ----------------------------- |
| Prometheus   | Metrics collection        | `prometheus.${DEFAULT_URL}`   |
| Grafana      | Visualization & Alerting  | `grafana.${DEFAULT_URL}`      |
| Loki         | Log aggregation           | (Port 3100)                   |
| Tempo        | Distributed tracing       | (Port 3200)                   |
| Alloy        | Telemetry collector      | (Local agent)                 |
| Alertmanager | Alert routing             | `alertmanager.${DEFAULT_URL}` |

## Dependencies

- **Storage**: services use named volumes (e.g., `loki-data`, `prometheus-data`).
- **Network**: All services reside on `infra_net` for internal scraping.

## File Map

| Path             | Description                                   |
| ---------------- | --------------------------------------------- |
| `docker-compose.yml` | Integrated observability stack definition. |
| `prometheus/`     | Prometheus config and rules.                  |
| `grafana/`        | Dashboards, datasources, and provisioning.    |
| `loki/`           | Loki configuration.                           |
| `tempo/`          | Tempo configuration.                          |
| `alloy/`          | Alloy pipeline config.                        |
| `README.md`       | Category overview.                            |
