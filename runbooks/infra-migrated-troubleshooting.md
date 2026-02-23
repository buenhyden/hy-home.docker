# Migrated Infra Troubleshooting

<!-- MIGRATED CONTENT BELOW -->

## Context: Observability Stack (LGTM + Alloy) (06-observability)

## Maintenance & Troubleshooting

### Reloading Configurations

Configurations can be reloaded without service restarts via HTTP POST:

```bash
# Reload Prometheus configuration and alert rules
curl -X POST https://prometheus.${DEFAULT_URL}/-/reload

# Reload Alertmanager configuration
curl -X POST https://alertmanager.${DEFAULT_URL}/-/reload
```

### Checking Scraping Status

- **Metric Targets**: Navigate to `https://prometheus.${DEFAULT_URL}/targets`.
- **Collector Status**: Navigate to `https://alloy.${DEFAULT_URL}` to view the internal component graph.

## Context: Kafka Cluster (KRaft Mode) (kafka)

## Troubleshooting

### "Inconsistent Cluster ID"

If you see errors about `CLUSTER_ID` mismatch in logs:

1. Stop the cluster: `docker compose down`
2. Remove volumes: `docker volume rm infra_kafka-1-data infra_kafka-2-data infra_kafka-3-data`
3. Restart: `docker compose up -d`

**\*Note**: This deletes all data! Ensure `KAFKA_CLUSTER_ID` in `.env` remains constant.\*

### Broker Not Joining

Check `KAFKA_CONTROLLER_QUORUM_VOTERS`. All nodes must list the exact same voters string.

### Connect Worker OOM

Kafka Connect is memory intensive. If it crashes, increase the memory limit in `docker-compose.yml` (currently `1.5G`).

### Grafana Kafka Dashboard Shows No Data

**Symptom**: Grafana dashboards show empty panels even though Kafka is running.

**Cause**: Prometheus scrape job name does not match Grafana's `job="kafka"` filter.

**Fix**:

1. Ensure Prometheus uses `job_name: "kafka"` for the Kafka JMX scrape targets.
2. Reload Prometheus configuration.
3. Refresh Grafana dashboards.

## Context: Traefik Edge Router (traefik)

## Troubleshooting

### "404 Not Found"

- Check if the container is running and healthy.
- Verify `traefik.enable=true` label exists.
- Ensure the container is on the same Docker network (`infra_net`) as Traefik.

### "Internal Server Error" (SSO)

- Verify `oauth2-proxy` service is running.
- Check Traefik logs for ForwardAuth failures.

## Context: Nginx Standalone Proxy (nginx)

## Troubleshooting

### "Redirect Loop"

- Ensure `proxy_set_header X-Forwarded-Proto https;` is set.
- Verify Keycloak and Nginx agree on the scheme (HTTP vs HTTPS).

### "401 Unauthorized" (SSO Path)

- Check if you are correctly logged in via Keycloak.
- Verify OAuth2 Proxy is receiving the sub-request and validating the session token.

## Context: InfluxDB (influxdb)

## Troubleshooting

### "Permission Denied on /var/lib/influxdb2"

Ensure the host directory mapped to the volume has the correct permissions for the `influxdb` user (UID 1000).

### "API Token Invalid"

If you manually change the token in the UI or CLI, ensure all dependent services (Telegraf, Airflow) are updated with the new `INFLUXDB_API_TOKEN`.

## Context: Management Databases Infrastructure (mng-db)

## Troubleshooting

### PostgreSQL "Connection Refused"

Check if `mng-pg` is healthy and `listen_addresses` covers the network (default `*`).
Ensure `pg_hba.conf` allows the subnet `172.19.0.0/16`.

### Initialization Failed

If `mng-pg-init` fails:

1. Check `docker compose logs mng-pg-init`.
2. Ensure `init_users_dbs.sql` syntax is correct.
3. Verify `PGPASSWORD_SUPERUSER` matches `POSTGRES_PASSWORD`.

## Context: Qdrant Vector Database (qdrant)

## Troubleshooting

### "Transport Error"

If Open WebUI cannot connect:

1. Verify `infra_net` connectivity.
2. Ensure Qdrant is healthy: `curl http://localhost:${QDRANT_HOST_PORT}/readyz`

### High Memory Usage

Vector databases hold indices in RAM for speed. If Qdrant OOMs:

1. Increase memory limit in `docker-compose.yml`.
2. Configure `memmap_threshold` in `config.yaml` (advanced).

## Context: Valkey Cluster (valkey-cluster)

## Troubleshooting

### "Cluster Down"

- Check `valkey-cluster-init` logs.
- Verify node health checks (`valkey-cli ping`).

### "MOVED Error"

