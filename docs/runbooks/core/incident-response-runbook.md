# Incident Response Framework Guide

_Target Directory: `runbooks/core/incident-response-runbook.md`_
_Note: Global protocol for managing system outages and service degradations._

---

## 1. Service Overview & Ownership

- **Description**: The coordination protocol for responding to infrastructure incidents.
- **Owner Team**: SRE / Ops
- **Primary Contact**: #incident-response (Slack)

## 2. Dependencies

| Dependency | Type | Impact if Down | Link to Runbook |
| ---------- | ---- | -------------- | --------------- |
| Slack / Comms | Internal | Zero coordination | N/A |
| Grafana / Loki | Observability | Blind response | [Monitoring Runbook](monitoring-runbook.md) |

## 3. Observability & Dashboards

- **Incident Central**: [System health dashboard](https://grafana.${DEFAULT_URL}/d/global-health)
- **Live Logs**: [Loki Explore view](https://grafana.${DEFAULT_URL}/explore)

## 4. Operational Scenarios

### Scenario A: SEV-1 (Core Outage)

- **Symptoms**: Dashboard shows 100% error rate on Gateway.
- **Remediation Action**:
  1. [ ] Declare Incident in Slack within 5 minutes.
  2. [ ] Assign IC (Incident Commander).
  3. [ ] Set update cadence to 15 minutes.
- **Expected Outcome**: Stakeholders informed; mitigation started.

### Scenario B: SEV-2 (Feature Degradation)

- **Symptoms**: Elevated 5xx errors; partial database lag.
- **Remediation Action**:
  1. [ ] Declare SEV-2.
  2. [ ] Set update cadence to 30 minutes.
- **Expected Outcome**: Engineers investigating root cause within 1 hour.

## 5. Safe Rollback Procedure

- [ ] **Method 1**: Git Revert to last stable commit and CI/CD redeploy.
- [ ] **Method 2**: Docker sidecar roll-back (manual image tag update in `.env`).

## 6. Data Safety Notes

- **Auditability**: Never delete logs during an incident.
- **Shadow Systems**: Avoid spinning up un-monitored "fix" containers.

## 7. Escalation Path

1. **On-Call**: SRE Rotation
2. **Secondary**: Engineering Lead (@handle)
3. **Emergency**: CTO (@handle)

## 8. Verification Steps (Post-Fix)

- [ ] Confirm error rates dropped to baseline.
- [ ] Create Postmortem document in `operations/postmortems/`.
- [ ] Close incident record in `operations/incidents/`.
