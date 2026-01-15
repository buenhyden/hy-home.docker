# Grafana Alloy

Grafana Alloy is a vendor-neutral OpenTelemetry Collector distribution with a programmable configuration setup. It serves as the central telemetry collector, receiving logs, metrics, and traces, and forwarding them to the respective backends (Loki, Prometheus, Tempo).

## 🚀 Overview

- **Service**: `alloy`
- **Docker Image**: `grafana/alloy:v1.12.1`
- **Ports**:
  - `12345`: Alloy UI (Internally exposed)
  - `4317`: OTLP gRPC Receiver
  - `4318`: OTLP HTTP Receiver

## ⚙️ Configuration

The configuration file is located at `config/config.alloy`.

### Setup

1. **Copy the example configuration:**

    ```bash
    cp config.alloy.example config.alloy
    ```

2. **Edit `config.alloy`:**
    - Review the pipelines. The default configuration sets up:
        - **Logging**: Collects Docker logs and pushes to Loki (`http://loki:3100`).
        - **Metrics**: Scrapes itself and pushes to Prometheus (`http://prometheus:9090`).
        - **Tracing**: Receives OTLP traces (gRPC/HTTP) and forwards to Tempo (`tempo:4317`).

### Pipelines

- **Logging Pipeline**:
  - `discovery.docker`: Discovers running containers.
  - `loki.source.docker`: Reads logs from containers.
  - `loki.write`: Sends logs to Loki.
- **Metrics Pipeline**:
  - `prometheus.exporter.self`: Exposes internal Alloy metrics.
  - `prometheus.remote_write`: Sends metrics to Prometheus.
- **Tracing Pipeline**:
  - `otelcol.receiver.otlp`: Listens on ports 4317/4318.
  - `otelcol.processor.batch`: Batches traces for efficiency.
  - `otelcol.exporter.otlp`: Sends traces to Tempo.

## 🔗 Integration

- **Traefik**: Exposed via `alloy.${DEFAULT_URL}` (HTTPS) for debugging pipelines.
- **Backends**: Connects to Loki, Prometheus, and Tempo.

## 🛠 Directory Structure

```text
alloy/
├── config/
│   ├── config.alloy          # Actual configuration (Ignored by Git)
│   ├── config.alloy.example  # Template configuration
└── README.md
```
