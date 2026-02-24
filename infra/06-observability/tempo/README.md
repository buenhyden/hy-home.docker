# Tempo

Tempo is a high-volume, low-cost distributed tracing backend.

## Services

| Service | Image                   | Role           | Resources         |
| :------ | :---------------------- | :------------- | :---------------- |
| `tempo` | `grafana/tempo:2.7.0`   | Tracing Server | 0.5 CPU / 1GB RAM |

## Networking

| Port | Protocol | Purpose                  |
| :--- | :------- | :----------------------- |
| 3200 | HTTP     | Web UI / Query API       |
| 4317 | OTLP/gRPC| Trace ingestion (gRPC)   |
| 4318 | OTLP/HTTP| Trace ingestion (HTTP)   |

## Persistence

- **Data**: `/tmp/tempo` (mounted to `tempo-data` volume).

## Configuration

- **Config**: Defined in `config/tempo-config.yml`.
- **Storage**: Configured for local block storage in development.

## File Map

| Path                   | Description              |
| ---------------------- | ------------------------ |
| `config/tempo-config.yml` | Master Tempo configuration. |
| `README.md`            | Service notes.           |
