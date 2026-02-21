# Service Runbook: [Service/Component Name]

*Target Directory: `runbooks/services/<service-name>.md`*
*Note: This is strictly for operational context. It MUST follow the deterministic rules in `0381-runbooks-oncall.md`.*

---

## 1. Service Overview & Ownership

- **Description**: [Briefly describe the service, its core function, and its business criticality.]
- **Owner Team**: [Name of the team responsible for this service]
- **Primary Contact**: [Slack channel, email, or paging handle]

## 2. Dependencies

| Dependency | Type | Impact if Down | Link to Runbook |
| ---------- | ---- | -------------- | --------------- |
| [e.g., PostgreSQL] | Database | Complete service failure | [Link] |
| [e.g., Analytics API] | External | Non-critical feature degradation | [Link] |

## 3. Observability & Dashboards

- **Primary Dashboard**: [Link to Grafana/Datadog dashboard showing RED metrics (Rate, Errors, Duration)]
- **SLOs/SLIs**: [e.g., Target 99.9% uptime, p95 latency < 200ms]
- **Alert Definitions**: [Link to where alerts are defined for this service]

## 4. Alerts & Common Failures

*Provide deterministic, checklist-based remediation steps for known alerts and common failures.*

### Scenario A: [e.g., High Latency Alert / CPU Saturation]

- **Symptoms**: [What does the alert say? What metrics are spiking?]
- **Investigation Steps**:
  1. [Check metric X on dashboard Y]
  2. [Run query Z to check database load]
- **Remediation Action**:
  - [ ] Action 1: [e.g., Scale up deployment] `kubectl scale deployment <name> --replicas=5`
  - [ ] Action 2: [Expected outcome of action 1]

### Scenario B: [e.g., Database Connection Pool Exhausted]

[Add specific checklists and expected outcomes here.]

## 5. Safe Rollback Procedure

*Crucial: What do we do if a deployment or config change fails? Provide deterministic rollback commands.*

- [ ] **Step 1**: [e.g., Identify the previous stable Git SHA]
- [ ] **Step 2**: [e.g., Execute rollback via ArgoCD/GitHub Actions / CLI command]
- [ ] **Step 3**: [Expected outcome: Service restores to previous image version]

## 6. Data Safety Notes (If Stateful)

- [Warning about data loss, corruption risks during restarts, or manual data migration constraints.]

## 7. Escalation Path

*If the primary on-call cannot resolve the issue, follow this path.*

1. **Primary On-Call**: [PagerDuty Schedule / Team Slack]
2. **Secondary Escalation**: [Secondary Pager / Tech Lead]
3. **Management Escalation (SEV-1)**: [Engineering Manager / VP of Eng]

## 8. Verification Steps (Post-Fix)

*How do we know the steps succeeded and the service is healthy again?*

- [ ] [e.g., Error rate on dashboard drops below 1%]
- [ ] [e.g., Synthetic monitoring (DataDog) reports 200 OK]
- [ ] [e.g., Check logs for successful database reconnection message]
