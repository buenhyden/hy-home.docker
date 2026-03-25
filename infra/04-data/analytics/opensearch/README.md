<!-- [ID:04-data:opensearch] -->
# OpenSearch

> Distributed search and analytics engine with Dashboards.

## 1. Context & Objective (SSoT)

The `opensearch` stack provides a scalable search backend for log aggregation, full-text search, and real-time visualization. It is designed for high-availability observability and analytical workloads.

- **Status**: Production / Search
- **SSoT Documentation**: [03.specialized-dbs.md](../../../docs/07.guides/04-data/03.specialized-dbs.md)
- **Monitoring**: Prometheus integration via `os-exporter`.

## 2. Requirements & Constraints

- **Resources**: JVM Heap settings (default 1GB) must be monitored.
- **Security**: Admin credentials managed via Docker secrets.
- **Ports**:
  - `9200`: Search API (HTTPS)
  - `5601`: Dashboards UI

## 3. Setup & Installation

The stack consists of the engine, visualization, and metric exporter.

```bash
docker compose up -d opensearch opensearch-dashboards
```

### Persistence

- **Volume**: `opensearch-data` (`/usr/share/opensearch/data`)
- **Host Path**: `${DEFAULT_DATA_DIR}/opensearch/opensearch1-data`

## 4. Usage & Integration

### Service Matrix

| Service | Technology | Role |
| :--- | :--- | :--- |
| **opensearch** | OpenSearch 2.18 | Search Engine |
| **os-dashboards** | OS Dashboards 3.4.0 | Visualization UI |
| **os-exporter** | Prometheus Exporter | Metrics |

### Integration Points
- **API**: `https://opensearch:9200`
- **Dashboards**: `https://opensearch-dashboard.${DEFAULT_URL}`
- **Metrics**: `http://opensearch-exporter:9114/metrics`

## 5. Maintenance & Safety

- **Identity**: Security settings in `config/opensearch-security/` must be synchronized across nodes.
- **Backups**: Use OpenSearch snapshots to S3 (MinIO) or local shared storage.
- **Health**: Monitor cluster state via `/_cluster/health` (Healthy: green/yellow).

---
Copyright (c) 2026. Licensed under the MIT License.
