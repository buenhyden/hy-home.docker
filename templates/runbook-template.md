# Runbook: [Service or Workflow Name]

> Use this template for `docs/runbooks/<topic>.md`.
>
> Repository-derived contract:
>
> - Use exactly one meaningful H1.
> - Use relative links only.
> - Remove every placeholder before saving.
> - Prefer direct, executable guidance over long background explanation.
> - Allowed runbook status values: `Active | Deprecated | Archived`.
> - Allowed scope values layer values: `common | architecture | backend | frontend | infra | mobile | product | qa | security`
> - If this runbook depends on canonical docs, link them explicitly near the top.
> - Keep all structural and narrative content in English.
> - Add exactly one `Overview (KR)` summary near the top. That overview summary alone should be written in Korean.
>
> Shape guidance:
>
> - Use the checklist form for repeatable review workflows such as active `docs/web` validation runbooks.
> - Use the extended troubleshooting form for operational investigation and recovery workflows such as `docs/content/runbooks/content-pipeline-verification.md`.

## Optional Frontmatter

```yaml
---
title: 'Runbook: [Service or Workflow Name]'
status: 'Active'
date: 'YYYY-MM-DD'
owner: '[Repository Owner or Responsible Maintainer]'
tags:
  - runbook
  - operation
layer: '<layer>'
---
```

## H1 and Metadata

# Runbook: [Service or Workflow Name]

- **Status**: [Active | Deprecated | Archived]
- **Owner**: [Repository Owner or Responsible Maintainer]
- **Last Reviewed**: [YYYY-MM-DD or `N/A`]
- **layer:** [common | architecture | backend | frontend | infra | mobile | product | qa | security]

**Overview (KR):** [Write a 1-2 sentence Korean summary of the operational problem this runbook addresses and when maintainers should use it.]

## Required Core Sections

## Purpose

[Describe what operational problem this runbook solves and when maintainers should use it.]

## Canonical References

- `[../adr/NNNN-decision.md]`
- `[../ard/system-or-domain-ard.md]`
- `[../prd/feature-or-system-prd.md]`
- `[../specs/YYYY-MM-DD-feature.md]`
- `[../plans/YYYY-MM-DD-feature.md]`

## Procedure or Checklist

Choose one of the two approved shapes below.

### Checklist form

## Review Checklist

- [ ] [Check 1]
- [ ] [Check 2]
- [ ] [Check 3]

### Procedure form

## Investigation Procedure

1. [Investigation step 1]
2. [Investigation step 2]
3. [Investigation step 3]

## Verification Steps

- [ ] [Verification command or manual check 1]
- [ ] [Verification command or manual check 2]
- [ ] [Verification command or manual check 3]

## Related Operational Documents

- **Incident examples**: `[../operations/incidents/YYYY-MM-DD-example-incident.md]`
- **Postmortem examples**: `[../operations/postmortems/YYYY-MM-DD-example-postmortem.md]`

## Optional Extended Sections

## When to Use This Runbook

- [Use case 1]
- [Use case 2]
- [Use case 3]

## Service or Workflow Overview

- **Description**: [Describe the workflow or service]
- **Owner Team**: [Responsible owner]
- **Primary Contact**: [Slack handle, local maintainer, or team]

## Dependencies

| Dependency   | Type                                     | Impact if Unavailable | Related Runbook        |
| ------------ | ---------------------------------------- | --------------------- | ---------------------- |
| [Dependency] | [Runtime / Build / Toolchain / External] | [Impact]              | `[./other-runbook.md]` |

## Observability and Evidence Sources

- **Primary signals**: [Logs, CI output, build errors, dashboards, browser errors]
- **Alert or failure trigger**: [Describe the trigger condition]
- **Evidence to capture**: [List the evidence to keep]

## Common Failure Scenarios

### Scenario A: [Failure Name]

- **Symptoms**: [What the maintainer sees]
- **Likely Cause**: [Most likely explanation]
- **Remediation**:
  - [ ] [Action 1]
  - [ ] [Action 2]

### Scenario B: [Failure Name]

- **Symptoms**: [What the maintainer sees]
- **Likely Cause**: [Most likely explanation]
- **Remediation**:
  - [ ] [Action 1]
  - [ ] [Action 2]

## Safe Rollback or Recovery Procedure

- [ ] **Step 1**: [Recovery step]
- [ ] **Step 2**: [Recovery step]
- [ ] **Step 3**: [Recovery step]

## Escalation Path

1. **Primary**: [Owner or on-call]
2. **Secondary**: [Lead or domain maintainer]
3. **Final escalation**: [Management, broader team, or N/A]
