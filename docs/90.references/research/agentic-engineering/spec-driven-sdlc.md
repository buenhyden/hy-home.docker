---
status: active
---
<!-- Target: docs/90.references/research/agentic-engineering/spec-driven-sdlc.md -->

# Reference: Spec-Driven Development and SDLC

## Overview

This reference analyzes spec-driven development, SDLC, traceability, and change control, then compares them with the stage-gated documentation lifecycle in `hy-home.docker`.

## Purpose

Explain why specifications in an agent-first workspace should act as contracts for planning, implementation, verification, and operations evidence rather than passive documentation.

## Repository Role

This reference provides background for Stage 00 governance and the lifecycle across `docs/01` through `docs/05`, `docs/90`, and `docs/99`. It does not create new requirements, architecture decisions, specifications, or execution plans.

## Scope

### In Scope

- Spec-driven development concepts
- Requirements and specification traceability
- SDLC and secure SDLC
- Executable specification and contract-first analogies
- Repo-local stage-gate mapping

### Out of Scope

- New PRD, ARD, ADR, or Spec authoring
- Implementation plan authoring
- Provider-specific prompt workflow adoption
- Active template changes

## Definitions / Facts

- **Spec-driven development**: GitHub Spec Kit describes an AI-assisted workflow where teams define what to build before building it and refine the work through structured phases.
- **Spec-first / spec-anchored / spec-as-source**: Martin Fowler's SDD article distinguishes writing a spec first, keeping the spec as an anchor, and treating the spec itself as the long-term source.
- **Requirements engineering**: ISO/IEC/IEEE 29148 public metadata identifies the standard as covering requirements engineering processes for systems and software engineering.
- **SDLC**: ISO/IEC/IEEE 12207 public metadata describes a framework for software life cycle processes.
- **Secure SDLC**: NIST SSDF SP 800-218 presents high-level secure development practices that can be integrated into SDLC implementations.
- **Executable specification**: Cucumber describes executable specifications written in plain text that validate software behavior.
- **Contract-first API**: OpenAPI provides a language-agnostic interface that lets humans and computers understand service capabilities without source code or network inspection.

## Repo-local SDLC Mapping

| SDLC Concern | External Pattern | Repo-local Stage |
| --- | --- | --- |
| intent and scope | requirements engineering | `docs/01.requirements/` |
| architecture constraints | lifecycle architecture and decisions | `docs/02.architecture/requirements/`, `docs/02.architecture/decisions/` |
| implementation contract | spec-driven / contract-first | `docs/03.specs/` |
| work sequencing | implementation planning | `docs/04.execution/plans/` |
| evidence capture | task execution and verification | `docs/04.execution/tasks/` |
| operations readiness | runbook/policy/guide lifecycle | `docs/05.operations/` |
| stable context | reference stage | `docs/90.references/` |
| document contract | templates | `docs/99.templates/` |

## Analysis

`hy-home.docker` already implements a spec-driven lifecycle through stage taxonomy. The root README describes requirements -> architecture -> specs -> execution -> operations as the ordinary work flow. `stage-authoring-matrix.md` assigns each stage a purpose, timing, persona, input docs, output docs, template, and done criteria.

Compared with external SDD sources, this repository is closer to spec-anchored governance than full spec-as-source code generation. That is a good fit for an infrastructure/documentation workspace. Instead of generating all code from specs, it preserves traceability across requirements, architecture, specifications, plans, evidence, and operations documents, then uses validation scripts to detect drift.

From a secure SDLC perspective, NIST SSDF practice groups align with this repository's governance, secret boundaries, validation scripts, and CI gates. Formal SSDF control mapping would require separate approved policy, specification, or task work; this reference does not adopt SSDF as active policy.

Docker Compose infrastructure work still follows Stage 01-05 when it changes requirements, architecture, implementation contracts, execution evidence, or operations behavior. A Compose edit may look like an infra-only change, but new service behavior, ports, networks, profiles, secrets, readiness expectations, or operations controls still need the same traceability as other implementation work.

QA evidence should keep formatting, linting, syntax checks, documentation contracts, Compose rendering, hardening, security baselines, and CI-only gates as separate evidence classes. Treating them separately makes skipped-check rationale and follow-up ownership clearer.

## Application Notes for This Workspace

- New active documents should start by selecting the target stage and template.
- Agent implementation should not start without an approved plan when the workflow requires one.
- Reference documents must not replace active specs or plans.
- Traceability is maintained through Related Documents, parent README sync, validation commands, and task evidence.
- Docker Compose infrastructure work should enter the Stage 01-05 lifecycle when it changes requirements, architecture, implementation contracts, execution evidence, or operations behavior.
- Secure SDLC frameworks remain references unless adopted through a separate approved policy, spec, or task.
- External SDD tool structures should be adapted into this repository's canonical stage paths rather than copied directly.

## Potential Follow-up / Gap

- A future implementation guide could compare official SDD workflows with the repo-local Stage 01-05 lifecycle.
- Mapping NIST SSDF practice groups to repository controls would require a separate approved policy or spec task.
- This research refresh now has a Stage 03 spec, Stage 04 plan, and Stage 04 task evidence; any next active change discovered from this reference pack should continue through the same stage-gated path.

## Source Rules

- Public metadata for standards must not be treated as full access to the standard text.
- AI-era SDD sources should distinguish official GitHub Spec Kit docs from broader engineering commentary.
- Repo-local stage facts must be verified against the Stage 00 matrix and root/docs README files.

## Sources

- [GitHub Spec Kit documentation](https://github.github.com/spec-kit/) - AI-assisted spec-driven development workflow overview
- [GitHub Spec Kit repository](https://github.com/github/spec-kit) - official toolkit source
- [GitHub spec-driven guide](https://github.com/github/spec-kit/blob/main/spec-driven.md) - SDD concept framing
- [Martin Fowler on spec-driven development tools](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) - spec-first/spec-anchored/spec-as-source distinction
- [ISO/IEC/IEEE 12207 public page](https://www.iso.org/standard/63712.html) - software lifecycle process framework metadata
- [ISO/IEC/IEEE 29148 public page](https://standards.ieee.org/standard/29148-2018.html) - requirements engineering metadata
- [NIST SP 800-218 SSDF final](https://csrc.nist.gov/pubs/sp/800/218/final) - secure software development practices
- [NIST SP 800-218 Rev. 1 initial public draft](https://csrc.nist.gov/pubs/sp/800/218/r1/ipd) - draft update caveat
- [Cucumber BDD docs](https://cucumber.io/docs/bdd/) - executable specification and shared language
- [OpenAPI Initiative: What is OpenAPI](https://www.openapis.org/what-is-openapi) - API-first lifecycle context
- [Stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md) - repo-local SDLC stage mapping
- [Documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md) - repo-local template and traceability contract

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when SDLC/stage taxonomy or SDD sources change
- **Update Trigger**: Update when Stage 01-05 lifecycle, templates, or external SDD guidance changes

## Related Documents

- [research pack index](./README.md)
- [workspace baseline](./workspace-baseline.md)
- [quality, CI, and formatting](./quality-ci-formatting.md)
- [stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md)
- [documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md)
