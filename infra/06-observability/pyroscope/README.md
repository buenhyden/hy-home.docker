# Pyroscope

Pyroscope is a continuous profiling backend for aggregating and querying performance profiles.

## Services

| Service     | Image                      | Role                | Resources       |
| :---------- | :------------------------- | :------------------ | :-------------- |
| `pyroscope` | `grafana/pyroscope:1.18.1` | Profiling backend   | 0.5 CPU / 512MB |

## Networking

| Port | Purpose             |
| :--- | :------------------ |
| 4040 | HTTP API / UI       |

> Port 4040 is published to the host (`${PYROSCOPE_HOST_PORT:-4040}:${PYROSCOPE_PORT:-4040}`). Alloy forwards profiles to `http://pyroscope:4040`.

## Persistence

- **Data**: `/var/lib/pyroscope` (mounted to `pyroscope-data` volume, bind-mounted to `${DEFAULT_OBSERVABILITY_DIR}/pyroscope`).

## Configuration

- **Config**: `config/pyroscope.yaml`.
- **Storage**: Filesystem backend (local disk, not S3).
- **Multitenancy**: Disabled — single-tenant setup.
- **Self-profiling**: `self_profiling.disable_push: true` (Pyroscope does not push its own profiles).

## File Map

| Path                        | Description                    |
| --------------------------- | ------------------------------ |
| `config/pyroscope.yaml`     | Pyroscope server configuration.|
| `README.md`                 | Service notes.                 |
