---
status: active
artifact_id: reference:agentic-research:spec-driven-sdlc
artifact_type: reference
parent_ids: [spec:123-agentic-engineering-audit-remediation]
reviewed_at: 2026-08-07
review_cycle: on-source-change
---

<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/spec-driven-sdlc.md -->

# Reference: Spec-Driven Development and SDLC

## Overview

This reference explains the tracked `hy-home.docker` lifecycle from intent
through release and operations. It records the owner, entry and exit evidence,
validation gate, feedback loop, and external comparison for every transition.

## Purpose

Make the workspace's spec-driven lifecycle explicit without substituting an
external tool workflow, Compose runtime, CI pipeline, or secure-development
framework for the active Stage 01-05 document chain.

## Repository Role

This Stage 90 reference interprets the active stage taxonomy defined by
`stage-authoring-matrix.md`. The matrix, active stage artifacts, tracked
runtime, and validators remain authoritative. This document creates no policy,
specification, plan, task, release procedure, or framework adoption.
Document-type responsibility is canonical in
[`sdlc-document-roles.md`](./sdlc-document-roles.md), while metadata and
transition semantics are canonical in
[`document-metadata-lifecycle.md`](./document-metadata-lifecycle.md). This file
owns only the end-to-end transition flow and does not duplicate those criteria.

## Scope

### In Scope

- Intent, requirements, architecture, specification, execution, and operations transitions
- Entry/exit evidence and validation for every transition
- Incident, postmortem, eval, QA, and security feedback
- Compose, CI, and secure SDLC as lifecycle participants
- Comparison with official or original SDLC/document-role sources

### Out of Scope

- Replacing the Stage 01-05 taxonomy with GitHub Spec Kit
- Formal ISO, NIST SSDF, or incident-framework adoption
- Runtime Compose, workflow, template, script, or policy changes
- Provider model and capability inventories

## Definitions / Facts

- **Intent** is stakeholder need, problem framing, constraint, or verified
  feedback that may trigger a Stage 01 PRD.
- **Entry evidence** is the approved, tracked input required before a transition.
- **Exit evidence** is the tracked artifact or verified result produced by the transition.
- **Validation gate** is the repository check or human approval proving the
  transition contract; a command listed here does not imply it always applies to
  every change type.
- **Feedback** is evidence routed to the earliest lifecycle owner that must
  change. An incident or failed check is not itself a new requirement.
- **External comparison** describes similarity or difference only. It is not an
  adopted workspace rule.

## Lifecycle Flow

```text
intent → PRD → ARD/ADR → Spec → Plan → Task/Evidence → Operations/Release
       ↖ incident/postmortem learning + eval/QA/security feedback ↙
```

### Transition Evidence Matrix

