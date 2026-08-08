---
status: draft
artifact_id: reference:agentic-engineering-research:sdlc-document-roles
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-08
review_cycle: on-source-change
---

# Reference: SDLC Document Roles

## Overview

The workspace uses twelve distinct lifecycle document roles. Each role owns a
different question, trigger, handoff, and evidence boundary. Similar subject
matter does not make the roles interchangeable: a Plan cannot report executed
results, a Guide cannot impose Policy, an Incident cannot contain reviewed
Postmortem causality, and a Release cannot stand in for deployment/runtime
proof.

This reference reflects the current Stage 00 and Stage 99 contracts at Task 5
baseline `0445a17860ac27f6bf5ff1f9a8ffcde32bc4f2ee`. `ARD` is explicitly
repository-local coinage rather than an industry-standard document name.

## Purpose

Satisfy REQ-10 through REQ-21 with one separate row for PRD, ARD, ADR,
Spec/child contract, Plan, Task, Guide, Incident, Postmortem, Policy, Release,
and Runbook. Make ownership and forbidden substitutions explicit so authors
select a role by the question it owns rather than by a convenient template.

## Repository Role

This Stage 90 reference is advisory. Exact machine fields, allowed relations,
lifecycle transitions, headings, and template mappings remain in Stage 99;
current policy remains in Stage 00 or Stage 05; actual work/results remain in
the active Spec/Plan/Task/Operations chain. This document neither creates a
role nor authorizes a target document.

## Scope

### In scope

- Human purpose, owned question, trigger, owner, consumer, system/path,
  template, lifecycle, relations, and forbidden substitutions for every role.
- External primary-source comparisons for ADR, incident, postmortem, release,
  requirements, architecture, standards, and version signals.
- Current unexercised role boundaries for Incident, Postmortem, and Release.

### Out of scope

- Restating the executable metadata registry or template heading arrays.
- Creating an event record without real event evidence.
- Treating external terminology as adopted repository policy.
- Changing owners, templates, profiles, stages, or runtime systems.

## Definitions / Facts

### Complete role contract

