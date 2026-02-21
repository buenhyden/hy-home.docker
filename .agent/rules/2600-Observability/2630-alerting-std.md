---
trigger: model_decision
glob: ["services/**", "docs/slo/**/*.md", "alerts/**/*.yaml", "monitoring/**/*.yaml"]
description: "Alerting and SLO Standards: Enforces burn-rate based paging, user-impact mapping, and error budget governance."
---

# Alerting & SLO Standards

- **Role**: SRE / SLO Governance Owner
- **Purpose**: Define standards for deterministic Service Level Objectives (SLOs) and actionable alerting policies that prioritize user impact over system symptoms.
- **Activates When**: Defining SLIs/SLOs, configuring alert thresholds, or designing incident response routing.

**Trigger**: model_decision — Apply during the design of reliability metrics and alerting logic.

## 1. Standards

### Principles

- **[REQ-ALT-01] User-Impact Mapping**
  - All paging alerts MUST be mapped to direct user impact (e.g., elevated error rates) rather than internal system resource utilization.
- **[REQ-ALT-02] Burn-Rate Based Paging**
  - Paging alerts MUST utilize multi-window, multi-burn-rate logic (Fast/Slow burn) to minimize noise and maximize precision.
- **[REQ-ALT-03] Actionable Response**
  - Every alert MUST be actionable. If an alert does not require immediate human intervention, it MUST be a "Ticket" alert, not a "Page".

### SLI Classification

| SLI Type | Metric Basis | Target Compliance |
| --- | --- | --- |
| Availability | Success / Total Ratio | 99.9% (Critical) |
| Latency | P99 / Threshold Ratio | < 300ms (Core) |
| Correctness | Fault / Valid Ratio | 100% (Metadata) |
| Freshness | Time Since Last Update | < 5m (Pipelines) |

### Must

- **[REQ-ALT-04] Deterministic SLI Query**
  - Every SLI MUST have a strictly defined PromQL/SQL query with explicit numerators and denominators.
- **[REQ-ALT-05] Mandatory Error Budget Policy**
  - Every service with an SLO MUST have a documented Error Budget Policy defining actions when the budget is exhausted.
- **[REQ-ALT-06] Runbook Linkage**
  - Every paging alert MUST include a direct link to a verified, up-to-date runbook documentation.

### Must Not

- **[BAN-ALT-01] Symptom-Only Paging**
  - Paging MUST NOT be triggered by internal metrics (e.g., CPU > 80%) unless they are proven to cause immediate user experience degradation.
- **[BAN-ALT-02] Silent SLO Violations**
  - SLO breaches MUST NOT be ignored; they MUST automatically trigger a review of the service's release constraints.

### Failure Handling

- **Stop Condition**: Stop deployment if an alert is configured without an owner team or a validated runbook link.

## 2. Procedures

- **[PROC-ALT-01] SLO Review Cycle**
  - Quarterly audit of SLO targets to ensure they align with current business requirements and user expectations.
- **[PROC-ALT-02] Noise Reduction Audit**
  - Monthly review of alert history to identify and suppress "Flapping" or low-value alerts.

## 3. Examples

### Burn-Rate Alert (Conceptual YAML)

```yaml
alert: HighErrorRateBurn
expr: (error_ratio > 10x_threshold) && (1h_window_burn > alert_target)
labels:
  severity: page
  team: payment-core
annotations:
  runbook: 'https://docs.example.com/runbooks/high-error-rate'
```

## 4. Validation Criteria

- **[VAL-ALT-01] Measurement Determinism**
  - [ ] SLI queries are verified to produce consistent results across multiple evaluation cycles.
- **[VAL-ALT-02] Paging Precision**
  - [ ] Historical audit confirms that > 90% of pages resulted in a "Confirmed Incident" or "Action Taken".
- **[VAL-ALT-03] Budget Enforcement**
  - [ ] System verifies that release gates automatically tighten when the 30-day error budget is depleted.
