# InfluxDB

## Overview

InfluxDB is an open-source time series database. This deployment uses **InfluxDB v2** and includes automated setup configuration.

## Services

- **Service Name**: `influxdb`
- **Image**: `influxdb:2.8`
- **Container Name**: `influxdb`
- **Restart Policy**: `unless-stopped`

## Networking

This service is key infrastructure and has a fixed configuration within the `infra_net` network:

- **Network**: `infra_net`
- **Static IPv4**: `172.19.0.11`
  - *Note*: This static IP is often used by other services (like Telegraf) to send metrics reliably without DNS lookups.

## Persistence

- **`influxdb-data`** → `/var/lib/influxdb2`: Persistent storage for time-series data and configuration.

## Configuration

| Variable | Description | Default |
| :--- | :--- | :--- |
| `INFLUXDB_DB` | Database Name | `${INFLUXDB_DB_NAME}` |
| `DOCKER_INFLUXDB_INIT_MODE` | Set to `setup` for auto-init | `setup` |
| `DOCKER_INFLUXDB_INIT_USERNAME` | Initial Admin Username | `${INFLUXDB_USERNAME}` |
| `DOCKER_INFLUXDB_INIT_PASSWORD` | Initial Admin Password | `${INFLUXDB_PASSWORD}` |
| `DOCKER_INFLUXDB_INIT_ORG` | Default Organization Name | `${INFLUXDB_ORG}` |
| `DOCKER_INFLUXDB_INIT_BUCKET` | Default Bucket Name | `${INFLUXDB_BUCKET}` |
| `DOCKER_INFLUXDB_INIT_ADMIN_TOKEN`| Admin API Token | `${INFLUXDB_API_TOKEN}` |

## Traefik Integration

- **Domain**: `influxdb.${DEFAULT_URL}`
- **Entrypoint**: `websecure` (TLS Enabled)
- **Service Port**: `${INFLUXDB_PORT}`

## Usage

### Accessing the UI

- **URL**: `https://influxdb.<your-domain>`
- **Login**: Use the `DOCKER_INFLUXDB_INIT_USERNAME` and `DOCKER_INFLUXDB_INIT_PASSWORD`.

### Connecting Clients (Telegraf, Airflow)

Use the **Admin Token** (`DOCKER_INFLUXDB_INIT_ADMIN_TOKEN`) and the Organization name (`DOCKER_INFLUXDB_INIT_ORG`) for authentication.
