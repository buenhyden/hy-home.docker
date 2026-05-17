---
status: draft
---
<!--
# Operation Template

Use this template for one `docs/05.operations` leaf document.

## Target Paths

- Direct target: `docs/05.operations/<bucket>/<topic>.md`
- Domain target: `docs/05.operations/<bucket>/<domain>/<topic>.md`
- Nested target: `docs/05.operations/<bucket>/<domain>/<subdomain>/<topic>.md`

## Purpose Selection

Pick exactly one profile and delete the other profile sections before committing.

- Guide: use `guides/` for usage context, prerequisites, onboarding, common checks, and handoff links.
- Policy: use `policies/` for controls, allowed/disallowed states, exceptions, verification, and review cadence.
- Runbook: use `runbooks/` for ordered procedures, evidence capture, rollback/recovery, and escalation.

Do not use this template for incident timelines or postmortems. Use `incident.template.md` or
`postmortem.template.md` under `docs/05.operations/incidents/`.

## Target-relative Link Rules

Calculate links from the copied target path, not from `docs/99.templates/`.

Direct target, for example `docs/05.operations/guides/<topic>.md`:

- Docs root: `../../`
- Sibling policy: `../policies/<topic>.md`
- Sibling runbook: `../runbooks/<topic>.md`
- Incident record: `../incidents/YYYY/YYYY-MM-DD-<incident-title>.md`

Domain target, for example `docs/05.operations/guides/<domain>/<topic>.md`:

- Docs root: `../../../`
- Sibling policy: `../../policies/<domain>/<topic>.md`
- Sibling runbook: `../../runbooks/<domain>/<topic>.md`
- Incident record: `../../incidents/YYYY/YYYY-MM-DD-<incident-title>.md`

Nested target, for example `docs/05.operations/guides/<domain>/<subdomain>/<topic>.md`:

- Docs root: `../../../../`
- Sibling policy: `../../../policies/<domain>/<subdomain>/<topic>.md`
- Sibling runbook: `../../../runbooks/<domain>/<subdomain>/<topic>.md`
- Incident record: `../../../incidents/YYYY/YYYY-MM-DD-<incident-title>.md`
-->

# {Topic Name} {Guide | Policy | Runbook}

> {One-line operational purpose.}

## Overview

{Explain what this document covers and when someone should use it.}

---

## Guide Profile

Keep this profile only for `docs/05.operations/guides/**`.

### Usage

{Describe the normal usage context, prerequisites, and expected operating state.}

### Common Checks

- {Check or command}
- {Expected result}

### Runbook Handoff

For repeatable procedures, recovery, rollback, or escalation, link to the matching runbook.

---

## Policy Profile

Keep this profile only for `docs/05.operations/policies/**`.

### Policy Scope

{List systems, configs, agents, environments, or workflows governed by this policy.}

### Controls

- **Required**: {Required state}
- **Allowed**: {Allowed variation}
- **Disallowed**: {Forbidden state}

### Exceptions

{State who may approve exceptions and what evidence must be recorded.}

### Verification

{State the checks that prove compliance.}

### Review Cadence

{Monthly, quarterly, per release, or on material change.}

---

## Runbook Profile

Keep this profile only for `docs/05.operations/runbooks/**`.

### When to Use

{Trigger conditions, symptoms, or scheduled operation criteria.}

### Procedure

1. {Step}
2. {Expected result}
3. {Failure handling}

### Evidence

- {Log, command output, dashboard, ticket, or trace to capture}

### Rollback or Recovery

{Safe rollback, fallback, or restoration steps.}

### Escalation

{Escalation owner, threshold, and required context.}

---

## Related Documents

Use only links that apply to the copied target path.

- [Operations index]({target-relative-link})
- [Usage guide]({target-relative-link})
- [Operations policy]({target-relative-link})
- [Recovery runbook]({target-relative-link})
- [Incident record]({target-relative-link})
