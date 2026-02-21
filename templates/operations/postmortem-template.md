# Postmortem: [INC-YYYYMMDD-XXX]

*Target Directory: `runbooks/postmortems/YYYY-MM-DD-[incident-name].md`*
*Note: This document follows the blameless postmortem culture defined in the Risk Management & Incident Response Standards.*

## 1. Incident Summary

- **Incident ID**: [INC-YYYYMMDD-XXX]
- **Date/Time (UTC)**: [YYYY-MM-DD HH:MM]
- **Severity**: [SEV-1/SEV-2/SEV-3]
- **Status**: [Resolved]
- **Owner (Incident Commander)**: [Name/Team]
- **Related Incident Doc**: [Link to `runbooks/incidents/[INC-ID].md`]

## 2. Impact

- **Affected Users/Services**: [Describe the blast radius and which user segments or downstream services were affected.]
- **Duration**: [e.g., 2 hours 15 minutes]
- **Business Impact**: [Describe the business impact, e.g., lost revenue, degraded user experience, broken SLAs.]

## 3. Timeline (UTC)

*Log all critical phases from detection to resolution.*

| Time | Event |
| ---- | ----- |
| HH:MM | **[Detection]** [How was the issue first noticed? (e.g., Alert, User report)] |
| HH:MM | **[Investigation]** [Key diagnostic action or discovery] |
| HH:MM | **[Mitigation]** [Action taken to stop the bleeding] |
| HH:MM | **[Resolved]** [Service returned to normal healthy state] |

## 4. Root Cause Analysis (Five Whys)

*Conduct a blameless "Five Whys" analysis to identify the fundamental systemic failure.*

1. **Why did the service fail?** -> [e.g., The database connection pool was exhausted.]
2. **Why was the pool exhausted?** -> [e.g., A recent deploy introduced a query without a timeout.]
3. **Why did the query lack a timeout?** -> [e.g., The new ORM library defaults to infinite timeouts.]
4. **Why wasn't this caught in CI/CD?** -> [e.g., Load testing is only run weekly, not per-PR.]
5. **Why is load testing not run per-PR?** -> [e.g., The load test suite takes 45 minutes to execute.]

- **Primary Root Cause**: [The final systemic issue identified above.]
- **Detection Gaps**: [Why didn't monitoring catch this *before* it impacted users?]

## 5. What Went Well

- [e.g., Automated rollback for the API gateway worked flawlessly.]
- [Item 2]

## 6. What Went Wrong

- [e.g., It took 20 minutes to identify the offending database query because logs lacked correlation IDs.]
- [Item 2]

## 7. Action Items (Remediation)

*Action items must be specific, assigned to an owner, and tracked to completion.*

| Action (Corrective/Preventive) | Owner | Priority | Ticket/Issue Link | Status |
| ------------------------------ | ----- | -------- | ----------------- | ------ |
| [e.g., Enforce 5s timeout on ORM global config] | [Name] | High | [Link] | Pending |
| [e.g., Add correlation IDs to database query logs] | [Name] | Medium | [Link] | Pending |
| [e.g., Create a 5-minute smoke load test for per-PR CI] | [Name] | Medium | [Link] | Pending |

## 8. Follow-up Links & Artifacts

- **Incident Slack Channel**: [Link]
- **Grafana/Datadog Snapshot**: [Link to metrics during the incident window]
- **Related PRs (The fix)**: [Link]
- **Related Runbook Updates**: [Link to updated runbooks based on this event]
