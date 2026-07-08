---
status: active
---

<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/sdlc-document-roles.md -->

# Reference: SDLC and Operations Document-Type Roles

## Overview

This reference defines the role and purpose of each document type used across the
`hy-home.docker` SDLC and operations lifecycle: PRD, ARD, ADR, spec, plan, task,
guide, policy, runbook, incident, postmortem, and release documentation. For each
type it records what the document answers, when it is authored, who owns it, its
repo-local template and stage, and the external practice that anchors it.

The other files in this pack analyze the lifecycle as a flow of stages
(`spec-driven-sdlc.md`) and the quality gates that protect it
(`quality-ci-formatting.md`). This file complements them by treating each
document type as a distinct artifact with its own contract, so authors can answer
"which document am I writing, and what is it for?" without inferring the answer
from a stage-to-concern table.

## Purpose

Give authors and agents a single source-backed map of document-type intent so
that:

- The right template is selected for the right artifact.
- Content lands in the artifact that owns it (decisions in ADRs, procedures in
  runbooks, learning in postmortems) rather than blurring across types.
- External standards and community practices behind each type are traceable.

## Repository Role

This reference supports Stage 00 governance and the lifecycle across `docs/01`
through `docs/05`, `docs/90`, and `docs/99`. It restates and cites the authoring
intent already fixed by `stage-authoring-matrix.md` and the template READMEs; it
does not create new requirements, decisions, specifications, plans, or operations
procedures, and it does not override the matrix. Where this reference and an
active governance document differ, the governance document wins.

## Scope

### In Scope

- Role, purpose, authoring timing, and owner for each SDLC and operations
  document type
- Repo-local template and target-stage mapping for each type
- External standard or community practice that anchors each type
- The gap that release documentation has no dedicated template or stage home

### Out of Scope

- New PRD, ARD, ADR, spec, plan, task, or operations document authoring
- Active policy, runbook, incident timeline, or runtime config source of truth
- Changes to templates or to the stage-authoring matrix
- Adoption of any external standard as active policy

## Definitions / Facts

- **PRD (Product Requirements Document)**: Captures product need, users,
  requirements, and success criteria. Repo-local Stage 01, authored by a Product
  Manager at discovery and scope definition; template `sdlc/prd.template.md`,
  target `docs/01.requirements/NNN-<feature-or-system>.md`. As a requirements
  artifact it is anchored by requirements-engineering practice
  (ISO/IEC/IEEE 29148).
- **ARD (Architecture Requirements Document)**: Describes system or domain
  architecture boundaries and quality attributes derived from the PRD.
  Repo-local Stage 02 (`architecture/requirements`), authored by a System
  Architect after the PRD baseline; template `sdlc/ard.template.md`. It is an
  architecture description artifact in the sense standardized by
  ISO/IEC/IEEE 42010, scoped to the requirements/quality-attribute view rather
  than full architecture description.
- **ADR (Architecture Decision Record)**: Records a single architectural
  decision, its alternatives, and its consequences. Repo-local Stage 02
  (`architecture/decisions`), authored by a System Architect when a non-trivial
  trade-off is made; template `sdlc/adr.template.md`. The practice was
  popularized by Michael Nygard (2011) and is curated at `adr.github.io`.
- **Spec (Specification)**: Defines the technical design, interfaces, data
  contracts, and verification criteria for a feature or workspace change.
  Repo-local Stage 03, authored by an implementing engineer before tasks start;
  template `sdlc/spec.template.md` plus optional contract templates. Anchored by
  contract-first / executable-specification practice (OpenAPI, BDD).
- **Plan (Implementation Plan)**: Sequences approved implementation work with
  risks, verification commands, and completion criteria. Repo-local Stage 04
  (`execution/plans`), authored by a Project/Engineering Lead after specs are
  stable.
- **Task (Task Evidence)**: Tracks execution state, validation evidence, and
  gaps during implementation. Repo-local Stage 04 (`execution/tasks`), authored
  by the Implementation/QA Engineer during work; it is the auditable evidence
  record, not a plan.
- **Guide (Operations Guide)**: Explains usage context, common checks, and
  handoff to runbooks for a service or process. Repo-local Stage 05
  (`operations/guides`). A guide is oriented to understanding and routine use;
  it hands off step-by-step recovery to a runbook.
