---
status: draft
---
<!--
Target: docs/05.operations/<bucket>/<topic>.md
Target: docs/05.operations/<bucket>/<domain>/<topic>.md
Target: docs/05.operations/<bucket>/<domain>/<subdomain>/<topic>.md

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

## Purpose Profile Contract

The copied target must keep the profile headings for its bucket and must not keep headings from the other profiles.

- `guides/**` must include `## Usage` and must not include policy or runbook profile headings such as `## Policy Scope`, `## Controls`, `## Review Cadence`, `## When to Use`, or `## Procedure`.
- `policies/**` must include `## Policy Scope`, `## Controls`, `## Verification`, and `## Review Cadence`; it must not include guide/runbook profile headings such as `## Usage`, `## Runbook Handoff`, `## When to Use`, or `## Procedure`.
- `runbooks/**` must include `## When to Use`, `## Procedure`, `## Evidence`, `## Rollback or Recovery`, and `## Escalation`; it must not include guide/policy profile headings such as `## Usage`, `## Policy Scope`, `## Controls`, `## Exceptions`, or `## Review Cadence`.
- `runbooks/**` must keep rollback/recovery factual-only. If no verified rollback or recovery steps exist, write a safe `N/A` reason and route readers to `## Escalation`; do not invent unverified recovery commands.

Do not use this template for incident timelines or postmortems. Use `incident.template.md` or
`postmortem.template.md` under `docs/05.operations/incidents/`.

When copying this template, keep only the target path comment that matches the
final document path and remove every unused profile and placeholder link.

## Target-relative Link Rules

Calculate links from the copied target path, not from `docs/99.templates/`.
Use Markdown links for repo-local documents. Do not use absolute filesystem paths,
`file://` URIs, or links calculated from this template source path.

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

## Overview (KR)

{Explain what this document covers and when someone should use it.}

---

<!-- GUIDE PROFILE: keep this profile only for `docs/05.operations/guides/**`; delete policy and runbook profile sections. -->

## Usage

{Describe the normal usage context, prerequisites, and expected operating state.}

## Common Checks

- {Check or command}
- {Expected result}

## Runbook Handoff

For repeatable procedures, recovery, rollback, or escalation, link to the matching runbook.

---

<!-- POLICY PROFILE: keep this profile only for `docs/05.operations/policies/**`; delete guide and runbook profile sections. -->

## Policy Scope

{List systems, configs, agents, environments, or workflows governed by this policy.}

## Controls

- **Required**: {Required state}
- **Allowed**: {Allowed variation}
- **Disallowed**: {Forbidden state}

## Exceptions

{State who may approve exceptions and what evidence must be recorded.}

## Verification

{State the checks that prove compliance.}

## Review Cadence

{Monthly, quarterly, per release, or on material change.}

---

<!-- RUNBOOK PROFILE: keep this profile only for `docs/05.operations/runbooks/**`; delete guide and policy profile sections. -->

## When to Use

{Trigger conditions, symptoms, or scheduled operation criteria.}

## Procedure

1. {Step}
2. {Expected result}
3. {Failure handling}

## Evidence

- {Log, command output, dashboard, ticket, or trace to capture}

## Rollback or Recovery

{Verified safe rollback, fallback, or restoration steps. If none are verified, write `N/A - no verified rollback or recovery procedure is documented yet` and send readers to `## Escalation` with the evidence they must provide.}

## Escalation

{Escalation owner, threshold, and required context.}

---

## Related Documents

Use only links that apply to the copied target path. Delete unused examples before committing.

Direct target examples:

- [Operations index](../README.md)
- [Usage guide](../guides/<topic>.md)
- [Operations policy](../policies/<topic>.md)
- [Recovery runbook](../runbooks/<topic>.md)

Domain target examples:

- [Operations index](../../README.md)
- [Usage guide](../../guides/<domain>/<topic>.md)
- [Operations policy](../../policies/<domain>/<topic>.md)
- [Recovery runbook](../../runbooks/<domain>/<topic>.md)

Nested target examples:

- [Operations index](../../../README.md)
- [Usage guide](../../../guides/<domain>/<subdomain>/<topic>.md)
- [Operations policy](../../../policies/<domain>/<subdomain>/<topic>.md)
- [Recovery runbook](../../../runbooks/<domain>/<subdomain>/<topic>.md)
