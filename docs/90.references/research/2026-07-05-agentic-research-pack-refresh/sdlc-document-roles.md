---
status: active
---

<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/sdlc-document-roles.md -->

# Reference: SDLC and Operations Document-Type Roles

## Overview

This reference maps each tracked workspace document type to the question it
answers, its authoring trigger and owner, its inputs and consumers, its lifecycle
status, its canonical template/path, and its external or repo-template basis.
Supporting API, agent, data, and test contracts are separate rows because they
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
this matrix.

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
- **Release notes/changelog** communicate changes; the release runbook owns
  procedure. They are not interchangeable.
- **Incident** preserves contemporaneous state; **postmortem** preserves reviewed
  learning and preventive actions.

## Canonical Document-Role Matrix

| Document | Primary question | Authoring trigger | Owner | Inputs | Outputs / consumers | Lifecycle status | Workspace template / path | External basis |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PRD | What problem, users, value, scope, requirements, and success criteria should the workspace address? | New or materially changed stakeholder intent | Product Manager | Stakeholder intent, constraints, verified current state | ARD/ADR, Spec, reviewers | Active Stage 01 requirements | `docs/99.templates/templates/sdlc/prd.template.md` → `docs/01.requirements/NNN-feature-or-system.md` | ISO/IEC/IEEE 29148:2018 requirements-engineering metadata; public page is not full standard text and is marked “to be revised.” |
| ARD | What architecture boundaries, stakeholders, concerns, and quality attributes constrain the solution? | Stable PRD needs enduring architecture requirements | System Architect | PRD, existing architecture/runtime, quality attributes | ADRs, Specs, architecture reviewers | Active Stage 02 architecture requirements | `sdlc/ard.template.md` → `docs/02.architecture/requirements/NNNN-short-title.md` | ISO/IEC/IEEE 42010:2022 architecture-description metadata; the repo ARD is narrower than a full standard-conforming description. |
| ADR | Which non-trivial architecture option was chosen, why, and with what consequences? | Architecturally significant trade-off or reversal | System Architect | PRD/ARD, alternatives, constraints, evidence | Specs, plans, future decision reviewers | Active Stage 02 decision record | `sdlc/adr.template.md` → `docs/02.architecture/decisions/NNNN-short-title.md` | ADR homepage definition plus Michael Nygard's 2011-11-15 original practice article. |
| Spec | What technical design, interfaces, contracts, and verification criteria will be implemented? | PRD/architecture baseline is sufficient for implementation design | Implementing engineer | PRD, ARD, ADRs, current implementation evidence | Supporting contracts, Plan, implementers, QA | Active Stage 03 technical contract | `sdlc/spec.template.md` → `docs/03.specs/NNN-feature-id/spec.md` | GitHub Spec Kit treats the specification as the context anchor that feeds Plan and Tasks; no Spec Kit runtime is adopted. |
| API Spec | What callable operations, schemas, auth rules, errors, and compatibility contract apply? | A Spec exposes or changes an API/interface | Backend/API owner | Parent Spec, architecture, security and data constraints | Implementers, clients, contract tests | Optional supporting Stage 03 contract | `spec-contracts/api-spec.template.md` → feature `api-spec.md`; machine contracts under `contracts/` | Repo-template basis; no separate external API standard is adopted by this task. |
| Agent Design | What agent purpose, inputs, outputs, tools, permissions, failure modes, and eval contract apply? | A Spec creates or materially changes agent behavior | Agent/feature owner | Parent Spec, Stage 00 governance, provider constraints | Runtime adapter work, tests/evals, reviewers | Optional supporting Stage 03 contract | `spec-contracts/agent-design.template.md` → feature `agent-design.md` | Repo-template basis; GitHub Spec Kit only supplies comparison for structured agent context, not this provider-neutral contract. |
| Data Model | What entities, relationships, integrity, storage, privacy, and migration rules apply? | A Spec creates or changes durable data shape | Data/feature owner | Parent Spec, architecture, privacy/security constraints | Implementers, migrations, API contracts, tests | Optional supporting Stage 03 contract | `spec-contracts/data-model.template.md` → feature `data-model.md` | Repo-template basis; no external data-model standard is adopted by this task. |
| Test Contract | What must be verified, with which fixtures, expected results, non-functional checks, and evals? | A Spec needs executable acceptance/verification detail | QA/feature owner | Parent Spec, API/agent/data contracts, risks | Plan, Task, CI, reviewers | Optional supporting Stage 03 contract | `spec-contracts/tests.template.md` → feature `tests.md` | Repo-template basis; Spec Kit quality checklists and NIST SSDF verification practices are comparison lenses only. |
| Plan | In what sequence will the approved Spec be implemented, controlled, verified, and completed? | Spec and supporting contracts are stable enough to schedule work | Project/Engineering Lead | PRD/ARD/ADR/Spec, dependencies, risks | Tasks, implementers, reviewers | Active Stage 04 execution plan | `sdlc/plan.template.md` → `docs/04.execution/plans/` | GitHub Spec Kit has a distinct Plan phase feeding Tasks; ISO 12207:2017 supplies withdrawn historical lifecycle metadata only. |
| Task | What was attempted, changed, validated, reviewed, committed, deferred, or blocked? | Approved plan work begins | Implementation/QA Engineer | Plan, Spec, task brief, baseline evidence | Reviewers, operations, release, audit trail | Active Stage 04 execution evidence | `sdlc/task.template.md` → `docs/04.execution/tasks/` | GitHub Spec Kit separates Tasks and Implement; the repo task additionally owns auditable execution evidence. |
| Guide | How should a person understand, use, and routinely check the service/process, and where do procedures live? | User/operator-facing usage or onboarding changes | Documentation Specialist / Operations/SRE | Spec, task evidence, actual behavior | Users/operators; policy/runbook handoff | Active Stage 05 operations guidance | `operations/guide.template.md` → `docs/05.operations/guides/` | Repo-template basis; external runbook sources do not replace a usage guide. |
| Policy | Which operational controls are required or prohibited, how are exceptions handled, and how is compliance reviewed? | An approved operational control or exception changes | Documentation Specialist / Operations/SRE, with policy approver | Requirements, architecture, security/compliance constraints, task evidence | Guides, runbooks, audits, operators | Active Stage 05 operating control | `operations/policy.template.md` → `docs/05.operations/policies/` | Repo-template basis; NIST SSDF is high-level comparison and is not adopted policy. |
| Runbook | What ordered, repeatable steps, evidence, recovery, rollback, and escalation execute an operation? | Repeatable operation, recovery, or incident response needs a procedure | Operations/SRE | Policy, Guide, Spec, task/incident evidence | Operators, incident responders, audits | Active Stage 05 operational procedure | `operations/runbook.template.md` → `docs/05.operations/runbooks/` | PagerDuty defines a runbook as a detailed how-to for a repeated operations task; the page is mutable vendor guidance with no visible update date. |
| Incident | What happened, when, with what impact/current state, command roles, actions, and handoffs? | A qualifying operational/security event begins | Operations/SRE or Security incident owner | Alerts, observations, commands, communications | Responders, stakeholders, Postmortem | Active/resolved Stage 05 incident record | `operations/incident.template.md` → `docs/05.operations/incidents/YYYY/INC-###-title/` | Google SRE incident command/live-state practice; NIST SP 800-61 Rev. 3 (April 2025) CSF 2.0 incident-response profile. |
| Postmortem | Why did the incident occur, what was learned, and which owned actions prevent recurrence? | Incident is stabilized and meets postmortem criteria | Operations/SRE with contributing owners/reviewers | Incident timeline, impact, mitigation, evidence | Requirements/architecture/spec/plan/runbook improvements | Stage 05 reviewed learning artifact | `operations/postmortem.template.md` → incident-folder `postmortem.md` | Google SRE defines a reviewed, blameless record of impact, mitigation, root causes, and preventive actions. |
| Release notes/changelog | What notable user/operator-facing changes are in a version? | A release/tag has notable changes to communicate | Release owner / Operations/SRE | Completed tasks, version, compatibility/upgrade notes | Users, operators, future release review | Root release communication plus Stage 05 release procedure | Root `CHANGELOG.md`; procedure at `docs/05.operations/runbooks/00-workspace/release-management.md` | Keep a Changelog 1.1.0 (2019-02-15 convention page) and Semantic Versioning 2.0.0; neither defines repo release approval. |
| Reference | What stable, source-backed context helps active work without owning decisions or procedures? | Durable facts, inventory, glossary, or research context is needed | Documentation maintainer / subject owner | Primary sources and tracked current evidence | Active stages, authors, reviewers | Supporting Stage 90 context | `common/reference.template.md` → `docs/90.references/` | Repo-template basis; external sources support each reference's facts but do not make the reference policy. |
| Audit | What was inspected, against which criteria, with what evidence, findings, severity, and disposition? | A bounded current-state/compliance review is authorized | Auditor / subject reviewer | Scope, criteria, tracked evidence, approved external benchmarks | Canonical gap owners, Specs/Plans/Tasks | Supporting Stage 90 evidence snapshot | `common/audit.template.md` → `docs/90.references/audits/` | Repo-template basis; any external benchmark must be named and remains comparison unless adopted elsewhere. |
| Archive tombstone | What active document was removed, why, and what current replacement should be followed? | A whole document conflicts with current implementation and must leave the active chain | Documentation Specialist / Agentic Workflow Specialist | Original path/status, archive reason, replacement | Maintainers and migration audit trail; active docs must not link back | Stage 98 tombstone; `status: archived` only | `common/archive.template.md` → `docs/98.archive/original-stage/original-path.md` | Repo-template basis; a tombstone preserves migration traceability, not historical current truth. |

