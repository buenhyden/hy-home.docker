# Grafana Alloy Telemetry Specification

## 1. Context

Grafana Alloy acts as the unified telemetry collector (OpenTelemetry / OTLP) for the `hy-home.docker` infrastructure. It sits between application metrics/logs/traces and the LGTM backend (Loki for logs, Grafana for visualization, Tempo for traces, Prometheus for metrics).

## 2. Network Integration

- **Container Name**: `alloy`
- **Network**: `infra_net`
- **Exposed Ports**:
  - `4317` (OTLP gRPC)
  - `4318` (OTLP HTTP)

## 3. Telemetry Flows

### 3.1 Traces

- **Format**: OTLP
- **Receiver**: `otelcol.receiver.otlp` listening on 0.0.0.0:4317.
- **Exporter**: `otelcol.exporter.otlp` forwarding batches to `tempo:4317`.

### 3.2 Metrics

- **Format**: OTLP / Prometheus Scrape
- **Receiver**:
  - Push: `otelcol.receiver.otlp`
  - Pull: Local scraping configs (e.g., `prometheus.scrape`) targeting local cadvisor and node_exporter endpoints.
- **Exporter**: `otelcol.exporter.prometheus` forwarding to Prometheus at `http://prometheus:9090/api/v1/write`.

### 3.3 Logs

- **Format**: OTLP / System Logs
- **Receiver**: `otelcol.receiver.otlp` and local Docker log tails.
- **Exporter**: `otelcol.exporter.loki` forwarding to `loki:3100`.

## 4. Required Environment Configurations for Apps

To route data to this OpenTelemetry collector natively, downstream containerized applications must attach to the `infra_net` and configure their OTLP SDKs as follows:

```env
OTEL_EXPORTER_OTLP_ENDPOINT=http://alloy:4317
OTEL_EXPORTER_OTLP_PROTOCOL=grpc
```