| Role | Purpose | Question owned | Trigger | Owner | Consumer | Stage / path | Template | Lifecycle | Relations | Forbidden substitutions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRD | Capture approved product intent, value, scope, requirements, and acceptance. | What problem, users, value, constraints, requirements, and success criteria should be addressed? | New or materially changed stakeholder intent or acceptance criteria. | Product Manager / human stakeholder owner. | ARD/ADR authors, Spec owners, reviewers. | Stage 01: `docs/01.requirements/NNN-feature-or-system.md`. | `docs/99.templates/templates/sdlc/prd.template.md`. | `draft -> active -> completed` or `active/completed -> superseded`; current path until reviewed archive migration. | Root role; downstream ARD, ADR, and Spec links. | Not an implementation design, architecture decision, task list, test result, or policy. |
| ARD | Preserve enduring architecture boundaries, concerns, views, constraints, and quality attributes. | Which architecture constraints and quality attributes shape the solution? | Approved requirements need architecture framing broader than one decision. | System Architect. | ADR and Spec authors, architecture reviewers. | Stage 02: `docs/02.architecture/requirements/NNNN-short-title.md`. | `docs/99.templates/templates/sdlc/ard.template.md`. | Same active-family lifecycle; typed parent must be PRD. | PRD parent; ADRs and Specs consume it. **ARD is local coinage**, not a recognized external standard document name. | Not a single decision, full technical Spec, implementation Plan, or claim of ISO 42010 conformance. |
| ADR | Preserve one architecturally significant decision, alternatives, rationale, status, and consequences. | Which significant option was chosen, why, and what consequences follow? | A material trade-off is decided, reversed, deprecated, or superseded. | System Architect / accountable decision owner. | Spec/Plan authors, implementers, future decision makers. | Stage 02: `docs/02.architecture/decisions/NNNN-short-title.md`. | `docs/99.templates/templates/sdlc/adr.template.md`. | Preserve history; create/supersede rather than rewrite the old decision into current truth. | PRD or ARD parent; later ADR may supersede it; Specs consume applicable decisions. | Not an ARD, design catalog, meeting minute, implementation Plan, or mutable latest-state summary. |
| Spec / child contract | Define implementable behavior, interfaces, data, failure modes, guardrails, and verification; isolate focused subcontracts when separately reviewable. | What exactly will be built and verified, and which API/agent/data/service/test or machine contract governs a focused concern? | Requirements/architecture are sufficient for an implementable contract; complexity warrants a focused child. | Engineering owner, with specialist owner for the child concern. | Plan/Task authors, implementers, QA, operations. | Stage 03 parent `docs/03.specs/NNN-feature-id/spec.md`; children inside that feature directory and machine contracts under `contracts/`. | `docs/99.templates/templates/sdlc/spec.template.md` plus registered `docs/99.templates/templates/spec-contracts/*`. | Active-family lifecycle; parent Spec owns child cross-links and remains durable even when execution completes. | Parent types PRD/ARD/ADR/Spec/archive; child remains part of Spec role, not a new lifecycle stage. | Not a PRD, ADR, prospective Plan, execution evidence, generated implementation, or runtime truth. |
| Plan | Define prospective sequence, dependencies, change boundary, intended verification, risks, rollback, and completion criteria. | In what order and under what controls will an approved contract be implemented? | Stable Spec/contracts are ready for implementation planning. | Project/Engineering Lead. | Task owners, implementers, QA, reviewers. | Stage 04: `docs/04.execution/plans/*.md`. | `docs/99.templates/templates/sdlc/plan.template.md`. | `active` while prospective work is current, `completed` when the planned unit is finished, or superseded with replacement evidence. | Direct upstream PRD/ARD/ADR/Spec/archive as evidenced; Tasks consume it. | Not executed commands/results, a change log, Task ledger, runbook, or approval inferred from prose. |
| Task | Record what was actually attempted, changed, validated, reviewed, committed, deferred, or blocked. | What happened within the approved boundary, with what evidence and disposition? | Plan work begins or its result/review/deferral state changes. | Implementation Engineer / QA evidence owner. | Reviewers, later Tasks, Release and Operations owners. | Stage 04: `docs/04.execution/tasks/*.md`. | `docs/99.templates/templates/sdlc/task.template.md`. | `active` during work, `completed` after evidence/closure, or superseded; history is retained. | Parent Spec/Plan/Task/archive; links exact commands, results, reviews, commits, and deferrals. | Not a prospective Plan, chat transcript, raw log, secret store, Incident, or proof of unobserved runtime/remote state. |
| Guide | Explain routine use, context, prerequisites, common checks, and handoff to authoritative controls/procedures. | How should a person understand or routinely use the service or process? | User/operator usage context materially changes. | Documentation Specialist with service/operations owner. | Users, operators, developers. | Stage 05: `docs/05.operations/guides/**/*.md`. | `docs/99.templates/templates/operations/guide.template.md`. | Current guidance uses active-family lifecycle and must track current implementation. | Parent Spec/Plan/Task/Policy as evidenced; links Policy and Runbook instead of copying them. | Not mandatory Policy, ordered recovery Runbook, Incident response, or proof a service is live. |
| Incident | Record a live or resolved event's severity, impact, timeline, response state, actions, evidence, leadership, and handoff. | What happened, when, with what impact/current state, actions, and handoffs? | A qualifying operational or security event begins or its state changes. | Operations/SRE or Security incident owner. | Responders, stakeholders, Postmortem reviewers. | Stage 05: `docs/05.operations/incidents/YYYY/INC-###-title/INC-###-title.md`. | `docs/99.templates/templates/operations/incident.template.md`. | May move through document lifecycle while body owns event state; a root Incident is allowed when no verified Runbook parent exists. | Optional evidenced Runbook parent; paired Postmortem is a strict child. | Not root-cause certainty, blame, reviewed Postmortem learning, a Runbook, or an alert/raw log dump. |
| Postmortem | Produce reviewed, blameless causal learning and owned preventive actions after stabilization. | Why did the incident occur, what was learned, and which verified actions reduce recurrence? | The paired Incident is stable and meets defined postmortem criteria. | Operations/SRE with contributing owners and independent reviewers. | PRD/ARD/ADR/Spec/Plan/Policy/Runbook owners and stakeholders. | Stage 05: paired incident folder `postmortem.md`. | `docs/99.templates/templates/operations/postmortem.template.md`. | Strict Incident child; `reviewed_at` required, `review_cycle` forbidden; reviewed evidence remains durable. | Exactly the paired Incident as typed parent; actions route to earliest canonical owners. | Not live incident state, blame, a speculative root cause, an unreviewed retrospective, or a replacement for action tracking. |
| Policy | Define approved required/prohibited operational states, controls, exceptions, verification, and review cadence. | Which controls apply, what is forbidden, and how are exceptions approved and reviewed? | An approved operational control or exception changes. | Documentation Specialist / Operations/SRE with policy approver; Security where applicable. | Guides, Runbooks, operators, audits. | Stage 05: `docs/05.operations/policies/**/*.md`. | `docs/99.templates/templates/operations/policy.template.md`. | Active-family lifecycle; both `reviewed_at` and `review_cycle` required. | Parent PRD/ARD/ADR/Spec/Plan/Task; downstream Guide/Runbook consumers. | Not a procedure, implementation detail, recommendation-only Guide, security framework adoption, or evidence that a control ran. |
| Release | Bind a real release event to identity, immutable artifacts, included changes, validation, approvals, rollout/rollback, outcome, and known issues. | What release actually occurred and which evidence supports its bounded outcome? | Actual release artifacts, validation, approval, and outcome evidence exist. | Release Owner / Operations/SRE. | Users, operators, auditors, later releases/incidents. | Stage 05: `docs/05.operations/releases/YYYY-MM-DD-release-name.md`. | `docs/99.templates/templates/operations/release.template.md`. | Event evidence may complete and remain durable; `reviewed_at` optional, `review_cycle` forbidden. | Parent Spec/Plan/Task; links artifact/tag/commit and separately evidenced rollout/runtime chain. | Not a changelog, readiness checklist, tag, version bump, CI build, deployment record, or runtime proof. **Release != deployment/runtime proof.** |
| Runbook | Supply a repeatable ordered procedure with prerequisites, safety, expected evidence, recovery/rollback, and escalation. | What exact steps execute, verify, recover, and escalate an operation? | A routine, maintenance, recovery, or response path needs executable procedure. | Operations/SRE owner with service/security review as applicable. | Operators, automation owners, incident responders. | Stage 05: `docs/05.operations/runbooks/**/*.md`. | `docs/99.templates/templates/operations/runbook.template.md`. | Active-family lifecycle; `reviewed_at` and `review_cycle` required. | Parent Spec/Plan/Task/Guide/Policy/archive; an Incident links it only when actually used/applicable. | Not a routine-use Guide, mandatory control Policy, Incident timeline, automation execution evidence, or proof the procedure succeeds in every environment. |

