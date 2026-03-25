<!-- [ID:04-data:influxdb] -->
# InfluxDB (TSDB)

> High-performance time series database for metrics and analytics.

## Overview (KR)

InfluxDB는 고성능 **시계열 데이터베이스(TSDB)**입니다. 인프라 메트릭, 어플리케이션 이벤트 및 실시간 분석 데이터를 효율적으로 저장하고 쿼리하는 데 최적화되어 있습니다.

## Overview

The `influxdb` service provides the time-series persistence layer for `hy-home.docker`. It is used for storing granular performance metrics and observability data, supporting high-ingest rates and complex analytical queries via Flux/SQL.

## Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **influxdb** | InfluxDB 3.8.3-core | Time Series Engine |

## Networking

| Service | Access | Description |
| :--- | :--- | :--- |
| **API Port** | `8181` | Standard InfluxDB 3.x API port. |
| **External URL** | `influxdb.${DEFAULT_URL}` | Secured access via Traefik. |

## Persistence

- **Data**: `influxdb-data` volume mapped to `/var/lib/influxdb3/data`.
- **Plugins**: `influxdb-plugins` volume for engine extensions.
- **Host Path**: `${DEFAULT_DATA_DIR}/influxdb/data`.

## Configuration

- **Authentication**: Uses `influxdb_password` and `influxdb_api_token` secrets.
- **Initialization**: Configured for automatic setup on first deployment.

## File Map

| Path | Description |
| :--- | :--- |
| `docker-compose.yml` | InfluxDB service definition. |
| `README.md` | Service overview. |

---

## Documentation References

- [Specialized DB Guide](../../../docs/07.guides/04-data/03.specialized-dbs.md)
- [Observability Guide](../../../docs/07.guides/99.observability/README.md)
