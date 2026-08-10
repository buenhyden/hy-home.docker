---
status: active
artifact_id: reference:agentic-research:sdlc-document-roles
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-07
---

<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/sdlc-document-roles.md -->

# Reference: SDLC and Operations Document-Type Roles

## Overview

This reference maps each tracked workspace document type to the question it
answers, its authoring trigger and owner, its inputs and consumers, its lifecycle
status, its canonical template/path, and its external or repo-template basis.
Supporting API, agent, data, service, and test contracts are separate rows because they
answer different questions and serve different consumers.

## Purpose

Help authors choose the earliest correct document owner and prevent requirements,
decisions, technical contracts, execution evidence, operating controls,
procedures, incidents, learning, releases, references, audits, and archive
tombstones from being conflated.

## Repository Role

This Stage 90 reference restates the active stage authoring matrix and template
catalog. Those tracked governance/template files remain authoritative. External
sources are comparison bases only and do not become workspace policy through
this matrix. This file is the canonical research owner for document and release
roles; [`document-metadata-lifecycle.md`](./document-metadata-lifecycle.md) owns
identity, profile, relation, freshness, transition, README, generator, and
semantic-validation criteria.

## Scope

### In Scope

- Active Stage 01-05 document roles
- Optional Stage 03 supporting contracts
- Root release notes plus Stage 90 reference/audit and Stage 98 tombstone roles
- External or repo-template basis and source caveats

### Out of Scope

- Creating a new document type, stage, template, or release procedure
- Adopting an external standard, framework, tool, or provider workflow
- Reclassifying historical artifacts outside the approved task scope

## Definitions / Facts

- **Primary question** is the one question the artifact owns; related context
  should link rather than duplicate ownership.
- **Authoring trigger** is the condition that justifies creating or updating the
  artifact.
- **Lifecycle status** describes the repo-local stage role, not the YAML
  frontmatter value of an individual file.
- **External basis** can state a repo-template basis when no external source is
  necessary or adopted for that document role.
- **Release notes/changelog** communicate changes; a **Release** records an
  executed release event; the release runbook owns procedure; deployment
  systems own promotion/runtime evidence. They are not interchangeable.
- **Incident** preserves contemporaneous state; **postmortem** preserves reviewed
  learning and preventive actions.

## Canonical Document-Role Matrix

