# Loki

Loki is a horizontally-scalable, highly-available, multi-tenant log aggregation system inspired by Prometheus.

## Services

| Service | Image                  | Role           | Resources         |
| :------ | :--------------------- | :------------- | :---------------- |
| `loki`  | `grafana/loki:3.3.0`   | Log Processor  | 0.5 CPU / 1GB RAM |

## Networking

| Port | Purpose                |
| :--- | :--------------------- |
| 3100 | HTTP API (Ingest/Query)|

## Persistence

- **Data**: `/loki` (mounted to `loki-data` volume).
- **Index**: BoltDB/TSDB (persisted in the data volume).

## Configuration

- **Config**: Defined in `config/loki-config.yml`.
- **Retention**: Configured via the `limits_config` in the YAML file.

## File Map

| Path                   | Description             |
| ---------------------- | ----------------------- |
| `config/loki-config.yml` | Master Loki configuration. |
| `README.md`            | Service notes.          |
