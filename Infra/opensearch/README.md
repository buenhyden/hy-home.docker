# OpenSearch Cluster

## Overview

A search and analytics suite. Current configuration is set for a **Single Node** (Dev/Test) environment, though config exists for a 3-node cluster.

## Service Details

### Nodes

- **Active**: `opensearch-node1`
- **Image**: `opensearchproject/opensearch:3.4.0`
- **Roles**: `cluster_manager`, `data`, `ingest`
- **Security**: HTTPS enabled (plugins.security.ssl).

## Custom Build (Plugins)

This directory contains a `Dockerfile` that builds a custom OpenSearch image with additional plugins pre-installed, following the [official Docker installation guide][opensearch-docker].

[opensearch-docker]: https://docs.opensearch.org/latest/install-and-configure/install-opensearch/docker/

**Installed Plugins:**

- `analysis-nori`: Korean (nori) analysis plugin.
- `ingest-attachment`: Ingest Processor Attachment plugin.
- `prometheus-exporter`: Prometheus Exporter for OpenSearch.
- `mapper-annotated-text`, `mapper-murmur3`, `mapper-size`, `discovery-azure-classic`, `repository-azure`.

### How to use

1. Open `docker-compose.yml`.
2. Comment out the `image` instruction.
3. Add/Uncomment the `build` instruction:

```yaml
services:
  opensearch-node1:
    # image: opensearchproject/opensearch:3.4.0
    build:
      context: .
      dockerfile: Dockerfile
```

1. Rebuild: `docker-compose up -d --build opensearch-node1`.

### Dashboards

- **Service**: `opensearch-dashboards`
- **Image**: `opensearchproject/opensearch-dashboards:3.4.0`
- **Port**: `5601` (Internal)

### Exporter

- **Service**: `opensearch-exporter`
- **Port**: `${ES_EXPORTER_PORT}`

## Network

Services are assigned static IPs in the `172.19.0.4X` range on `infra_net`.

| Service | IP Address | Notes |
| :--- | :--- | :--- |
| `opensearch-node1` | `172.19.0.44` | Active |
| `opensearch-node2` | `172.19.0.45` | Commmented Out |
| `opensearch-node3` | `172.19.0.46` | Commmented Out |
| `opensearch-dashboards` | `172.19.0.47` | |
| `opensearch-exporter` | `172.19.0.48` | |

## Traefik Configuration

- **OpenSearch API**: `opensearch.${DEFAULT_URL}`
  - **Note**: Traefik communicates with backend via **HTTPS**.
- **Dashboards**: `opensearch-dashboard.${DEFAULT_URL}`

## Environment Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `OPENSEARCH_INITIAL_ADMIN_PASSWORD`| Admin Password | `${ELASTIC_PASSWORD}` |
| `OPENSEARCH_JAVA_OPTS` | JVM Options | `-Xms1g -Xmx1g` |
| `OPENSEARCH_HOSTS` | Dashboards target | `["https://opensearch-node1:9200"]` |
| `OPENSEARCH_USERNAME` | Dashboards User | `${ELASTIC_USERNAME}` |
| `OPENSEARCH_PASSWORD` | Dashboards Password | `${ELASTIC_PASSWORD}` |
| `ES_USERNAME` | Exporter User | `${ELASTIC_USERNAME}` |
| `ES_PASSWORD` | Exporter Password | `${ELASTIC_PASSWORD}` |
