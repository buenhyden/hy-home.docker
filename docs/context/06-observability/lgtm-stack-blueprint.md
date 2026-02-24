# LGTM (Loki, Grafana, Tempo, Metrics) Stack Blueprint

> **Tier**: `06-observability`
> **Collector**: Grafana Alloy
> **Backend**: MinIO (S3)

## 1. Observability Architecture

The platform utilizes a modern push-based telemetry model. All services ship logs, metrics, and traces to a centralized **Grafana Alloy** collector.

- **Grafana (Port 3000)**: Visualization/Alerting Dashboard.
- **Prometheus (Port 9090)**: Metrics persistence.
- **Loki (Port 3100)**: Log aggregation.
- **Tempo (Port 3200)**: Distributed tracing.

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
