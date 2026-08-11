---
status: draft
artifact_id: reference:agentic-engineering-research:spec-driven-sdlc
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-11
review_cycle: on-source-change
---

# Reference: Spec-Driven Development and SDLC

## Overview

Spec-driven development in this workspace is a traceable engineering lifecycle,
not the installation of a particular AI tool. Product intent, architecture,
technical contracts, prospective execution, observed execution, and operations
evidence remain separate artifacts with named owners. Implementation is
acceptable only when the applicable contract, change boundary, validation,
review, and evidence chain agree.

This analysis re-measured the current tree at Task 5 baseline
`0445a17860ac27f6bf5ff1f9a8ffcde32bc4f2ee`. It does not reuse the predecessor
pack's `59 specs / 0 archived specs` figure. The stale Graphify report was used
only as a navigation aid and every relationship below was corroborated against
tracked Stage 00, Stage 01-05, Stage 98, and Stage 99 sources.

## Purpose

Define REQ-06 and REQ-09: the workspace's spec-driven concepts, lifecycle,
traceability, gates, feedback, ownership, evidence, and enforcement boundaries.
The companion role reference owns document-by-document distinctions, while the
metadata reference owns profile and state semantics.

## Repository Role

This is advisory Stage 90 research. It explains current tracked contracts and
external comparisons; it does not approve a requirement, choose architecture,
authorize implementation, establish policy, execute a release, prove runtime
state, or change any Stage 00/99 contract. Canonical authority remains in the
stage matrix, documentation protocol, typed metadata registry, lifecycle
contracts, active Spec/Plan/Task chain, implementation, and validation evidence.

## Scope

### In scope

- The current Stage 01-05 lifecycle and Stage 90/98/99 support boundaries.
- Entry and exit evidence, feedback routing, validation, review, and ownership.
- Spec-driven tool comparison at immutable upstream revisions.
- Current active/archive counts and lifecycle-state distribution.

### Out of scope

- Adopting ISO, IETF, NIST, Spec Kit, OpenSpec, or another external method.
- Changing templates, metadata profiles, lifecycle transitions, stages, or archives.
- Starting services, observing private runtime state, or mutating remote controls.
- Treating a tracked workflow, tag, Release record, or Stage 90 statement as
  deployment/runtime proof.

## Definitions / Facts

### Working definition

Spec-driven development is the practice of making an explicit, reviewable
contract the controlling input to implementation and keeping bidirectional
traceability among intent, decisions, design, work, validation, and outcomes.
The contract must be specific enough to reject an implementation, not merely
describe it after the fact. In this workspace, that principle spans more than a
single `spec.md`: PRD, ARD/ADR, Spec and child contracts, Plan, Task evidence,
and Operations each own a different question.

The lifecycle is iterative rather than a one-way waterfall. A failed check,
incident, postmortem, release outcome, vulnerability, or verified drift routes
back to the earliest canonical owner whose truth must change. The downstream
artifact links the correction; it does not copy the upstream contract and
become a competing source of truth.

### Current corpus measurement

Counts below exclude `README.md` navigation files. They are path and parsed
frontmatter measurements, not claims that every legacy leaf has completed typed
metadata migration. Re-verified at the 2026-08-11 source-refresh boundary: the
totals below are one leaf higher than the Task 5 baseline because this pack's
own source-refresh Task added one `draft` Stage 04 Task leaf.

| Surface                            | Current measured result                                                     | Interpretation                                                                                                                                              |
| ---------------------------------- | --------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Stage 01-05 lifecycle leaves       | 532                                                                         | 25 requirements, 50 architecture, 30 Spec-stage, 235 execution, and 192 operations leaves.                                                                  |
| Lifecycle statuses in those leaves | 294 `active`, 235 `completed`, 3 `draft`                                    | Status exists across the measured active-stage corpus; `completed` remains durable evidence, not archive.                                                   |
| Current parent Specs               | 28 `docs/03.specs/*/spec.md`                                                | Replaces the predecessor's stale active-Spec count.                                                                                                         |
| Archived parent Specs              | 32 `docs/98.archive/**/spec.md`                                             | Archive is populated after the 2026-08-08 migration; zero is false.                                                                                         |
| Stage 98 non-README leaves         | 52, all `status: archived`                                                  | Includes 32 typed archive leaves and 20 legacy tombstones without `artifact_type`; path/profile evidence and typed-field evidence must remain distinct.     |
| Stage 99 Markdown                  | 43 total, 35 non-README                                                     | Template/support corpus; 24 non-README sources declare `status: draft`, while support contracts are governance sources rather than copied target artifacts. |
| Current role paths                 | PRD 25; ARD 25; ADR 25; Plan 103; Task 132; Guide 66; Policy 64; Runbook 62 | Role counts are derived from canonical paths. Legacy `artifact_type` coverage is incomplete and cannot replace path measurement.                            |
| Event roles                        | Incident 0; Postmortem 0; Release 0                                         | Registered templates/profiles are not proof that an event occurred or that the contracts have been exercised by a real target.                              |

