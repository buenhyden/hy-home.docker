---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/harness-engineering-implementation.md -->

# Reference: Harness Engineering Implementation

## Overview

This reference audits the current implementation status of harness engineering
in `hy-home.docker`. It compares the researched harness model with repo-local
governance, validation, provider, CI, script, infrastructure, and evidence
surfaces.

## Purpose

The purpose is to identify which harness elements are implemented, which are
partial, and which should become future automation or governance work.

## Repository Role

This document supports future Stage 03/04 planning for harness improvements.
It does not replace Stage 00 governance, the HAFE operations policy, CI
workflow source, scripts, infrastructure files, or task evidence.

## Scope

### In Scope

- Governance harness.
- Runtime/provider harness.
- Validation and CI harness.
- Infrastructure and Docker Compose harness.
- Evidence and approval harness.
- Security and secret-boundary harness.

### Out of Scope

- Changing protected surfaces.
- Adding new validators or CI jobs.
- Running deployments or service restarts.
- Secret values, credentials, tokens, private keys, raw logs, shell history, or
  `.env` values.

## Definitions / Facts

- **Harness engineering** means the surrounding system of rules, adapters,
  scripts, CI gates, evidence, and approval boundaries that makes agentic work
  repeatable and auditable.
- **Runtime harness** in this repository is provider-adapter wiring plus shared
  governance, not a separate provider-local policy source.
- **Evidence harness** is primarily Stage 04 task evidence, progress memory,
  PR validation evidence, and generated indexes.

## Assessment Method

The audit compared the harness research reference with local canonical paths:
Stage 00 governance, HAFE operations docs, provider notes, provider adapter
directories, scripts, CI workflow, infrastructure inventory, template support
contracts, and task evidence.

## Implementation Status Matrix

| Harness Element | Status | Evidence | Notes |
| --- | --- | --- | --- |
| Governance SSoT | Implemented | [Stage 00 governance hub](../../../00.agent-governance/README.md) | Stage 00 owns policy, provider overlays, agent catalog, memory, QA/CI/CD, model policy, template contract, and clarification duty. |
| Root entry shims | Implemented | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` | Root shims route into Stage 00 and remain thin by contract. |
| Provider adapter model | Implemented | [provider capability matrix](../../../00.agent-governance/rules/provider-capability-matrix.md), [subagent protocol](../../../00.agent-governance/subagent-protocol.md) | Claude, Codex, and Gemini map to shared catalog and model tiers. |
| Runtime provider surfaces | Partially Implemented | `.claude/`, `.codex/`, `.agents/` | Claude and Codex have native hooks/subagents; Gemini is pointer/behavioral for hooks and first-class subagent parity. |
| Validation harness | Implemented | [scripts README](../../../../scripts/README.md), `scripts/validation/**` | Repo contracts, doc alignment, traceability, Compose validation, local QA gate, and template/security checks exist. |
| CI harness | Implemented | `.github/workflows/ci-quality.yml` | CI runs docs, contracts, Compose, hardening, pre-commit, frontend, coverage, and workflow-security jobs. |
| Docker Compose / infrastructure harness | Implemented | [infra README](../../../../infra/README.md), `docker-compose.yml`, `infra/**/docker-compose*.yml` | Modular include/profile topology, service READMEs, version registry, and validation scripts exist. |
| Hook harness | Partially Implemented | [Claude provider notes](../../../00.agent-governance/providers/claude.md), [Codex provider notes](../../../00.agent-governance/providers/codex.md), [Gemini provider notes](../../../00.agent-governance/providers/gemini.md) | Claude/Codex use runtime hooks; Gemini follows behavioral contracts because official/native parity is absent. |
| Approval harness | Implemented | [approval boundaries](../../../00.agent-governance/rules/approval-boundaries.md) | Protected surfaces and hard stops are explicit. |
| Evidence harness | Implemented | [task evidence](../../../04.execution/tasks/2026-07-05-agentic-engineering-implementation-audit-pack.md), [progress memory](../../../00.agent-governance/memory/progress.md) | Stage 04 task evidence and progress memory record work and validation. |
| Security harness | Partially Implemented | [approval boundaries](../../../00.agent-governance/rules/approval-boundaries.md), `.github/SECURITY.md`, `.github/workflows/ci-quality.yml` | Secret and workflow controls exist; full supply-chain attestation maturity is not claimed. |

## Findings

- The repository implements harness engineering as a multi-layer system:
  governance, provider adapters, validation scripts, CI, infrastructure
  inventory, hooks, evidence, and operations guidance.
- The harness is strongest where it can be validated statically: template
  shape, provider catalog parity, script inventory, Compose syntax, hardening,
  and documentation traceability.
- The harness is weaker where runtime semantics are provider-specific:
  Gemini hook/subagent behavior, semantic equivalence of generated adapters,
  and agent-output quality scoring.

## Gap / Follow-up

| Gap | Status | Follow-up Direction |
| --- | --- | --- |
| Provider adapter semantic parity | Partially Implemented | Add a validator that compares important behavioral clauses, not only names, models, and scope imports. |
| Gemini native hooks and subagents | Partially Implemented | Keep Gemini as behavioral/pointer parity until official sources support native parity. |
| Agent eval harness | Partially Implemented | Add eval fixtures for common agent tasks, report scoring, and regression tracking. |
| Supply-chain evidence | Partially Implemented | Consider SLSA/attestation mapping as a separate security plan. |

## Automation Impact

Current automation is strong for structural validation. The next automation
layer should produce machine-readable harness coverage summaries from Stage 00,
provider adapters, scripts, CI, and infrastructure paths so audit reports can
be refreshed with less manual interpretation.

## Source Rules

- Repo-local harness implementation claims must cite Stage 00, scripts, CI,
  provider surfaces, HAFE operations docs, or infrastructure files.
- External harness concepts remain research criteria and are not adopted
  policy without a separate active-stage change.

## Sources

- [Harness engineering research](../../research/2026-07-05-agentic-research-pack-refresh/harness-engineering.md) - research criteria.
- [Harness implementation map](../../../00.agent-governance/harness-implementation-map.md) - surface-to-source routing.
- [Approval boundaries](../../../00.agent-governance/rules/approval-boundaries.md) - protected-surface matrix.
- [Subagent protocol](../../../00.agent-governance/subagent-protocol.md) - provider model and delegation policy.
- [Provider capability matrix](../../../00.agent-governance/rules/provider-capability-matrix.md) - provider adapter mapping.
- [scripts README](../../../../scripts/README.md) - validation and automation harness.
- [CI quality workflow](../../../../.github/workflows/ci-quality.yml) - remote CI harness.
- [infra README](../../../../infra/README.md) - infrastructure harness.
- [HAFE guide](../../../05.operations/guides/00-workspace/harness-agent-first-engineering.md) - operational usage.
- [HAFE policy](../../../05.operations/policies/00-workspace/harness-agent-first-engineering.md) - operational controls.

## Maintenance

- **Owner**: Agentic Workflow Specialist.
- **Review Cadence**: Review after Stage 00, provider adapter, scripts, CI, or
  infrastructure validation changes.
- **Update Trigger**: Update when a harness surface is added, removed, or
  changes validation depth.

## Related Documents

- [Audit pack README](./README.md)
- [Implementation overview](./implementation-overview.md)
- [Loop implementation audit](./loop-engineering-implementation.md)
- [Research pack](../../research/2026-07-05-agentic-research-pack-refresh/README.md)
- [Audit pack task evidence](../../../04.execution/tasks/2026-07-05-agentic-engineering-implementation-audit-pack.md)
