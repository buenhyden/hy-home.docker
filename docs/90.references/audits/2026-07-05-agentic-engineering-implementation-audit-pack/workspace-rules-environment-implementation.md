---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/workspace-rules-environment-implementation.md -->

# Reference: Workspace Rules and Environment Implementation

## Overview

This reference audits the workspace rules, system, environment, Docker Compose,
infrastructure, templates, scripts, and common provider-neutral contracts that
support agentic engineering in `hy-home.docker`.

## Purpose

The purpose is to show whether the workspace has the environment and rule
system needed to apply harness engineering and loop engineering consistently
across Claude, Codex, and Gemini.

## Repository Role

This document supports future workspace governance and environment planning. It
does not replace Stage 00 policy, operations procedures, infrastructure source,
or template contracts.

## Scope

### In Scope

- Workspace purpose and role surfaces.
- Governance rules and documentation contracts.
- Templates and frontmatter contracts.
- Scripts and automation environment.
- Docker Compose and infrastructure topology.
- Security and protected-surface rules.
- Provider-neutral common contracts.

### Out of Scope

- Editing runtime infrastructure.
- Changing templates or governance policy.
- Secret values, credentials, tokens, private keys, raw logs, shell history, or
  `.env` values.

## Definitions / Facts

- **Workspace environment** means the files, scripts, CI jobs, provider
  adapters, templates, Compose topology, and documentation stages that shape
  how work is performed.
- **Common contract** means a provider-neutral rule in Stage 00 or Stage 99
  that provider surfaces bind to but do not redefine.
- **Protected surface** means a path that requires explicit approval before
  mutation.

## Assessment Method

The audit compared workspace-baseline research against root shims, Stage 00,
Stage 03/04/05/90/99 READMEs, template support contracts, scripts, CI workflow,
infra README, root Compose, provider notes, and approval boundaries.

## Implementation Status Matrix

| Area | Status | Evidence | Notes |
| --- | --- | --- | --- |
| Workspace purpose and role | Implemented | `README.md`, `AGENTS.md`, [Stage 00 governance hub](../../../00.agent-governance/README.md) | Purpose is shared harness-engineering and agent-first engineering over modular Docker Compose infrastructure and stage-gated docs. |
| Stage taxonomy | Implemented | [docs index](../../../README.md), [Stage 03 README](../../../03.specs/README.md), [Stage 04 READMEs](../../../04.execution/README.md), [90 references](../../README.md) | Requirements, architecture, specs, plans, tasks, operations, references, archive, and templates are separated. |
| Documentation contract | Implemented | [documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md), [stage authoring matrix](../../../00.agent-governance/rules/stage-authoring-matrix.md) | Target-stage templates, language boundaries, frontmatter, and related-doc rules are active. |
| Template/frontmatter system | Implemented | [template contract](../../../99.templates/support/template-contract.md), [frontmatter contract](../../../99.templates/support/frontmatter-contract.md) | Repo contracts enforce normalized target-stage documents. |
| Provider-neutral rules | Implemented | [provider capability matrix](../../../00.agent-governance/rules/provider-capability-matrix.md), [subagent protocol](../../../00.agent-governance/subagent-protocol.md) | Common capabilities and model tiers are defined once. |
| Scripts environment | Implemented | [scripts README](../../../../scripts/README.md) | Purpose-folder scripts cover validation, hardening, hooks, knowledge, and operations. |
| CI/CD environment | Implemented | `.github/workflows/ci-quality.yml` | CI quality gates enforce docs, contracts, Compose, hardening, pre-commit, frontend quality, and workflow security. |
| Docker Compose topology | Implemented | [infra README](../../../../infra/README.md), `docker-compose.yml`, `infra/**/docker-compose*.yml` | Root include, profiles, tiers, root-active inventory, and service docs exist. |
| Infrastructure version registry | Implemented | `infra/tech-stack.versions.json`, `scripts/operations/sync-tech-stack-versions.sh` | Version registry and sync script exist. |
| Security/protected-surface rules | Partially Implemented | [approval boundaries](../../../00.agent-governance/rules/approval-boundaries.md), `.github/SECURITY.md`, `.github/workflows/ci-quality.yml` | Secret, workflow, Compose, and governance boundaries are explicit; full external framework maturity is not claimed. |
| Operations contract | Implemented | `docs/05.operations/**`, [HAFE policy](../../../05.operations/policies/00-workspace/harness-agent-first-engineering.md) | Guides, policies, runbooks, incidents, and postmortem routing exist. |

## Findings

- The workspace has the core system needed to apply harness and loop
  engineering: stage taxonomy, templates, provider-neutral governance,
  provider adapters, validation scripts, CI, Compose infrastructure, and
  operations contracts.
- Docker Compose and Infrastructure are implemented as a modular environment
  with tiered service definitions, root-active inventory, profiles, service
  READMEs, validation, hardening, and version registry.
- The main partiality is not the absence of rules; it is enforcement depth:
  semantic provider parity, full security-framework automation, and complete
  cross-language formatting/linting coverage.

## Gap / Follow-up

| Gap | Impact | Follow-up Direction |
| --- | --- | --- |
| Common rules are strong but distributed. | New contributors may need several hops to understand the full contract. | Generate a concise provider-neutral rule digest from Stage 00 and Stage 99. |
| Docker/infrastructure maturity is validation-heavy but not deployment-maturity certified. | Compose checks do not prove production rollout readiness. | Keep deployment readiness in operations/runbook scope. |
| Security maturity is policy-backed but not fully framework-scored. | Cannot claim full SSDF/SLSA adoption. | Create separate security maturity audit if needed. |

## Automation Impact

Useful automation includes a generated workspace-control map, protected-surface
coverage report, provider-neutral rule digest, and a Compose/profile inventory
that updates audit rows from tracked files.

## Source Rules

- Workspace claims must cite tracked repo-local files.
- Official external references can support criteria but do not override Stage
  00, Stage 05, scripts, CI, templates, or infra files.

## Sources

- [Workspace baseline research](../../research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md) - research criteria.
- [Stage 00 governance hub](../../../00.agent-governance/README.md) - governance SSoT.
- [Documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md) - target-stage and template rules.
- [Approval boundaries](../../../00.agent-governance/rules/approval-boundaries.md) - protected surfaces.
- [scripts README](../../../../scripts/README.md) - automation environment.
- [infra README](../../../../infra/README.md) - Docker Compose and infrastructure environment.
- [CI quality workflow](../../../../.github/workflows/ci-quality.yml) - remote QA/CI environment.
- [Template contract](../../../99.templates/support/template-contract.md) - template rules.
- [HAFE policy](../../../05.operations/policies/00-workspace/harness-agent-first-engineering.md) - operations controls.

## Maintenance

- **Owner**: Repository Maintainer / Documentation Specialist.
- **Review Cadence**: Review after Stage 00, Stage 99, scripts, CI, infra, or
  operations taxonomy changes.
- **Update Trigger**: Update when workspace rules, protected surfaces,
  template contracts, provider adapters, or Compose topology changes.

## Related Documents

- [Audit pack README](./README.md)
- [Implementation overview](./implementation-overview.md)
- [Provider harness and loop audit](./provider-harness-loop-implementation.md)
- [Automation candidates](./automation-candidates.md)
