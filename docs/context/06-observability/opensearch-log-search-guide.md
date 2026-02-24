# OpenSearch Log Analytics Guide

> **Component**: `opensearch`
> **Internal API Port**: `9200`
> **Log Viewer**: OpenSearch Dashboards (`5601`)

## 1. Analytics & Log Hub

The stack provides a centralized platform for searching, visualizing, and alerting on application logs.

- **Dashboards URL**: `https://opensearch-dashboard.${DEFAULT_URL}`
- **Internal API**: `http://opensearch:9200` (HTTPS enabled in standard profile)

## 2. Standard Querying

Interact with the cluster health and indices via standard REST calls:

```bash
curl -k -u admin:${OPENSEARCH_ADMIN_PASSWORD} https://opensearch.${DEFAULT_URL}/_cluster/health?pretty
```

## 3. System Tuning

OpenSearch utilizes an embedded JVM. If memory pressure errors occur:

1. Ensure host `vm.max_map_count` is set to `262144`.
2. Inspect `OPENSEARCH_JAVA_OPTS` within the compose file to adjust Heap sizes.

## 4. Ingress Configuration

Traefik must use the `insecureTransport` middleware when proxying to OpenSearch due to its internal self-signed TLS requirements.
