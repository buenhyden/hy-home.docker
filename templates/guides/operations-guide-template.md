# Operations Blueprint (OPERATIONS.md)

*Target Location: `OPERATIONS.md` (Project Root)*
*Description: This document defines the project's operational baseline, including environments, deployment strategies, observability, and continuity plans, as per the `0301-operations-blueprint-standard.md` rule.*

---

## 1. Environment Hierarchy & Promotion Rules

Define the tiers of environments and the strict rules for promoting code between them.

| Environment | Purpose | Promotion Gate / Rule |
| ----------- | ------- | --------------------- |
| **Development** | Sandbox for active feature testing | Auto-deploy from `develop` branch or PRs |
| **Staging** | Pre-production validation matching prod | Manual approval from TL / QA sign-off |
| **Production** | Live serving environment | Manual Gate after staging validation |

## 2. Deployment Strategy

Define the default deployment method to ensure safe releases without silent production changes.

- **Default Strategy**: [e.g., Rolling Update / Blue-Green / Canary]
- **When to use Canary**: [e.g., High-risk feature flags, core routing changes]
- **Rollback Policy**: [e.g., Automated rollback if error rate spikes > 2% within 5 minutes of deploy]
- **Pre-Deploy Checklist**:
  - [ ] Ops/Observability section in feature Spec is approved.
  - [ ] Rollback plan is documented in the specific runbook.

## 3. Observability Baseline

Define how the application state will be monitored (Logs, Metrics, Alerts).

### Logging

- **Format**: [e.g., JSON structured logging]
- **Required Fields**: `trace_id`, `user_id`, `severity`, `event_type`
- **Storage/Aggregation**: [e.g., Datadog, ELK Stack, AWS CloudWatch]

### Monitoring & Metrics (RED)

- **Rate**: [e.g., HTTP Requests per second]
- **Errors**: [e.g., HTTP 5xx rate]
- **Duration**: [e.g., p95 and p99 Latency]
- **Dashboards Location**: [Link to primary dashboards]

### Alerts & Routing

| Alert Condition | Severity | Routing Destination |
| --------------- | -------- | ------------------- |
| API 5xx > 5% for 5m | SEV-1 | PagerDuty (Primary On-Call) |
| Latency p95 > 2s | SEV-2 | Slack `#ops-alerts` |

## 4. Continuity Plan (Backups & Disaster Recovery)

Define targets for data safety and recovery speed.

- **RTO (Recovery Time Objective)**: [e.g., < 4 hours]
- **RPO (Recovery Point Objective)**: [e.g., < 1 hour of data loss]
- **Backup Strategy**:
  - **Database**: [e.g., Hourly snapshots, retained for 30 days]
  - **Storage (S3/GCS)**: [e.g., Cross-region replication enabled]
- **Disaster Recovery Drill Schedule**: [e.g., Bi-annually]

## 5. Security & Infrastructure Cost

- **Secret Management**: [e.g., AWS Secrets Manager, HashiCorp Vault]
- **Cost Monitoring**: [e.g., Billing alerts set to $X/month, resources tagged with `env:prod`]

## 6. Incident Response & Runbooks

- **Incident Runbooks Location**: `runbooks/incidents/`
- **Service Runbooks Location**: `runbooks/services/`
- **Postmortems Location**: `runbooks/postmortems/`
