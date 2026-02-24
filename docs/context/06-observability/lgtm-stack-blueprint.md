# LGTM (Loki, Grafana, Tempo, Metrics) Stack Blueprint

> **Tier**: `06-observability`
> **Collector**: Grafana Alloy
> **Backend**: MinIO (S3)

## 1. Observability Architecture

The platform utilizes a push-based model where all services ship OTLP telemetry to **Grafana Alloy**.

### Technical Specifications

| Tool | Internal Port | Logic |
| --- | --- | --- |
| **Prometheus** | `9090` | Metrics (v3.9+) |
| **Loki** | `3100` | Logs (v3.6+) |
| **Tempo** | `3200` | Traces (v2.10+) |
| **Alloy** | `12345` | Collector Hub |

### Telemetry Ports (OTLP)

- **gRPC**: `alloy:4317`
- **HTTP**: `alloy:4318`

## 2. Telemetry Ingestion Flow

Alloy acts as the OpenTelemetry (OTLP) bridge inside `infra_net`.

1. **Host Monitoring**: Alloy reads `/var/lib/docker/containers` and system metrics.
2. **Application OTLP**: Services push to `http://alloy:4318` (HTTP) or `4317` (gRPC).
3. **Storage Offload**: Loki and Tempo ship cold chunks to **MinIO** buckets.

## 3. Initial Setup & Verification

Grafana is provisioned via static YAML/JSON files in the `./grafana` directory.

### Verification Steps

1. Navigate to `https://grafana.${DEFAULT_URL}`.
2. Check `Explore -> Loki` to confirm container logs are flowing.
3. Check `Explore -> Tempo` to verify TraceQL query resolution.

## 4. Maintenance

To add custom dashboards or update datasources, modify the files in `infra/06-observability/grafana/provisioning/` and restart the Grafana container.
