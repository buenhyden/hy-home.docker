# Observability Setup Guide

> Comprehensive guide to the LGTM (Loki, Grafana, Tempo, Metrics/Prometheus) stack configured in `06-observability`.

## 1. Stack Components

- **Grafana (Port: 3000)**: Visualization and alerting Dashboard.
- **Prometheus (Port: 9090)**: Metrics collection via pull model and target scraping.
- **Loki (Port: 3100)**: Log aggregation system integrated directly with Grafana.
- **Tempo (Port: 3200)**: Distributed tracing backend.
- **Alloy**: Telemetry collector that reads Docker logs and system stats, shipping them to upstream targets.
- **AlertManager / Pushgateway**: Auxiliary Prometheus tools for short-lived jobs and notification integrations.

## 2. Telemetry Ingestion Flow (Grafana Alloy)

Alloy serves as the OpenTelemetry Collector and unified agent.

1. **Logs**: Alloy reads `/var/lib/docker/containers` and pushes logs to Loki.
2. **Metrics**: Alloy scrapes Prom targets and pushes to Prometheus.
3. **Traces**: Alloy listens on OTLP ports (`4317` gRPC / `4318` HTTP) and routes traces to Tempo.

## 3. Storage Dependencies

Loki and Tempo utilize **MinIO** (from `04-data`) as their primary object storage backend.
> [!WARNING]
> Loki and Tempo will fail to start or operate correctly if the `minio` container is not healthy. Ensure MinIO is provisioned with appropriate keys before deploying observability.

## 4. Automatic Provisioning

Grafana is provisioned statelessly:

- **Dashboards**: Bind mounted via `./grafana/dashboards`.
- **Datasources**: Configured via `./grafana/provisioning/datasources/datasource.yml`.

To deploy changes to dashboards or datasources, simply update the JSON/YAML files and restart the Grafana container (`docker restart infra-grafana`).
