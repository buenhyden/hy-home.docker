# Observability Stack (LGTM + Alloy)

## Overview

A comprehensive observability stack based on the **LGTM** (Loki, Grafana, Tempo, Mimir-like Prometheus) pattern, with **Grafana Alloy** as the central collector.

## Services

| Service | Image | Role |
| :--- | :--- | :--- |
| [`prometheus`](./prometheus/README.md) | `prom/prometheus:v3.9.0` | Metrics Database (Time Series) |
| [`loki`](./loki/README.md) | `grafana/loki:3.6.3` | Logs Aggregation System |
| [`tempo`](./tempo/README.md) | `grafana/tempo:2.9.0` | Distributed Tracing Backend |
| [`grafana`](./grafana/README.md) | `grafana/grafana:12.3.1` | Visualization Dashboard & Alerting UI |
| [`alloy`](./alloy/README.md) | `grafana/alloy:v1.12.1` | OpenTelemetry Collector & Scraper |
| `cadvisor` | `gcr.io/cadvisor/cadvisor:v0.55.1` | Container Metrics Exporter |
| [`alertmanager`](./alertmanager/README.md) | `prom/alertmanager:v0.30.0` | Alert Handling & Notification |
| [`pushgateway`](./pushgateway/README.md) | `prom/pushgateway:v1.11.2` | Ephemeral Metrics Cache |

## Networking

All services run on `infra_net` with static IPs (172.19.0.3X).

### IP & Port Mapping

| Service | Static IP | Internal Port | Host Port | Traefik Domain |
| :--- | :--- | :--- | :--- | :--- |
| [`prometheus`](./prometheus/README.md) | `172.19.0.30` | `${PROMETHEUS_PORT}` | - | `prometheus.${DEFAULT_URL}` |
| [`loki`](./loki/README.md) | `172.19.0.31` | `${LOKI_PORT}` | `${LOKI_HOST_PORT}` | - |
| [`tempo`](./tempo/README.md) | `172.19.0.32` | `${TEMPO_PORT}` | `${TEMPO_HOST_PORT}` | - |
| [`grafana`](./grafana/README.md) | `172.19.0.33` | `${GRAFANA_PORT}` | - | `grafana.${DEFAULT_URL}` |
| [`alloy`](./alloy/README.md) | `172.19.0.34` | `${ALLOY_PORT}` (UI)<br>`${ALLOY_OTLP_GRPC_PORT}`<br>`${ALLOY_OTLP_HTTP_PORT}` | `${ALLOY_OTLP_GRPC_HOST_PORT}`<br>`${ALLOY_OTLP_HTTP_HOST_PORT}` | `alloy.${DEFAULT_URL}` |
| `cadvisor` | `172.19.0.35` | `${CADVISOR_PORT}` | - | - |
| [`alertmanager`](./alertmanager/README.md) | `172.19.0.36` | `${ALERTMANAGER_PORT}` | - | `alertmanager.${DEFAULT_URL}` |
| [`pushgateway`](./pushgateway/README.md) | `172.19.0.37` | `${PUSHGATEWAY_PORT}` | - | `pushgateway.${DEFAULT_URL}` |

## Persistence

Data is persisted in named volumes and configuration via bind mounts:

- **Metrics**: `prometheus-data` → `/prometheus`
- **Logs**: `loki-data` → `/loki`
- **Traces**: `tempo-data` → `/var/tempo`
- **Visualizations**: `grafana-data` → `/var/lib/grafana`
- **Alerts**: `alertmanager-data` → `/alertmanager`
- **Configs**: `*/config/*` directories are mounted Read-Only.

## Configuration

Most services are configured via mounted YAML files in their respective subdirectories (`prometheus/`, `loki/`, etc). However, Grafana and Alertmanager rely heavily on Environment Variables.

### Grafana Environment Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `GF_SERVER_ROOT_URL` | Root URL | `https://grafana.${DEFAULT_URL}` |
| `GF_SECURITY_ADMIN_USER` | Admin Username | `${GRAFANA_ADMIN_USERNAME}` |
| `GF_SECURITY_ADMIN_PASSWORD` | Admin Password | `${GRAFANA_ADMIN_PASSWORD}` |
| `GF_AUTH_GENERIC_OAUTH_ENABLED` | Enable OAuth | `true` |
| `GF_AUTH_GENERIC_OAUTH_CLIENT_ID` | OAuth Client ID | `${OAUTH2_PROXY_CLIENT_ID}` |

### Alertmanager Environment Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `SMTP_USERNAME` | SMTP Sender User | `${SMTP_USERNAME}` |
| `SMTP_PASSWORD` | SMTP Sender Password | `${SMTP_PASSWORD}` |
| `SLACK_ALERTMANAGER_WEBHOOK_URL` | Slack Webhook URL | `${SLACK_ALERTMANAGER_WEBHOOK_URL}` |

## Usage

1. **Grafana**: `https://grafana.${DEFAULT_URL}` (Login via SSO).
2. **Prometheus**: `https://prometheus.${DEFAULT_URL}` (Check targets/metrics).
3. **Alertmanager**: `https://alertmanager.${DEFAULT_URL}` (Check silences/alerts).
4. **Alloy UI**: `https://alloy.${DEFAULT_URL}` (Debug pipelines).