## Analysis

The 19 rows form five ownership bands:

1. PRD, ARD, and ADR own intent and architecture rationale.
2. Spec plus API, agent, data, and test contracts own implementable technical
   and verification contracts.
3. Plan and Task separate intended sequencing from actual execution evidence.
4. Guide, Policy, Runbook, Incident, Postmortem, and Release separate use,
   controls, procedure, live state, learning, and communication.
5. Reference, Audit, and Archive tombstone preserve supporting context,
   bounded findings, and migration traceability without becoming active truth.

Three boundaries are especially important. An ADR records why; a Spec records
what design results. A Policy states controls; a Runbook executes procedures.
An Incident records current chronology/state; a Postmortem is reviewed learning.
Crossing any of these boundaries weakens ownership and makes validation evidence
harder to interpret.

## Application Notes for This Workspace

- Choose the document by its primary question, then load its mapped template.
- Route a new gap to the earliest owner and link downstream consumers.
- Keep optional supporting contracts separate when their interface, agent, data,
  or test question is material.
- Put notable release communication in `CHANGELOG.md` and procedure in the
  release runbook.
- Keep Stage 90 references/audits advisory and Stage 98 tombstones out of the
  active link chain.

## Potential Follow-up / Gap

- Release notes have a tracked home and convention but no dedicated workspace
  template; any template addition requires separately approved Stage 99 work.
