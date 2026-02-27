# InfluxDB

InfluxDB is an open-source time series database (TSDB) developed by InfluxData.

## Services

| Service    | Image          | Role           | Resources         |
| :--------- | :------------- | :------------- | :---------------- |
| `influxdb` | `influxdb:2.8` | Time Series DB | 1.0 CPU / 1GB RAM |

## Networking

- **Internal DNS**: `influxdb:${INFLUXDB_PORT:-8086}` (within `infra_net`)
- **External URL**: `https://influxdb.${DEFAULT_URL}` (via Traefik, if included/routed)

## Persistence

- **Data**: `influxdb-data` mapped to `/var/lib/influxdb2`.

## Configuration

- **Init Mode**: `setup` (Automatic initialization).
- **Secrets**: Uses `influxdb_password` and `influxdb_api_token`.

## File Map

| Path        | Description                         |
| ----------- | ----------------------------------- |
| `README.md` | Service overview and CLI usage.     |
