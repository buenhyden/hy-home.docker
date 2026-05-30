---
status: active
---
<!-- Target: docs/05.operations/policies/06-observability/prometheus.md -->

# [OPERATIONAL-POLICY] 06-observability: prometheus Operations Policy

Standardized procedures for maintaining Prometheus metrics collection and alerting integrity.

## Overview (KR)

This policy defines the Prometheus controls for scrape target registration, alerting rule management, performance monitoring, and TSDB integrity. Ordered recovery or reload procedures belong in the matching runbook.

## Policy Details

### Scrape Target Registration Requirements

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

### Alerting Rule Management Requirements

- **Definition**: Rules must be added to the appropriate file in `config/alert_rules/`.
- **Naming**: Use camelCase for alert names (e.g., `PostgresInstanceDown`).
- **Standard Labels**:
  - `severity`: `critical` (immediate action), `warning` (investigation), `info` (notification only).
- **Testing**:

  ```bash
  promtool test rules config/alert_rules/tests/*.yml
  ```

### Performance Monitoring Requirements

- **Cardinality Audit**: Periodically review high-cardinality metrics (e.g., `container_...` from cAdvisor).
- **Rule Evaluation**: Monitor `prometheus_rule_evaluation_duration_seconds` to ensure evaluations complete within the `15s` window.
- **TSDB Integrity**: Check for compaction failures in Prometheus logs.

## Constraints

- **Scrape Intervals**: Never set below `10s` without architectural approval.
- **Retention**: Default is `15d`; any changes require volume resizing.
- **Rule Format**: Use `expr`, `for`, `labels`, and `annotations` (Summary/Description).

---
**AI Agent Note**: AI agents must verify that every new infrastructure component includes a corresponding scrape configuration and basic "up" alert.

## Policy Scope

This policy applies to Prometheus scrape target registration, alerting rule management, performance monitoring, and TSDB integrity controls for the observability tier.

## Controls

- **Required**: Preserve the operational contract documented in the linked guide and source configuration.
- **Allowed**: Documentation-only corrections that keep links and verification evidence current.
- **Disallowed**: Secret values, credential dumps, or unapproved runtime changes in this policy document.

## Exceptions

N/A — 현재 승인된 예외 없음.

## Verification

- Review this policy with its matching guide, runbook, and linked infra/config documents before material operations changes.
- Run `bash scripts/validation/check-repo-contracts.sh` after policy or linked operations document updates.
- Run `bash scripts/validation/check-doc-traceability.sh` when execution or operations links change.

## Review Cadence

- Review when linked service configuration, architecture, or runbook behavior changes.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/06-observability/prometheus.md)
- [Recovery runbook](../../runbooks/06-observability/prometheus.md)
