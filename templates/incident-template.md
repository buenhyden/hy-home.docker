# Incident: INC-YYYYMMDD-XXX / [Short Incident Title]

> Use this template for `docs/operations/incidents/YYYY-MM-DD-<slug>.md`.
>
> Repository-derived contract:
>
> - Use exactly one meaningful H1.
> - Use relative links only.
> - Remove every placeholder before saving.
> - Allowed incident status values: `Investigating | Identified | Mitigating | Monitoring | Resolved | Closed`.
> - Allowed scope values layer values: `common | architecture | backend | frontend | infra | mobile | product | qa | security`
> - Prefer UTC timestamps, and include local time only if it helps the maintainer.
> - This document tracks live or recently resolved response work, not blameless analysis.
> - Keep all structural and narrative content in English.
> - Add exactly one `Overview (KR)` summary near the top. That overview summary alone should be written in Korean.
>
> Shape guidance:
>
> - The repository currently uses both a compact active-incident form and a more detailed response-ledger form.
> - The core sections below are mandatory in both cases.
> - Add the optional response-roster and communication sections when the incident is long-running, multi-step, or handoff-heavy.

## Optional Frontmatter

```yaml
---
title: 'Incident: INC-YYYYMMDD-XXX / [Short Incident Title]'
status: 'Investigating'
date: 'YYYY-MM-DD'
incident_id: 'INC-YYYYMMDD-XXX'
severity: 'SEV-3'
owner: '[Incident Commander or Responsible Maintainer]'
tags:
  - incident
  - operation
layer: '<layer>'
---
```

## H1 and Metadata

# Active Incident: INC-YYYYMMDD-XXX / [Short Incident Title]

**Postmortem Link**: [N/A or `../postmortems/YYYY-MM-DD-incident-postmortem.md`]

**Overview (KR):** [Write a 1-2 sentence Korean summary of the incident impact, the main blocker, and the current response state.]

## Required Core Sections

## Incident Metadata

| Field                     | Value                                                  |
| ------------------------- | ------------------------------------------------------ | ---------- | ---------- | ---------- | -------- | -------- |
| **Incident ID**           | `INC-YYYYMMDD-XXX`                                     |
| **Severity**              | `[SEV-1                                                | SEV-2      | SEV-3]`    |
| **Status**                | `[Investigating                                        | Identified | Mitigating | Monitoring | Resolved | Closed]` |
| **Detection Time**        | `YYYY-MM-DD HH:MM UTC`                                 |
| **Primary Service**       | [Affected service or workflow]                         |
| **Affected Dependencies** | [Key dependency or `N/A`]                              |
| **Evidence Source**       | [CI log, local command output, dashboard, user report] |
| **Runbook Link**          | `[../../runbooks/<related-runbook>.md]`                |
| **layer:** |  [common \| architecture \| backend \| frontend \| infra \| mobile \| product \| qa \| security]|

## Incident Summary

[Summarize the operational problem in one short paragraph.]

## Impact

- [Impact statement 1]
- [Impact statement 2]

## Timeline

| Time (UTC) | Actor  | Detail                                             |
| ---------- | ------ | -------------------------------------------------- |
| HH:MM      | [Name] | **[Detection]** [What was observed]                |
| HH:MM      | [Name] | **[Investigation]** [What was learned]             |
| HH:MM      | [Name] | **[Mitigation]** [What action reduced impact]      |
| HH:MM      | [Name] | **[Verification]** [What proved the current state] |

## Detection and Response or Root Cause and Resolution

Use the heading that best matches the current state of the incident.

- **Current Hypothesis**: [Best current explanation]
- **Mitigation Actions**: [Actions already taken]
- **Resolution State**: [Resolved | Monitoring | Open]

## Evidence

- [Evidence summary 1]
- [Evidence summary 2]
- [Evidence summary 3]

## Follow-up Actions

- [ ] [Follow-up action] - **Owner**: [Name]
- [ ] [Follow-up action] - **Owner**: [Name]

- **Postmortem Required?**: [Yes | No]

## Optional Extended Sections

## Response Roster

| Role                    | Name   | Contact                   |
| ----------------------- | ------ | ------------------------- |
| **Incident Commander**  | [Name] | [Handle or local session] |
| **Communications Lead** | [Name] | [Handle or local session] |
| **Operations Lead**     | [Name] | [Handle or local session] |

## Latest Status Update

- **Current Impact**: [Describe the current operational impact]
- **Current Hypothesis**: [Describe the best current explanation]
- **Mitigation Actions**: [Describe current mitigation work]
- **Next Update**: [Time or `None` if resolved]

## Recovery and Verification

- [Recovery step or verification outcome 1]
- [Recovery step or verification outcome 2]

## Communication Record

- [Time] [Audience] [Update]

## End State & Handoff

- **Mitigation Complete**: [HH:MM UTC or `No`]
- **Resolution Verified**: [Yes | No | Partially]

> If this incident is SEV-1 or SEV-2, or if it reveals a systemic gap, create a postmortem and link it at the top of this file.
