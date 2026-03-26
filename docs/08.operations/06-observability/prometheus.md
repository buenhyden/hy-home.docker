# [OPERATIONAL-POLICY] 06-observability: prometheus

Standardized procedures for maintaining Prometheus metrics collection and alerting integrity.

## Procedures

### 1. Scrape Target Registration

To add a new service for monitoring:

1. Ensure the target service exposes metrics (usually on port `9090` or `8080`).
2. Update `infra/06-observability/prometheus/config/prometheus.yml`:

   ```yaml
   - job_name: 'new-service'
     static_configs:
       - targets: ['new-service:port']
   ```

3. Validate configuration:

   ```bash
   docker exec infra-prometheus promtool check config /etc/prometheus/prometheus.yml
   ```

4. Reload Prometheus (send `SIGHUP` or use API `-X POST /-/reload`).

### 2. Alerting Rule Management

- **Definition**: Rules must be added to the appropriate file in `config/alert_rules/`.
- **Naming**: Use camelCase for alert names (e.g., `PostgresInstanceDown`).
- **Standard Labels**:
  - `severity`: `critical` (immediate action), `warning` (investigation), `info` (notification only).
- **Testing**:

  ```bash
  promtool test rules config/alert_rules/tests/*.yml
  ```

### 3. Performance Monitoring

- **Cardinality Audit**: Periodically review high-cardinality metrics (e.g., `container_...` from cAdvisor).
- **Rule Evaluation**: Monitor `prometheus_rule_evaluation_duration_seconds` to ensure evaluations complete within the `15s` window.
- **TSDB Integrity**: Check for compaction failures in Prometheus logs.

## Constraints

- **Scrape Intervals**: Never set below `10s` without architectural approval.
- **Retention**: Default is `15d`; any changes require volume resizing.
- **Rule Format**: Use `expr`, `for`, `labels`, and `annotations` (Summary/Description).

---
**AI Agent Note**: AI agents must verify that every new infrastructure component includes a corresponding scrape configuration and basic "up" alert.