| Transition                                                                          | Repo-local owner                                                                           | Entry evidence                                                                                            | Exit evidence                                                                                                       | Validation gate                                                                                                        | Feedback loop                                                                                       | External comparison                                                                                                                                                                                                                               |
| ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| intent → PRD                                                                        | Product Manager; `docs/01.requirements/`                                                   | Stakeholder need, problem, constraints, existing policy/runtime evidence                                  | Numbered PRD with users, scope, requirements, success criteria, and downstream links                                | PRD template review and `bash scripts/validation/check-repo-contracts.sh`                                              | Rejected or ambiguous requirements return to intent clarification                                   | ISO 29148:2018 provides requirements-engineering metadata; the public page is not full standard text. GitHub Spec Kit begins at a specification, while this workspace preserves an earlier product-intent artifact.                               |
| PRD → ARD/ADR                                                                       | System Architect; `docs/02.architecture/requirements/` and `decisions/`                    | Approved PRD plus current architecture/runtime constraints                                                | ARD boundaries/quality attributes and ADRs for non-trivial choices, alternatives, and consequences                  | Architecture templates, PRD links, and repository-contract validation                                                  | Architecture infeasibility or trade-off evidence can revise the PRD or create a new ADR             | ISO 42010:2022 frames architecture description; ADR practice records one decision and rationale. The repo ARD is narrower than a full 42010 architecture description.                                                                             |
| ARD/ADR → Spec                                                                      | Implementing engineer; `docs/03.specs/NNN-feature-id/`                                     | PRD, ARD, applicable ADRs, current implementation evidence                                                | Parent `spec.md` plus optional API, agent, data, service, test, or machine-readable contracts                       | Spec/template traceability, `check-repo-contracts.sh`, and applicable contract checks                                  | Interface ambiguity, failed feasibility, or security review returns to architecture/requirements    | GitHub Spec Kit makes a specification an executable-context anchor; this workspace retains explicit product and architecture predecessors.                                                                                                        |
| Spec → Plan                                                                         | Project or Engineering Lead; `docs/04.execution/plans/`                                    | Stable spec and supporting contracts with verification criteria                                           | Sequenced plan with scope, risks, commands, rollback/recovery, and done criteria                                    | Plan-template review, `check-doc-traceability.sh`, and repository contracts                                            | Planning gaps return to the spec or an earlier owner instead of being hidden in tasks               | Spec Kit's Plan phase feeds later tasks; Kiro's `tasks.md` and OpenSpec's `tasks.md` occupy the same position. ISO 12207:2017 is withdrawn and superseded by 12207:2026; neither edition was read, so no 12207 lifecycle claim supports this row. |
| Plan → Task/Evidence                                                                | Implementation and QA engineers; `docs/04.execution/tasks/`                                | Approved plan, scoped task brief, clean baseline, and required approvals                                  | Current task state, changed-file record, validation results, deviations, reviews, and logical commit evidence       | Task-specific checks plus `git diff --check`, traceability, alignment, and repository contracts as applicable          | Failed implementation/QA/security evidence returns to the owning spec, plan, or task                | Spec Kit separates Plan, Tasks, and Implement. The workspace combines implementation status and auditable evidence in Stage 04 task records.                                                                                                      |
| Task/Evidence → Operations/Release                                                  | Documentation Specialist and Operations/SRE; `docs/05.operations/`, root `CHANGELOG.md`    | Completed implementation evidence, operator impact, release scope, and rollback/recovery needs            | Updated guide/policy/runbook/incident linkage and human-readable release notes when applicable                      | `check-doc-implementation-alignment.sh`, repository contracts, applicable runtime checks, and tag-time changelog check | Operational validation or release failure returns evidence to the task/plan/spec owner              | PagerDuty frames runbooks as repeatable procedures; Keep a Changelog and SemVer frame human release communication/version signals. They do not prescribe this repo's release gate.                                                                |
| incident/postmortem + eval/QA/security feedback → intent or earliest affected owner | Operations/SRE, QA, Security, then Product/Architecture/Spec owner selected by gap routing | Incident state, reviewed postmortem, eval result, failed check, vulnerability evidence, or verified drift | New/changed intent, requirement, decision, spec, plan, task, or operations artifact at the earliest canonical owner | Incident/postmortem templates, gap routing, relevant validator rerun, and required human approval                      | Closed-loop learning is complete only when preventive action has an owner and verification evidence | Google SRE separates live incident state from reviewed blameless postmortems; NIST SP 800-61 Rev. 3 frames incident response in CSF 2.0; NIST SSDF v1.1 supplies high-level secure-development feedback practices.                                |

## Lifecycle Participants, Not Replacements

| Participant                     | Lifecycle contribution                                                                                                         | Evidence boundary                                                                                                            | Why it is not the lifecycle owner                                                                                                          |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Docker Compose / infrastructure | Supplies current implementation/runtime evidence and validation targets for architecture, specs, tasks, and operations.        | `docker-compose.yml`, `infra/**`, version registry, Compose validation, and hardening checks are tracked runtime evidence.   | Compose describes deployable configuration; it does not own user intent, architecture rationale, execution planning, or incident learning. |
| CI / GitHub Actions             | Runs repeatable validation and reports job/step evidence at task and release gates.                                            | Tracked workflow YAML proves definitions; it does not by itself prove remote required-check enforcement or a successful run. | A pipeline verifies artifacts but does not replace the PRD, ADR, spec, plan, task, or operations document that owns the decision/evidence. |
| Secure SDLC / NIST SSDF         | Provides an external practice lens for organizational, software-protection, production, and vulnerability-response activities. | NIST SP 800-218 v1.1 is a high-level framework dated February 2022; no formal repo control mapping is adopted here.          | A framework comparison does not create workspace policy or supersede the Stage 00 security scope and active stage documents.               |

## External Comparison

- **GitHub Spec Kit** currently presents `Spec → Plan → Tasks → Implement`
  and says each Markdown artifact feeds the next. The workspace adopts no Spec
  Kit runtime; it has a broader `intent → PRD → ARD/ADR` prefix and an
  operations/release plus feedback suffix.
- **ISO/IEC/IEEE 29148:2018** is published and marked “to be revised”; it supports
  requirements-engineering framing only.
