# Tempo

Grafana Tempo is an open-source, easy-to-use, and high-scale distributed tracing backend. Tempo is cost-efficient, requiring only object storage (S3/MinIO) to operate, and is deeply integrated with Grafana, Prometheus, and Loki.

## 🚀 Overview

- **Service**: `tempo`
- **Docker Image**: `grafana/tempo:2.9.0`
- **Ports**:
  - `3200`: HTTP (Distributor/Otlp)
  - `4317`: OTLP gRPC Receiver
  - `4318`: OTLP HTTP Receiver

## ⚙️ Configuration

The configuration file is located at `config/tempo.yaml`.

### Setup

1. **Copy the example configuration:**

    ```bash
    cp tempo.yaml.example tempo.yaml
    ```

2. **Edit `tempo.yaml`:**
    - **Storage (S3/MinIO)**: This setup uses MinIO for trace storage.
        - `endpoint`: `minio:9000`
        - `access_key`: Ensure this matches `MINIO_ROOT_USER` in `.env` (default: `minio_user`)
        - `secret_key`: **Update this** to match `MINIO_ROOT_PASSWORD` in `.env`.
    - **Remote Write**:
        - The `metrics_generator` sends metrics to `http://prometheus:9090/api/v1/write`. Ensure Prometheus is reachable.

### Key Features

- **S3 Backend**: Stores traces in MinIO buckets (`tempo-bucket`).
- **Metrics Generator**: Derives metrics (RED method) from spans and sends them to Prometheus (Service Graphs).
- **OTLP Support**: Accepts traces via OpenTelemetry Protocol (gRPC/HTTP).

## 📦 Storage

Tempo requires an Object Store.
- **Bucket**: `tempo-bucket` (must be created in MinIO).
- **Volume**: `tempo-data` (Docker volume, mostly for WAL).

## 🔗 Integration

- **Applications**: Send traces (spans) to Tempo via OTLP.
- **Grafana**: Visualizes traces. Can correlate with Logs (Loki) and Metrics (Prometheus).

## 🛠 Directory Structure

```text
tempo/
├── config/
│   ├── tempo.yaml          # Actual configuration (Ignored by Git)
│   └── tempo.yaml.example  # Template configuration
└── README.md
```
