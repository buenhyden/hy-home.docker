# OpenSearch

## Overview

Distributed search and analytics suite.

## Services

- **opensearch-node1**: Single-node cluster (configurable for multi-node).
  - URL: `https://opensearch.${DEFAULT_URL}`
- **opensearch-dashboards**: Visualization tool (Kibana fork).
  - URL: `https://opensearch-dashboard.${DEFAULT_URL}`
- **opensearch-exporter**: Prometheus metrics.

## Configuration

### Environment Variables

- `OPENSEARCH_INITIAL_ADMIN_PASSWORD`: Admin password.
- `OPENSEARCH_JAVA_OPTS`: JVM Heap settings.
- `plugins.security.ssl.http.enabled`: `true`

### Volumes

- `opensearch-data1`: `/usr/share/opensearch/data`
- `./certs`: SSL Certificates.

## Networks

- `infra_net`
  - opensearch-node1: `172.19.0.44`

## Traefik Routing

- **API Domain**: `opensearch.${DEFAULT_URL}`
- **Dashboards Domain**: `opensearch-dashboard.${DEFAULT_URL}`
