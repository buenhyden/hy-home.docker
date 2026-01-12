# OpenSearch Cluster

## Overview

A search and analytics suite. Current configuration is set for a **Single Node** (Dev/Test) environment, though config exists for a 3-node cluster.

## Service Details

### Nodes

- **Active**: `opensearch-node1`
- **Image**: `opensearchproject/opensearch:3.4.0`
- **Roles**: `cluster_manager`, `data`, `ingest`
- **Security**: HTTPS enabled (plugins.security.ssl).

### Dashboards

- **Service**: `opensearch-dashboards`
- **Image**: `opensearchproject/opensearch-dashboards:3.4.0`
- **Port**: `5601` (Internal)

### Exporter

- **Service**: `opensearch-exporter`
- **Port**: `${ES_EXPORTER_PORT}`

## Traefik Configuration

- **OpenSearch API**: `opensearch.${DEFAULT_URL}`
  - **Note**: Traefik communicates with backend via **HTTPS**.
- **Dashboards**: `opensearch-dashboard.${DEFAULT_URL}`

## Environment Variables

- `${OPENSEARCH_INITIAL_ADMIN_PASSWORD}` / `${ELASTIC_PASSWORD}`
- `${OPENSEARCH_JAVA_OPTS}`
