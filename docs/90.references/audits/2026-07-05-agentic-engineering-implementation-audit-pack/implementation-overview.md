---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/implementation-overview.md -->

# Reference: Agentic Engineering Implementation Overview

## Overview

This reference summarizes how much of the researched agentic engineering model
is currently implemented in `hy-home.docker`. It is a point-in-time audit
snapshot built from the Stage 90 research pack and repo-local evidence.

## Purpose

The purpose is to give maintainers and agents a cross-category maturity view
before deeper category reports are read. It supports follow-up planning without
turning audit findings into active policy.

## Repository Role

This document supports Stage 03 and Stage 04 planning for future governance,
automation, and provider work. It must not replace Stage 00 policy, Stage 04
task evidence, Stage 05 operations procedures, CI workflow source, scripts, or
runtime Compose files.

## Scope

### In Scope

- Harness engineering implementation status.
- Loop engineering implementation status.
- Provider harness and loop parity.
- Common workspace rules and environment.
- Automation, pipeline, workflow, spec-driven SDLC, Docker Compose,
  infrastructure, CI/CD, QA, formatting, linting, and security status.

### Out of Scope

- Fixing discovered gaps.
- Changing provider, CI, runtime, operations, script, or security behavior.
- Deployment readiness claims.
- Secret values, credentials, tokens, private keys, shell history, raw logs, or
  `.env` values.

## Definitions / Facts

- **Implemented**: repo-local evidence exists and current validators,
  documentation, or runtime surfaces support the claim.
- **Partially Implemented**: a surface exists, but parity, automation,
  validation, freshness, or operational linkage is incomplete.
- **Not Implemented**: the research baseline identifies a relevant capability,
  but no repo-local artifact was found.
- **Unknown / Needs Revalidation**: the current implementation or provider
  behavior cannot be asserted without renewed evidence.

## Assessment Method

The audit used the research pack as the criteria source, read repo-local
canonical surfaces, and rechecked fast-moving provider sources on 2026-07-05.
The assessment favors conservative status labels when provider-native behavior
or enforcement depth differs from repository policy.

## Implementation Status Matrix

| Category | Status | Evidence | Summary |
| --- | --- | --- | --- |
| Harness engineering | Implemented | [Harness map](../../../00.agent-governance/harness-implementation-map.md), [approval boundaries](../../../00.agent-governance/rules/approval-boundaries.md), [scripts README](../../../../scripts/README.md) | Governance, runtime, validation, CI, scripts, hooks, evidence, and operations surfaces are mapped and validation-backed. |
| Loop engineering | Partially Implemented | [Subagent protocol](../../../00.agent-governance/subagent-protocol.md), [provider capability matrix](../../../00.agent-governance/rules/provider-capability-matrix.md), `.github/workflows/ci-quality.yml` | Context, validation, CI, memory, approval, and hook loops exist; eval and semantic feedback loops are less complete. |
| Claude provider harness/loop | Implemented | [Claude provider notes](../../../00.agent-governance/providers/claude.md), `.claude/settings.json`, `.claude/agents/`, `.claude/hooks/` | Repo-local Claude adapter aligns with official first-class subagents and hooks. |
| Codex provider harness/loop | Implemented | [Codex provider notes](../../../00.agent-governance/providers/codex.md), `.codex/hooks.json`, `.codex/agents/`, `.codex/skills/` | Repo-local Codex adapter aligns with official AGENTS.md, subagent, hook, sandbox, and approval concepts. |
| Gemini provider harness/loop | Partially Implemented | [Gemini provider notes](../../../00.agent-governance/providers/gemini.md), `.agents/`, official Gemini CLI docs | Repo-local pointer adapters and behavioral contracts exist; official Gemini CLI evidence supports ReAct/MCP/context, not Claude/Codex-style native subagents or hooks. |
| Common provider-neutral rules/environment | Implemented | [Stage 00 governance hub](../../../00.agent-governance/README.md), [provider capability matrix](../../../00.agent-governance/rules/provider-capability-matrix.md), [documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md) | Shared policy, templates, scopes, model tiers, memory, and provider-adapter routing exist. |
| Automation, pipeline, workflow | Partially Implemented | [scripts README](../../../../scripts/README.md), `.github/workflows/ci-quality.yml`, `.claude/hooks/`, `.codex/hooks.json` | Local scripts, CI gates, provider hooks, generated indexes, and sync checks exist; semantic agent-eval automation and Gemini native hooks remain partial. |
| Spec-driven SDLC | Implemented | [Stage 03 README](../../../03.specs/README.md), [Stage 04 plans README](../../../04.execution/plans/README.md), [Stage 04 tasks README](../../../04.execution/tasks/README.md) | Stage-gated spec, plan, task, operations, and reference taxonomy is active and validator-backed. |
| Docker Compose / infrastructure | Implemented | [infra README](../../../../infra/README.md), `docker-compose.yml`, `infra/**/docker-compose*.yml`, `infra/tech-stack.versions.json` | Modular Compose topology, profiles, root-active inventory, service READMEs, version registry, validation, and hardening checks exist. |
| CI/CD | Implemented | `.github/workflows/ci-quality.yml`, [GitHub governance](../../../00.agent-governance/rules/github-governance.md) | CI quality gates cover docs, repo contracts, Compose, hardening, template/security, pre-commit, frontend quality, coverage, and workflow security. |
| QA, formatting, linting, syntax | Partially Implemented | `.github/workflows/ci-quality.yml`, [scripts README](../../../../scripts/README.md), [Codex provider notes](../../../00.agent-governance/providers/codex.md) | Strong docs, shell, Compose, frontend, pre-commit, and contract checks exist; universal language-specific formatting/linting coverage is not complete across every surface. |
| Security | Partially Implemented | [approval boundaries](../../../00.agent-governance/rules/approval-boundaries.md), `.github/SECURITY.md`, `.github/workflows/ci-quality.yml`, [security research](../../research/2026-07-05-agentic-research-pack-refresh/security-governance.md) | Secret boundaries, workflow permissions, hardening, security reporting, and approvals exist; full SSDF/SLSA maturity and attestation automation are not fully adopted. |

