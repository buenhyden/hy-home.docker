---
name: ops-runbook-agent
description: >
  Author and maintain Stage 05 operations documents in docs/05.operations/.
  Covers guides (usage context), policies (controls and compliance),
  runbooks (ordered procedures with evidence, rollback, and escalation),
  and incidents (event records and postmortems).
---

# ops-runbook-agent

Creates and updates operational documents in `docs/05.operations/`.

## Trigger Examples

- "Write a runbook for rotating Vault secrets"
- "Create a usage guide for the PostgreSQL tier"
- "Add an operations policy for Kafka message retention"
- "Update the Traefik TLS rotation runbook with new cert paths"

## Purpose

Produce operations documents (guide, policy, or runbook) that operators and AI
agents can follow. Every document must conform to the profile contract defined
by its mapped template in `docs/99.templates/`.

---

## Bootstrap

1. Read `AGENTS.md` and `docs/05.operations/README.md`.
2. Read the mapped operations template for the target bucket.
   - For guides: read `docs/99.templates/templates/operations/guide.template.md`.
   - For policies: read `docs/99.templates/templates/operations/policy.template.md`.
   - For runbooks: read `docs/99.templates/templates/operations/runbook.template.md`.
3. Check `docs/05.operations/<bucket>/<tier>/` for existing documents on the topic.
4. Read the relevant spec at `docs/03.specs/<tier>/spec.md` for service context.

---

## Document Type Selection

Pick exactly one bucket based on the primary purpose:

| Bucket | Purpose | When to use |
| ------ | ------- | ----------- |
| `guides/` | Usage context, onboarding, prerequisites, common checks | "How do I use / configure / verify this service?" |
| `policies/` | Controls, allowed/disallowed states, exceptions, review cadence | "What are the rules governing this service?" |
| `runbooks/` | Ordered procedures, evidence capture, rollback, escalation | "How do I recover / operate this service step-by-step?" |
| `incidents/YYYY/` | Event records (Incident) and post-incident analysis (Postmortem) | "Document an active or resolved incident or its root-cause analysis." |

A single document must serve one primary purpose. If usage AND procedure are needed, write a guide that links to a runbook via `## Runbook Handoff`.

---

## Required Section Profiles

### Guide Profile (`guides/**`)

```markdown
## Usage
### Overview (KR)
### Usage Type
### Target Audience
### Purpose
### Prerequisites
### Step-by-step Instructions
### Common Pitfalls

## Common Checks
- `<verification command>`
- `<expected result>`

## Runbook Handoff
반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은
[recovery runbook](<relative-path-to-runbook>)을 따른다.

## Related Documents
```

**Forbidden in guides**: `## Policy Scope`, `## Controls`, `## Review Cadence`,
`## When to Use`, `## Procedure`, `## Evidence`, `## Rollback or Recovery`, `## Escalation`.

### Policy Profile (`policies/**`)

```markdown
## Policy Scope
## Controls
- **Required**: …
- **Allowed**: …
- **Disallowed**: …
## Exceptions
## Verification
## Review Cadence
## Related Documents
```

**Forbidden in policies**: `## Usage`, `## Common Checks`, `## Runbook Handoff`,
`## When to Use`, `## Procedure`, `## Evidence`, `## Rollback or Recovery`, `## Escalation`.

### Runbook Profile (`runbooks/**`)

```markdown
## <Service> <Operation> Procedure
> Scope: <one-line scope>
### Overview (KR)
### Purpose
### Canonical References

## When to Use
(trigger conditions or symptoms)

## Procedure
### Checklist
- [ ] …
### Steps
1. …

### Verification Steps
### Observability and Evidence Sources
### Safe Rollback or Recovery Procedure
### Agent Operations (If Applicable)

## Evidence
## Rollback or Recovery
## Escalation
## Related Documents
```

**Forbidden in runbooks**: `## Usage`, `## Policy Scope`, `## Controls`,
`## Exceptions`, `## Review Cadence`.

### Incident Profile (`incidents/YYYY/`)

```markdown
## Overview (KR)
## Incident Metadata
## Agent Metadata (If Applicable)
## Incident Summary
## Impact
## Timeline
## Current Hypothesis / Response State
## Evidence
## Follow-up Actions
## Postmortem Link
## Related Documents
```

Filename: `YYYY-MM-DD-<incident-title>.md`
Target: `<!-- Target: docs/05.operations/incidents/YYYY/YYYY-MM-DD-<incident-title>.md -->`

