# OpenSearch Cluster

## Overview

A search and analytics suite. Current configuration is set for a **Single Node** (Dev/Test) environment, though config exists for a 3-node cluster.

## Services

| Service | Image | Role |
| :--- | :--- | :--- |
| `opensearch-node1` | `opensearchproject/opensearch:3.4.0` | Cluster Manager, Data, Ingest Node |
| `opensearch-dashboards` | `opensearchproject/opensearch-dashboards:3.4.0` | Visualization Dashboard |
| `opensearch-exporter` | `prometheuscommunity/elasticsearch-exporter:v1.10.0` | Prometheus Metrics Exporter |

## Custom Build (Plugins)

A `Dockerfile` is provided to build a custom OpenSearch image with pre-installed plugins.

**Installed Plugins:**

- `analysis-nori` (Korean Analysis)
- `ingest-attachment` (File Processing)
- `prometheus-exporter` (Native Metrics)
- `mapper-annotated-text`, `mapper-murmur3`, `mapper-size`
- `discovery-azure-classic`, `repository-azure`

To use the custom build, uncomment the `build` section in `docker-compose.yml`.

## Networking

Services run on `infra_net` with static IPs (172.19.0.4X).

| Service | Static IP | Internal Port | Host Port | Traefik Domain |
| :--- | :--- | :--- | :--- | :--- |
| `opensearch-node1` | `172.19.0.44` | `9200` | - | `opensearch.${DEFAULT_URL}` |
| `opensearch-dashboards` | `172.19.0.47` | `5601` | - | `opensearch-dashboard.${DEFAULT_URL}` |
| `opensearch-exporter` | `172.19.0.48` | `${ES_EXPORTER_PORT}` | `${ES_EXPORTER_HOST_PORT}` | - |

## Persistence

- **Data**: `opensearch-data1` → `/usr/share/opensearch/data`
- **Certificates**: `./certs` → `/usr/share/opensearch/config/certs` (Read-only)

## Configuration

### Environment Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `OPENSEARCH_INITIAL_ADMIN_PASSWORD`| Admin Password | `${ELASTIC_PASSWORD}` |
| `OPENSEARCH_JAVA_OPTS` | JVM Options | `-Xms1g -Xmx1g` |
| `OPENSEARCH_HOSTS` | Dashboards target | `["https://opensearch-node1:9200"]` |
| `OPENSEARCH_USERNAME` | Dashboards User | `${ELASTIC_USERNAME}` |
| `OPENSEARCH_PASSWORD` | Dashboards Password | `${ELASTIC_PASSWORD}` |
| `ES_USERNAME` | Exporter User | `${ELASTIC_USERNAME}` |
| `ES_PASSWORD` | Exporter Password | `${ELASTIC_PASSWORD}` |

## Traefik Integration

Services are exposed via Traefik with TLS enabled (`websecure`). Note that backend communication uses **HTTPS** (self-signed certs).

- **OpenSearch API**: `opensearch.${DEFAULT_URL}`
- **Dashboards**: `opensearch-dashboard.${DEFAULT_URL}`

## Usage

1. **Dashboards**: Access `https://opensearch-dashboard.${DEFAULT_URL}` (Login via `${ELASTIC_USERNAME}`).
2. **API**: Access `https://opensearch.${DEFAULT_URL}`.
3. **Rebuild**: If adding plugins, run `docker-compose up -d --build opensearch-node1`.