## Findings

- The workspace has a mature documentation and validation harness. Stage 00,
  Stage 03, Stage 04, Stage 90, Stage 99, CI, scripts, provider surfaces, and
  operations documents are connected by explicit contracts.
- The strongest implementation areas are governance, template contracts,
  documentation traceability, Compose validation, local/remote quality gates,
  and Claude/Codex runtime adapters.
- The main partial areas are semantic agent evaluation, Gemini native feature
  parity, full provider-adapter semantic parity checks, and complete
  supply-chain/security maturity automation.

## Gap / Follow-up

| Gap | Impact | Candidate Owner |
| --- | --- | --- |
| Semantic parity checks across provider adapter content are limited. | Provider surfaces can match catalog shape while drifting in detailed behavior. | Stage 00 governance / validation follow-up |
| Gemini native hook and subagent parity is not proven by official sources. | Gemini must remain behavioral/pointer parity, not first-class parity. | Provider research follow-up |
| Agent-result eval harness now has fixtures but no executable gate. | Loop engineering maturity still depends on manual review and task evidence for many agent outputs. | [Agent-output eval fixtures](../../data/governance/agent-output-eval-fixtures.md) |
| Security framework adoption is reference-backed and now mapped, but not fully automated. | SSDF/SLSA maturity cannot be claimed as fully implemented because SBOM, provenance, attestation, and vulnerability-gate evidence is still incomplete. | [Security framework maturity coverage](./security-framework-maturity.md) |

## Automation Impact

The highest-value remaining automation candidates are an executable
agent-output eval runner, full automated audit-matrix refresh from repo paths,
vulnerability gating, SBOM, and provenance/attestation automation. Changed-path
QA recommendations are now surfaced in CI Step Summary, audit-pack
implementation-status coverage is now reportable through repo contracts, and
LLM Wiki safe-path coverage is grouped by source bucket/category in Stage 90
data.

## Source Rules

- Prefer Stage 00, Stage 04, Stage 90 research, scripts, CI workflows, and
  infrastructure files for repo-local claims.
- Prefer official vendor docs and standards for provider or framework facts.
- Re-check provider docs before making current parity claims.

## Sources

- [Agentic engineering research pack](../../research/2026-07-05-agentic-research-pack-refresh/README.md) - criteria source.
- [Audit pack task evidence](../../../04.execution/tasks/2026-07-05-agentic-engineering-implementation-audit-pack.md) - source inventory and validation evidence.
- [Stage 00 governance hub](../../../00.agent-governance/README.md) - governance SSoT.
- [Provider capability matrix](../../../00.agent-governance/rules/provider-capability-matrix.md) - common capability mapping.
- [Harness implementation map](../../../00.agent-governance/harness-implementation-map.md) - harness surface routing.
- [scripts README](../../../../scripts/README.md) - local automation and validation surface.
- [infra README](../../../../infra/README.md) - Compose/infrastructure topology.
- [CI quality workflow](../../../../.github/workflows/ci-quality.yml) - remote CI/CD and QA gates.
- [Claude Code docs](https://code.claude.com/docs/en/overview) - external Claude Code capability criteria.
- [Codex CLI docs](https://developers.openai.com/codex/cli) - external Codex capability criteria.
- [Gemini CLI docs](https://developers.google.com/gemini-code-assist/docs/gemini-cli) - external Gemini CLI capability criteria.

## Maintenance

- **Owner**: Documentation Specialist / Agentic Workflow Specialist.
- **Review Cadence**: Review after provider adapter, CI, scripts, Stage 00, or
  infrastructure-harness changes.
- **Update Trigger**: Update when the research pack changes, provider docs add
  or remove native capabilities, or validation scripts change coverage.

## Related Documents

- [Audit pack README](./README.md)
- [Harness implementation audit](./harness-engineering-implementation.md)
- [Loop implementation audit](./loop-engineering-implementation.md)
- [Security framework maturity coverage](./security-framework-maturity.md)
- [Research pack](../../research/2026-07-05-agentic-research-pack-refresh/README.md)
- [Audit pack spec](../../../03.specs/105-agentic-engineering-implementation-audit-pack/spec.md)
- [Audit pack plan](../../../04.execution/plans/2026-07-05-agentic-engineering-implementation-audit-pack.md)
