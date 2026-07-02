---
status: active
---
<!-- Target: docs/90.references/data/glossary/stable-reference-terms.md -->

# Reference: Stable Reference Terms

## Overview

This document defines stable reference terms repeatedly used in `docs/90.references` and documentation governance. It is a reference for aligning term meaning and does not define new active policy.

## Purpose

Help document authors and AI Agents interpret reference stage, runtime truth, and generated evidence boundaries consistently.

## Repository Role

This reference is shared vocabulary for explaining role boundaries between document stages. The source of truth for policy is `docs/00.agent-governance/`; the source of truth for operations procedures is `docs/05.operations/`; the source of truth for runtime configuration is `infra/`, `scripts/`, and registry files.

## Scope

### In Scope

- terms repeatedly used in the reference stage
- distinction between source-backed reference and runtime truth
- usage boundaries for advisory graph context and generated indexes

### Out of Scope

- active governance policy revisions
- operations procedures or runbook steps
- implementation plans or task evidence
- secret values, credentials, tokens

## Definitions / Facts

- **Stable reference**: Document containing slowly changing background knowledge, standards, terms, and source-backed facts. It does not replace requirements, decisions, execution plans, or operations procedures.
- **Stable context**: Background information that multiple active stage documents can repeatedly reference. It should change more slowly than current runtime state.
- **Source-backed reference**: Reference that briefly connects a fact to a repo-local canonical file or external primary source.
- **Runtime truth**: Source that directly defines current runtime configuration or validation criteria. In this repository, this usually means `infra/`, `scripts/`, registry JSON files, Docker Compose files, and `docs/00.agent-governance/`.
- **Active stage document**: Document that directly drives current work and judgment, such as requirements, architecture, specs, execution, operations, or incidents.
- **Advisory graph context**: Supporting material such as Graphify output that helps exploration but is not promoted to canonical evidence.
- **Generated tracked index**: Tracked Markdown index refreshed by script. Prefer the generator and freshness check over manual editing.

## Source Rules

- When a term changes active policy, update the governance rule or scope document instead of this reference.
- When operations procedures are needed, link to `docs/05.operations/`.
- Link runtime values or current config to `infra/`, `scripts/`, and registry files instead of copying them into the body.
- Use Graphify, generated indexes, and validator output only as navigation/evidence and confirm them with canonical sources.

## Sources

- [documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md) - documentation stage boundaries and DOCS 3 rules
- [stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md) - stage roles and template mapping
- [90.references](../../README.md) - reference stage purpose and lifecycle
- [LLM Wiki repository map](../../llm-wiki/repository-map.md) - tracked-source boundary and Graphify advisory rules

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when documentation governance, stage taxonomy, or generated evidence boundaries change
- **Update Trigger**: Update when a repeated term causes ambiguity across stage docs

## Related Documents

- [Glossary references](./README.md)
- [90.references](../../README.md)
- [docs index](../../README.md)
- [documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md)
- [stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md)
