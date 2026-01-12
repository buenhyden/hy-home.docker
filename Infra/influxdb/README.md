# InfluxDB

## Overview

InfluxDB is an open-source time series database.

## Services

- **influxdb**: InfluxDB Server.
  - URL: `https://influxdb.${DEFAULT_URL}`

## Configuration

### Environment Variables

- `INFLUXDB_DB`: Database name.
- `DOCKER_INFLUXDB_INIT_MODE`: `setup`
- `DOCKER_INFLUXDB_INIT_USERNAME`: Initial admin username.
- `DOCKER_INFLUXDB_INIT_PASSWORD`: Initial admin password.
- `DOCKER_INFLUXDB_INIT_ORG`: Initial organization.
- `DOCKER_INFLUXDB_INIT_BUCKET`: Initial bucket.
- `DOCKER_INFLUXDB_INIT_ADMIN_TOKEN`: Initial admin token.

### Volumes

- `influxdb-data`: `/var/lib/influxdb2`

## Networks

- `infra_net`
  - IP: `172.19.0.11`

## Traefik Routing

- **Domain**: `influxdb.${DEFAULT_URL}`
