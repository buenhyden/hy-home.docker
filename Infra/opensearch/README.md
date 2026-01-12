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

- `${OPENSEARCH_INITIAL_ADMIN_PASSWORD}` / `${ELASTIC_PASSWORD}`
- `${OPENSEARCH_JAVA_OPTS}`
