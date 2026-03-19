---
layer: infra
---
# Observability Stack — System Context

**Overview (KR):** `06-observability` 티어의 서비스 구성, 역할, 의존성, 데이터 흐름을 설명하는 컨텍스트 문서입니다.

> **Tier**: `06-observability`
> **Profile**: `obs`
> **Network**: `infra_net`

## Purpose

The observability stack gives infrastructure-wide visibility into three signals:

- **Metrics** — time-series counters and gauges (Prometheus)
- **Logs** — structured log streams from all containers (Loki)
- **Traces** — distributed request traces across services (Tempo)
- **Profiles** — continuous CPU/memory profiles for performance analysis (Pyroscope)

Grafana provides a unified query and visualization UI over all four backends.

## Service Inventory

| Service        | Image                              | Internal Port | Role                            |
| :------------- | :--------------------------------- | :------------ | :------------------------------ |
| `prometheus`   | `prom/prometheus:v3.9.0`           | 9090          | Metrics storage (TSDB)          |
| `loki`         | `hy/loki:3.6.6-custom`             | 3100          | Log storage (S3 via MinIO)      |
| `tempo`        | `hy/tempo:2.10.1-custom`           | 3200          | Trace storage (S3 via MinIO)    |
| `alloy`        | `grafana/alloy:v1.13.1`            | 12345 / 4317 / 4318 | Telemetry hub / OTLP endpoint |
| `grafana`      | `grafana/grafana:12.3.3`           | 3000          | Visualization UI                |
| `alertmanager` | `prom/alertmanager:v0.30.0`        | 9093          | Alert routing                   |
| `pushgateway`  | `prom/pushgateway:v1.11.2`         | 9091          | Ephemeral metrics buffer        |
| `cadvisor`     | `gcr.io/cadvisor/cadvisor:v0.55.1` | 8080          | Container resource metrics      |
| `pyroscope`    | `grafana/pyroscope:1.18.1`         | 4040          | Continuous profiling            |

## External Dependencies

| Dependency  | Tier           | Usage                                                    |
| :---------- | :------------- | :------------------------------------------------------- |
| **MinIO**   | `04-data`      | S3 object storage for Loki (`loki-bucket`) and Tempo (`tempo-bucket`) |
| **Keycloak**| `02-auth`      | SSO for Grafana (Generic OAuth / PKCE)                   |
| **Traefik** | `01-gateway`   | HTTPS routing for Grafana, Prometheus, Alertmanager, Alloy, Pushgateway |

## Secrets

| Secret name                 | Used by           | Purpose                                  |
| :-------------------------- | :---------------- | :--------------------------------------- |
| `opensearch_exporter_password` | prometheus     | OpenSearch metrics scrape credential     |
| `minio_app_user_password`   | loki, tempo       | MinIO S3 authentication                  |
| `grafana_admin_password`    | grafana           | Grafana admin account fallback           |
| `oauth2_proxy_client_secret`| grafana           | Keycloak OAuth client secret             |
| `smtp_username`             | alertmanager      | Gmail SMTP account                       |
| `smtp_password`             | alertmanager      | Gmail app password                       |
| `slack_webhook`             | alertmanager      | Slack Incoming Webhook URL               |

## Data Flow

```
Applications / Services
        │
        │  OTLP gRPC :4317 / HTTP :4318
        ▼
  ┌─────────────┐   Traces batch (OTLP)    ┌──────────┐
  │    Alloy    │ ─────────────────────── ▶ │  Tempo   │ ──▶ MinIO (tempo-bucket)
  │  (hub)      │                           └──────────┘
  │             │   Log push (HTTP)         ┌──────────┐
  │             │ ─────────────────────── ▶ │   Loki   │ ──▶ MinIO (loki-bucket)
  │             │                           └──────────┘
  │             │   Remote write            ┌──────────────┐
  │             │ ─────────────────────── ▶ │  Prometheus  │
  └─────────────┘                           └──────────────┘
        ▲                                         │
        │  Docker socket (log discovery)          │ remote_write (span metrics)
  /var/run/docker.sock                            │
                                                  ▼
                                           ┌──────────────┐
                                           │  Prometheus  │ ◀── cAdvisor (container metrics)
                                           └──────────────┘
                                                  │
                                           ┌──────▼──────┐   Alert rules
                                           │ Alertmanager│ ──▶ Slack / Gmail
                                           └─────────────┘
```

Grafana queries all four backends (Prometheus, Loki, Tempo, Pyroscope) and is the single operator-facing UI.

## Network

All services communicate on `infra_net` (Docker bridge). No static IP addresses — DNS resolution uses Docker service names.

Traefik exposes the following over HTTPS:

| FQDN                                    | Backend port |
| :-------------------------------------- | :----------- |
| `grafana.${DEFAULT_URL}`                | 3000         |
| `prometheus.${DEFAULT_URL}`             | 9090         |
| `alertmanager.${DEFAULT_URL}`           | 9093         |
| `alloy.${DEFAULT_URL}`                  | 12345        |
| `pushgateway.${DEFAULT_URL}`            | 9091         |
