# Observability Stack (06-observability)

This category manages the LGTM (Loki, Grafana, Tempo, Mimir/Prometheus) stack for monitoring, logging, and tracing.

## Stack Overview

| Service | Image | Role | IP |
| :--- | :--- | :--- | :--- |
| `prometheus` | `prometheus:v3.9.0` | Metrics Storage | `172.19.0.30` |
| `loki` | `loki:3.6.6` | Log Storage | `172.19.0.31` |
| `tempo` | `tempo:2.10.1` | Trace Storage | `172.19.0.32` |
| `grafana` | `grafana:12.3.3` | Visualization | `172.19.0.33` |
| `alloy` | `alloy:v1.13.1` | Telemetry Collector| `172.19.0.34` |
| `alertmanager`| `alertmanager:v0.30.0`| Alert Routing | `172.19.0.36` |
| `pushgateway` | `pushgateway:v1.11.2`| Ephemeral Metrics | `172.19.0.37` |
| `cadvisor` | `cadvisor:v0.55.1` | Container Metrics | `172.19.0.35` |

## Dependencies

- **Storage**: Objects are backed by MinIO (`tfstate` bucket for state, etc.) and local volumes.
- **Network**: All services on `infra_net` with static IP assignments.
- **Auth**: SSO via Keycloak for Grafana and potentially Prometheus/Alertmanager.

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
