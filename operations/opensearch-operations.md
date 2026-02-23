# OpenSearch Operations Blueprint

> Standard operating procedures for the OpenSearch data node and UI dashboards.

## 1. Description

This document details operational patterns for managing the OpenSearch analytics and search engine deployed via `infra/04-data/opensearch/docker-compose.yml`.

## 2. System Resource Tuning

OpenSearch heavily depends on adequate memory and Host OS limits (like `net.ipv4.tcp_max_syn_backlog` and memory locking).

- The `docker-compose` is statically configured (`bootstrap.memory_lock=true`, `-Xms1g -Xmx1g`) alongside `shm_size: 1g`.
- Ensure your WSL/Linux Daemon limits satisfy `vm.max_map_count=262144`.

If crashes occur stating out of memory constraints:

1. Temporarily bump reservations inside the `OPENSEARCH_JAVA_OPTS` setting.
2. Make sure the container limit `memory:` exceeds the `-Xmx` setting by at least 25% (e.g. limit 1.5G, heap 1G) to account for off-heap buffers.

## 3. Data Integrity & Index Management

All indexes and PA (Performance Analyzer) agents retain data perpetually in `opensearch-data` volume mounts mapped to the host `${DEFAULT_DATA_DIR}/opensearch/opensearch1-data`.

### Manually Clearing Storage

Avoid direct OS file deletion inside the mounted folders. Instead, query the API:

```bash
# Obtain Index list
curl -k -u admin:${OPENSEARCH_ADMIN_PASSWORD} -X GET "https://opensearch.${DEFAULT_URL}/_cat/indices?v"

# Drop bloated index
curl -k -u admin:${OPENSEARCH_ADMIN_PASSWORD} -X DELETE "https://opensearch.${DEFAULT_URL}/<index-name>"
```

### Dashboard Configurations

`opensearch-dashboards` binds natively and handles graphical index mapping. If visual reporting hangs, restart the dashboard service, leaving the engine intact:

```bash
docker compose -f infra/04-data/opensearch/docker-compose.yml restart opensearch-dashboards
```