- **Policy (Operations Policy)**: Defines controls, exceptions, verification,
  and review cadence. Repo-local Stage 05 (`operations/policies`). A policy
  states the rules; a runbook states how to execute them.
- **Runbook**: Provides ordered execution steps, evidence, recovery, and
  escalation for a specific repeatable operation or incident response.
  Repo-local Stage 05 (`operations/runbooks`). Industry practice defines a
  runbook as step-by-step procedures for commonly repeated operations tasks,
  distinct from a policy (rules) and a broader playbook (multi-runbook response).
- **Incident (Incident Record)**: Records an active or resolved incident
  timeline and response state. Repo-local Stage 05
  (`operations/incidents/YYYY/INC-###-*`). Anchored by security incident-handling
  guidance (NIST SP 800-61) and SRE incident-management practice; it captures
  what happened and when, distinct from the learning artifact.
- **Postmortem**: Analyzes incident impact, root cause, action items, and
  prevention. Repo-local Stage 05, co-located with its incident as
  `postmortem.md`. Google SRE defines a postmortem as a written record of an
  incident, its impact, mitigation, root cause, and follow-up, produced under a
  blameless culture; it is a learning tool requiring review, not mere
  documentation.
- **Release documentation**: Communicates notable changes per version to
  humans (release notes / changelog), anchored by Keep a Changelog and Semantic
  Versioning. Repo-local status: **no dedicated template and no canonical stage
  home** exists today (see Potential Follow-up / Gap).

## Repo-local Document-Type Mapping

| Document   | Role (answers)                                                | Stage           | Owner                | Template                            |
| ---------- | ------------------------------------------------------------- | --------------- | -------------------- | ----------------------------------- |
| PRD        | What to build and why; users, requirements, success criteria  | 01              | Product Manager      | `sdlc/prd.template.md`              |
| ARD        | Architecture boundaries and quality attributes                | 02/requirements | System Architect     | `sdlc/ard.template.md`              |
| ADR        | One architectural decision, its alternatives and consequences | 02/decisions    | System Architect     | `sdlc/adr.template.md`              |
| Spec       | Technical design, interfaces, contracts, verification         | 03              | Impl Engineer        | `sdlc/spec.template.md`             |
| Plan       | Implementation sequencing, risks, verification, done criteria | 04/plans        | Project/Eng Lead     | `sdlc/plan.template.md`             |
| Task       | Execution state and validation evidence                       | 04/tasks        | Impl/QA Engineer     | `sdlc/task.template.md`             |
| Guide      | How to use and routinely check a service; runbook handoff     | 05/guides       | Doc Specialist / SRE | `operations/guide.template.md`      |
| Policy     | Controls, exceptions, verification, review cadence            | 05/policies     | Doc Specialist / SRE | `operations/policy.template.md`     |
| Runbook    | Ordered steps, evidence, recovery, escalation                 | 05/runbooks     | Operations/SRE       | `operations/runbook.template.md`    |
| Incident   | Incident timeline and response state                          | 05/incidents    | Operations/SRE       | `operations/incident.template.md`   |
| Postmortem | Impact, root cause, action items, prevention                  | 05/incidents    | Operations/SRE       | `operations/postmortem.template.md` |
| Release    | Notable changes per version for humans                        | — (none)        | —                    | — (gap)                             |

## Analysis

The repository's document types cluster into three intents. Intent-and-design
types (PRD, ARD, ADR, spec) fix what to build and how before code exists.
Execution types (plan, task) sequence the work and hold the evidence that it was
done and verified. Operations types (guide, policy, runbook, incident,
postmortem) govern and sustain the running system. This mirrors the external
lifecycle: requirements engineering feeds architecture description and decisions,
which feed specification and contract-first design, which feed implementation and
then operations and incident learning.

Two boundaries are worth stating explicitly because they are the most common
places content lands in the wrong artifact:

- **Decision vs. specification.** An ADR captures why a path was chosen and what
  it costs; a spec captures the resulting design. Rationale that drifts into a
  spec, or design that drifts into an ADR, breaks traceability.
