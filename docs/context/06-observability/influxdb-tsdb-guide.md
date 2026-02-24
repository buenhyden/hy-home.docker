# InfluxDB Time-Series Database Guide

> **Component**: `influxdb`
> **Internal API Port**: `8086`
> **Query Language**: Flux, InfluxQL

## 1. Time-Series Storage

InfluxDB v2 serves as the primary engine for high-resolution operational metrics and sensor data.

- **Internal DNS**: `influxdb`
- **Dashboard**: `https://influxdb.${DEFAULT_URL}`

## 2. Integration Pattern

Applications should connect via the InfluxDB client libraries using the following parameters:

- **Org**: `${INFLUXDB_ORG}`
- **Bucket**: `${INFLUXDB_BUCKET}`
- **Token**: Bearer authentication via Docker Secret `influxdb_api_token`.

## 3. Data Retention

Retention policies are managed per-bucket. For performance preservation:

1. Long-term cold data should be aggregated using TASKS to downsampled buckets.
2. Short-term high-fidelity data should utilize a 30-day retention window to limit disk growth.

## 4. Troubleshooting

If CLI access is needed from the host:

```bash
docker exec -it infra-influxdb influx [command]
```