The measured status total is deliberately not called an "active document"
count: `active`, `completed`, and `draft` are different lifecycle states, yet
all 532 leaves still reside in current Stage 01-05 paths. Likewise, Stage 98
tombstones preserve provenance and are not current guidance.

### Lifecycle and gates

```text
stakeholder intent
  -> PRD
  -> ARD + decision-specific ADRs
  -> parent Spec + focused child contracts
  -> prospective Plan
  -> Task implementation/validation/review evidence
  -> Operations and evidenced Release events
  -> feedback to the earliest owner that must change
```

| Transition                                        | Entry evidence                                                                 | Owner and exit evidence                                                                                            | Gate and failure route                                                                                                    |
| ------------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| Intent -> PRD                                     | Stakeholder problem, users, value, constraints, and verified current state     | Product owner; numbered PRD with testable requirements, scope, success criteria, and links                         | Human approval plus template/metadata/repository checks; ambiguity returns to intent.                                     |
| PRD -> ARD/ADR                                    | Approved intent and current architecture constraints                           | System Architect; enduring boundaries/quality attributes plus one ADR per significant choice                       | Architecture review and traceability; infeasibility returns to PRD, while a changed decision creates/supersedes an ADR.   |
| ARD/ADR -> Spec                                   | Approved upstream constraints and applicable implementation evidence           | Engineering owner; implementable behavior, interfaces, failure modes, verification, and optional focused contracts | Spec and contract checks; gaps return to the earliest requirement/architecture owner.                                     |
| Spec -> Plan                                      | Stable technical contract and known dependencies                               | Engineering/Project Lead; prospective sequence, risk, intended checks, rollback, and completion criteria           | Plan review and traceability; no executed-result claim belongs here.                                                      |
| Plan -> Task evidence                             | Approved scope, authority, baseline, dependencies, and approvals               | Implementer/QA; actual changes, commands/results, impact, reviews, commits, deferrals, and blockers                | Focused checks and independent review; failure returns to Task implementation or an earlier contract.                     |
| Task -> Operations/Release                        | Completed implementation evidence and operator/release impact                  | Operations/Release owner; changed guidance/control/procedure or a real release-event record                        | Runtime-specific checks and event evidence; a document, tag, changelog, or CI definition alone does not prove deployment. |
| Incident/Postmortem/QA/Security -> earliest owner | Observed impact, reviewed learning, failed validation, vulnerability, or drift | Owner selected by gap-to-stage routing; corrected PRD/ARD/ADR/Spec/Plan/Task/Operations artifact                   | Re-run the applicable gate and retain the causal evidence; Stage 90 analysis cannot close the loop.                       |

### Traceability model

Traceability has four distinct forms that must agree:

1. `artifact_id`, `artifact_type`, `parent_ids`, and `supersedes` encode typed
   identity and direct relations where the target profile admits them.
2. Human `Related Documents` links explain the broader upstream/downstream
   context; they are not a substitute for direct typed parents.
3. Requirement IDs, acceptance criteria, verification cases, Task evidence,
   and commit identities connect intended behavior to observed results.
4. Runtime or remote claims require an authorized observation of the named
   target and time. Tracked files prove definitions/configuration only.

Broken or ambiguous traceability fails closed. An author must not invent a
parent, infer priority from `parent_ids` order, or copy a requirement into a
later artifact merely to make a check pass.

### Enforcement layers