- Formal ISO/NIST conformance or control mapping requires an approved policy,
  specification, and task rather than a Stage 90 role description.
- Optional supporting-contract adoption should remain feature-driven; a template
  does not prove that every feature needs every support file.

## Source Rules

- Repo-local roles come from the tracked stage matrix, documentation protocol,
  and template catalog.
- External sources were retrieved on `2026-07-10`; mutable pages without a
  displayed update date prove retrieval-time content only.
- ISO pages provide metadata and summaries rather than full standards.
- ISO/IEC/IEEE 12207:2017 is withdrawn and is not a current normative basis.
- External sources remain comparisons; repo-template bases are labeled explicitly.

## Sources

- [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md) - stage purpose, timing, owner, inputs, outputs, and templates
- [Documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md) - type-to-template and gap-routing contracts
- [SDLC templates](../../../99.templates/templates/sdlc/README.md) - PRD through Task template intent
- [Supporting contract templates](../../../99.templates/templates/spec-contracts/README.md) - API, agent, data, and test roles
- [Operations templates](../../../99.templates/templates/operations/README.md) - Guide through Postmortem roles
- [Common templates](../../../99.templates/templates/common/README.md) - Reference, Audit, and Archive roles
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
- [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) - changelog convention
- [Semantic Versioning 2.0.0](https://semver.org/) - version signal convention

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when the stage matrix, templates, or cited role sources change
- **Update Trigger**: Update when a document role, canonical owner, path, or lifecycle status changes

## Related Documents

- [research pack index](./README.md)
- [workspace baseline](./workspace-baseline.md)
- [spec-driven development and SDLC](./spec-driven-sdlc.md)
- [release management runbook](../../../05.operations/runbooks/00-workspace/release-management.md)
- [stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md)
- [documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md)
