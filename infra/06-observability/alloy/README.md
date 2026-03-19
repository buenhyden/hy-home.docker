# Grafana Alloy

Alloy is a vendor-neutral OpenTelemetry Collector distribution optimized for the Grafana LGTM stack.

## Services

| Service | Image                   | Role            | Resources       |
| :------ | :---------------------- | :-------------- | :-------------- |
| `alloy` | `grafana/alloy:v1.13.1` | Telemetry hub   | 0.2 CPU / 256MB |

## Networking

| Port  | Purpose                            |
| :---- | :--------------------------------- |
| 12345 | Health endpoint / Alloy UI         |
| 4317  | OTLP gRPC ingestion (from apps)    |
| 4318  | OTLP HTTP ingestion (from apps)    |

## Roles

Alloy is the central telemetry hub with four active pipelines:

1. **Logs**: Reads Docker container logs via the Docker socket and forwards to `loki:3100`.
2. **Metrics**: Scrapes its own metrics and remote-writes to `prometheus:9090`.
3. **Traces**: Receives OTLP traces from apps (gRPC 4317 / HTTP 4318) and forwards to `tempo:4317`.
4. **Profiling**: Forwards profiles to `pyroscope:4040` via `pyroscope.write`.

## Configuration

- **Config**: Defined in `config/config.alloy` using the Alloy configuration language (HCL-like).
- **Side effects**: Alloy mounts the Docker socket (`/var/run/docker.sock`) and container log path (`/var/lib/docker/containers`) as read-only to enable log discovery.

## File Map

| Path                  | Description                |
| --------------------- | -------------------------- |
| `config/config.alloy` | Telemetry pipeline config. |
| `README.md`           | Service notes.             |
