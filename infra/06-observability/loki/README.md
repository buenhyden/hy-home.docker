# Loki

Loki is a horizontally-scalable, highly-available log aggregation system inspired by Prometheus.

## Services

| Service | Image | Role | Resources |
| :--- | :--- | :--- | :--- |
| `loki` | `hy/loki:3.6.6-custom` | Log storage | 1.0 CPU / 1GB RAM |

> Built from a custom Dockerfile (`loki/Dockerfile`) layered on `grafana/loki:3.6.6` with an Alpine base for a minimal image.

## Networking

| Port | Purpose                 |
| :--- | :---------------------- |
| 3100 | HTTP API (Ingest/Query) |
| 9096 | gRPC (internal)         |

## Persistence

- **Data**: `/loki` (mounted to `loki-data` volume).
- **Index**: TSDB (schema v13, persisted in the data volume).
- **Cold storage**: S3 bucket `loki-bucket` via MinIO.

## Configuration

- **Config**: Defined in `config/loki-config.yaml`.
- **Retention**: 7 days — configured via `limits_config.retention_period` in the YAML.
- **Secret**: `minio_app_user_password` — injected via Docker Secret and read as `${MINIO_APP_USER_PASSWORD}` in the config.

## File Map

| Path                      | Description                |
| ------------------------- | -------------------------- |
| `Dockerfile`              | Custom image build.        |
| `docker-entrypoint.sh`    | Entrypoint wrapper.        |
| `config/loki-config.yaml` | Master Loki configuration. |
| `README.md`               | Service notes.             |
