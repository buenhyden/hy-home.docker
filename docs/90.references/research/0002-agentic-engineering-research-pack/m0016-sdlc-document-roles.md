---
title: "Reference: SDLC Document Roles"
version: "1.1.0"
type: "reference/research"
status: "published"
owner: "@buenhyden"
updated: "2026-09-05"
layer: "references"
artifact_id: "RES-0002-m0016"
parent_ids:
- "RES-0002"
created: "2026-08-23"
observed_at: "2026-09-05"
reviewed_at: "2026-09-05"
review_cycle: "on-source-change"
---

# Reference: SDLC Document Roles

## Overview

The workspace uses twelve distinct lifecycle document roles. Each role owns a
different question, trigger, handoff, and evidence boundary. Similar subject
matter does not make the roles interchangeable: a Plan cannot report executed
results, a Guide cannot impose Policy, an Incident cannot contain reviewed
Postmortem causality, and a Release cannot stand in for deployment/runtime
proof.

This reference reflects the current Stage 00 and Stage 99 contracts, re-read
directly at HEAD `ece3eda9c3e1a603c6495dd55caba7df1c29ef6c` (2026-08-14),
superseding the Task 5 baseline `0445a17860ac27f6bf5ff1f9a8ffcde32bc4f2ee`
this leaf previously cited. `ARD` is explicitly repository-local coinage
rather than an industry-standard document name. The twelve roles below are a
proper subset of a larger 21-profile metadata registry; the metadata
reference owns that wider catalog, while this reference stays scoped to the
human lifecycle roles a document author actually chooses between.

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

