# InfluxDB (TSDB)

> High-performance time series database for metrics and analytics.

## 1. Context & Objective

The `influxdb` service provides the time-series persistence layer for `hy-home.docker`. It is designed for storing granular performance metrics and observability data, supporting high-ingest rates and analytical queries via Flux/SQL.

### Role
- **Observability Backend**: Stores metrics from Telegraf and exporters.
- **Analytics Engine**: Provides real-time data processing for dashboards.

## 2. Requirements & Constraints

- **Engine**: InfluxDB 3.x (Clustered or Single-node configurations).
- **Secrets**: API tokens and passwords MUST be managed via Docker secrets.
- **Network**: Standard API port `8181` secured via Traefik.

## 3. Setup & Installation

### Deployment
```bash
# Start the InfluxDB service
docker compose up -d
```

### Verification
```bash
# Check service health
curl -i http://influxdb:8181/health
```

## 4. Usage & Integration

### Operational Status
- **API Endpoint**: `influxdb:8181` / `https://influxdb.${DEFAULT_URL}`
- **Persistence**: Data is mapped to `${DEFAULT_DATA_DIR}/influxdb/data`.

### Integration Pointers
- Consult the [Observability Guide](../../../docs/07.guides/06-observability/README.md) for data forwarding patterns.
- Use `influx` CLI for bucket management and task scheduling.

## 5. Maintenance & Safety

### Data Integrity
1. Retention policies MUST be defined to prevent storage saturation.
2. Regularly monitor `influxdb-data` volume sizing.
3. API tokens should have the minimal required scopes for each application.

---

Copyright (c) 2026. Licensed under the MIT License.
