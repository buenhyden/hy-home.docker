# InfluxDB

## Overview

InfluxDB is an open-source time series database. This deployment uses InfluxDB v2.

## Service Details

- **Image**: `influxdb:2.8`
- **Container Name**: `influxdb`
- **Volumes**:
  - `influxdb-data`: `/var/lib/influxdb2` (Read/Write)
- **Network**: `infra_net` (Static IP: `172.19.0.11`)

## Environment Variables

- `INFLUXDB_DB`: Database name.
- `DOCKER_INFLUXDB_INIT_MODE`: `setup`
- `DOCKER_INFLUXDB_INIT_USERNAME`: Admin username.
- `DOCKER_INFLUXDB_INIT_PASSWORD`: Admin password.
- `DOCKER_INFLUXDB_INIT_ORG`: Organization name.
- `DOCKER_INFLUXDB_INIT_BUCKET`: Initial bucket name.
- `DOCKER_INFLUXDB_INIT_ADMIN_TOKEN`: Admin API token.

## Traefik Configuration

- **Domain**: `influxdb.${DEFAULT_URL}`
- **Port**: `${INFLUXDB_PORT}`
- **Entrypoint**: `websecure`
- **TLS**: Enabled
