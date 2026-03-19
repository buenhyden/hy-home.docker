# Observability Stack (06-observability)

This category manages the LGTM (Loki, Grafana, Tempo, Mimir/Prometheus) stack for monitoring, logging, and tracing.

## Stack Overview

| Service | Image | Role |
| :--- | :--- | :--- |
| `prometheus` | `prom/prometheus:v3.9.0` | Metrics storage |
| `loki` | `hy/loki:3.6.6-custom` | Log storage (S3 backend via MinIO) |
| `tempo` | `hy/tempo:2.10.1-custom` | Trace storage (S3 backend via MinIO) |
| `grafana` | `grafana/grafana:12.3.3` | Dashboards / UI |
| `alloy` | `grafana/alloy:v1.13.1` | Telemetry collector / OTLP endpoint |
| `alertmanager`| `prom/alertmanager:v0.30.0`| Alert routing |
| `pushgateway` | `prom/pushgateway:v1.11.2`| Ephemeral metrics |
| `cadvisor` | `gcr.io/cadvisor/cadvisor:v0.55.1` | Container metrics |
| `pyroscope` | `grafana/pyroscope:1.18.1` | Continuous profiling |

## Dependencies

- **Storage**: Loki and Tempo use MinIO (S3) buckets; Prometheus/Grafana/etc. persist to bind-mounted volumes under `${DEFAULT_OBSERVABILITY_DIR}`.
- **Network**: All services communicate via Docker DNS on `infra_net` (no static IP assumptions).
- **Auth**: Grafana is protected via Traefik SSO middleware and integrates with Keycloak (generic OAuth).

## File Map

| Path             | Description                                   |
| ---------------- | --------------------------------------------- |
| `docker-compose.yml` | Integrated observability stack definition. |
| `prometheus/`     | Prometheus config and rules.                  |
| `grafana/`        | Dashboards, datasources, and provisioning.    |
| `loki/`           | Loki configuration.                           |
| `tempo/`          | Tempo configuration.                          |
| `alloy/`          | Alloy pipeline config.                        |
| `alertmanager/`   | Alertmanager routing config.                  |
| `pushgateway/`    | Pushgateway service (no config dir).          |
| `pyroscope/`      | Pyroscope profiling backend config.           |
| `README.md`       | Category overview.                            |
