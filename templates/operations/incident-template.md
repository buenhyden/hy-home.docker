# Active Incident: [INC-YYYYMMDD-XXX]

*Target Directory: `runbooks/incidents/`*
*Note: This document tracks the real-time response to a production event.*

**Postmortem Link**: [To be linked here once `runbooks/postmortems/...` is created]

## 1. Incident Metadata

| Field          | Value                                                         |
| -------------- | ------------------------------------------------------------- |
| Incident ID    | [INC-YYYYMMDD-XXX]                                            |
| Severity       | [SEV-1 / SEV-2 / SEV-3] (See legend below)                    |
| Status         | [Investigating / Identified / Mitigating / Resolved / Closed] |
| Detection Time | [YYYY-MM-DD HH:MM UTC]                                        |
| Primary Service| [Service Name]                                                |
| Affected Deps  | [Upstream/Downstream systems experiencing impact]             |
| Dashboard Link | [URL to primary monitoring dashboard]                         |
| Runbook Link   | [URL to relevant service runbook in `runbooks/`]              |

> **Severity Legend**:
>
> - **SEV-1 (Critical)**: Total loss of core service or data corruption affecting many users.
> - **SEV-2 (High)**: Significant degradation of a core feature; no workaround exists.
> - **SEV-3 (Moderate)**: Partial degradation or non-critical feature broken; workaround exists.

## 2. Response Roster

| Role                     | Name/Team | Slack/Contact |
| ------------------------ | --------- | ------------- |
| Incident Commander (IC)  | [Name]    | [@handle]     |
| Communications Lead (CL) | [Name]    | [@handle]     |
| Operations Lead (OL)     | [Name]    | [@handle]     |

## 3. Communication Cadence

*Updates must be posted on the following interval: [every 15m / 30m / 60m]*

### Latest Status Update

**Time**: [HH:MM]

- **Current Impact**: [Description of what users are experiencing right now]
- **Current Hypothesis**: [What we think is causing the issue]
- **Mitigation Actions**: [What we are currently doing to stop the bleeding]
- **Next Update**: [HH:MM]

## 4. Timeline

*Log all actions, discoveries, and state changes here during the incident. Include UTC times.*

| Time (UTC) | Actor  | Detail / Event               |
| ---------- | ------ | ---------------------------- |
| HH:MM      | -      | [Detection] Incident Declared|
| HH:MM      | [Name] | [Action] Investigating logs at [link] |
| HH:MM      | [Name] | [Mitigation] Restarting pods in deployment xyz |
| HH:MM      | [Name] | [Status update] 500 errors dropping, but not zero |

## 5. End State & Handoff

- **Mitigation Complete Time**: [HH:MM UTC]
- **Resolution Verified Time**: [HH:MM UTC]

### Follow-up Actions (Action Items)

*List any temporary mitigations that need permanent fixes, or cleanup tasks required immediately after the incident.*

- [ ] [e.g., Re-enable the rate limit rule we temporarily bypassed] - **Owner**: [Name]
- [ ] [e.g., Create Jira ticket for database index missing] - **Owner**: [Name]

- **Postmortem Required?**: [Yes/No]

*If yes, DevOps Agent or Human must generate `runbooks/postmortems/YYYY-MM-DD-[incident-name].md` using the postmortem template and link it at the top of this file.*
