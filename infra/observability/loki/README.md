# Loki

Loki is a horizontally scalable, highly available, multi-tenant log aggregation system inspired by Prometheus. It is designed to be very cost-effective and easy to operate. It does not index the contents of the logs, but rather a set of labels for each log stream.

## 🚀 Overview

- **Service**: `loki`
- **Docker Image**: `grafana/loki:3.6.3`
- **Ports**:
  - `3100`: HTTP (Ingestion/Query)
  - `9096`: gRPC

## ⚙️ Configuration

The configuration file is located at `config/loki-config.yaml`.

### Setup

1. **Copy the example configuration:**

    ```bash
    cp loki-config.yaml.example loki-config.yaml
    ```

2. **Edit `loki-config.yaml`:**
    - **Storage (S3/MinIO)**: This setup uses MinIO for object storage.
        - `endpoint`: `http://minio:9000`
        - `access_key_id`: Ensure this matches `MINIO_ROOT_USER` in `.env` (default: `minio_user`)
        - `secret_access_key`: **Update this** to match `MINIO_ROOT_PASSWORD` in `.env`.

### Key Features

- **S3 Backend**: Configured to use MinIO for storing chunks and indices.
- **Compactor**: Manages retention and deduplication of logs.
- **Ruler**: Configured to send alerts to Alertmanager (`http://alertmanager:9093`).

## 📦 Storage

Loki requires an Object Store (like AWS S3 or MinIO).
- **Bucket**: `loki-bucket` (must be created in MinIO).
- **Volume**: `loki-data` (Docker volume).

## 🔗 Integration

- **Promtail / Alloy**: Agents push logs to Loki.
- **Grafana**: Queries Loki for log visualization (Data Source: Loki).

## 🛠 Directory Structure

```text
loki/
├── config/
│   ├── loki-config.yaml          # Actual configuration (Ignored by Git)
│   └── loki-config.yaml.example  # Template configuration
└── README.md
```
