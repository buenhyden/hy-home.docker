---
layer: infra
---
# Observability Stack — Operations Runbook

**Overview (KR):** `06-observability` 스택의 일상적인 운영, 헬스체크, 트러블슈팅, 알림 관리 절차를 설명하는 운영 가이드입니다.

> Related: [System Context](observability-context.md) · [Lifecycle & Procedures](observability-lifecycle.md)

## Health Checks

Run a quick status check across all observability services:

```bash
docker ps \
  --filter "label=hy-home.tier=observability" \
  --format "table {{.Names}}\t{{.Status}}\t{{.Image}}"
```

| Service        | Health endpoint                                  |
| :------------- | :----------------------------------------------- |
| Prometheus     | `http://prometheus:9090/-/healthy`               |
| Loki           | `http://loki:3100/ready`                         |
| Tempo          | `http://tempo:3200/ready`                        |
| Alloy          | `http://alloy:12345/-/healthy`                   |
| Grafana        | `http://grafana:3000/api/health`                 |
| Alertmanager   | `http://alertmanager:9093/-/ready`               |
| Pushgateway    | `http://pushgateway:9091/-/ready`                |
| Pyroscope      | `http://pyroscope:4040/ready`                    |

## Alert Routing

Alertmanager receives fired alerts from Prometheus and routes them to the `team-notifications` receiver.

- **Slack**: `#notification` channel (configured via `slack_webhook` secret).
- **Email**: Gmail SMTP (configured via `smtp_username` / `smtp_password` secrets).

To temporarily silence an alert without changing config:

```bash
# Via Alertmanager UI
open https://alertmanager.${DEFAULT_URL}
```

Create a silence from the "Silences" tab with a time-bounded matcher.

## Prometheus: Alerting Rules

Alert rules live in `infra/06-observability/prometheus/config/alert_rules/`.

To reload rules without restarting Prometheus (requires `--web.enable-lifecycle`):

```bash
curl -s -XPOST http://localhost:9090/-/reload && echo "Reloaded"
```

## Grafana: Dashboard Management

### Add / update a pre-provisioned dashboard

1. Export the dashboard JSON from Grafana (Dashboard menu → Export → Save to file).
2. Place the JSON file in `infra/06-observability/grafana/dashboards/`.
3. Restart Grafana:

   ```bash
   docker compose -f infra/06-observability/docker-compose.yml restart grafana
   ```

### Add / update a datasource

Edit or add YAML files in `infra/06-observability/grafana/provisioning/datasources/` and restart Grafana.

## Troubleshooting

### Loki not receiving logs

1. Check Alloy is running and healthy.
2. Inspect Alloy logs for connection errors to Loki:

   ```bash
   docker logs infra-alloy --tail 50 | grep -i "loki\|error"
   ```

3. Verify the Docker socket is mounted: `docker exec infra-alloy ls /var/run/docker.sock`.
4. Confirm `loki-bucket` exists in MinIO and the `minio_app_user_password` secret matches.

### Tempo not storing traces

1. Check Alloy OTLP receiver is up: `curl -sf http://localhost:12345/-/healthy`.
2. Inspect Tempo logs:

   ```bash
   docker logs infra-tempo --tail 50 | grep -i "error\|s3\|minio"
   ```

3. Confirm `tempo-bucket` exists in MinIO.

### Grafana SSO login fails

1. Verify Keycloak realm `hy-home.realm` is running and the `grafana` client is enabled.
2. Check the redirect URI matches: `https://grafana.${DEFAULT_URL}/login/generic_oauth`.
3. Verify `oauth2_proxy_client_secret` matches the Keycloak client secret.
4. Inspect Grafana logs:

   ```bash
   docker logs infra-grafana --tail 50 | grep -i "oauth\|auth\|error"
   ```

### Prometheus scrape errors

1. Navigate to `https://prometheus.${DEFAULT_URL}/targets` and check for failed targets.
2. For the OpenSearch exporter target, confirm `opensearch_exporter_password` is correct.
3. Reload Prometheus config if you edited `prometheus.yml`:

   ```bash
   curl -XPOST http://localhost:9090/-/reload
   ```

### Alertmanager not sending notifications

1. Verify all three secrets exist: `docker secret ls | grep -E "smtp|slack"`.
2. Inspect Alertmanager container logs:

   ```bash
   docker logs infra-alertmanager --tail 50 | grep -i "error\|notify"
   ```

3. Test the Slack webhook with `curl`:

   ```bash
   curl -X POST -H 'Content-type: application/json' \
     --data '{"text":"Test from alertmanager"}' \
     <webhook-url>
   ```

## Log Access (Loki)

Query logs from any container in Grafana `Explore → Loki`, filtering by label:

- `{compose_project="hy-home"}` — all project containers
- `{service_name="infra-grafana", env="dev"}` — a specific service
- `{scope="infra"}` — infrastructure-tier containers only

## Metrics Retention

- **Prometheus**: 15 days (default `--storage.tsdb.retention.time`).
- **Loki**: 7 days (`limits_config.retention_period: 168h` in `loki-config.yaml`).
- **Tempo**: 24 hours (`compactor.compaction.block_retention: 24h` in `tempo.yaml`).

To change retention, edit the relevant config file and restart the service. No data is lost on restart — volumes are persisted.