### Why ARD is local coinage

The repository uses "Architecture Requirements Document" as a practical name
for its Stage 02 requirements form. The ISO/IEC/IEEE 42010:2022 public catalog
describes an architecture description and explicitly distinguishes it from the
architecture itself; it does not establish this repository's `ARD` name or
template. Therefore the ARD row is a local contract with an external comparison,
not a standards-conformance claim.

### Decision, event, and procedure separations

- Nygard's original ADR article and the ADR community both frame an ADR as one
  significant decision plus rationale, trade-offs, and consequences. The
  workspace preserves a superseded ADR rather than rewriting decision history.
- NIST SP 800-61 Rev. 3 is the current April 2025 incident-response source and
  supersedes Rev. 2. It supplies comparison context; it does not define this
  repository's Incident template or constitute framework adoption.
- Google SRE separates the incident record from a reviewed, blameless
  Postmortem containing impact, response, causes, and preventive actions.
- A Guide teaches routine use, Policy establishes controls, and a Runbook
  executes ordered steps. Linking these roles is required where relevant;
  merging them destroys ownership and validation semantics.

### Release, version, and deployment boundary

GitHub describes releases as tag-based packaged software iterations with notes
and assets. Semantic Versioning describes compatibility signals for a declared
public API. Neither proves that this repository performed a rollout or that a
runtime accepted it. A workspace Release target is valid only after the real
event has immutable artifacts, validation, approval, rollout/rollback evidence,
outcome, and known issues. Deployment environments, secrets, promotion rules,
and observed runtime state remain in their separately authorized chain.

### Unexercised contracts

The current tree has zero Incident, zero Postmortem, and zero Release targets,
even though Stage 99 registers all three profiles/templates. Their contract is
implemented as tracked schema but not validated by a real event document. A
future first target should expect focused template/profile review and must not
be created merely to exercise the schema.

## Scope Implications

