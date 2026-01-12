# Observability Stack (LGTM + Alloy)

## Overview

A comprehensive observability stack based on the LGTM (Loki, Grafana, Tempo, Mimir-like Prometheus) pattern, with Grafana Alloy as the collector.

## Service Details

### 1. Prometheus (Metrics)

- **Image**: `prom/prometheus:v3.9.0`
- **Port**: `${PROMETHEUS_PORT}` (9090)
- **Traefik**: `prometheus.${DEFAULT_URL}`

### 2. Loki (Logs)

- **Image**: `grafana/loki:3.6.3`
- **Port**: `${LOKI_PORT}` (3100)
- **Traefik**: Not exposed directly (internal use by Alloy/Grafana).

### 3. Tempo (Traces)

- **Image**: `grafana/tempo:2.9.0`
- **Port**: `${TEMPO_PORT}` (3200)

### 4. Grafana (Visualization)

- **Image**: `grafana/grafana:12.3.1`
- **Port**: `${GRAFANA_PORT}` (3000)
- **Traefik**: `grafana.${DEFAULT_URL}` (with SSO)
- **Auth**: Integrated with Keycloak via Generic OAuth.
  - `GF_AUTH_OAUTH_AUTO_LOGIN=true`
  - `GF_AUTH_DISABLE_LOGIN_FORM=true`

### 5. Alloy (Collector)

- **Image**: `grafana/alloy:v1.12.1`
- **Purpose**: OpenTelemetry Collector & Prometheus Scraper.
- **Ports**:
  - `${ALLOY_PORT}` (12345): UI/internal
  - `${ALLOY_OTLP_GRPC_PORT}` (4317): OTLP gRPC
  - `${ALLOY_OTLP_HTTP_PORT}` (4318): OTLP HTTP
- **Traefik**: `alloy.${DEFAULT_URL}`

### 6. cAdvisor (Container Metrics)

- **Image**: `gcr.io/cadvisor/cadvisor:v0.55.1`
- **Purpose**: Exposes low-level container metrics.

### 7. Alertmanager

- **Image**: `prom/alertmanager:v0.30.0`
- **Traefik**: `alertmanager.${DEFAULT_URL}`

### 8. Pushgateway

- **Image**: `prom/pushgateway:v1.11.2`
- **Traefik**: `pushgateway.${DEFAULT_URL}`

## Network

All services are assigned static IPs in the `172.19.0.3X` range on `infra_net`.

| Service | IP Address |
| :--- | :--- |
| **Prometheus** | `172.19.0.30` |
| **Loki** | `172.19.0.31` |
| **Tempo** | `172.19.0.32` |
| **Grafana** | `172.19.0.33` |
| **Alloy** | `172.19.0.34` |
| **cAdvisor** | `172.19.0.35` |
| **Alertmanager** | `172.19.0.36` |
| **Pushgateway** | `172.19.0.37` |