| Document          | Primary question                                                                                                                             | Authoring trigger                                                                                                 | Owner                                                           | Inputs                                                                                                         | Outputs / consumers                                                   | Lifecycle status                                                | Workspace template / path                                                                                                                                     | External basis                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| PRD               | What problem, users, value, scope, requirements, and success criteria should the workspace address?                                          | New or materially changed stakeholder intent                                                                      | Product Manager                                                 | Stakeholder intent, constraints, verified current state                                                        | ARD/ADR, Spec, reviewers                                              | Active Stage 01 requirements                                    | `docs/99.templates/templates/sdlc/prd.template.md` → `docs/01.requirements/NNN-feature-or-system.md`                                                          | ISO/IEC/IEEE 29148:2018 requirements-engineering metadata; public page is not full standard text and is marked “to be revised.”                                                                                                                                                                                                                                                                                                                                                                              |
| ARD               | What architecture boundaries, stakeholders, concerns, and quality attributes constrain the solution?                                         | Stable PRD needs enduring architecture requirements                                                               | System Architect                                                | PRD, existing architecture/runtime, quality attributes                                                         | ADRs, Specs, architecture reviewers                                   | Active Stage 02 architecture requirements                       | `sdlc/ard.template.md` → `docs/02.architecture/requirements/NNNN-short-title.md`                                                                              | **Local coinage.** No external convention defines an "Architecture Requirements Document." See [ARD Has No External Basis](#ard-has-no-external-basis). ISO/IEC/IEEE 42010:2022 architecture-description metadata is the nearest standards framing, and the repo ARD is narrower than a full standard-conforming description.                                                                                                                                                                                |
| ADR               | Which non-trivial architecture option was chosen, why, and with what consequences?                                                           | Architecturally significant trade-off or reversal                                                                 | System Architect                                                | PRD/ARD, alternatives, constraints, evidence                                                                   | Specs, plans, future decision reviewers                               | Active Stage 02 decision record                                 | `sdlc/adr.template.md` → `docs/02.architecture/decisions/NNNN-short-title.md`                                                                                 | ADR homepage definition plus Michael Nygard's 2011-11-15 original practice article.                                                                                                                                                                                                                                                                                                                                                                                                                          |
| Spec              | What technical design, interfaces, contracts, and verification criteria will be implemented?                                                 | PRD/architecture baseline is sufficient for implementation design                                                 | Implementing engineer                                           | PRD, ARD, ADRs, current implementation evidence                                                                | Supporting contracts, Plan, implementers, QA                          | Active Stage 03 technical contract                              | `sdlc/spec.template.md` → `docs/03.specs/NNN-feature-id/spec.md`                                                                                              | GitHub Spec Kit treats the specification as the context anchor that feeds Plan and Tasks; no Spec Kit runtime is adopted.                                                                                                                                                                                                                                                                                                                                                                                    |
| API Spec          | What callable operations, schemas, auth rules, errors, and compatibility contract apply?                                                     | A Spec exposes or changes an API/interface                                                                        | Backend/API owner                                               | Parent Spec, architecture, security and data constraints                                                       | Implementers, clients, contract tests                                 | Optional supporting Stage 03 contract                           | `spec-contracts/api-spec.template.md` → feature `api-spec.md`; machine contracts under `contracts/`                                                           | Repo-template basis; no separate external API standard is adopted by this task.                                                                                                                                                                                                                                                                                                                                                                                                                              |
| Agent Design      | What agent purpose, inputs, outputs, tools, permissions, failure modes, and eval contract apply?                                             | A Spec creates or materially changes agent behavior                                                               | Agent/feature owner                                             | Parent Spec, Stage 00 governance, provider constraints                                                         | Runtime adapter work, tests/evals, reviewers                          | Optional supporting Stage 03 contract                           | `spec-contracts/agent-design.template.md` → feature `agent-design.md`                                                                                         | Repo-template basis; GitHub Spec Kit only supplies comparison for structured agent context, not this provider-neutral contract.                                                                                                                                                                                                                                                                                                                                                                              |
| Data Model        | What entities, relationships, integrity, storage, privacy, and migration rules apply?                                                        | A Spec creates or changes durable data shape                                                                      | Data/feature owner                                              | Parent Spec, architecture, privacy/security constraints                                                        | Implementers, migrations, API contracts, tests                        | Optional supporting Stage 03 contract                           | `spec-contracts/data-model.template.md` → feature `data-model.md`                                                                                             | Repo-template basis; no external data-model standard is adopted by this task.                                                                                                                                                                                                                                                                                                                                                                                                                                |
| Service Scaffold  | What service boundary, dependencies, configuration, health, observability, and implementation skeleton apply?                                | A Spec creates or materially changes a service-shaped implementation                                              | Service/feature owner                                           | Parent Spec, architecture, API/data/security constraints                                                       | Implementers, Compose/runtime design, tests, operators                | Optional supporting Stage 03 contract                           | `spec-contracts/service.template.md` → feature `service.md`                                                                                                   | Repo-template basis; the scaffold does not prove deployed service runtime.                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| Test Contract     | What must be verified, with which fixtures, expected results, non-functional checks, and evals?                                              | A Spec needs executable acceptance/verification detail                                                            | QA/feature owner                                                | Parent Spec, API/agent/data contracts, risks                                                                   | Plan, Task, CI, reviewers                                             | Optional supporting Stage 03 contract                           | `spec-contracts/tests.template.md` → feature `tests.md`                                                                                                       | Repo-template basis; Spec Kit quality checklists and NIST SSDF verification practices are comparison lenses only.                                                                                                                                                                                                                                                                                                                                                                                            |
| Plan              | In what sequence will the approved Spec be implemented, controlled, verified, and completed?                                                 | Spec and supporting contracts are stable enough to schedule work                                                  | Project/Engineering Lead                                        | PRD/ARD/ADR/Spec, dependencies, risks                                                                          | Tasks, implementers, reviewers                                        | Active Stage 04 execution plan                                  | `sdlc/plan.template.md` → `docs/04.execution/plans/`                                                                                                          | GitHub Spec Kit has a distinct Plan phase feeding Tasks; ISO 12207:2017 supplies withdrawn historical lifecycle metadata only.                                                                                                                                                                                                                                                                                                                                                                               |
| Task              | What was attempted, changed, validated, reviewed, committed, deferred, or blocked?                                                           | Approved plan work begins                                                                                         | Implementation/QA Engineer                                      | Plan, Spec, task brief, baseline evidence                                                                      | Reviewers, operations, release, audit trail                           | Active Stage 04 execution evidence                              | `sdlc/task.template.md` → `docs/04.execution/tasks/`                                                                                                          | GitHub Spec Kit separates Tasks and Implement; the repo task additionally owns auditable execution evidence.                                                                                                                                                                                                                                                                                                                                                                                                 |
| Guide             | How should a person understand, use, and routinely check the service/process, and where do procedures live?                                  | User/operator-facing usage or onboarding changes                                                                  | Documentation Specialist / Operations/SRE                       | Spec, task evidence, actual behavior                                                                           | Users/operators; policy/runbook handoff                               | Active Stage 05 operations guidance                             | `operations/guide.template.md` → `docs/05.operations/guides/`                                                                                                 | Repo-template basis; external runbook sources do not replace a usage guide.                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| Policy            | Which operational controls are required or prohibited, how are exceptions handled, and how is compliance reviewed?                           | An approved operational control or exception changes                                                              | Documentation Specialist / Operations/SRE, with policy approver | Requirements, architecture, security/compliance constraints, task evidence                                     | Guides, runbooks, audits, operators                                   | Active Stage 05 operating control                               | `operations/policy.template.md` → `docs/05.operations/policies/`                                                                                              | Repo-template basis; NIST SSDF is high-level comparison and is not adopted policy.                                                                                                                                                                                                                                                                                                                                                                                                                           |
| Runbook           | What ordered, repeatable steps, evidence, recovery, rollback, and escalation execute an operation?                                           | Repeatable operation, recovery, or incident response needs a procedure                                            | Operations/SRE                                                  | Policy, Guide, Spec, task/incident evidence                                                                    | Operators, incident responders, audits                                | Active Stage 05 operational procedure                           | `operations/runbook.template.md` → `docs/05.operations/runbooks/`                                                                                             | PagerDuty defines a runbook as a detailed how-to for a repeated operations task; the page is mutable vendor guidance with no visible update date.                                                                                                                                                                                                                                                                                                                                                            |
| Incident          | What happened, when, with what impact/current state, command roles, actions, and handoffs?                                                   | A qualifying operational/security event begins                                                                    | Operations/SRE or Security incident owner                       | Alerts, observations, commands, communications                                                                 | Responders, stakeholders, Postmortem                                  | Active/resolved Stage 05 incident record                        | `operations/incident.template.md` → `docs/05.operations/incidents/YYYY/INC-###-incident-title/INC-###-incident-title.md`                                      | Google SRE incident command/live-state practice; NIST SP 800-61 Rev. 3 (April 2025) CSF 2.0 incident-response profile.                                                                                                                                                                                                                                                                                                                                                                                       |
| Postmortem        | Why did the incident occur, what was learned, and which owned actions prevent recurrence?                                                    | Incident is stabilized and meets postmortem criteria                                                              | Operations/SRE with contributing owners/reviewers               | Incident timeline, impact, mitigation, evidence                                                                | Requirements/architecture/spec/plan/runbook improvements              | Stage 05 reviewed learning artifact                             | `operations/postmortem.template.md` → incident-folder `postmortem.md`                                                                                         | Google SRE defines a reviewed, blameless record of impact, mitigation, root causes, and preventive actions.                                                                                                                                                                                                                                                                                                                                                                                                  |
| Release           | What real release event occurred, which artifacts, validation, approvals, rollout or rollback evidence support it, and what was the outcome? | A release event has immutable artifact and outcome evidence; a changelog or readiness check alone is insufficient | Release owner / Operations/SRE                                  | Completed Specs/Plans/Tasks, artifact identifiers, approvals, compatibility/readiness inputs, rollout evidence | Users, operators, audits, later releases and incidents                | Stage 05 release event record, distinct from deployment runtime | `operations/release.template.md` → `docs/05.operations/releases/YYYY-MM-DD-release-name.md`; `CHANGELOG.md` and release runbook remain inputs/adjacent owners | GitHub Releases and deployment history illustrate distinct release/deployment evidence; repo-local approval and runtime remain canonical.                                                                                                                                                                                                                                                                                                                                                                    |
| Reference         | What stable, source-backed context helps active work without owning decisions or procedures?                                                 | Durable facts, inventory, glossary, or research context is needed                                                 | Documentation maintainer / subject owner                        | Primary sources and tracked current evidence                                                                   | Active stages, authors, reviewers                                     | Supporting Stage 90 context                                     | `common/reference.template.md` → `docs/90.references/`                                                                                                        | Repo-template basis; external sources support each reference's facts but do not make the reference policy.                                                                                                                                                                                                                                                                                                                                                                                                   |
| Audit             | What was inspected, against which criteria, with what evidence, findings, severity, and disposition?                                         | A bounded current-state/compliance review is authorized                                                           | Auditor / subject reviewer                                      | Scope, criteria, tracked evidence, approved external benchmarks                                                | Canonical gap owners, Specs/Plans/Tasks                               | Supporting Stage 90 audit profile                               | `common/audit.template.md` → `docs/90.references/audits/`                                                                                                     | Repo-template basis. **Corrected 2026-08-07:** Audit is a first-class role with its own template and its own registered metadata profile, not a Reference-template variant. `docs/99.templates/support/template-selection.md:29` routes `docs/90.references/audits/**/*.md` to `common/audit.template.md`, and `docs/99.templates/support/document-metadata-profiles.yaml:410-416` registers a distinct `audit` profile sourced from it. Any external benchmark remains comparison unless adopted elsewhere. |
| Archive tombstone | What active document was removed, why, and what current replacement should be followed?                                                      | A whole document conflicts with current implementation and must leave the active chain                            | Documentation Specialist / Agentic Workflow Specialist          | Original path/status, archive reason, replacement                                                              | Maintainers and migration audit trail; active docs must not link back | Stage 98 tombstone; `status: archived` only                     | `common/archive.template.md` → `docs/98.archive/original-stage/original-path.md`                                                                              | Repo-template basis; a tombstone preserves migration traceability, not historical current truth.                                                                                                                                                                                                                                                                                                                                                                                                             |

## Instantiation Census

Counts are from the tracked tree at `HEAD` on 2026-08-07. Two counting rules
give different numbers for the operations buckets and both are recorded, because
conflating them is the most common source of drift in this pack.

| Role              | Leaf documents                          | All `*.md` including folder indexes       | Numbering observed                      | Path                                 |
| ----------------- | --------------------------------------- | ----------------------------------------- | --------------------------------------- | ------------------------------------ |
| PRD               | 25                                      | 26                                        | `001`-`025`, contiguous                 | `docs/01.requirements/`              |
| ARD               | 25                                      | 26                                        | `0001`-`0028` with `0015`-`0017` absent | `docs/02.architecture/requirements/` |
| ADR               | 25                                      | 26                                        | `0001`-`0028` with `0012`-`0014` absent | `docs/02.architecture/decisions/`    |
| Spec              | 59 directories, each with one `spec.md` | —                                         | `001`-`012` then `090`-`136`            | `docs/03.specs/`                     |
| Plan              | 101                                     | —                                         | dated                                   | `docs/04.execution/plans/`           |
| Task              | 130                                     | —                                         | dated                                   | `docs/04.execution/tasks/`           |
| Guide             | 66                                      | 88 (22 are folder indexes)                | tiered folders                          | `docs/05.operations/guides/`         |
| Policy            | 64                                      | 87 (23 are folder indexes)                | tiered folders                          | `docs/05.operations/policies/`       |
| Runbook           | 62                                      | 85 (23 are folder indexes)                | tiered folders                          | `docs/05.operations/runbooks/`       |
| **Incident**      | **0**                                   | 1, the README only                        | —                                       | `docs/05.operations/incidents/`      |
| **Postmortem**    | **0**                                   | none; the folder holds no incident packet | —                                       | incident-folder `postmortem.md`      |
| **Release**       | **0**                                   | 1, the README only                        | —                                       | `docs/05.operations/releases/`       |
| Reference         | 72                                      | 92                                        | —                                       | `docs/90.references/`                |
| Audit             | 34                                      | —                                         | —                                       | `docs/90.references/audits/`         |
| Archive tombstone | 20                                      | 21                                        | —                                       | `docs/98.archive/`                   |

### The Three Uninstantiated Templates

`incident.template.md`, `postmortem.template.md`, and `release.template.md`
have **zero** instantiated documents. `git ls-files 'docs/05.operations/incidents/*'`
and `git ls-files 'docs/05.operations/releases/*'` each return exactly one path,
the folder `README.md`. There is no `YYYY/INC-###-*/` packet anywhere in the
tree, so no postmortem can exist either, because
`document-metadata-profiles.yaml:392` scopes the postmortem profile to
`docs/05.operations/incidents/*/INC-*/postmortem.md`.

This is a measured fact about the corpus, not a defect claim. Three readings
are available and this reference does not choose between them:

1. **Nothing qualifying has happened.** No operational event has met the
   incident threshold and no release event has produced immutable artifact and
   outcome evidence. The templates are correctly idle.
2. **The threshold is unreachable in practice.** The Release row already
   requires artifact identifiers, digests, approvals, and rollout evidence
   before a record may exist. If no deployment pipeline produces those, the
   template can never be satisfied and is aspirational rather than operational.
3. **Events occurred but routed elsewhere.** Operational learning may be
   landing in Stage 04 task records or Stage 00 memory notes instead of the
   Stage 05 roles designed for it, which would make the incident and postmortem
   boundary described above unenforced in practice.

Distinguishing these requires evidence outside this document. What can be
stated from the tree alone is that three of the seven operations templates, and
both of the two roles that own operational learning, have never been exercised.

### ARD Has No External Basis

The `ARD` acronym as used in this repository is a **local coinage**. This was
re-verified on 2026-08-07 and the finding holds.

| Claim                                                                    | Status                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| An external convention named "Architecture Requirements Document" exists | **Not found.** No standard, framework, or widely cited practice defines this artifact under this name.                                                                                                                                                                                                                                                                                                                                  |
| "ARD" is in circulation as an acronym                                    | **Yes, but for something else.** It denotes an _Agile Requirements Document_, a planning-phase artifact used to seed the initial product backlog and described as conceptually similar to a Business Requirements Document. That artifact sits **above** a PRD in scope, not beneath it, which is the opposite of this repository's placement.                                                                                          |
| A standards analogue exists for the _role_                               | **Yes, under other names — but UNVERIFIED at primary source.** TOGAF is reported to define an _Architecture Requirements Specification_ deliverable giving quantitative, measurable criteria an implementation project must satisfy, as the companion to the qualitative Architecture Definition Document. The Open Group publication server requires SSO, so this was not read from the standard and must not be treated as normative. |
| A lightweight analogue exists                                            | **Yes.** arc42 places quality requirements in section 10, "Quality Requirements", and architecture decisions in section 9, "Architecture Decisions". One arc42 document therefore holds both concerns that this repository splits into ARD and ADR.                                                                                                                                                                                     |

Two consequences follow for authors:

- The repository ARD's closest external kin is TOGAF's Architecture
  Requirements Specification and arc42 section 10, not any document called an
  ARD. Cite those when an external framing is needed, and do not imply that
  "ARD" is an industry term.
- arc42 keeping sections 9 and 10 in one document shows the split is a choice,
  not a requirement. The 25 ARD and 25 ADR documents here are a deliberate
  separation of enduring constraint from point-in-time decision.

### ADR Practice Is Unanimous on Identity, Not on Storage

Re-verified 2026-08-07 against the primary sources.

| Property                   | Nygard, 2011-11-15                                                                       | MADR                                                                          | Repository state                                                                                                 |
| -------------------------- | ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Numbering                  | "ADRs will be numbered sequentially and monotonically. Numbers will not be reused."      | `NNNN-title-with-dashes.md`, a consecutive number, up to 9,999 per repository | Four-digit `NNNN-short-title.md` under `docs/02.architecture/decisions/`, matching MADR's form exactly           |
| Supersession               | "If a decision is reversed, we will keep the old one around, but mark it as superseded." | Optional status element including `superseded by ADR-0123`                    | `document-metadata-lifecycle.md` DML-04 requires a resolvable replacement ID and a link from the superseded body |
| Relocation on supersession | Not addressed explicitly; the instruction is to keep the old record                      | Not addressed explicitly                                                      | No ADR appears under `docs/98.archive/`; the archive stage holds only Stage 04 and Stage 05 paths                |

The often-repeated claim that an ADR is "never relocated to an archive" is a
sound **inference** from the keep-and-mark-superseded rule, but neither Nygard
nor MADR states it in those words. It is recorded here as an inference, not a
quotation. The repository's zero-ADR-tombstone state is consistent with it.

The numbering gaps are worth noting alongside this. ARD is missing
`0015`-`0017` and ADR is missing `0012`-`0014`. The two families are separate
sequences that each skipped a block, not one shared pool partitioned between
them: both occupy `0001`-`0011` and `0018`-`0028`.

Each folder README records its own occupied ranges and its own count.
`docs/02.architecture/requirements/README.md:58-60` states 25 leaves with
`0001`-`0014` and `0018`-`0026` occupied, and
`docs/02.architecture/decisions/README.md:58-60` states 25 leaves with
`0001`-`0011` and `0015`-`0026` occupied. Both self-reported counts match the
tracked tree exactly. What neither README records is _why_ those particular
blocks were skipped. Under Nygard's "numbers will not be reused" rule a gap is
correct behavior rather than corruption, so this is a provenance question, not
a defect.

## Analysis

The 20 rows form five ownership bands:

1. PRD, ARD, and ADR own intent and architecture rationale.
2. Spec plus API, agent, data, service, and test contracts own implementable technical
   and verification contracts.
3. Plan and Task separate intended sequencing from actual execution evidence.
4. Guide, Policy, Runbook, Incident, Postmortem, and Release separate use,
   controls, procedure, live state, learning, and executed-event evidence.
5. Reference, Audit, and Archive tombstone preserve supporting context,
   bounded findings, and migration traceability without becoming active truth.

Three boundaries are especially important. An ADR records why; a Spec records
what design results. A Policy states controls; a Runbook executes procedures.
An Incident records current chronology/state; a Postmortem is reviewed learning.
Crossing any of these boundaries weakens ownership and makes validation evidence
harder to interpret.

GitHub's content guidance begins with audience, purpose, and content type, while
Diataxis separates tutorial, how-to, reference, and explanation needs. Those
models support the repository's decision to keep role-specific documents and
link across them. They do not replace the richer PRD-to-Release lifecycle or
collapse Guide, Runbook, Reference, and research explanation into one type.

## Application Notes for This Workspace

- Choose the document by its primary question, then load its mapped template.
- Route a new gap to the earliest owner and link downstream consumers.
- Keep optional supporting contracts separate when their interface, agent, data,
  service, or test question is material.
- Put notable release communication in `CHANGELOG.md`, procedure in the release
  runbook, real event evidence in Release, and deployment runtime in its
  separately approved technical/operational chain.
- Keep Stage 90 references/audits advisory and Stage 98 tombstones out of the
  active link chain.
- Use the DML criterion IDs for metadata audits; do not infer metadata
  requirements from the role matrix's descriptive lifecycle column.
- Never describe `ARD` as an industry term. It is a local coinage; cite TOGAF's
  Architecture Requirements Specification or arc42 section 10 when an external
  framing is genuinely needed.
- Route audits to `common/audit.template.md`, not to the Reference template.

### Workspace Application: What to Investigate or Change Here

Each item is an investigation prompt with a named owner. None is approved work.

1. **Resolve the audit-role heading conflict.** The `reference` profile forbids
   `## Findings` while the `audit` profile requires it
   (`document-metadata-profiles.yaml:409` and `:414`). That separation is
   correct and should stay. The residual defect is the audit profile's
   forbidden-heading entry, `## Facts and Definitions`
   (`document-metadata-profiles.yaml:416`), which matches **zero** documents
   anywhere in `docs/90.references/`, while all 34 audit leaves carry
   `## Definitions / Facts`. The rule is vacuous as written. Investigate
   whether it should be retargeted, which would surface 34 violations, or
   deleted as dead. Owner: `docs/99.templates/support/document-metadata-profiles.yaml`.
2. **Repair the audit-template contradiction.** Three tracked files disagree
   about which template an audit uses. `template-selection.md:29` and
   `document-metadata-profiles.yaml:411` both name `common/audit.template.md`,
   but `docs/90.references/audits/README.md:80` still instructs authors that a
   new non-README reference in that folder follows the required sections of
   `common/reference.template.md`, and line 90 links the reference template as
   the folder's template. An author following the folder README would produce a
   document that the registered audit profile rejects, since the two profiles
   require disjoint heading sets. Owner: `docs/90.references/audits/README.md`.
3. **Decide the fate of the three uninstantiated templates.** Determine which
   of the three readings in the census above applies to incident, postmortem,
   and release. If reading 2 holds and the Release evidence bar is unreachable
   without a deployment pipeline, the template is aspirational and should say
   so. If reading 3 holds, operational learning is landing in Stage 04 and the
   incident/postmortem boundary needs enforcement, not just description.
   Owner: Stage 05 operations owner.
4. **Record the ARD/ADR numbering-gap provenance.** Six numbers are permanently
   unusable across the two families and no rationale is tracked. A one-line
   note in each folder README would close it. Owner: Stage 02 owners.
5. **Check whether the ARD role duplicates ADR context in practice.** arc42
   holds both concerns in one document, which means the split here must earn
   its cost. Sample ARDs and ADRs at the same tier and test whether the ARD
   states enduring constraints or is restating decisions. Owner: System
   Architect.
6. **Reconcile the guide/policy/runbook stage-matrix row.** The stage authoring
   matrix collapses all three into a single `05 operations` row while the
   validator enforces three distinct heading profiles with mutual
   forbidden-heading rules. The matrix under-describes an enforced separation.
   Owner: `docs/00.agent-governance/rules/stage-authoring-matrix.md`.

## Potential Follow-up / Gap

- Release now has a profile, template, selection route, and Stage 05 index, but
  no event leaf exists. Create one only after real event evidence exists. The
  same is true of incident and postmortem: three templates, zero instances.
- Deployment promotion, environment approval, artifact integrity, and tested
  rollback still require their own approved implementation chain; a Release
  template does not prove any of them.
- Formal ISO/NIST conformance or control mapping requires an approved policy,
  specification, and task rather than a Stage 90 role description.
- Optional supporting-contract adoption should remain feature-driven; a template
  does not prove that every feature needs every support file.

## Source Rules

- Repo-local roles come from the tracked stage matrix, documentation protocol,
  and template catalog.
- External sources were originally retrieved on `2026-07-10` and revalidated
  on `2026-07-11`. The canonical YAML, GitHub content/frontmatter, Diataxis,
  CommonMark/GFM, and GitHub release/deployment sources were re-opened on
  `2026-07-13`; mutable pages without a displayed update date prove only the
  content visible at the latest revalidation.
- ISO pages provide metadata and summaries rather than full standards.
- ISO/IEC/IEEE 12207:2017 is withdrawn and is not a current normative basis.
  The 2026-08-07 revalidation confirmed this from the ISO-operated
  `committee.iso.org` catalog after `www.iso.org` returned HTTP 403 to
  automated retrieval: record 63712 is at stage 95.99, withdrawal of an
  International Standard, and names ISO/IEC/IEEE 12207:2026 as its successor.
  ISO/IEC/IEEE 29148:2018 and 42010:2022 are both at stage 60.60 and remain
  current.
- A further revalidation ran on `2026-08-07` and added the ARD-basis, arc42,
  MADR, and Nygard findings. Two sources could not be read at their primary
  location and are labeled UNVERIFIED inline rather than dropped: the Open
  Group TOGAF publication server, which redirects to an SSO authorize endpoint,
  and `www.iso.org`, which returns HTTP 403 to automated retrieval. Nothing in
  either was disproven; both are simply unread.
- Repository counts in the census are derived from `git ls-files` against the
  tracked tree, so untracked local files cannot inflate them. Where a leaf count
  and an all-files count differ, both are shown, because folder `README.md`
  index files are the entire difference.
- External sources remain comparisons; repo-template bases are labeled explicitly.

## Sources

- [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md) - stage purpose, timing, owner, inputs, outputs, and templates
- [Documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md) - type-to-template and gap-routing contracts
- [SDLC templates](../../../99.templates/templates/sdlc/README.md) - PRD through Task template intent
- [Supporting contract templates](../../../99.templates/templates/spec-contracts/README.md) - API, agent, data, service, and test roles
- [Operations templates](../../../99.templates/templates/operations/README.md) - Guide through Postmortem roles
- [Common templates](../../../99.templates/templates/common/README.md) - Reference, Audit, Archive, content-archive, and README templates
- [Template selection](../../../99.templates/support/template-selection.md) - line 29 routes `docs/90.references/audits/**` to `common/audit.template.md`
- [Document metadata profiles](../../../99.templates/support/document-metadata-profiles.yaml) - lines 403-416 register separate `reference` and `audit` profiles with opposing `## Findings` rules
- [TOGAF Standard, Architecture Deliverables](https://pubs.opengroup.org/togaf-standard/architecture-content/chap04.html) - Architecture Requirements Specification as the quantitative companion to the Architecture Definition Document. **UNVERIFIED at primary source on 2026-08-07:** `pubs.opengroup.org` returns HTTP 302 to an `identity.opengroup.org` OAuth authorize endpoint for both the current and the TOGAF 9 deliverable pages, so the deliverable text was not read. The characterization above is secondary and must be confirmed against the standard before any normative use
- [arc42 section 9, Architecture Decisions](https://docs.arc42.org/section-9/) - recommends ADR and the Nygard structure; retrieved 2026-08-07
- [arc42 section 10, Quality Requirements](https://docs.arc42.org/section-10/) - architecture-level quality requirements held in the same document as decisions; retrieved 2026-08-07
- [MADR](https://adr.github.io/madr/) - `NNNN-title-with-dashes.md` naming, consecutive numbering, and `superseded by ADR-0123` status; retrieved 2026-08-07
- [SDLC document contract](../../../99.templates/support/sdlc-document-contract.md) - human family ownership and Release boundary
- [Common document contract](../../../99.templates/support/common-document-contract.md) - Reference, Audit, Archive, and repository-surface ownership
- [Audit references](../../audits/README.md) - audit-category role; lines 80 and 90 still route to the Reference template and contradict `template-selection.md:29`
- [GitHub Spec Kit documentation](https://github.github.com/spec-kit/) - Spec → Plan → Tasks → Implement artifacts
- [ISO/IEC/IEEE 12207:2017](https://www.iso.org/standard/63712.html) - withdrawn lifecycle-process metadata
- [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html) - requirements-engineering metadata
- [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html) - architecture-description metadata
- [ADR homepage](https://adr.github.io/) - single-decision record definition
- [Michael Nygard: Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) - original ADR practice
- [Google SRE incident management](https://sre.google/sre-book/managing-incidents/) - incident roles and state document
- [Google SRE postmortem culture](https://sre.google/sre-book/postmortem-culture/) - blameless reviewed learning
- [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) - incident-response CSF profile
- [PagerDuty runbook overview](https://www.pagerduty.com/resources/learn/what-is-a-runbook/) - repeatable operations procedure
- [Keep a Changelog 1.1.2](https://keepachangelog.com/en/1.1.2/) - changelog convention
- [Semantic Versioning 2.0.0](https://semver.org/) - version signal convention
- [GitHub Docs content best practices](https://docs.github.com/en/contributing/writing-for-github-docs/best-practices-for-github-docs) - audience, purpose, content-type, and scannability guidance
- [Diataxis](https://diataxis.fr/) - the site returns a Cloudflare bot
  challenge to automated clients; content was re-verified 2026-08-07 from the
  pinned upstream source, which is the current upstream head. See
  [documentation architecture](./documentation-architecture.md) - purpose separation across tutorial, how-to, reference, and explanation
- [GitHub deployments and environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments) - deployment approvals, restrictions, and environment evidence
- [GitHub deployment history](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/view-deployment-history) - deployment commits, environments, logs, URLs, and status history

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when the stage matrix, templates, or cited role sources change
- **Update Trigger**: Update when a document role, canonical owner, path, or lifecycle status changes

## Related Documents

- [research pack index](./README.md)
- [workspace baseline](./workspace-baseline.md)
- [spec-driven development and SDLC](./spec-driven-sdlc.md)
- [document metadata and lifecycle criteria](./document-metadata-lifecycle.md)
- [release management runbook](../../../05.operations/runbooks/00-workspace/release-management.md)
- [stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md)
- [documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md)