- **ISO/IEC/IEEE 42010:2022** is published and supports architecture-description
  framing. The workspace ARD covers architecture requirements and quality
  attributes, not full conformance.
- **ISO/IEC/IEEE 12207:2017** is withdrawn and now has a published successor.
  The IEEE SA catalog record for IEEE/ISO/IEC 12207-2026 shows board approval
  on 2026-02-12, publication on 2026-04-15, and a `Superseding` entry naming
  `12207-2017`; the ISO catalog number for the new edition is 90219. Neither
  edition was read: both are paywalled and `www.iso.org` returns HTTP 403 to
  automated retrieval. Only catalog status metadata is cited here, and no 12207
  text is used for or against any workspace structure.
- **ADR practice** uses a record for one decision, its rationale, trade-offs,
  and consequences; Michael Nygard's original article is dated 2011-11-15.
- **NIST SSDF v1.1** and **NIST SP 800-61 Rev. 3** are comparison frameworks,
  not adopted controls. The latter is dated April 2025 and supersedes Rev. 2.

## Concrete Spec-Driven Implementations

Four named implementations were re-verified on 2026-08-07. Each is described by
what it actually prescribes on disk, because that is the only part comparable
with a repository lifecycle.

| Implementation          | Prescribed artifacts                                                                                                                                                  | Placement on disk                                                                                                                                      | Durability contract                                                                                                                                                                                                                                                   | Distance from this workspace                                                                                                                                                                                                             |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **GitHub Spec Kit**     | `spec.md`, `plan.md`, `tasks.md`, plus optional `data-model.md`, `research.md`, `quickstart.md`, and a `contracts/` directory; project-level `memory/constitution.md` | One branch-scoped folder per feature, `specs/[branch-name]/`, created automatically from a semantic branch name generated from the feature description | The published `spec-driven.md` frames specifications as "the primary artifact" and does not prescribe deletion. Böckeler's independent analysis records uncertainty about long-term retention and classes Spec Kit as spec-first rather than spec-anchored over time. | Spec Kit starts at a specification. This workspace has an explicit product and architecture prefix (`docs/01.requirements/`, `docs/02.architecture/`) that Spec Kit routes into a constitution instead.                                  |
| **AWS Kiro**            | `requirements.md`, `design.md`, `tasks.md`; requirements use EARS notation                                                                                            | One feature folder per spec under `.kiro/specs/`                                                                                                       | Böckeler records that after implementation "the specs are deleted, and during evolution a new spec is created that describes the change".                                                                                                                             | The closest structural analogue to `docs/01` → `docs/02` → `docs/04`, but with the opposite durability contract: this workspace keeps every stage artifact tracked.                                                                      |
| **Fission-AI OpenSpec** | Durable `openspec/specs/` holding requirements and scenarios; ephemeral `openspec/changes/<change>/` holding `proposal.md`, `specs/`, `design.md`, `tasks.md`         | Two separate roots, not one co-located folder                                                                                                          | On completion the change folder moves to `openspec/changes/archive/<date>-<name>/` and the durable specs are updated.                                                                                                                                                 | The only surveyed implementation that separates durable contract from ephemeral change, which is the same split this workspace makes between Stage 03 specs and Stage 04 plans/tasks. Its archive-on-completion rule parallels Stage 98. |
| **Tessl**               | Not inspected directly in this revalidation                                                                                                                           | Not inspected                                                                                                                                          | Böckeler places it at the spec-as-source end, where the spec is the main source file over time and only the spec is human-edited.                                                                                                                                     | No workspace analogue. This repository never treats a spec as the compiled source of its runtime.                                                                                                                                        |

Böckeler's article separates three ascending levels of commitment rather than
one binary: **spec-first** writes the spec before code, **spec-anchored**
maintains the spec across feature evolution, and **spec-as-source** makes the
spec the main edited artifact over time.

By that taxonomy this workspace is **spec-anchored**, not spec-as-source. Stage
03 specs persist and are revised rather than discarded, Stage 04 tasks carry
execution evidence against them, and code and Compose configuration remain the
edited runtime truth. The workspace also anchors above the specification, which
none of the four implementations does: Stage 01 PRDs and Stage 02 ARD/ADR
records own intent and architecture rationale that Spec Kit compresses into a
constitution and that Kiro and OpenSpec do not model at all.

### Repository Evidence for the Spec-Anchored Claim

