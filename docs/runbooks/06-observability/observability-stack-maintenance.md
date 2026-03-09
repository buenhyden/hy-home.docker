# Runbook: Observability Stack & Alloy Maintenance

> **Tier**: `06-observability`
> **Stack**: LGTM (Loki, Grafana, Tempo, Metrics)
> **Collector**: Grafana Alloy

## 1. Issue: Metric or Trace Gaps in Grafana

**Given**: Grafana dashboards show "No data" or incomplete trace waterfall.
**When**: The Alloy collector or upstream push logic is hindered.
**Then**:

1. **Reload Configuration**: Reach the collector's lifecycle endpoint:

   ```bash
   # Reload Prometheus rules
   curl -X POST https://prometheus.${DEFAULT_URL}/-/reload
   # Reload Alloy (if lifecycle is enabled)
   curl -X POST https://alloy.${DEFAULT_URL}/-/reload
   ```

2. **Check Scraping**: Navigate to `https://prometheus.${DEFAULT_URL}/targets` to verify all infra endpoints are `UP`.

## 2. Issue: Loki Data Not Found (Retention/Storage)

**Given**: "Data not found" error when querying logs older than 24h.
**When**: Retention policy or MinIO backend flushing fails.
**Then**:

1. **MinIO Audit**: Ensure the `loki-data` bucket exists and is accessible.
2. **Loki Logs**: `docker compose logs loki` to look for "compactor" or "s3 gateway" timeouts.

## 3. Dashboard Management

**Given**: You need to import a specialized dashboard.
**When**: The dashboard is exported as JSON.
**Then**:
Place the JSON into `infra/06-observability/grafana/dashboards/` and restart Grafana:

```bash
docker compose -f infra/06-observability/docker-compose.yml restart grafana
```
