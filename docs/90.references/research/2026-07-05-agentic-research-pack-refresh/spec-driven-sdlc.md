---
status: active
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

| Transition | Repo-local owner | Entry evidence | Exit evidence | Validation gate | Feedback loop | External comparison |
| --- | --- | --- | --- | --- | --- | --- |
| intent → PRD | Product Manager; `docs/01.requirements/` | Stakeholder need, problem, constraints, existing policy/runtime evidence | Numbered PRD with users, scope, requirements, success criteria, and downstream links | PRD template review and `bash scripts/validation/check-repo-contracts.sh` | Rejected or ambiguous requirements return to intent clarification | ISO 29148:2018 provides requirements-engineering metadata; the public page is not full standard text. GitHub Spec Kit begins at a specification, while this workspace preserves an earlier product-intent artifact. |
| PRD → ARD/ADR | System Architect; `docs/02.architecture/requirements/` and `decisions/` | Approved PRD plus current architecture/runtime constraints | ARD boundaries/quality attributes and ADRs for non-trivial choices, alternatives, and consequences | Architecture templates, PRD links, and repository-contract validation | Architecture infeasibility or trade-off evidence can revise the PRD or create a new ADR | ISO 42010:2022 frames architecture description; ADR practice records one decision and rationale. The repo ARD is narrower than a full 42010 architecture description. |
| ARD/ADR → Spec | Implementing engineer; `docs/03.specs/NNN-feature-id/` | PRD, ARD, applicable ADRs, current implementation evidence | Parent `spec.md` plus optional API, agent, data, service, test, or machine-readable contracts | Spec/template traceability, `check-repo-contracts.sh`, and applicable contract checks | Interface ambiguity, failed feasibility, or security review returns to architecture/requirements | GitHub Spec Kit makes a specification an executable-context anchor; this workspace retains explicit product and architecture predecessors. |
| Spec → Plan | Project or Engineering Lead; `docs/04.execution/plans/` | Stable spec and supporting contracts with verification criteria | Sequenced plan with scope, risks, commands, rollback/recovery, and done criteria | Plan-template review, `check-doc-traceability.sh`, and repository contracts | Planning gaps return to the spec or an earlier owner instead of being hidden in tasks | Spec Kit's Plan phase feeds later tasks. ISO 12207:2017 offers historical lifecycle-process framing but is now marked withdrawn. |
| Plan → Task/Evidence | Implementation and QA engineers; `docs/04.execution/tasks/` | Approved plan, scoped task brief, clean baseline, and required approvals | Current task state, changed-file record, validation results, deviations, reviews, and logical commit evidence | Task-specific checks plus `git diff --check`, traceability, alignment, and repository contracts as applicable | Failed implementation/QA/security evidence returns to the owning spec, plan, or task | Spec Kit separates Plan, Tasks, and Implement. The workspace combines implementation status and auditable evidence in Stage 04 task records. |
| Task/Evidence → Operations/Release | Documentation Specialist and Operations/SRE; `docs/05.operations/`, root `CHANGELOG.md` | Completed implementation evidence, operator impact, release scope, and rollback/recovery needs | Updated guide/policy/runbook/incident linkage and human-readable release notes when applicable | `check-doc-implementation-alignment.sh`, repository contracts, applicable runtime checks, and tag-time changelog check | Operational validation or release failure returns evidence to the task/plan/spec owner | PagerDuty frames runbooks as repeatable procedures; Keep a Changelog and SemVer frame human release communication/version signals. They do not prescribe this repo's release gate. |
| incident/postmortem + eval/QA/security feedback → intent or earliest affected owner | Operations/SRE, QA, Security, then Product/Architecture/Spec owner selected by gap routing | Incident state, reviewed postmortem, eval result, failed check, vulnerability evidence, or verified drift | New/changed intent, requirement, decision, spec, plan, task, or operations artifact at the earliest canonical owner | Incident/postmortem templates, gap routing, relevant validator rerun, and required human approval | Closed-loop learning is complete only when preventive action has an owner and verification evidence | Google SRE separates live incident state from reviewed blameless postmortems; NIST SP 800-61 Rev. 3 frames incident response in CSF 2.0; NIST SSDF v1.1 supplies high-level secure-development feedback practices. |

## Lifecycle Participants, Not Replacements

| Participant | Lifecycle contribution | Evidence boundary | Why it is not the lifecycle owner |
| --- | --- | --- | --- |
| Docker Compose / infrastructure | Supplies current implementation/runtime evidence and validation targets for architecture, specs, tasks, and operations. | `docker-compose.yml`, `infra/**`, version registry, Compose validation, and hardening checks are tracked runtime evidence. | Compose describes deployable configuration; it does not own user intent, architecture rationale, execution planning, or incident learning. |
| CI / GitHub Actions | Runs repeatable validation and reports job/step evidence at task and release gates. | Tracked workflow YAML proves definitions; it does not by itself prove remote required-check enforcement or a successful run. | A pipeline verifies artifacts but does not replace the PRD, ADR, spec, plan, task, or operations document that owns the decision/evidence. |
| Secure SDLC / NIST SSDF | Provides an external practice lens for organizational, software-protection, production, and vulnerability-response activities. | NIST SP 800-218 v1.1 is a high-level framework dated February 2022; no formal repo control mapping is adopted here. | A framework comparison does not create workspace policy or supersede the Stage 00 security scope and active stage documents. |

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
- **ISO/IEC/IEEE 12207:2017** was published in November 2017 but is now marked
  withdrawn. It is retained only as historical lifecycle metadata.
- **ADR practice** uses a record for one decision, its rationale, trade-offs,
  and consequences; Michael Nygard's original article is dated 2011-11-15.
- **NIST SSDF v1.1** and **NIST SP 800-61 Rev. 3** are comparison frameworks,
  not adopted controls. The latter is dated April 2025 and supersedes Rev. 2.

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

## Potential Follow-up / Gap

- A formal NIST SSDF-to-workspace control map requires separate approved
  security policy/spec/task work.
- Remote required-check and branch-protection evidence requires a separately
  authorized remote-state verification task.
- ISO 12207 lifecycle comparison should move to a current edition/source if a
  future task needs normative lifecycle claims.

## Source Rules

- Repo-local transitions are based on the tracked stage matrix, documentation
  protocol, templates, current stage artifacts, and validators.
- External sources were retrieved on `2026-07-10`; mutable pages without an
  update date prove retrieval-time content only.
- ISO pages expose metadata and short summaries, not the full standards.
- No external comparison is adopted workspace policy by this reference.

## Sources

- [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md) - repo-local lifecycle owners and evidence
- [Documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md) - template, traceability, and routing contracts
- [GitHub Spec Kit documentation](https://github.github.com/spec-kit/) - current SDD phase flow
- [GitHub spec-driven guide](https://github.com/github/spec-kit/blob/main/spec-driven.md) - specification-as-context and constitution framing
- [ISO/IEC/IEEE 12207:2017](https://www.iso.org/standard/63712.html) - withdrawn lifecycle-process metadata
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
- [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) - human-readable changelog convention
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
