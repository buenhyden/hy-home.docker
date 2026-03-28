# [RECOVERY-RUNBOOK] 06-observability: prometheus

Recovery procedures for common Prometheus service disruptions and metrics collection failures.

## Incident Scenarios

### 1. Prometheus Container Crash (OOM/Corruption)

**Symptoms**: Prometheus UI unreachable, Grafana metrics `NaN` or missing, alerts stop firing.
**Recovery**:

1. Check container logs:

   ```bash
   docker logs infra-prometheus
   ```

2. If OOM, increase memory limits in `infra/06-observability/docker-compose.yml`.
3. If corruption, check TSDB integrity and consider restarting without the corrupted WAL.
4. Final restart:

   ```bash
   docker compose restart prometheus
   ```

### 2. Scrape Target Unavailable

**Symptoms**: Alert `PrometheusAllTargetsMissing` or specific service metrics missing.
**Recovery**:

1. Identify failing job in Prometheus UI (`/targets`).
2. Verify target reachability:

   ```bash
   docker exec -it infra-prometheus ping <target-service-name>
   ```

3. Ensure target service is healthy and exposing `/metrics`.
4. Validate `prometheus.yml` configuration (ports, job name).

### 3. Alerting Rule Evaluation Failure

**Symptoms**: Alert `PrometheusRuleEvaluationFailures` is firing.
**Recovery**:

1. Check Prometheus logs for syntax or performance errors in rules.
2. Validate rule files using `promtool`:

   ```bash
   docker exec infra-prometheus promtool check rules /etc/prometheus/alert_rules/*.yml
   ```

3. Fix any syntax errors or simplify expensive PromQL expressions.

## Verification

1. Access the Prometheus UI: [http://prometheus.hy-home.local/-/healthy](http://prometheus.hy-home.local/-/healthy) (or internal port `9090`).
2. Verify all "critical" scrape targets are "UP" in the `/targets` page.
3. Confirm that Grafana dashboards are receiving new metrics data.

---
**AI Agent Note**: AI agents should use the `promtool` command to verify any proposed changes to Prometheus or Alerting configurations before applying them.

## Related Operational Documents

- **Operation**: [prometheus.md](../../08.operations/06-observability/prometheus.md)
- **Plan**: [2026-03-26-06-observability-standardization.md](../../05.plans/2026-03-26-06-observability-standardization.md)