| Scope | Application and disposition |
| --- | --- |
| `agentic` | Agents select the role by owned question, preserve evidence boundaries, and must not compress Plan, Task, review, and event records into chat or provider artifacts. |
| `architecture` | ARD and ADR remain separate: enduring constraints versus one significant decision; Specs consume both without replacing them. |
| `backend` | Backend APIs, data, and service behavior belong in parent/focused Specs; operator usage and recovery split into Guide/Runbook. |
| `common` | Common standards guide clarity and review but do not redefine role ownership or machine profiles. |
| `docs` | Owns template-first role selection, metadata/link checks, language boundaries, and advisory Stage 90 framing. |
| `entry` | Gateway intent, architecture, implementation, operations, and incidents use the same separate roles and explicit runtime boundary. |
| `frontend` | UI requirements and contracts belong upstream; usage in Guide, repeatable recovery in Runbook, and observed failures in Incident/Task evidence. |
| `infra` | Compose/runtime implementation cannot substitute for Spec, Plan, Task, Policy, Runbook, Release, or Incident evidence. |
| `meta` | Exact fields, parents, headings, and lifecycle semantics remain in the registry/templates; this row model is explanatory only. |
| `mobile` | No current mobile target exists; future work requires the same role separation plus mobile-specific verification evidence. |
| `ops` | Owns Guide, Policy, Runbook, Incident, Postmortem, and Release distinctions and their human/event evidence. |
| `product` | Human stakeholders own PRD approval; architecture, Specs, and agent output cannot silently manufacture product intent. |
| `qa` | QA consumes acceptance/contracts, records actual evidence in Tasks, reviews Postmortem/Release verification, and keeps intended versus actual results separate. |
| `security` | Security controls belong in Policy/Spec, response state in Incident, learning in Postmortem, and executable recovery in Runbook with redaction and approval. |

## Sources

| Source | Accessed | Class | Use and verification state |
| --- | --- | --- | --- |
| [Michael Nygard, Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) | 2026-08-08 | External fixed article | HTTP 200; one significant decision, context, status, consequences, monotonic numbering, and supersession. |
| [ADR organization](https://adr.github.io/) | 2026-08-08 | External mutable | HTTP 200; ADR definition, rationale, trade-offs, consequences, and decision-log framing. |
| [ISO/IEC/IEEE 29148:2018 catalog](https://www.iso.org/standard/72089.html) | 2026-08-08 | External catalog | Public abstract/status accessible; purchased standard text **UNVERIFIED**. |
| [ISO/IEC/IEEE 42010:2022 catalog](https://www.iso.org/standard/74393.html) | 2026-08-08 | External catalog | Public abstract/status accessible; purchased standard text **UNVERIFIED**; no ARD naming basis. |
| [RFC Editor](https://www.rfc-editor.org/) | 2026-08-08 | External mutable catalog | Official RFC publication series only; no workspace-role adoption. |
| [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) | 2026-08-08 | External fixed | HTTP 200; current incident-response CSF 2.0 profile, April 2025; Rev. 2 is superseded. |
| [Google SRE postmortem culture](https://sre.google/sre-book/postmortem-culture/) | 2026-08-08 | External fixed publication | HTTP 200; triggers, blameless reviewed learning, impact, causes, action plan, and sharing. |
| [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases) | 2026-08-08 | External mutable | HTTP 200; tag-based packaged iteration, notes, and assets; not deployment proof. |
| [Semantic Versioning 2.0.0](https://semver.org/) | 2026-08-08 | External fixed specification | HTTP 200; public-API compatibility/version signal only. |
| [SDLC document contract](../../../99.templates/support/sdlc-document-contract.md) | 2026-08-08 | Workspace tracked | Canonical human role and handoff owner. |
| [Template selection](../../../99.templates/support/template-selection.md) | 2026-08-08 | Workspace tracked | Canonical role-to-path/template mapping. |
| [Metadata profiles](../../../99.templates/support/document-metadata-profiles.yaml) | 2026-08-08 | Workspace tracked | Exact role fields, parents, states, headings, and exceptions. |
| [Graphify report](../../../../graphify-out/GRAPH_REPORT.md) | 2026-08-08 | Workspace stale/advisory | Built from `f8a72211`; role relationships corroborated against current tracked owners. |

## Maintenance

Recheck when Stage 99 adds/removes a role, path, template, parent relation,
lifecycle/freshness rule, or first real Incident/Postmortem/Release target.
Re-open mutable external pages and repin repository sources before changing a
comparative claim. Keep ARD labeled local coinage and Release separated from
deployment/runtime proof.

## Related Documents

- [Spec-driven SDLC](./spec-driven-sdlc.md)
- [Document metadata lifecycle](./document-metadata-lifecycle.md)
- [Workspace baseline](./workspace-baseline.md)
- [Execution Task](../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md)
