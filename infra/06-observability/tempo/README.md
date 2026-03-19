# Tempo

Tempo is a high-volume, low-cost distributed tracing backend.

## Services

| Service | Image | Role | Resources |
| :--- | :--- | :--- | :--- |
| `tempo` | `hy/tempo:2.10.1-custom` | Trace storage | 1.0 CPU / 1GB RAM |

> Built from a custom Dockerfile (`tempo/Dockerfile`) layered on `grafana/tempo:2.10.1` with an Alpine base for a minimal image.

## Networking

| Port | Protocol | Purpose              |
| :--- | :------- | :------------------- |
| 3200 | HTTP     | Query API / Web UI   |

> OTLP ingestion (gRPC 4317 / HTTP 4318) is handled by **Alloy**, which batches and forwards to Tempo's internal distributor. Applications should target Alloy, not Tempo directly.

## Persistence

- **Data**: `/var/tempo` (mounted to `tempo-data` volume).
- **WAL**: Written locally to `/var/tempo/wal` before flushing to S3.
- **Cold storage**: S3 bucket `tempo-bucket` via MinIO.

## Configuration

- **Config**: Defined in `config/tempo.yaml`.
- **Retention**: 24h — configured via `compactor.compaction.block_retention`.
- **MetricsGenerator**: Span metrics and service-graph metrics are remote-written to Prometheus (`http://prometheus:9090/api/v1/write`).
- **Secret**: `minio_app_user_password` — injected via Docker Secret and read as `${MINIO_APP_USER_PASSWORD}` in the config.

## File Map

| Path                 | Description               |
| -------------------- | ------------------------- |
| `Dockerfile`         | Custom image build.       |
| `docker-entrypoint.sh` | Entrypoint wrapper.     |
| `config/tempo.yaml`  | Master Tempo configuration. |
| `README.md`          | Service notes.            |
