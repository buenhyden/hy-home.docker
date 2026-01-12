# InfluxDB

## Overview

InfluxDB is an open-source time series database. This deployment uses **InfluxDB v2** and includes automated setup configuration.

## Service Details

- **Service Name**: `influxdb`
- **Image**: `influxdb:2.8`
- **Container Name**: `influxdb`
- **Restart Policy**: `unless-stopped`

## Networking

This service is key infrastructure and has a fixed configuration within the `infra_net` network:

- **Network**: `infra_net`
- **Static IPv4**: `172.19.0.11`
  - *Note*: This static IP is often used by other services (like Telegraf) to send metrics reliably without DNS lookups.

## Volumes

- **`influxdb-data`** → `/var/lib/influxdb2`: Persistent storage for time-series data and configuration.

## Environment Variables (Initialization)

The container is configured to automatically initialize on the first run (`DOCKER_INFLUXDB_INIT_MODE=setup`).

| Variable | Description |
| :--- | :--- |
| `INFLUXDB_DB` | Database Name |
| `DOCKER_INFLUXDB_INIT_MODE` | Set to `setup` for auto-init |
| `DOCKER_INFLUXDB_INIT_USERNAME` | Initial Admin Username |
| `DOCKER_INFLUXDB_INIT_PASSWORD` | Initial Admin Password |
| `DOCKER_INFLUXDB_INIT_ORG` | Default Organization Name |
| `DOCKER_INFLUXDB_INIT_BUCKET` | Default Bucket Name |
| `DOCKER_INFLUXDB_INIT_ADMIN_TOKEN`| Admin API Token (Important for clients) |

## Traefik Configuration

- **Domain**: `influxdb.${DEFAULT_URL}`
- **Entrypoint**: `websecure` (TLS Enabled)
- **Service Port**: `${INFLUXDB_PORT}`

## Usage

### Accessing the UI

- **URL**: `https://influxdb.<your-domain>`
- **Login**: Use the `DOCKER_INFLUXDB_INIT_USERNAME` and `DOCKER_INFLUXDB_INIT_PASSWORD`.

### Connecting Clients (Telegraf, Airflow)

Use the **Admin Token** (`DOCKER_INFLUXDB_INIT_ADMIN_TOKEN`) and the Organization name (`DOCKER_INFLUXDB_INIT_ORG`) for authentication.
