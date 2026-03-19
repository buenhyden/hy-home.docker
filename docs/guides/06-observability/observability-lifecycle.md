---
layer: infra
---
# Observability Stack — Lifecycle & Procedures

**Overview (KR):** `06-observability` 스택의 초기 설정, 시작, 종료, 업그레이드, 백업, 시크릿 교체 절차를 설명하는 라이프사이클 가이드입니다.

> Related: [System Context](observability-context.md) · [Operations Runbook](observability-operations.md)

## Prerequisites

The following services must be running before starting the observability stack:

- **MinIO** (`04-data` tier, profile `storage`) — S3 buckets `loki-bucket` and `tempo-bucket` must exist.
- **Traefik** (`01-gateway` tier) — required for HTTPS routing to Grafana, Prometheus, Alloy, etc.
- **Keycloak** (`02-auth` tier) — required for Grafana SSO login.

All Docker Secrets listed in [observability-context.md](observability-context.md#secrets) must be created before startup.

## Initial Setup

### 1. Create MinIO Buckets

Log in to MinIO (`https://minio.${DEFAULT_URL}`) and create two buckets:

```
loki-bucket
tempo-bucket
```

Both can use the default settings (no versioning required).

### 2. Create App User and Secrets

Create the MinIO application user (e.g., `minio-app-user`) and note the password. Then populate all Docker Secrets:

```bash
cd /path/to/hy-home.docker
echo "value" | docker secret create minio_app_user_password -
echo "value" | docker secret create opensearch_exporter_password -
echo "value" | docker secret create grafana_admin_password -
echo "value" | docker secret create oauth2_proxy_client_secret -
echo "value" | docker secret create smtp_username -
echo "value" | docker secret create smtp_password -
echo "value" | docker secret create slack_webhook -
```

### 3. Create Keycloak OAuth Client

In Keycloak realm `hy-home.realm`:

1. Create a client with ID `grafana` (or whatever `OAUTH2_PROXY_CLIENT_ID` is set to).
2. Enable PKCE — set `PKCECodeChallengeMethod` to `S256`.
3. Set redirect URI: `https://grafana.${DEFAULT_URL}/login/generic_oauth`.
4. Note the client secret → populate `oauth2_proxy_client_secret`.

### 4. Grafana Group Mapping

Create the following groups in Keycloak:

| Group      | Grafana role |
| :--------- | :----------- |
| `/admins`  | Admin        |
| `/editors` | Editor       |

Assign users to groups as appropriate.

## Startup

```bash
cd infra
docker compose \
  -f 06-observability/docker-compose.yml \
  --profile obs \
  up -d
```

### Expected startup order

Docker Compose uses `depends_on` + `condition: service_healthy` to enforce the following order:

```
Prometheus (healthy)
    └─▶ Alloy, Grafana, Alertmanager, Pushgateway
         └─▶ (Grafana healthy) ─▶ Alertmanager, Pushgateway
```

Loki and Tempo start in parallel with Prometheus. Alloy waits for Prometheus to be healthy, and Loki/Tempo to have started.

Allow 60–90 seconds after `up -d` for all services to pass their health checks.

## Verification

```bash
# Check all containers are healthy
docker ps --filter "label=hy-home.tier=observability" --format "table {{.Names}}\t{{.Status}}"

# Prometheus up?
curl -sf http://localhost:9090/-/healthy && echo "OK"

# Loki up?
curl -sf http://localhost:3100/ready && echo "OK"

# Tempo up?
curl -sf http://localhost:3200/ready && echo "OK"

# Alloy up?
curl -sf http://localhost:12345/-/healthy && echo "OK"

# Pyroscope up?
curl -sf http://localhost:4040/ready && echo "OK"
```

Then log in to `https://grafana.${DEFAULT_URL}` and verify:

1. **Explore → Loki** — select a label stream and confirm container logs appear.
2. **Explore → Tempo** — run a TraceQL query, e.g. `{}` with a time range.
3. **Explore → Prometheus** — confirm targets at `https://prometheus.${DEFAULT_URL}/targets`.

## Shutdown

```bash
docker compose \
  -f infra/06-observability/docker-compose.yml \
  --profile obs \
  down
```

Data volumes (`prometheus-data`, `loki-data`, `tempo-data`, `grafana-data`, `alertmanager-data`, `pyroscope-data`, `alloy-data`) are preserved on the host under `${DEFAULT_OBSERVABILITY_DIR}`.

## Upgrade Procedure

1. Update the image tag in `docker-compose.yml` (for Prometheus, Grafana, Alloy, Alertmanager, Pushgateway) or in the respective `Dockerfile` (for Loki, Tempo custom builds).
2. For Loki and Tempo, rebuild and push the custom images:

   ```bash
   docker build -t hy/loki:<new-version>-custom infra/06-observability/loki/
   docker build -t hy/tempo:<new-version>-custom infra/06-observability/tempo/
   ```

3. Validate compose config:

   ```bash
   docker compose -f infra/06-observability/docker-compose.yml config --quiet
   ```

4. Pull/restart:

   ```bash
   docker compose -f infra/06-observability/docker-compose.yml --profile obs pull
   docker compose -f infra/06-observability/docker-compose.yml --profile obs up -d
   ```

5. Verify all services are healthy (see Verification section above).

## Backup & Restore

All data is bind-mounted under `${DEFAULT_OBSERVABILITY_DIR}` on the host. A filesystem snapshot or `rsync` backup of that directory captures:

- Prometheus TSDB
- Loki index and chunks cache (cold chunks are in MinIO)
- Tempo WAL (cold blocks are in MinIO)
- Grafana SQLite DB + plugins
- Alertmanager silence state

> MinIO bucket data (`loki-bucket`, `tempo-bucket`) should also be backed up separately — see the `04-data` tier lifecycle guide.

## Secret Rotation

All secrets are Docker Secrets. Rotation requires:

1. Remove the old secret: `docker secret rm <name>`.
2. Create the new secret: `echo "new-value" | docker secret create <name> -`.
3. Restart the affected service: `docker compose -f infra/06-observability/docker-compose.yml --profile obs up -d --force-recreate <service>`.

No other configuration file changes are needed — secrets are injected at container startup via template substitution or direct `/run/secrets/<name>` file reads.
