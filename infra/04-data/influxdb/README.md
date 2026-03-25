<!-- [ID:04-data:influxdb] -->
# InfluxDB (TSDB)

> High-performance time series database for metrics and analytics.

## Overview (KR)

이 서비스는 인프라 메트릭 및 어플리케이션 이벤트 저장에 최적화된 **고성능 시계열 데이터베이스(TSDB)**입니다. 실시간 데이터 분석 및 모니터링 백엔드로 활용됩니다.

## Overview

The `influxdb` service provides the time-series persistence layer for `hy-home.docker`. It is used for storing granular performance metrics and observability data, supporting high-ingest rates and complex analytical queries via Flux/SQL.

## Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **influxdb** | InfluxDB 3.8 | Time Series Engine |

## Networking

| Service | Port | Description |
| :--- | :--- | :--- |
| **API Port** | `8181` | Standard InfluxDB 3.x API port. |
| **External URL** | `influxdb.${DEFAULT_URL}` | Secured access via Traefik. |

## Persistence

- **Volumes**: `influxdb-data`, `influxdb-plugins`.
- **Secrets**: `influxdb_password`, `influxdb_api_token`.
- **Path**: `${DEFAULT_DATA_DIR}/influxdb/data` on the host.

## File Map

| Path | Description |
| :--- | :--- |
| `docker-compose.yml` | InfluxDB service definition. |

---

## Documentation References

- [Specialized DB Guide](../../../docs/07.guides/04-data/03.specialized-dbs.md)
- [Observability Guide](../../../docs/07.guides/06-observability/README.md)
