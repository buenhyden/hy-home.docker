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
by the Stage 00 documentation protocol and its mapped template under
`docs/99.templates/`.

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

Pick exactly one bucket based on the primary purpose. The canonical bucket,
section, frontmatter, and language contracts are owned by
`docs/00.agent-governance/rules/documentation-protocol.md`,
`docs/00.agent-governance/rules/stage-authoring-matrix.md`, and the mapped
operations templates.

| Bucket | Purpose | When to use |
| ------ | ------- | ----------- |
| `guides/` | Usage context, onboarding, prerequisites, common checks | "How do I use / configure / verify this service?" |
| `policies/` | Controls, allowed/disallowed states, exceptions, review cadence | "What are the rules governing this service?" |
| `runbooks/` | Ordered procedures, evidence capture, rollback, escalation | "How do I recover / operate this service step-by-step?" |
| `incidents/YYYY/INC-###-<title>/` | Incident packet containing the live event record and postmortem | "Document an active or resolved incident and its root-cause analysis." |

A single document must serve one primary purpose. If usage AND procedure are needed, write a guide that links to a runbook via `## Runbook Handoff`.

---

## Required Section Profiles

Do not copy section profiles from this adapter. Load the mapped template before
writing or editing:

- Guide: `docs/99.templates/templates/operations/guide.template.md`
- Policy: `docs/99.templates/templates/operations/policy.template.md`
- Runbook: `docs/99.templates/templates/operations/runbook.template.md`
- Incident: `docs/99.templates/templates/operations/incident.template.md`
- Postmortem: `docs/99.templates/templates/operations/postmortem.template.md`

If a template and this adapter disagree, the template and Stage 00 governance
win. Update the owner document first, then adjust this adapter.

Incident packet routing invariant:
Filename: `postmortem.md`
Target folder: `incidents/YYYY/INC-###-<incident-title>/`.

---

## Working Rules

- Follow `docs/00.agent-governance/rules/documentation-protocol.md` for
  frontmatter, target comments, language boundary, heading profile, and
  related-document requirements.
- Follow `docs/99.templates/support/template-selection.md` for target path to
  template mapping.
- Never include secret values, tokens, or credential content.
- Calculate all links relative to the target document path, not the template path.
- After adding a new document, update the parent `<bucket>/<tier>/README.md` index.
- **No flat-file + same-name subfolder coexistence**: if a subdomain folder (e.g., `relational/`) already exists inside a tier directory, do NOT create a flat `relational.md` at the same level. Place new content inside the subfolder instead.
- **Cross-service workspace-level documents** (e.g., `developer-setup.md`, `harness-agent-first-engineering.md`, `release-management.md`) that span multiple tiers belong directly under `<bucket>/` root without a tier subfolder. Service-specific documents always go into `<bucket>/<tier>/`.
- **Naming convention for cross-service root files**: use the associated ADR/spec number prefix (`0012-`, `0026-`) when the document corresponds to a numbered architecture decision. Do not mix numbered and unnumbered naming for the same cross-service document across buckets (guides, policies, runbooks must use the same filename).
- **Incident packet placement**: place both files under `incidents/YYYY/INC-###-<incident-title>/`. The incident file is `INC-###-<incident-title>.md`; the postmortem file is `postmortem.md`. The Incident must link to its Postmortem via `## Postmortem Link`, and the Postmortem must reference the Incident via `## Incident Summary`.
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

For an incident packet at depth `incidents/YYYY/INC-###-<title>/`:

- Same-incident postmortem from the incident file: `./postmortem.md`
- Same-incident record from the postmortem file: `./INC-###-<title>.md`
- Direct runbook: `../../../runbooks/<topic>.md`
- Follow-up task: `../../../../04.execution/tasks/YYYY-MM-DD-<topic>.md`

---

## Inputs

| Input | Source |
| ----- | ------ |
| Service spec | `docs/03.specs/<tier>/spec.md` |
| Operations template | `docs/99.templates/templates/operations/guide.template.md`, `docs/99.templates/templates/operations/policy.template.md`, `docs/99.templates/templates/operations/runbook.template.md`, `docs/99.templates/templates/operations/incident.template.md`, or `docs/99.templates/templates/operations/postmortem.template.md` |
| Existing documents | `docs/05.operations/<bucket>/<tier>/` |

## Outputs

- New or updated document at `docs/05.operations/<bucket>/<tier>/<topic>.md`
- New or updated incident packet at `docs/05.operations/incidents/YYYY/INC-###-<title>/`
- Updated `docs/05.operations/<bucket>/<tier>/README.md` index entry

## Related Skills

- `task-breakdown-agent` — task evidence that may graduate to a runbook
- `execution-plan-agent` — plan/task traceability before runbook authoring
