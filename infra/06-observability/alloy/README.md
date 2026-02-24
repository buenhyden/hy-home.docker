# Grafana Alloy

Alloy is a vendor-neutral distribution of the OpenTelemetry Collector and Prometheus agent, optimized for the Grafana LGTM stack.

## Services

| Service | Image                  | Role           | Resources         |
| :------ | :--------------------- | :------------- | :---------------- |
| `alloy` | `grafana/alloy:v1.6.1` | Telemetry Guard| 0.2 CPU / 256MB   |

## Networking

| Port | Purpose                |
| :--- | :--------------------- |
| 12345| Health / UI            |

## Roles

Alloy acts as a central collector for:

1. **Metrics**: Scrapes Prometheus targets and forwards to `prometheus:9090`.
2. **Logs**: Scrapes Docker logs and forwards to `loki:3100`.
3. **Traces**: Recieves OTLP traces and forwards to `tempo:3200`.

## Configuration

- **Config**: Defined in `config/config.alloy`. Uses the Alloy configuration language (HCL-like).

## File Map

| Path                   | Description              |
| ---------------------- | ------------------------ |
| `config/config.alloy`  | Telemetry pipeline config. |
| `README.md`            | Service notes.           |