Counts are from the tracked tree at `HEAD` on 2026-08-07 and exclude folder
`README.md` files.

| Fact                                 | Measured value                                                   | Derivation                                                                                                             |
| ------------------------------------ | ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Feature spec directories             | 59                                                               | `git ls-files 'docs/03.specs/*/spec.md'`                                                                               |
| Spec numbering                       | `001`-`012` then `090`-`136`, with a reserved gap at `013`-`089` | directory listing of `docs/03.specs/`                                                                                  |
| Execution plans                      | 101                                                              | `docs/04.execution/plans/` leaves                                                                                      |
| Execution tasks                      | 130                                                              | `docs/04.execution/tasks/` leaves                                                                                      |
| Spec tombstones in the archive stage | 0                                                                | `docs/98.archive/` holds 21 files, all under `04.execution/` and `05.operations/`; no `03.specs/` subtree exists there |

The zero-archival result is the operative difference from Kiro. A completed
spec here changes `status` in place and stays in the active chain; it is not
deleted and not relocated.

## Analysis

The lifecycle is spec-driven but not spec-only. Intent and architecture constrain
the specification; plans sequence it; tasks carry implementation and validation
evidence; operations and release communicate and sustain the result. Feedback
does not jump directly into runtime mutation: it re-enters at the earliest owner
whose contract must change.

This makes validation evidence part of every transition without confusing
validation with ownership. Compose proves configuration behavior, CI automates
checks, and secure-SDLC sources offer comparison criteria, while active stage
documents continue to own requirements, decisions, contracts, sequencing, and
operations.

## Application Notes for This Workspace

- Select the earliest lifecycle owner before editing a downstream artifact.
- Require entry evidence before advancing and preserve failed-gate evidence in
  the active Stage 04 task.
- Keep incident chronology in the incident record and learning/action ownership
  in the postmortem.
- Distinguish tracked CI definitions from remote execution/enforcement evidence.
- Do not claim ISO, NIST, Spec Kit, SRE, PagerDuty, Keep a Changelog, or SemVer
  adoption from a Stage 90 comparison.
- Apply metadata and lifecycle audits through the stable DML criterion IDs in
  `document-metadata-lifecycle.md`, not ad hoc transition checks in this flow.

### Workspace Application: What to Investigate or Change Here

These are investigation prompts derived from the comparison above. None is an
approved change, and each needs its own Stage 03 or Stage 04 authorization.

1. **Decide whether the spec-anchored claim is enforced or merely observed.**
   Nothing in the tracked validators forbids deleting a completed spec; the
   durability contract is currently a convention, not a check. Investigate
   whether `docs/99.templates/support/corpus-migration-contract.md` already
   covers spec removal, and if so, cite it as the enforcement point instead of
   leaving the claim to observation.
2. **Examine the reserved spec-number gap `013`-`089`.** Seventy-seven spec
   numbers are unused between `012` and `090`. Determine whether that is a
   deliberate reservation with a recorded rationale or an artifact of an earlier
   renumbering. `document-metadata-lifecycle.md` DML-06 requires a
   reserved-number check; the gap is the largest live instance of it.
3. **Test the OpenSpec split against Stage 03/Stage 04.** OpenSpec's durable
   `specs/` versus ephemeral `changes/` separation is the closest external
   analogue to this workspace's Spec-versus-Plan/Task split. Investigate whether
   any Stage 03 spec currently carries change-shaped content that belongs in a
   plan, which is the failure mode that split is designed to prevent.
4. **Do not import a constitution.** Spec Kit's `memory/constitution.md` is the
   nearest analogue to `docs/00.agent-governance/`, but this workspace already
   has a richer, validator-backed governance stage. Any proposal to add a
   constitution file should be treated as duplication of Stage 00 and rejected
   unless it names a consumer Stage 00 cannot serve.

## Potential Follow-up / Gap

- A formal NIST SSDF-to-workspace control map requires separate approved
  security policy/spec/task work.
- Remote required-check and branch-protection evidence requires a separately
  authorized remote-state verification task.
- ISO 12207 now has a current edition (12207:2026, ISO record 90219) but it
  remains paywalled and unread. A future task needing normative lifecycle
  claims must acquire the text; catalog metadata alone can never support a
  structural claim.
- No surveyed spec-driven implementation models a product-intent artifact above
  the specification. If a future task wants external validation for the Stage 01
  PRD layer, it must look outside the SDD tool space, since Spec Kit, Kiro, and
  OpenSpec all begin at or below the specification.