- **Incident vs. postmortem.** The incident record is the contemporaneous
  timeline and state; the postmortem is the after-the-fact, blameless analysis
  and prevention plan. Google SRE treats them as separate artifacts for exactly
  this reason, and the repo co-locates them under one incident folder while
  keeping them as distinct files.

Guide, policy, and runbook form a deliberate triad: the policy sets the rules,
the guide explains routine use and hands off to procedures, and the runbook
carries the ordered recovery and escalation steps. Industry runbook practice
draws the same policy-versus-runbook line the repo templates already encode.

Release documentation is the one requested type with no repo-local home. There is
no `release.template.md` and no stage folder that owns per-version, human-readable
release notes. Conventional-commit history and CI provide raw change data, but a
curated changelog (the Keep a Changelog / Semantic Versioning practice) is a
distinct human-facing artifact that the current taxonomy does not template.

## Application Notes for This Workspace

- Select the document type first, then load its template from `docs/99.templates/`
  before authoring; the stage-authoring matrix row is the binding contract.
- Keep decision rationale in ADRs, technical design in specs, contemporaneous
  timeline in incident records, and blameless analysis in postmortems.
- Treat a guide as usage-and-handoff and a runbook as ordered recovery; do not
  merge them.
- Release notes currently have no template; until a decision is made, record any
  release-note content through an approved stage rather than inventing an
  untracked location.

## Potential Follow-up / Gap

- **Release documentation has no template or stage home.** A future governance
  decision (ADR) could either add a `release`/changelog template under
  `docs/99.templates/` mapped to a Stage 05 operations subfolder, or explicitly
  delegate release notes to an external changelog convention. Either path is a
  separate approved change, not part of this reference.
- Mapping incident and postmortem practice to a formal framework (NIST SP 800-61
  Rev. 3, which superseded the withdrawn Rev. 2, or SRE incident management)
  would require a separate approved policy or spec.
- The ARD-to-42010 relationship is partial: the repo ARD is scoped to
  architecture requirements and quality attributes, not a full 42010 architecture
  description. Any move toward fuller architecture-description conformance would
  be a separate decision.

## Source Rules

- Repo-local role, stage, owner, and template facts are taken from
  `stage-authoring-matrix.md` and the template READMEs, not inferred.
- External standard pages provide framing only; public metadata is not full
  access to the standard text.
- Re-check product-documentation and SRE sources before using them for current
  decisions, and prefer the current revision (for example NIST SP 800-61 Rev. 3
  over the withdrawn Rev. 2).

## Sources

- [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md) - repo-local per-stage purpose, timing, persona, template, done criteria
- [SDLC templates README](../../../99.templates/templates/sdlc/README.md) - repo-local PRD/ARD/ADR/spec/plan/task template intent and targets
- [Operations templates README](../../../99.templates/templates/operations/README.md) - repo-local guide/policy/runbook/incident/postmortem template intent and targets
- [ADR homepage (adr.github.io)](https://adr.github.io/) - ADR definition and curated practice
- [Michael Nygard: Documenting Architecture Decisions](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions.html) - origin of the ADR practice
- [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html) - architecture description standard metadata
- [ISO/IEC/IEEE 29148](https://www.iso.org/standard/72089.html) - requirements engineering standard metadata
- [Google SRE Book: Postmortem Culture](https://sre.google/sre-book/postmortem-culture/) - postmortem definition, triggers, blameless culture
- [NIST SP 800-61](https://csrc.nist.gov/pubs/sp/800/61) - computer security incident handling guidance (Rev. 2 withdrawn; see Rev. 3)
- [PagerDuty: What is a runbook](https://www.pagerduty.com/resources/learn/what-is-a-runbook/) - runbook definition and runbook-vs-policy distinction
- [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) - release-notes/changelog convention
- [Semantic Versioning](https://semver.org/) - version-signal convention for releases

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when the stage-authoring matrix, templates, or
  document taxonomy change
- **Update Trigger**: Update when a document type is added or removed, or when a
  template target or owner changes

## Related Documents

- [research pack index](./README.md)
- [spec-driven development and SDLC](./spec-driven-sdlc.md)
- [quality, CI, and formatting](./quality-ci-formatting.md)
- [stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md)
- [documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md)
