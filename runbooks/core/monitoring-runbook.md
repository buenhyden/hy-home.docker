# Monitoring Runbook

## 1. Document Purpose

Procedure for monitoring service health and responding to alert signals.

## 2. Prerequisites

- Access Requirements: Monitoring dashboards and alerting tools
- Tools: Metrics dashboard, logs viewer, tracing (if enabled)

## 3. Dashboards & Alerts (Required Links)

- [ ] **Primary Dashboard**: `[Link to grafana/datadog]`
- [ ] **SLOs / SLIs**: `[Link to SLO definitions]`
- [ ] **Alert Routing**: `[Where does this alert page? PagerDuty/Slack]`

## 4. Execution Steps

1. Check primary dashboard (latency, traffic, errors, saturation).

   ```bash
   # Open service dashboard and inspect last 30-60 minutes.
   ```

2. Correlate alerts with logs and traces.

   ```bash
   # Filter by correlation or trace id where available.
   ```

3. Classify incident severity and engage response flow.

   ```bash
   # Use SEV criteria from incident policy.
   ```

## 5. Validation

- Alert cause identified and documented.
- Mitigation action validated by metric recovery.

## 6. Rollback / Reversal Procedure

- If recovery fails, follow deployment rollback runbook.

## 7. Escalation Contacts

- Primary Contact: On-call rotation
- Secondary Contact: Platform/SRE team
