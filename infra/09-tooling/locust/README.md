# Locust

Locust is an open-source, Python-based distributed load testing tool. This setup runs a master-worker architecture with integrated InfluxDB metrics reporting.

## Services

| Service          | Role                    | Resources              |
| :---             | :---                    | :---                   |
| `locust-master`  | Test controller / Web UI| med (0.5 CPU / 512 MB) |
| `locust-worker`  | Load generator (2 replicas) | med (0.5 CPU / 512 MB) |

## Build

The image is built from the local `Dockerfile`:

| Base Image              | Additional Packages    |
| :---                    | :---                   |
| `locustio/locust:2.43.2`| `influxdb-client` (PyPI) |

## Networking

- **Web UI**: `http://localhost:${LOCUST_HOST_PORT:-18089}` (direct port exposure, no Traefik proxy).
- **Master-Worker**: Workers connect to `locust-master` via Docker internal DNS.
- **Target Host Resolution**: `extra_hosts` maps `${DEFAULT_URL}` → `host-gateway` so load tests can reach host-network services.

## Persistence

- **Locustfile Volume**: `locust-data` → `${DEFAULT_TOOLING_DIR}/locust` bind mount, exposed at `/mnt/locust` in both master and worker containers.
- **Locustfile Path**: `/mnt/locust/locustfile.py` (must be created manually by operator).

## Dependencies

- **InfluxDB** (`infra/06-observability/influxdb`) — healthcheck dependency, receives metrics from master.

## Secrets

| Secret              | Description                                         |
| :---                | :---                                                |
| `influxdb_api_token`| API token for writing metrics to InfluxDB bucket.  |

## Configuration

Key environment variables (from `.env`):

| Variable               | Default   | Description                         |
| :---                   | :---      | :---                                |
| `LOCUST_HOST_PORT`     | `18089`   | External port for the Web UI.       |
| `LOCUST_PORT`          | `8089`    | Internal Locust port.               |
| `INFLUXDB_PORT`        | `8086`    | InfluxDB connection port.           |
| `INFLUXDB_ORG`         | —         | InfluxDB organization name.         |
| `INFLUXDB_BUCKET`      | —         | InfluxDB bucket for metrics.        |

## File Map

| Path                | Description                                         |
| ------------------- | --------------------------------------------------- |
| `Dockerfile`        | Custom image built on `locustio/locust:2.43.2`.     |
| `docker-compose.yml`| Master and worker service definitions.              |
| `README.md`         | Service overview (this file).                       |