This workspace's twelve roles split into two families that this reference
previously narrated in one undifferentiated table. Re-read directly this
revision rather than assumed: `docs/99.templates/templates/sdlc/` holds
exactly six role templates (`prd`, `ard`, `adr`, `spec`, `plan`,
`task.template.md`, alongside its own `README.md`), and
`docs/99.templates/templates/operations/` holds exactly six role templates
(`guide`, `incident`, `policy`, `postmortem`, `release`,
`runbook.template.md`, alongside its own `README.md`). The split is not this
leaf's invention; it is the directory boundary the templates already carry.
The [stage authoring matrix](../../../00.agent-governance/policies/stage-authoring-matrix.md),
re-read directly this revision, assigns the first family to Stages 01-04 and
the second to Stage 05: PRD to Stage 01, ARD/ADR to Stage 02, Spec to Stage
03, and Plan/Task to Stage 04 execution — each triggered by a discovery,
decision, contract-readiness, or in-progress-work event that precedes or
constitutes building the thing. Guide/Policy/Runbook/Incident/Postmortem/
Release all sit in Stage 05, triggered instead by "operational guidance,
controls, or repeatable procedures" changing, or by a real incident/release
event occurring after something already exists to operate. The typed
artifact-profile registry (`docs/99.templates/support/document-metadata-profiles.yaml`,
re-read this revision) preserves the same split at the field level: PRD,
ARD, ADR, Spec, Plan, and Task each require a direct parent drawn only from
other SDLC-family profiles or Archive (see the companion metadata-lifecycle
reference's profile table), while Guide, Policy, and Runbook admit Spec/
Plan/Task as parents but never the reverse — no SDLC profile accepts a
Guide, Policy, Runbook, Incident, Postmortem, or Release as a `parent_ids`
entry. Substitution across the boundary is therefore not just a style
violation but a typed-relation violation: an operations document cannot
serve as an SDLC lifecycle document's parent, and neither the stage
authoring matrix nor the metadata registry gives an SDLC document (PRD
through Task) a path into `docs/05.operations/`. The reverse failure mode is
equally concrete — an operations document cannot _substitute for_ an SDLC
document, because Stage 05 artifacts describe how to run or govern
something that Stage 01-04 artifacts must already have specified, decided,
contracted, planned, and evidenced; a Guide or Runbook with no upstream
Spec/Plan/Task to link is describing a service this workspace has not
actually built through its own lifecycle.

#### Historical SDLC lifecycle role matrix

**Superseded taxonomy notice (2026-09-05).** The table below is retained as the
2026-08-14 research state. Its Stage 04 Plan/Task routes, `artifact_type`
classifier, three-digit examples, independent Release profile, and generic
PRD/ARD role paths are not current repository authority. Current roles and
paths come from the Stage 99 Registry; the revalidation section near the end of
this member summarizes the present Requirement, Architecture/ADR, co-located
Spec/Plan/Task, and Operations model.

| Role                  | Purpose                                                                                                                                                | Question owned                                                                                                                | Trigger                                                                                                      | Owner                                                           | Consumer                                                 | Stage / path                                                                                                                             | Template                                                                                                            | Lifecycle                                                                                                                           | Relations                                                                                                          | Forbidden substitutions                                                                                                |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------- | -------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- |
| PRD                   | Capture approved product intent, value, scope, requirements, and acceptance.                                                                           | What problem, users, value, constraints, requirements, and success criteria should be addressed?                              | New or materially changed stakeholder intent or acceptance criteria.                                         | Product Manager / human stakeholder owner.                      | ARD/ADR authors, Spec owners, reviewers.                 | Stage 01: `docs/01.requirements/NNN-feature-or-system.md`.                                                                               | `docs/99.templates/templates/sdlc/prd.template.md`.                                                                 | `draft -> active -> completed` or `active/completed -> superseded`; current path until reviewed archive migration.                  | Root role; downstream ARD, ADR, and Spec links.                                                                    | Not an implementation design, architecture decision, task list, test result, or policy.                                |
| ARD                   | Preserve enduring architecture boundaries, concerns, views, constraints, and quality attributes.                                                       | Which architecture constraints and quality attributes shape the solution?                                                     | Approved requirements need architecture framing broader than one decision.                                   | System Architect.                                               | ADR and Spec authors, architecture reviewers.            | Stage 02: `docs/02.architecture/requirements/NNNN-short-title.md`.                                                                       | `docs/99.templates/templates/sdlc/ard.template.md`.                                                                 | Same active-family lifecycle; typed parent must be PRD.                                                                             | PRD parent; ADRs and Specs consume it. **ARD is local coinage**, not a recognized external standard document name. | Not a single decision, full technical Spec, implementation Plan, or claim of ISO 42010 conformance.                    |
| ADR                   | Preserve one architecturally significant decision, alternatives, rationale, status, and consequences.                                                  | Which significant option was chosen, why, and what consequences follow?                                                       | A material trade-off is decided, reversed, deprecated, or superseded.                                        | System Architect / accountable decision owner.                  | Spec/Plan authors, implementers, future decision makers. | Stage 02: `docs/02.architecture/decisions/NNNN-short-title.md`.                                                                          | `docs/99.templates/templates/sdlc/adr.template.md`.                                                                 | Preserve history; create/supersede rather than rewrite the old decision into current truth.                                         | PRD or ARD parent; later ADR may supersede it; Specs consume applicable decisions.                                 | Not an ARD, design catalog, meeting minute, implementation Plan, or mutable latest-state summary.                      |
| Spec / child contract | Define implementable behavior, interfaces, data, failure modes, guardrails, and verification; isolate focused subcontracts when separately reviewable. | What exactly will be built and verified, and which API/agent/data/service/test or machine contract governs a focused concern? | Requirements/architecture are sufficient for an implementable contract; complexity warrants a focused child. | Engineering owner, with specialist owner for the child concern. | Plan/Task authors, implementers, QA, operations.         | Stage 03 parent `docs/03.specs/NNN-feature-id/spec.md`; children inside that feature directory and machine contracts under `contracts/`. | `docs/99.templates/templates/sdlc/spec.template.md` plus registered `docs/99.templates/templates/spec-contracts/*`. | Active-family lifecycle; parent Spec owns child cross-links and remains durable even when execution completes.                      | Parent types PRD/ARD/ADR/Spec/archive; child remains part of Spec role, not a new lifecycle stage.                 | Not a PRD, ADR, prospective Plan, execution evidence, generated implementation, or runtime truth.                      |
| Plan                  | Define prospective sequence, dependencies, change boundary, intended verification, risks, rollback, and completion criteria.                           | In what order and under what controls will an approved contract be implemented?                                               | Stable Spec/contracts are ready for implementation planning.                                                 | Project/Engineering Lead.                                       | Task owners, implementers, QA, reviewers.                | Stage 04: `docs/04.execution/plans/*.md`.                                                                                                | `docs/99.templates/templates/sdlc/plan.template.md`.                                                                | `active` while prospective work is current, `completed` when the planned unit is finished, or superseded with replacement evidence. | Direct upstream PRD/ARD/ADR/Spec/archive as evidenced; Tasks consume it.                                           | Not executed commands/results, a change log, Task ledger, runbook, or approval inferred from prose.                    |
| Task                  | Record what was actually attempted, changed, validated, reviewed, committed, deferred, or blocked.                                                     | What happened within the approved boundary, with what evidence and disposition?                                               | Plan work begins or its result/review/deferral state changes.                                                | Implementation Engineer / QA evidence owner.                    | Reviewers, later Tasks, Release and Operations owners.   | Stage 04: `docs/04.execution/tasks/*.md`.                                                                                                | `docs/99.templates/templates/sdlc/task.template.md`.                                                                | `active` during work, `completed` after evidence/closure, or superseded; history is retained.                                       | Parent Spec/Plan/Task/archive; links exact commands, results, reviews, commits, and deferrals.                     | Not a prospective Plan, chat transcript, raw log, secret store, Incident, or proof of unobserved runtime/remote state. |

#### Operations roles (Guide, Incident, Postmortem, Policy, Release, Runbook)

| Role       | Purpose                                                                                                                                           | Question owned                                                                              | Trigger                                                                        | Owner                                                                                      | Consumer                                                      | Stage / path                                                                  | Template                                                         | Lifecycle                                                                                                                           | Relations                                                                                            | Forbidden substitutions                                                                                                                                    |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------- | ----------------------------------------------------------------------------- | ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Guide      | Explain routine use, context, prerequisites, common checks, and handoff to authoritative controls/procedures.                                     | How should a person understand or routinely use the service or process?                     | User/operator usage context materially changes.                                | Documentation Specialist with service/operations owner.                                    | Users, operators, developers.                                 | Stage 05: `docs/05.operations/guides/**/*.md`.                                | `docs/99.templates/templates/operations/guide.template.md`.      | Current guidance uses active-family lifecycle and must track current implementation.                                                | Parent Spec/Plan/Task/Policy as evidenced; links Policy and Runbook instead of copying them.         | Not mandatory Policy, ordered recovery Runbook, Incident response, or proof a service is live.                                                             |
| Incident   | Record a live or resolved event's severity, impact, timeline, response state, actions, evidence, leadership, and handoff.                         | What happened, when, with what impact/current state, actions, and handoffs?                 | A qualifying operational or security event begins or its state changes.        | Operations/SRE or Security incident owner.                                                 | Responders, stakeholders, Postmortem reviewers.               | Stage 05: `docs/05.operations/incidents/YYYY/INC-###-title/INC-###-title.md`. | `docs/99.templates/templates/operations/incident.template.md`.   | May move through document lifecycle while body owns event state; a root Incident is allowed when no verified Runbook parent exists. | Optional evidenced Runbook parent; paired Postmortem is a strict child.                              | Not root-cause certainty, blame, reviewed Postmortem learning, a Runbook, or an alert/raw log dump.                                                        |
| Postmortem | Produce reviewed, blameless causal learning and owned preventive actions after stabilization.                                                     | Why did the incident occur, what was learned, and which verified actions reduce recurrence? | The paired Incident is stable and meets defined postmortem criteria.           | Operations/SRE with contributing owners and independent reviewers.                         | PRD/ARD/ADR/Spec/Plan/Policy/Runbook owners and stakeholders. | Stage 05: paired incident folder `postmortem.md`.                             | `docs/99.templates/templates/operations/postmortem.template.md`. | Strict Incident child; `reviewed_at` required, `review_cycle` forbidden; reviewed evidence remains durable.                         | Exactly the paired Incident as typed parent; actions route to earliest canonical owners.             | Not live incident state, blame, a speculative root cause, an unreviewed retrospective, or a replacement for action tracking.                               |
| Policy     | Define approved required/prohibited operational states, controls, exceptions, verification, and review cadence.                                   | Which controls apply, what is forbidden, and how are exceptions approved and reviewed?      | An approved operational control or exception changes.                          | Documentation Specialist / Operations/SRE with policy approver; Security where applicable. | Guides, Runbooks, operators, audits.                          | Stage 05: `docs/05.operations/policies/**/*.md`.                              | `docs/99.templates/templates/operations/policy.template.md`.     | Active-family lifecycle; both `reviewed_at` and `review_cycle` required.                                                            | Parent PRD/ARD/ADR/Spec/Plan/Task; downstream Guide/Runbook consumers.                               | Not a procedure, implementation detail, recommendation-only Guide, security framework adoption, or evidence that a control ran.                            |
| Release    | Bind a real release event to identity, immutable artifacts, included changes, validation, approvals, rollout/rollback, outcome, and known issues. | What release actually occurred and which evidence supports its bounded outcome?             | Actual release artifacts, validation, approval, and outcome evidence exist.    | Release Owner / Operations/SRE.                                                            | Users, operators, auditors, later releases/incidents.         | Stage 05: `docs/05.operations/releases/YYYY-MM-DD-release-name.md`.           | `docs/99.templates/templates/operations/release.template.md`.    | Event evidence may complete and remain durable; `reviewed_at` optional, `review_cycle` forbidden.                                   | Parent Spec/Plan/Task; links artifact/tag/commit and separately evidenced rollout/runtime chain.     | Not a changelog, readiness checklist, tag, version bump, CI build, deployment record, or runtime proof. **Release != deployment/runtime proof.**           |
| Runbook    | Supply a repeatable ordered procedure with prerequisites, safety, expected evidence, recovery/rollback, and escalation.                           | What exact steps execute, verify, recover, and escalate an operation?                       | A routine, maintenance, recovery, or response path needs executable procedure. | Operations/SRE owner with service/security review as applicable.                           | Operators, automation owners, incident responders.            | Stage 05: `docs/05.operations/runbooks/**/*.md`.                              | `docs/99.templates/templates/operations/runbook.template.md`.    | Active-family lifecycle; `reviewed_at` and `review_cycle` required.                                                                 | Parent Spec/Plan/Task/Guide/Policy/archive; an Incident links it only when actually used/applicable. | Not a routine-use Guide, mandatory control Policy, Incident timeline, automation execution evidence, or proof the procedure succeeds in every environment. |

### Why ARD is local coinage

The repository uses "Architecture Requirements Document" as a practical name
for its Stage 02 requirements form. The ISO/IEC/IEEE 42010:2022 public catalog
describes an architecture description and explicitly distinguishes it from the
architecture itself; it does not establish this repository's `ARD` name or
template. Therefore the ARD row is a local contract with an external comparison,
not a standards-conformance claim.

### Current typed-role coverage

The prior revision of this reference described role paths but did not
directly re-measure typed `artifact_type` migration depth per role. Direct
`grep -l 'artifact_type: <role>'` counts against each family's canonical path
on 2026-08-14 give:

| Role    | Path count | Typed count | Typed depth                                                                     |
| ------- | ---------- | ----------- | ------------------------------------------------------------------------------- |
| PRD     | 25         | 1           | One current leaf exposes `artifact_type: prd`; the rest are path-only evidence. |
| ARD     | 25         | 1           | Same pattern; typed migration has touched one representative leaf per family.   |
| ADR     | 25         | 1           | Same pattern.                                                                   |
| Plan    | 103        | 16          | Deepest non-Task migration; still under one-sixth of the path population.       |
| Task    | 133        | 20          | Deepest migration overall; still under one-sixth of the path population.        |
| Guide   | 66         | 1           | Same shallow pattern as PRD/ARD/ADR.                                            |
| Policy  | 64         | 1           | Same shallow pattern.                                                           |
| Runbook | 62         | 2           | Marginally deeper than Guide/Policy; still shallow in absolute terms.           |

Two conclusions follow directly from this table, not from inference. First,
canonical **path** remains the dominant role-evidence signal for this corpus
today; typed-field coverage is real but shallow everywhere except Plan and
Task. Second, the shallowness is uniform enough (roughly 1-2% for PRD/ARD/
ADR/Guide/Policy, roughly 15% for Plan/Task, roughly 3% for Runbook) that no
single role's typed migration should be read as "further along" in a way that
changes how an author should choose a role — path-based role selection
remains correct and required everywhere in this corpus today.

### Registered focused Spec-contract types

The Spec row's "optional focused contracts" claim has eight concrete
registered templates under `docs/99.templates/templates/spec-contracts/`,
re-listed directly this revision: `agent-design.template.md`,
`api-spec.template.md`, `data-model.template.md`,
`openapi.template.yaml`, `schema.template.graphql`, `service.template.md`,
`service.template.proto`, and `tests.template.md`. Each remains part of the
Spec role rather than a new lifecycle stage — a focused child contract shares
the parent Spec's lifecycle and evidence obligations and is not independently
promotable to `active`/`completed` outside its parent's disposition.

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
be created merely to exercise the schema. Re-counted directly on 2026-08-14 by
`find`ing `docs/05.operations/incidents`, `docs/05.operations/releases`, and
any `postmortem.md` leaf: the count is still 0/0/0, unchanged since the
2026-08-08 baseline. This is now two independent zero-observations six days
apart, which strengthens confidence that the gap is structural (no qualifying
event has occurred) rather than a stale one-time measurement.

### Operations path convergence in progress

The operations paths recorded in the role contract above are the paths tracked
on the current branch. A taxonomy convergence is underway on the separate
`codex/sdlc-taxonomy-convergence` branch, unmerged as of 2026-08-14, that moves
every operations role to a different layout. A reader creating a document today
follows the current column; a reader planning structure should expect the target.

| Role       | Current tracked path                                               | Convergence target                                                    |
| ---------- | ------------------------------------------------------------------ | --------------------------------------------------------------------- |
| Guide      | `docs/05.operations/guides/<NN>-<domain>/<slug>.md`                | `docs/05.operations/catalog/<NN>-<domain>/ops-####-<slug>/guide.md`   |
| Policy     | `docs/05.operations/policies/<NN>-<domain>/<slug>.md`              | `docs/05.operations/catalog/<NN>-<domain>/ops-####-<slug>/policy.md`  |
| Runbook    | `docs/05.operations/runbooks/<NN>-<domain>/<slug>.md`              | `docs/05.operations/catalog/<NN>-<domain>/ops-####-<slug>/runbook.md` |
| Incident   | `docs/05.operations/incidents/YYYY/INC-###-title/INC-###-title.md` | `docs/05.operations/incidents/YYYY/inc-####-<slug>/incident.md`       |
| Postmortem | paired incident folder `postmortem.md`                             | unchanged: paired incident folder `postmortem.md`                     |
| Release    | `docs/05.operations/releases/YYYY-MM-DD-release-name.md`           | directory retained; no target instance observed on either branch      |

Two structural changes drive this. Document type moves from the directory name
into a fixed file name, so `guide.md`, `policy.md`, and `runbook.md` identify the
role while the enclosing `ops-####-<slug>` directory identifies the subject. And
the subject, not the role, becomes the grouping key: `llm-wiki-maintenance`
currently exists as three files under three separate role directories, and
converges into one `catalog/00-workspace/ops-0007-llm-wiki-maintenance/`
directory holding all three. The incident packet already worked this way, which
is why only its identifier form and inner file name change.

The identifier form also normalizes. The current tree uses an upper-case
three-digit `INC-###`; the target uses a lower-case four-digit `inc-####`,
matching the `ops-####`, `ref-####`, `chg-####`, and `spec-####` series used
elsewhere in the convergence branch.

This entry records an observed in-flight migration. It does not authorize either
layout, and the convergence branch owns its own sequencing, validators, and
review. `tests/validation/test_document_metadata.py` still asserts the current
form on this branch, so the two contracts are not simultaneously satisfiable and
the merge, not this reference, resolves them.

### Carried source-evidence claims

Source-evidence claims carried forward from the superseded 2026-07-05
research pack on 2026-08-19. Each states what the upstream evidence supports
and, where it matters more, what it does not.

- **The committee catalog is the fallback route when the main standards host refuses.** The main standards site `www.iso.org` returned HTTP 403 to automated retrieval, and the ISO-operated `committee.iso.org` catalog served the same records. Recorded as the method, not as the dated stage codes: when `www.iso.org` refuses, `committee.iso.org` is the corroborating route. **Stage codes carried 2026-08-19** after a seat measured that one of them survives nowhere else: `60.60` occurs in no tracked file outside the retiring leaf and this migration's own ledger, so the claim that the codes are preserved elsewhere held for one half and not the other. The observed codes are recorded here rather than dropped — ISO/IEC/IEEE 29148:2018 and 42010:2022 were both read at stage `60.60` and current, and record 63712 — ISO/IEC/IEEE **12207:2017**, whose named successor is **12207:2026** — was read at stage `95.99`, which the source states as withdrawal of an International Standard rather than of an earlier edition. Both the identifier and the exact stage wording are restored 2026-08-19; `12207` occurred zero times in this leaf, so the record was unrecoverable after deletion. These are dated catalog readings, not conformance claims, and the 95.99 reading remains part of this protected research record. The hostnames are stated because the method is not reproducible from a description of them.

## Scope Implications

| Scope          | Application and disposition                                                                                                                                          |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agentic`      | Agents select the role by owned question, preserve evidence boundaries, and must not compress Plan, Task, review, and event records into chat or provider artifacts. |
| `architecture` | ARD and ADR remain separate: enduring constraints versus one significant decision; Specs consume both without replacing them.                                        |
| `backend`      | Backend APIs, data, and service behavior belong in parent/focused Specs; operator usage and recovery split into Guide/Runbook.                                       |
| `common`       | Common standards guide clarity and review but do not redefine role ownership or machine profiles.                                                                    |
| `docs`         | Owns template-first role selection, metadata/link checks, language boundaries, and advisory Stage 90 framing.                                                        |
| `entry`        | Gateway intent, architecture, implementation, operations, and incidents use the same separate roles and explicit runtime boundary.                                   |
| `frontend`     | UI requirements and contracts belong upstream; usage in Guide, repeatable recovery in Runbook, and observed failures in Incident/Task evidence.                      |
| `infra`        | Compose/runtime implementation cannot substitute for Spec, Plan, Task, Policy, Runbook, Release, or Incident evidence.                                               |
| `meta`         | Exact fields, parents, headings, and lifecycle semantics remain in the registry/templates; this row model is explanatory only.                                       |
| `mobile`       | No current mobile target exists; future work requires the same role separation plus mobile-specific verification evidence.                                           |
| `ops`          | Owns Guide, Policy, Runbook, Incident, Postmortem, and Release distinctions and their human/event evidence.                                                          |
| `product`      | Human stakeholders own PRD approval; architecture, Specs, and agent output cannot silently manufacture product intent.                                               |
| `qa`           | QA consumes acceptance/contracts, records actual evidence in Tasks, reviews Postmortem/Release verification, and keeps intended versus actual results separate.      |
| `security`     | Security controls belong in Policy/Spec, response state in Incident, learning in Postmortem, and executable recovery in Runbook with redaction and approval.         |

## Sources

| Source                                                                                                                         | Accessed   | Class                        | Use and verification state                                                                                 |
| ------------------------------------------------------------------------------------------------------------------------------ | ---------- | ---------------------------- | ---------------------------------------------------------------------------------------------------------- |
| [Michael Nygard, Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) | 2026-08-08 | External fixed article       | HTTP 200; one significant decision, context, status, consequences, monotonic numbering, and supersession.  |
| [ADR organization](https://adr.github.io/)                                                                                     | 2026-08-08 | External mutable             | HTTP 200; ADR definition, rationale, trade-offs, consequences, and decision-log framing.                   |
| [ISO/IEC/IEEE 29148:2018 catalog](https://www.iso.org/standard/72089.html)                                                     | 2026-08-08 | External catalog             | Public abstract/status accessible; purchased standard text **UNVERIFIED**.                                 |
| [ISO/IEC/IEEE 42010:2022 catalog](https://www.iso.org/standard/74393.html)                                                     | 2026-08-08 | External catalog             | Public abstract/status accessible; purchased standard text **UNVERIFIED**; no ARD naming basis.            |
| [RFC Editor](https://www.rfc-editor.org/)                                                                                      | 2026-08-08 | External mutable catalog     | Official RFC publication series only; no workspace-role adoption.                                          |
| [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final)                                                         | 2026-08-08 | External fixed               | HTTP 200; current incident-response CSF 2.0 profile, April 2025; Rev. 2 is superseded.                     |
| [Google SRE postmortem culture](https://sre.google/sre-book/postmortem-culture/)                                               | 2026-08-08 | External fixed publication   | HTTP 200; triggers, blameless reviewed learning, impact, causes, action plan, and sharing.                 |
| [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)                         | 2026-08-08 | External mutable             | HTTP 200; tag-based packaged iteration, notes, and assets; not deployment proof.                           |
| [Semantic Versioning 2.0.0](https://semver.org/)                                                                               | 2026-08-08 | External fixed specification | HTTP 200; public-API compatibility/version signal only.                                                    |
| SDLC document contract (retired path: `../../../99.templates/support/sdlc-document-contract.md`)                                              | 2026-08-08 | Workspace tracked            | Canonical human role and handoff owner.                                                                    |
| Template selection (retired path: `../../../99.templates/support/template-selection.md`)                                                      | 2026-08-08 | Workspace tracked            | Canonical role-to-path/template mapping.                                                                   |
| Metadata profiles (retired path: `../../../99.templates/support/document-metadata-profiles.yaml`)                                             | 2026-08-14 | Workspace tracked            | Re-read to confirm 21 total profiles versus this leaf's 12 human roles.                                    |
| [Task template](../../../99.templates/templates/specs/task.template.md)                                                         | 2026-08-14 | Workspace tracked            | Direct read confirming Verification/Review/Commit-Ledger/Deferred sections absent from the Plan template.  |
| [Plan template](../../../99.templates/templates/specs/plan.template.md)                                                         | 2026-08-14 | Workspace tracked            | Direct read confirming "Verification Plan" (prospective) versus Task's "Verification Evidence" (observed). |
| Spec-contracts templates (retired path: `../../../99.templates/templates/spec-contracts/`)                                                    | 2026-08-14 | Workspace tracked            | Directory listing confirming eight registered focused-contract template files.                             |
| [Graphify report](../../../../graphify-out/GRAPH_REPORT.md)                                                                    | 2026-08-08 | Workspace stale/advisory     | Built from `f8a72211`; role relationships corroborated against current tracked owners.                     |

## Architecture Practice Delta Claims

| Claim ID | Owner leaf | Evidence mode | Source family |
| --- | --- | --- | --- |
| `SDLCDOC-ADR-001` | `sdlc-document-roles.md` | source-backed | `https://adr.github.io/` |
| `SDLCDOC-ADR-002` | `sdlc-document-roles.md` | source-backed | `https://adr.github.io/` |
| `SDLCDOC-ADR-003` | `sdlc-document-roles.md` | source-backed | `https://adr.github.io/` |

## Architecture Practice Direct-Page Evidence

| Page key | Source ID | Claim ID | Family root | Direct URL | Accessed at | State |
| --- | --- | --- | --- | --- | --- | --- |
| `ADR-ROLE` | `SDR-SRC-001` | `SDLCDOC-ADR-001` | `https://adr.github.io/` | `https://adr.github.io/madr/decisions/0000-use-markdown-architectural-decision-records.html` | 2026-08-28 | VERIFIED |
| `ADR-LIFECYCLE` | `SDR-SRC-002` | `SDLCDOC-ADR-002` | `https://adr.github.io/` | `https://adr.github.io/madr/decisions/0008-add-status-field.html` | 2026-08-28 | UNVERIFIED |
| `ADR-RELATIONSHIPS` | `SDR-SRC-003` | `SDLCDOC-ADR-003` | `https://adr.github.io/` | `https://adr.github.io/madr/` | 2026-08-28 | UNVERIFIED |

## Scope Application

| Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
| --- | --- | --- | --- | --- |
| agentic | applies | Agents consume approved Spec and Task boundaries. | Inspect Stage 03 links. | No agent behavior proof. |
| architecture | applies | Use AD for structure and ADR for decision-ready choices. | Confirm registry profiles. | ADR gaps remain UNVERIFIED. |
| common | applies | Keep owner/consumer handoffs explicit. | Review role table. | Advisory analysis. |
| docs | applies | Publish typed documents in registered paths. | Check registry path patterns. | Legacy support is not authority. |
| infra | applies | Apply Guide/Policy/Runbook roles to infrastructure catalog subjects. | Confirm `docs/05.operations/catalog/<domain>/<subject>/` ownership. | No runtime claim. |
| ops | applies | Select Guide, Policy, Runbook, Incident, or Postmortem by purpose. | Check catalog/packet convention. | No live incident is asserted. |
| qa | applies | Attach verification evidence to Task. | Inspect Task evidence. | A Task record is not execution proof. |
| security | applies | Use Policy constraints and incident handling boundaries. | Inspect scoped source references. | No control effectiveness claim. |

## Architecture Practice Composition Links

- [Documentation architecture](./m0007-documentation-architecture.md)
- [Scope application matrix](./m0015-scope-application-matrix.md)

## 2026-09-05 Revalidation

Baseline: `main@4c6d211129615eab372d720ebd209b6c27618c86`.
Current execution evidence is co-located as Plan and Task inside its Stage 03
Spec package. Stage 05 registers Guide, Policy, Runbook, Incident, and
Postmortem. It intentionally has no independent Release profile: release
evidence is composed from the owning Task, changelog/tag, CI, and applicable
Runbook evidence.

| Artifact role | Current owner | Evidence depth | Non-substitution rule |
| --- | --- | --- | --- |
| Requirement/PRD/SRS/interface perspective | Stage 01 package | Repository-enforced | Does not become architecture or implementation |
| Architecture Description/ADR | Stage 02 | Repository-enforced | Description is current design; ADR preserves decision |
| Spec/Plan/Task | Stage 03 package | Repository-enforced | Behavior, prospective sequence, and executed evidence stay separate |
| Guide/Policy/Runbook/Incident/Postmortem | Stage 05 | Repository-enforced | Reader help, control, procedure, event, and learning stay separate |
| Release/deployment evidence | Task + tag/changelog + CI + Runbook as applicable | Defined | A document title cannot prove deployment |

Recommendation: add or change a role only through Registry, template,
consumer, validator, and lifecycle evidence as one contract slice.

## Maintenance

Recheck when Stage 99 adds/removes a role, path, template, parent relation,
lifecycle/freshness rule, or first real Incident/Postmortem/Release target.
Re-open mutable external pages and repin repository sources before changing a
comparative claim. Keep ARD labeled local coinage and Release separated from
deployment/runtime proof. Re-run the typed-role-coverage `grep -l` counts on
each future revision; Plan/Task migration depth in particular is likely to
keep moving faster than the other roles and the table above will go stale
first.

## Related Documents

- [Verification and validation](./m0019-verification-validation.md)
- [Spec-driven SDLC](./m0018-spec-driven-sdlc.md)
- [Document metadata lifecycle](./m0006-document-metadata-lifecycle.md)
- [Workspace baseline](./m0020-workspace-baseline.md)
- Execution Task (retired path: `../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`)
