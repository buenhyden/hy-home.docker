# InfluxDB

InfluxDB is an open-source time series database (TSDB) developed by InfluxData.

## Services

| Service    | Image               | Role           | Resources         | Port       |
| :--------- | :------------------ | :------------- | :---------------- | :--------- |
| `influxdb` | `influxdb:2.7-alpine`| Time Series DB | 0.5 CPU / 1GB RAM | 8086 (Int) |

## Networking

| Endpoint                    | Port | Purpose                 |
| :-------------------------- | :--- | :---------------------- |
| `influxdb.${DEFAULT_URL}`   | 8086 | Web UI / Ingest API     |

## Persistence

- **Data**: `/var/lib/influxdb2` (mounted to `influxdb-data` volume).

## Configuration

- **Initialization**: Configured via `DOCKER_INFLUXDB_INIT_*` environment variables.

## File Map

| Path        | Description                         |
| ----------- | ----------------------------------- |
| `README.md` | Service overview and CLI usage.     |