## Source Rules

- Repo-local transitions are based on the tracked stage matrix, documentation
  protocol, templates, current stage artifacts, and validators.
- External sources were originally retrieved on `2026-07-10` and revalidated
  on `2026-07-11`; mutable pages without an update date prove only the content
  visible at the latest revalidation.
- A further revalidation ran on `2026-08-07`. Every non-ISO source cited below
  was re-requested and returned HTTP 200. The spec-driven implementation
  sources, the Böckeler analysis, and the 12207 successor metadata are new at
  that date.
- ISO pages expose metadata and short summaries, not the full standards.
  `www.iso.org` returns HTTP 403 to automated retrieval, so ISO record status
  for 12207 was corroborated from non-ISO catalogue publishers rather than read
  from `iso.org` directly. The 29148:2018 and 42010:2022 status claims retain
  their earlier retrieval provenance and were **not re-verified** on
  `2026-08-07`.
- No external comparison is adopted workspace policy by this reference.

## Sources

- [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md) - repo-local lifecycle owners and evidence
- [Documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md) - template, traceability, and routing contracts
- [GitHub Spec Kit documentation](https://github.github.com/spec-kit/) - current SDD phase flow; HTTP 200 on 2026-08-07
- [GitHub spec-driven guide](https://github.com/github/spec-kit/blob/main/spec-driven.md) - `specs/[branch-name]/` layout, `spec.md`/`plan.md`/`tasks.md`, and `memory/constitution.md`; read from the `main` raw source on 2026-08-07
- [Birgitta Böckeler, Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) - dated 2025-10-15; source of the spec-first / spec-anchored / spec-as-source levels and of the Kiro spec-deletion finding; HTTP 200 on 2026-08-07
- [Kiro specs documentation](https://kiro.dev/docs/specs/) - `requirements.md`, `design.md`, `tasks.md` under `.kiro/specs/`, with EARS requirement notation; HTTP 200 on 2026-08-07
- [Fission-AI OpenSpec](https://github.com/Fission-AI/OpenSpec) - durable `openspec/specs/` versus ephemeral `openspec/changes/`, archived to `openspec/changes/archive/<date>-<name>/` on completion; read from the `main` README on 2026-08-07
- [ISO/IEC/IEEE 12207:2017](https://www.iso.org/standard/63712.html) - withdrawn lifecycle-process metadata; **UNVERIFIED on 2026-08-07**, `www.iso.org` returns HTTP 403 to automated retrieval
- [ISO/IEC/IEEE 12207:2026 catalog record 90219](https://www.iso.org/standard/90219.html) - published successor; **UNVERIFIED directly**, HTTP 403 to automated retrieval
- [IEEE SA IEEE/ISO/IEC 12207-2026](https://standards.ieee.org/ieee/12207/11416/) - corroborating catalog record read on 2026-08-07: board approval 2026-02-12, published 2026-04-15, and a `Superseding` entry naming `12207-2017`. Catalog metadata only; the standard text was not read
- [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html) - requirements-engineering metadata
- [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html) - architecture-description metadata
- [ADR homepage](https://adr.github.io/) - single-decision record and rationale
- [Michael Nygard: Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) - original ADR article
- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) - workflow/job/step automation
- [NIST SP 800-218 SSDF v1.1](https://csrc.nist.gov/pubs/sp/800/218/final) - secure-development practice framework
- [Google SRE incident management](https://sre.google/sre-book/managing-incidents/) - roles and live incident state
- [Google SRE postmortem culture](https://sre.google/sre-book/postmortem-culture/) - reviewed blameless learning
- [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) - incident-response CSF profile
- [PagerDuty runbook overview](https://www.pagerduty.com/resources/learn/what-is-a-runbook/) - repeatable operational procedure
- [Keep a Changelog 1.1.2](https://keepachangelog.com/en/1.1.2/) - human-readable changelog convention
- [Semantic Versioning 2.0.0](https://semver.org/) - version signal convention

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when stage taxonomy, templates, validators, or cited lifecycle sources change
- **Update Trigger**: Update when a transition owner, evidence gate, or source status changes

## Related Documents

- [research pack index](./README.md)
- [workspace baseline](./workspace-baseline.md)
- [SDLC and operations document-type roles](./sdlc-document-roles.md)
- [document metadata and lifecycle criteria](./document-metadata-lifecycle.md)
- [quality, CI, and formatting](./quality-ci-formatting.md)
- [stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md)
- [documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md)
