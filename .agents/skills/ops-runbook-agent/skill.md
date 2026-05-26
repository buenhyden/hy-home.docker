---
name: ops-runbook-agent
description: >
  Author and maintain Stage 05 operations documents in docs/05.operations/.
  Covers guides (usage context), policies (controls and compliance), and
  runbooks (ordered procedures with evidence, rollback, and escalation).
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
in `docs/99.templates/operation.template.md`.

---

## Bootstrap

1. Read `AGENTS.md` and `docs/05.operations/README.md`.
2. Read `docs/99.templates/operation.template.md` — use the correct profile section.
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
| Operations template | `docs/99.templates/operation.template.md` |
| Existing documents | `docs/05.operations/<bucket>/<tier>/` |

## Outputs

- New or updated document at `docs/05.operations/<bucket>/<tier>/<topic>.md`
- Updated `docs/05.operations/<bucket>/<tier>/README.md` index entry

## Related Skills

- `task-breakdown-agent` — task evidence that may graduate to a runbook
- `execution-plan-agent` — plan/task traceability before runbook authoring
