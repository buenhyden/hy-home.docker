# Postmortem: [Short Incident Title]

> Use this template for `docs/<category>/operations/postmortems/YYYY-MM-DD-<slug>.md`.
>
> Repository-derived contract:
>
> - Use exactly one meaningful H1.
> - Use relative links only.
> - Remove every placeholder before saving.
> - Allowed postmortem status values: `Resolved | Archived`.
> - Keep the tone blameless and system-focused.
> - A postmortem should explain why the system allowed the incident, not just what command fixed it.
> - Keep all structural and narrative content in English.
> - Add exactly one `Overview (KR)` summary near the top. That overview summary alone should be written in Korean.

## Optional Frontmatter

```yaml
---
title: 'Postmortem: [Short Incident Title]'
status: 'Resolved'
date: 'YYYY-MM-DD'
incident_id: 'INC-YYYYMMDD-XXX'
severity: 'SEV-3'
owner: '[Repository Owner or Incident Commander]'
tags:
  - postmortem
  - operations
---
```

## H1 and Metadata

# Postmortem: [Short Incident Title]

**Overview (KR):** [Write a 1-2 sentence Korean summary of the incident, the systemic cause, and the prevention intent of this postmortem.]

## Required Core Sections

## 1. Incident Summary

| Field | Value |
| ----- | ----- |
| **Incident ID** | `INC-YYYYMMDD-XXX` |
| **Incident Date** | `YYYY-MM-DD` |
| **Analysis Date** | `YYYY-MM-DD` |
| **Duration** | [For example: `2h 15m`] |
| **Severity** | `[SEV-1 \| SEV-2 \| SEV-3]` |
| **Status** | `Resolved` |
| **Incident Document** | `[../incidents/YYYY-MM-DD-incident.md]` |

## 2. Impact

- **Affected Users or Systems**: [Describe who or what was affected]
- **Operational Impact**: [Describe the operational effect]
- **Business or Maintenance Impact**: [Describe the broader effect]

## 3. Timeline

| Time (UTC) | Event |
| ---------- | ----- |
| HH:MM | **[Detection]** [How the issue surfaced] |
| HH:MM | **[Investigation]** [What was learned] |
| HH:MM | **[Mitigation]** [What reduced impact] |
| HH:MM | **[Resolved]** [When the issue was considered fixed] |

## 4. Root Cause Analysis

### Primary Root Cause

[Describe the direct systemic reason the issue happened.]

### Contributing Factors

- [Contributing factor 1]
- [Contributing factor 2]

### Detection Gaps

- [Detection gap 1]
- [Detection gap 2]

## 5. What Went Well

- [Positive response point 1]
- [Positive response point 2]

## 6. What Went Wrong

- [Failure point 1]
- [Failure point 2]

## 7. Action Items

| Action | Owner | Priority | Ticket / Reference | Status |
| ------ | ----- | -------- | ------------------ | ------ |
| [Action item] | [Name] | High | [Link or `N/A`] | Pending |
| [Action item] | [Name] | Medium | [Link or `N/A`] | Pending |

## 8. Prevention and Verification

- [Prevention work or verification rule 1]
- [Prevention work or verification rule 2]

## 9. Related Links

- **Incident Document**: `[../incidents/YYYY-MM-DD-incident.md]`
- **Runbook**: `[../../runbooks/<related-runbook>.md]`
- **Related PRs or commits**: [Link or `N/A`]

## Optional Extended Section

## Lessons for Future Changes

- [Lesson 1]
- [Lesson 2]

> A strong postmortem ends with concrete prevention work, clear ownership, and a better system than the one that failed.