| Layer                                     | What it establishes                                                                                   | What it cannot establish                                                                   |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Stage and role contracts                  | Canonical question, path, owner, template, consumer, and evidence duty                                | That a target followed the contract or was approved.                                       |
| Metadata registry and checker             | Profile match, fields, relations, headings, lifecycle transitions, and changed/new blocking semantics | Product correctness, runtime state, or remote enforcement.                                 |
| Specs and child contracts                 | Implementable behavior and verification criteria                                                      | That implementation or tests passed.                                                       |
| Plans and Tasks                           | Intended work versus observed work/evidence                                                           | That a remote CI rule, provider, deployment, or service executed unless directly observed. |
| Focused validation and independent review | Reproducible local results and a bounded verdict over an exact range                                  | Universal correctness beyond the reviewed inputs and environment.                          |
| CI/workflow configuration                 | A tracked automation definition                                                                       | A successful run, required-check configuration, branch protection, or production outcome.  |
| Release/operations evidence               | A bounded event or operating contract                                                                 | Deployment/runtime proof outside the separately evidenced chain.                           |

### External implementations and standards boundary

| Source                                                            | Verified observation                                                                                                                                                         | Workspace disposition                                                                                                                                                                   |
| ----------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GitHub Spec Kit at `684b3d8e05263a7c1948d3d0699ab1cb4f77c3d5`     | Current core flow is `Spec -> Plan -> Tasks -> Implement`; Markdown artifacts feed subsequent phases and optional analysis/checklists add gates.                             | Useful comparative harness, not installed lifecycle authority. This workspace adds explicit PRD/architecture prefixes, durable Task evidence, operations, archive, and feedback owners. |
| Fission-AI OpenSpec at `e50bd0983dc8dc48250e3181f36e28450542f2ab` | A change folder contains `proposal.md`, `specs/`, `design.md`, and `tasks.md`; archive moves it under `openspec/changes/archive/` and updates live Specs.                    | Its live-spec/in-flight-change split resembles durable Spec versus execution evidence, but its paths, commands, and archive semantics are not adopted.                                  |
| ISO/IEC/IEEE 12207:2026                                           | Public catalog says it covers conception through retirement and permits concurrent, iterative, recursive, and incremental application without requiring one lifecycle model. | Catalog/abstract comparison only. Purchased full text was not accessed and is **UNVERIFIED**; no conformance claim is made.                                                             |
| ISO/IEC/IEEE 29148:2018 and 42010:2022                            | Public catalogs describe requirements-engineering information items and architecture descriptions.                                                                           | Context for PRD/architecture analysis only. Purchased full text was not accessed and is **UNVERIFIED**.                                                                                 |
| RFC Editor                                                        | Official home and archive for RFCs, including Standards and Best Current Practices.                                                                                          | Example of a governed publication series, not a template or lifecycle owner for this repository.                                                                                        |

### Feedback and evidence rules

- A validation failure changes Task evidence first; revise a Spec only when the
  failure demonstrates that the technical contract is wrong or incomplete.
- An incident owns live event state. A Postmortem owns reviewed causal learning
  and preventive actions after stabilization.
- A vulnerability can route to Policy, ADR, Spec, Plan, Task, Runbook, or all of
  them through links, but each fact has one earliest canonical owner.
- A Release record requires actual event evidence and remains distinct from
  deployment/runtime proof. Release notes, SemVer, a tag, a successful build,
  and readiness evidence each prove only their own fact.
- A reference, audit, graph, generated index, or template may inform work but
  cannot authorize a lifecycle transition or protected mutation.

## Scope Implications

| Scope          | Application and disposition                                                                                                                                                          |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `agentic`      | Agents must load the applicable contract, preserve stage ownership, use bounded loops, record evidence, and stop on missing authority; automation does not collapse lifecycle roles. |
| `architecture` | Architecture constraints belong in ARDs and significant choices in ADRs before Specs consume them; runtime architecture remains separately evidenced.                                |
| `backend`      | API, data, failure, and service behavior requires a parent Spec and focused contracts/tests where complexity warrants them.                                                          |
| `common`       | Shared standards and review conventions support every gate but cannot create a parallel lifecycle or bypass canonical owners.                                                        |
| `docs`         | Owns template-first authoring, metadata/link validation, archive boundaries, and Stage 90 advisory framing; Stage 01-99 writes still require explicit scope.                         |
| `entry`        | Gateway changes route through requirements, architecture, Spec, Task, and operations evidence with explicit runtime/rollback boundaries.                                             |
| `frontend`     | UI behavior, accessibility, state, and browser evidence follow the same Spec-to-Task chain; generated UI is not accepted from screenshots or prompts alone.                          |
| `infra`        | Compose and infrastructure definitions are implementation evidence and require Spec, validation, rollback, and operations handoff; they are not the SDLC owner.                      |
| `meta`         | The registry, templates, validators, and taxonomy encode lifecycle semantics; changes require their own approved metadata/docs chain rather than edits in this reference.            |
| `mobile`       | No current mobile implementation is established; any future work needs an approved product/architecture/Spec chain plus device-specific evidence.                                    |
| `ops`          | Owns guides, policies, runbooks, incidents, postmortems, and releases; event evidence feeds upstream owners without turning operations prose into product intent.                    |
| `product`      | Human stakeholders own intent, value, scope, requirements, and acceptance; an agent or external tool cannot infer approval.                                                          |
| `qa`           | Owns verification strategy, focused evidence, failure routing, and independent quality review; a passing local check is bounded to its command/environment.                          |
| `security`     | Security requirements, decisions, controls, tests, incidents, and remediation remain traceable with least privilege, redaction, and approval boundaries.                             |

