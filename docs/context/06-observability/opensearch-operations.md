# OpenSearch Operations

> **Component**: `opensearch`

## Usage

### 1. Accessing Dashboards

- **URL**: `https://opensearch-dashboard.${DEFAULT_URL}`
- **Credentials**: user: `${ELASTIC_USERNAME}` / pass: `${ELASTIC_PASSWORD}`

### 2. Accessing API

- **URL**: `https://opensearch.${DEFAULT_URL}`
- **Note**: Self-signed certificate warning is expected.

```bash
curl -k -u admin:${OPENSEARCH_ADMIN_PASSWORD} https://opensearch.${DEFAULT_URL}/_cluster/health?pretty
```

### 3. Scaling to 3 Nodes

1. Edit `docker-compose.yml`:
   - Uncomment `opensearch-node2` and `opensearch-node3`.
   - Comment out `discovery.type=single-node`.
   - Uncomment `discovery.seed_hosts` and `cluster.initial_cluster_manager_nodes`.
2. Deploy:

   ```bash
   docker compose up -d
   ```

## Troubleshooting

### Node Not Joining

Check logs for discovery errors. Ensure `discovery.seed_hosts` matches container names.

### "max virtual memory areas vm.max_map_count is too low"

Linux hosts require increasing the mmap count:

```bash
sysctl -w vm.max_map_count=262144
```

### Certificate Issues

If Traefik returns "Bad Gateway", it might be due to SSL verification failure.
Check `traefik.http.services.opensearch.loadbalancer.server.scheme=https`.
