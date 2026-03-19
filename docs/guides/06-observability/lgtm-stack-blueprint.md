---
layer: infra
---
# LGTM (Loki, Grafana, Tempo, Metrics) Stack Blueprint

**Overview (KR):** Grafana, Loki, Tempo를 포함한 통합 관측성(Observability) 스택의 설계 청사진입니다.

> **Tier**: `06-observability`
> **Collector**: Grafana Alloy
> **Backend**: MinIO (S3)

## 1. Observability Architecture

The platform uses a push-based model where all services ship OTLP telemetry to **Grafana Alloy**.

### Technical Specifications

| Tool           | Internal Port | Role                                    |
| -------------- | ------------- | --------------------------------------- |
| **Prometheus** | `9090`        | Metrics backend (v3.9+)                 |
| **Loki**       | `3100`        | Log storage, S3 backend via MinIO       |
| **Tempo**      | `3200`        | Trace storage, S3 backend via MinIO     |
| **Alloy**      | `12345`       | Telemetry collector / OTLP endpoint     |
| **Pyroscope**  | `4040`        | Continuous profiling backend            |
| **Alertmanager**| `9093`       | Alert routing (email + Slack)           |
| **Pushgateway**| `9091`        | Ephemeral metrics buffer for batch jobs |
| **cAdvisor**   | `8080`        | Container-level resource metrics        |

### Telemetry Ingestion Ports (OTLP — on Alloy)

- **gRPC**: `alloy:4317`
- **HTTP**: `alloy:4318`

> Alloy is the sole OTLP ingestion point. Tempo has its own internal OTLP distributor (also 4317/4318), but applications target **Alloy**, which batches and forwards to Tempo.

## 2. Telemetry Ingestion Flow

Alloy is the OpenTelemetry bridge inside `infra_net`.

1. **Host Monitoring**: Alloy reads socket at `/var/run/docker.sock` and `/var/lib/docker/containers` to collect container logs, forwarding them to Loki.
2. **Application OTLP**: Services push traces to `http://alloy:4318` (HTTP) or `alloy:4317` (gRPC). Alloy batches and forwards to Tempo.
3. **Metrics**: Alloy scrapes its own metrics and remote-writes to Prometheus. Tempo's metrics generator also remote-writes span metrics to Prometheus.
4. **Profiling**: Alloy can forward profiles to Pyroscope via `pyroscope.write`.
5. **Storage Offload**: Loki and Tempo ship cold data to **MinIO** S3 buckets (`loki-bucket`, `tempo-bucket`).

## 3. Initial Setup & Verification

Grafana is provisioned from static YAML/JSON files in `./grafana/provisioning`.

### Startup Order

```text
MinIO (02-storage tier) → Prometheus, Loki, Tempo → Alloy → Grafana, Alertmanager, Pushgateway
```

### Verification Steps

1. Navigate to `https://grafana.${DEFAULT_URL}`.
2. Check `Explore → Loki` to confirm container logs are flowing.
3. Check `Explore → Tempo` — run a TraceQL query to confirm traces are stored.
4. Check `Explore → Prometheus` — verify target scrape status at `https://prometheus.${DEFAULT_URL}/targets`.
5. Navigate to `https://grafana.${DEFAULT_URL}/pyroscope` or send a profile to Alloy to confirm Pyroscope receives data.

## 4. Maintenance

- **Dashboards / datasources**: modify files under `infra/06-observability/grafana/provisioning/` and restart Grafana.
- **Alert rules**: edit `infra/06-observability/prometheus/config/alert_rules/` and reload Prometheus (`curl -XPOST http://prometheus:9090/-/reload`).
- **Alert routing**: edit `infra/06-observability/alertmanager/config/config.yml` — secrets (`smtp_password`, `slack_webhook`) are injected via Docker Secrets and template substitution at startup.
- **Retention**: tune `limits_config.retention_period` in `loki/config/loki-config.yaml` and `compactor.compaction.block_retention` in `tempo/config/tempo.yaml`.