- Ensure your client is "Cluster Aware".
- Do not use a standalone client for cluster operations.

## Context: MinIO Object Storage (minio)

## Troubleshooting

### "Bucket already owned by you"

The init container prints "ignore-existing" warnings if buckets already exist. This is normal and indicates idempotency.

### "Init container fails"

If `minio-create-buckets` fails:

1. Check if `minio` service is healthy.
2. Verify secrets are correctly populated in `/run/secrets/`.
3. Check logs: `docker compose logs minio-create-buckets`

## Context: CouchDB Cluster (couchdb)

## Troubleshooting

### "Cluster not fully joined"

Check the logs of the initialization container:

```bash
docker logs couchdb-cluster-init
```

### "Consistency Issues"

Ensure your client supports HTTP cookies to take advantage of Traefik's sticky sessions, or target a specific node alias if performing cluster maintenance.

## Context: OpenSearch Cluster (opensearch)

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

## Context: PostgreSQL HA Cluster (postgresql-cluster)

## Troubleshooting

### Split Brain / No Leader

If `etcd` quorum is lost (e.g., 2 nodes down), the cluster becomes Read-Only.

- Check etcd health: `docker compose logs etcd-1`
- Ensure at least 2 etcd nodes are healthy.

### Node Flapping

If a PG node keeps restarting:

1. Check logs: `docker compose logs pg-0`
2. Look for "WalSender" or "Replication" errors.
3. Verify `etcd` connectivity from the PG container.

## Context: n8n (Workflow Automation) (n8n)

## Troubleshooting

### "Workflow Loop Detected"

Ensure `N8N_PROXY_HOPS` is set correctly (default: 1) if using multiple layers of proxies.

### "PDF/Image Rendering Issues"

Verify that the custom build was successful and fonts are available in `/usr/share/fonts` within the container.

## Context: Apache Airflow (airflow)

## Troubleshooting

### "Database is locked" or Migration Fails

If `airflow-init` hangs or fails, ensure the PostgreSQL database is healthy and reachable.
Check logs:

```bash
docker compose logs airflow-init
```

### Scheduler Not Warning Tasks

Check if the Scheduler is running and healthy:

```bash
docker compose ps airflow-scheduler
docker compose logs airflow-scheduler
```

### Worker Not Picking Up Tasks

1. Check Celery connection to Redis.
2. Verify `AIRFLOW__CELERY__BROKER_URL` matches the active Redis/Valkey service.
3. Check Flower UI to see if workers are online.

## Context: SonarQube (sonarqube)

## Troubleshooting

### "ElasticSearch did not exit normally"

Check `vm.max_map_count` as described in Configuration.

### "Database connection failed"

Ensure the PostgreSQL container is consistent and the `sonarqube` database exists and is accessible by the configured user.

## Context: Terrakube (terrakube)

## Troubleshooting

### "Executor not picking up jobs"

- Check the `InternalSecret` matches between API and Executor.
- Ensure `terrakube-executor` can resolve `terrakube-api` (Docker DNS).

### "State Locking Issues"

- Verify connection to `mng-redis` (Valkey).
- Check `terrakube-api` logs for Redis connection errors.

## Context: OAuth2 Proxy (SSO) (oauth2-proxy)

## Troubleshooting

### "500 Internal Server Error"

Usually indicates Redis connection failure or Misconfigured Secret.

1. Check logs: `docker compose logs oauth2-proxy`
2. Verify Redis connection URL in `docker-compose.yml`.

### "x509: certificate signed by unknown authority"

The OAuth2 Proxy container doesn't trust the IdP (Keycloak) certificate.

- Ensure `rootCA.pem` is valid.
- Verify `SSL_CERT_FILE` env var is set correctly.

## Context: Ollama & Open WebUI (open-webui)

## Troubleshooting

### "GPU Not Found"

- Ensure `nvidia-smi` works on the host.
- Verify `deploy.resources.reservations.devices` is enabled in `docker-compose.yml`.

### "RAG Not Working"

- Check if `qwen3-embedding:0.6b` (or your configured `RAG_EMBEDDING_MODEL`) is actually pulled.
- Verify connectivity to **Qdrant** (`http://qdrant:6333` from WebUI container).

## Context: Ollama & Open WebUI (ollama)

## Troubleshooting

### "GPU Not Found"

- Ensure `nvidia-smi` works on the host.
- Verify `deploy.resources.reservations.devices` is enabled in `docker-compose.yml`.

### "RAG Not Working"

- Check if `qwen3-embedding:0.6b` (or your configured `RAG_EMBEDDING_MODEL`) is actually pulled.
- Verify connectivity to **Qdrant** (`http://qdrant:6333` from WebUI container).
