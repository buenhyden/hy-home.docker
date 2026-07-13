---
layer: agentic
---

# SDLC Document Contract

## Overview

This contract explains the human authoring roles in the SDLC document family.
The machine-readable source of truth for artifact types, metadata fields,
parent constraints, lifecycle transitions, serialization order, templates, and
exceptions is
[`document-metadata-profiles.yaml`](./document-metadata-profiles.yaml). This
document does not reproduce that schema or validator behavior.

## Ownership Boundary

Choose a role by the question the document owns. Put a decision, contract, or
result in its earliest canonical owner, then link downstream consumers instead
of repeating the same content. Template shape is owned by
[`template-contract.md`](./template-contract.md), template selection by
[`template-selection.md`](./template-selection.md), and machine semantics by
the registry.

## Document Roles

| Role | Question owned | Create or update when | Durable handoff |
| --- | --- | --- | --- |
| PRD | What user problem, value, scope, requirements, and success criteria are approved? | Product intent or acceptance criteria materially change. | Architecture and specification work consumes the approved intent. |
| ARD | Which architecture boundaries, concerns, and quality attributes constrain the solution? | Stable requirements need an enduring architecture description. | ADRs and Specs consume the constraints. |
| ADR | Which significant architecture option was chosen, why, and with what consequences? | A material trade-off is decided or superseded. | Specs and plans follow the decision; later ADRs supersede rather than rewrite history. |
| Spec | What technical design, interfaces, contracts, and verification criteria will be implemented? | Requirements and architecture are sufficient to define implementable behavior. | Plans, tasks, implementation, and QA consume the contract. |
| Spec children | Which API, agent, data, service, test, or machine-readable sub-contract needs focused detail? | The parent Spec needs a separately reviewable concern. | The parent Spec owns the relationship and cross-links; children remain part of the Spec role. |
| Plan | In what sequence will the approved Spec be implemented, controlled, and verified? | Stable contracts are ready for execution planning. | Tasks consume sequencing, risks, gates, and completion criteria. |
| Task | What was attempted, changed, validated, reviewed, committed, deferred, or blocked? | Approved plan work begins or its disposition changes. | Reviewers and later operational/release work consume auditable execution evidence. |
| Guide | How should a person understand or routinely use a service or process? | User- or operator-facing usage context changes. | Policies and runbooks are linked for controls and ordered procedures. |
| Policy | Which operational states or controls are required or prohibited, and how are exceptions governed? | An approved operational control or exception changes. | Guides, runbooks, operators, and audits consume the control. |
| Runbook | What repeatable ordered steps, evidence, recovery, rollback, and escalation execute an operation? | An operation or recovery path needs an executable procedure. | Operators and incident responders execute it and record evidence elsewhere. |
| Incident | What is happening, when, with what impact, actions, current state, and handoffs? | A qualifying event begins or its live state changes. | The stabilized record feeds review and a Postmortem when required. |
| Postmortem | Why did the incident occur, what was learned, and which owned actions prevent recurrence? | The incident is stable enough for reviewed learning. | Requirements, architecture, Specs, plans, policies, and runbooks receive approved follow-up. |
| Release | What real release event occurred, which immutable artifacts and approvals support it, and what was the outcome? | A release has actual artifact, validation, approval, rollout or rollback, and outcome evidence. | Operators, users, audits, and later releases consume the event record. |

## Operations Evidence Semantics

A Runbook is executable only when its body makes prerequisites, safety
conditions, ordered steps, expected results, and a verification record
explicit. That record names the environment, the command or procedure used,
its result, and where the evidence is retained. An automation handoff names
the candidate or invocation while preserving the boundary where human or
operator judgment is required; rollback or recovery remains the procedure's
separate recovery boundary.

An Incident body owns the event severity, incident leadership, current
response state, response actions, mitigation, resolution, and handoff. These
facts remain body evidence and do not create a second lifecycle-state key in
frontmatter.

A reviewed Postmortem keeps each follow-up as an owned, prioritized action with
a stable tracking identity and verification ownership. A Release binds its
immutable release identity, version or tag, commit, immutable artifact
evidence, validation, approvals, compatibility, rollout or rollback, outcome,
and known issues into one event record.

## Lifecycle and Relation Semantics

- An Incident may start as a root record when no verified Runbook parent exists;
  link a Runbook parent only when that direct relationship is evidenced. A
  Postmortem remains a strict child of its paired Incident, and a Release
  remains a strict child of real Spec, Plan, or Task evidence. Do not invent a
  parent merely to populate frontmatter.
- Use the target profile's lifecycle state honestly. A template source's draft
  state is not automatic evidence that a copied target is draft.
- Forward, terminal, and exceptional transitions are interpreted only by the
  registry and validator. Reverse transitions require scoped Stage 04 approval
  evidence; prose in a document cannot authorize one.
- `parent_ids` names direct upstream artifacts. It is not a complete Related
  Documents list and does not replace human-readable traceability links.
- Direct parents have set-like semantic meaning. Their serialized order is
  deterministic presentation—profile precedence followed by stable artifact
  identity—not priority, approval rank, chronology, or dependency strength.
- Supersession preserves direction and evidence. Do not rewrite an ADR,
  incident, task, or release record merely to make history resemble current
  guidance.

## Release and Deployment Boundary

A Release document is evidence for an executed release event. A changelog,
readiness checklist, pushed tag, successful CI build, or template proves only
its own narrower fact and cannot manufacture a Release record. Deployment
runtime, promotion environments, protection rules, secrets, and rollback
execution remain in a separately approved technical and operational chain.

## Authoring Workflow

1. Select the role by its owned question and canonical target path.
2. Load the mapped copyable template and the registry profile.
3. Resolve direct parents without inferring semantic priority from YAML order.
4. Replace every template placeholder with artifact-specific content.
5. Link upstream and downstream owners without copying their contracts.
6. Record validation, deviations, protected-surface evidence, and review in the
   active Stage 04 task.

## Iterative Feedback

The forward route is PRD to architecture and decisions, then Spec and focused
contracts, Plan, Task evidence, Release evidence, and Operations. It is a set
of review gates, not a one-way waterfall. Evidence can route work back to the
earliest owner that must change: an Incident or Postmortem can create a
requirement; an operational finding can supersede an ADR; validation can revise
a Spec or test contract; repeated procedure failure can revise Policy or
Runbook; and a Release outcome can create a follow-up Plan and Task.

Keep stable identities and links in both directions. Do not copy a requirement,
decision, or result into a second artifact as competing truth.

## Related Documents

- [document metadata profiles](./document-metadata-profiles.yaml)
- [common document contract](./common-document-contract.md)
- [README profile contract](./readme-profile-contract.md)
- [template contract](./template-contract.md)
- [template selection](./template-selection.md)
- [lifecycle status](./lifecycle-status.md)
