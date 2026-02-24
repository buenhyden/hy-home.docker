# InfluxDB

InfluxDB is an open-source time series database (TSDB) developed by InfluxData.

## Services

| Service    | Image          | Role           | Resources         | Profile    |
| :--------- | :------------- | :------------- | :---------------- | :--------- |
| `influxdb` | `influxdb:2.8` | Time Series DB | 1.0 CPU / 1GB RAM | `influxdb` |

## Networking

- **Static IP**: `172.19.0.11`
- **External**: `influxdb.${DEFAULT_URL}` via Traefik.
- **Internal Port**: `${INFLUXDB_PORT}` (default 8086).

## Persistence

- **Data**: `influxdb-data` mapped to `/var/lib/influxdb2`.

## Configuration

- **Init Mode**: `setup` (Automatic initialization).
- **Secrets**: Uses `influxdb_password` and `influxdb_api_token`.

## File Map

| Path        | Description                         |
| ----------- | ----------------------------------- |
| `README.md` | Service overview and CLI usage.     |
