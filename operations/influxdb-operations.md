# InfluxDB Operations

> **Component**: `influxdb`

## Usage

### 1. Web UI Dashboard

Access the integrated dashboard at `https://influxdb.${DEFAULT_URL}`.

- Visualize data using Data Explorer (InfluxQL / Flux).
- Manage Buckets, Tokens, and Scrapers.
- Build and share multi-dimensional dashboards.

### 2. Client Connection (Python/Telegraf)

Use the **Internal Address** `http://influxdb:8086` with the following credentials:

- **Org**: `${INFLUXDB_ORG}`
- **Bucket**: `${INFLUXDB_BUCKET}`
- **Token**: Bearer or API Token authentication.

## Troubleshooting

### "Permission Denied on /var/lib/influxdb2"

Ensure the host directory mapped to the volume has the correct permissions for the `influxdb` user (UID 1000).

### "API Token Invalid"

If you manually change the token in the UI or CLI, ensure all dependent services (Telegraf, Airflow) are updated with the new `INFLUXDB_API_TOKEN`.
