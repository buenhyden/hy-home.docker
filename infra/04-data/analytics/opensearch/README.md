<!-- [ID:04-data:opensearch] -->
# OpenSearch Cluster

> Distributed search and analytics engine with Dashboards.

## 1. Context (SSoT)

The `opensearch` stack provides a scalable search backend for log aggregation, full-text search, and real-time visualization.

- **Status**: Production / Search
- **SSoT Documentation**: [docs/07.guides/04-data/03.specialized-dbs.md](../../../docs/07.guides/04-data/03.specialized-dbs.md)
- **Monitoring**: Integrated with Prometheus via exporter.

## 2. Structure

```text
opensearch/
├── docker-compose.yml   # Stack definition
└── config/              # Security & Engine config
```

## 3. Tech Stack

| Service | Technology | Role |
| :--- | :--- | :--- |
| **opensearch** | OpenSearch 2.18 | Search Engine |
| **os-dashboards** | OS Dashboards | Visualization UI |
| **os-exporter** | Prometheus Exporter | Metrics |

## 4. Configuration (Secrets & Env)

- **Secrets**: Admin credentials managed via Docker secrets.
- **Node Settings**: Configured for single-node development or multi-node production via `config/`.
- **JVM**: Heap settings defined in `docker-compose.yml`.

## 5. Persistence

- **Data**: `os-data` volume mapped to `${DEFAULT_DATA_DIR}/os`.

## 6. Operational Status

- **API**: `opensearch:9200`
- **Dashboards**: `os-dashboards:5601`
- **Metrics**: `os-exporter:9108`

---
Copyright (c) 2026. Licensed under the MIT License.