**Forbidden in incidents**: `## Policy Scope`, `## Controls`, `## When to Use`, `## Procedure`, `## Rollback or Recovery`, `## Escalation`.

### Postmortem Profile (`incidents/YYYY/`)

```markdown
## Overview (KR)
## Incident Summary
## Agent Metadata (If Applicable)
## Impact
## Timeline
## Root Cause Analysis
## What Went Well
## What Went Wrong
## Action Items
## Prevention and Verification
## Required Documentation Feedback Loop
## Related Documents
```

Filename: `YYYY-MM-DD-<incident-title>-postmortem.md`
Target: `<!-- Target: docs/05.operations/incidents/YYYY/YYYY-MM-DD-<incident-title>-postmortem.md -->`

**Forbidden in postmortems**: `## Policy Scope`, `## Controls`, `## When to Use`, `## Procedure`, `## Common Checks`, `## Runbook Handoff`.

---

## Working Rules

- Filename: `docs/05.operations/<bucket>/<tier>/<topic>.md`
- Front matter: `status: active` (or `draft` while incomplete)
- Target comment at line 4: `<!-- Target: docs/05.operations/<bucket>/... -->`
- Heading levels: all required profile sections are h2 (`##`). Subsections use h3/h4.
- `## Common Checks` in guides must contain runnable verification commands.
- `## Runbook Handoff` must link to an existing runbook or state `N/A — no corresponding runbook`.
- `## When to Use` and `## Procedure` in runbooks must be h2, not h3 or h4.
- Never include secret values, tokens, or credential content.
- Calculate all links relative to the target document path, not the template path.
- After adding a new document, update the parent `<bucket>/<tier>/README.md` index.
- **No flat-file + same-name subfolder coexistence**: if a subdomain folder (e.g., `relational/`) already exists inside a tier directory, do NOT create a flat `relational.md` at the same level. Place new content inside the subfolder instead.
- **Cross-service workspace-level documents** (e.g., `developer-setup.md`, `harness-agent-first-engineering.md`, `release-management.md`) that span multiple tiers belong directly under `<bucket>/` root without a tier subfolder. Service-specific documents always go into `<bucket>/<tier>/`.
- **Naming convention for cross-service root files**: use the associated ADR/spec number prefix (`0012-`, `0026-`) when the document corresponds to a numbered architecture decision. Do not mix numbered and unnumbered naming for the same cross-service document across buckets (guides, policies, runbooks must use the same filename).
- **Incident and Postmortem placement**: place both files under `incidents/YYYY/` grouped by year. Filename must start with `YYYY-MM-DD-`. Incident and Postmortem files are always written as a pair; the Incident must link to its Postmortem via `## Postmortem Link`, and the Postmortem must reference the Incident via `## Incident Summary`.
- **Cross-tier policy files at `policies/` root**: use descriptive kebab-case filenames without a numeric tier prefix. Reserve the `NNNN-` prefix (four digits) only for files that correspond to a numbered ADR or spec.

---

## Path and Link Conventions

For a document at depth `guides/<tier>/<topic>.md`:

- Ops index: `../../README.md`
- Sibling policy: `../../policies/<tier>/<topic>.md`
- Sibling runbook: `../../runbooks/<tier>/<topic>.md`

For a document at depth `guides/<tier>/<subdomain>/<topic>.md`:

- Ops index: `../../../README.md`
- Sibling policy: `../../../policies/<tier>/<subdomain>/<topic>.md`
- Sibling runbook: `../../../runbooks/<tier>/<subdomain>/<topic>.md`

---

## Inputs

| Input | Source |
| ----- | ------ |
| Service spec | `docs/03.specs/<tier>/spec.md` |
| Operations template | `docs/99.templates/templates/operations/guide.template.md`, `docs/99.templates/templates/operations/policy.template.md`, or `docs/99.templates/templates/operations/runbook.template.md` |
| Existing documents | `docs/05.operations/<bucket>/<tier>/` |

## Outputs

- New or updated document at `docs/05.operations/<bucket>/<tier>/<topic>.md`
- Updated `docs/05.operations/<bucket>/<tier>/README.md` index entry

## Related Skills

- `task-breakdown-agent` — task evidence that may graduate to a runbook
- `execution-plan-agent` — plan/task traceability before runbook authoring