## Sources

| Source                                                                                                                                | Accessed   | Class                      | Use and verification state                                                                       |
| ------------------------------------------------------------------------------------------------------------------------------------- | ---------- | -------------------------- | ------------------------------------------------------------------------------------------------ |
| [GitHub Spec Kit documentation](https://github.github.com/spec-kit/)                                                                  | 2026-08-08 | External mutable           | HTTP 200; current phase flow and artifact handoff.                                               |
| [GitHub Spec Kit immutable tree](https://github.com/github/spec-kit/tree/684b3d8e05263a7c1948d3d0699ab1cb4f77c3d5)                    | 2026-08-08 | External fixed             | `git ls-remote` HEAD pin plus immutable repository content.                                      |
| [OpenSpec immutable README](https://raw.githubusercontent.com/Fission-AI/OpenSpec/e50bd0983dc8dc48250e3181f36e28450542f2ab/README.md) | 2026-08-08 | External fixed             | Change artifacts, live Specs, apply/archive flow, and immutable pin.                             |
| [ISO/IEC/IEEE 12207:2026 catalog](https://www.iso.org/standard/90219.html)                                                            | 2026-08-08 | External catalog           | Public status/abstract accessible; purchased standard text **UNVERIFIED**.                       |
| [ISO/IEC/IEEE 29148:2018 catalog](https://www.iso.org/standard/72089.html)                                                            | 2026-08-08 | External catalog           | Public status/abstract accessible; purchased standard text **UNVERIFIED**.                       |
| [ISO/IEC/IEEE 42010:2022 catalog](https://www.iso.org/standard/74393.html)                                                            | 2026-08-08 | External catalog           | Public status/abstract accessible; purchased standard text **UNVERIFIED**.                       |
| [RFC Editor](https://www.rfc-editor.org/)                                                                                             | 2026-08-08 | External mutable catalog   | HTTP 200; official RFC series and publication classes only.                                      |
| [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final)                                                                | 2026-08-08 | External fixed             | HTTP 200; April 2025 final CSF 2.0 incident-response profile. Rev. 2 is superseded and not used. |
| [Google SRE postmortem culture](https://sre.google/sre-book/postmortem-culture/)                                                      | 2026-08-08 | External fixed publication | HTTP 200; learning, triggers, blamelessness, review, and preventive actions.                     |
| [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md)                                                | 2026-08-08 | Workspace tracked          | Canonical stage purposes, inputs, templates, and done criteria at Task 5 baseline.               |
| [SDLC document contract](../../../99.templates/support/sdlc-document-contract.md)                                                     | 2026-08-08 | Workspace tracked          | Human lifecycle and feedback boundary.                                                           |
| [Metadata profiles](../../../99.templates/support/document-metadata-profiles.yaml)                                                    | 2026-08-08 | Workspace tracked          | Sole machine owner for typed profiles and transitions.                                           |
| [Graphify report](../../../../graphify-out/GRAPH_REPORT.md)                                                                           | 2026-08-08 | Workspace stale/advisory   | Built from `f8a72211`; all used claims corroborated against current tracked sources.             |

## Maintenance

Re-measure counts and re-open mutable sources when stages, templates, metadata
profiles, lifecycle/archive contracts, validator behavior, Spec Kit, OpenSpec,
or official standard status changes. Keep current-path counts separate from
typed-metadata coverage and never infer runtime, remote, release, or deployment
outcomes from tracked documentation alone.

## Related Documents

- [Verification and validation](./verification-validation.md)
- [SDLC document roles](./sdlc-document-roles.md)
- [Document metadata lifecycle](./document-metadata-lifecycle.md)
- [Workspace baseline](./workspace-baseline.md)
- [Scope application matrix](./scope-application-matrix.md)
- [Execution Task](../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md)
