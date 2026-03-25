<!-- [ID:04-data:opensearch] -->
# OpenSearch Cluster

> Distributed search and analytics engine with Dashboards.

## Overview (KR)

이 스택은 강력한 검색 및 분석 엔진인 OpenSearch를 제공합니다. 시각화를 위한 Dashboards와 성능 모니터링을 위한 Exporter가 포함되어 있습니다.

## Overview

The `opensearch` stack provides a scalable search and analytics backend for the `hy-home.docker` ecosystem. It is used for log aggregation, full-text search, and real-time data visualization.

## Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **opensearch** | OpenSearch 2.18 | Search Engine |
| **os-dashboards** | OpenSearch Dashboards | Visualization UI |
| **os-exporter** | Prometheus Exporter | Metrics |

## Networking

| Purpose | Address | Description |
| :--- | :--- | :--- |
| **API** | `opensearch:9200` | REST API |
| **Dashboards** | `os-dashboards:5601` | Web UI |
| **Metrics** | `os-exporter:9108` | Prometheus metrics |

## Persistence

- **Data Volume**: `os-data` volume mounted to `/usr/share/opensearch/data`.
- **Storage Path**: `${DEFAULT_DATA_DIR}/os` on the host.

## File Map

| Path | Description |
| :--- | :--- |
| `docker-compose.yml` | OpenSearch stack definition. |
| `config/` | Security and engine configurations. |

---

## Documentation References

- [Specialized DB Guide](../../../docs/07.guides/04-data/03.specialized-dbs.md)
- [Backup Operations](../../../docs/08.operations/04-data/README.md)
