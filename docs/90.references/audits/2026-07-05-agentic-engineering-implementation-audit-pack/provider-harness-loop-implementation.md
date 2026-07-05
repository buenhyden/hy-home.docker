---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/provider-harness-loop-implementation.md -->

# Reference: Provider Harness and Loop Implementation

## Overview

This reference audits Claude, Codex, and Gemini provider implementation status
for harness and loop engineering in `hy-home.docker`.

## Purpose

The purpose is to distinguish repository-local provider adapter parity from
official provider-native feature parity. This prevents the workspace from
overstating Gemini native hook or subagent capabilities while preserving the
shared provider-neutral governance contract.

## Repository Role

This document supports provider maintenance and future provider-parity work. It
does not replace provider runtime files, Stage 00 provider notes, or official
provider documentation.

## Scope

### In Scope

- Claude, Codex, and Gemini harness/loop implementation status.
- Common provider-neutral rules and environment.
- Runtime adapter evidence under `.claude/`, `.codex/`, and `.agents/`.
- Official provider source revalidation for subagents, hooks, context, and MCP.

### Out of Scope

- Changing provider runtime configuration.
- Adding or deleting agents, hooks, or skills.
- Changing model policy.
- Claiming provider-native parity without current official source support.

## Definitions / Facts

- **Repo-local parity** means the repository exposes common roles, scopes,
  templates, memory, and rules through provider adapters.
- **Provider-native parity** means the upstream product has the same native
  primitive, such as first-class subagents or programmatic hooks.
- **Behavioral parity** means a provider follows the shared rule manually or by
  convention when it lacks a native primitive.

## Assessment Method

The audit read Stage 00 provider notes, the provider capability matrix, the
subagent protocol, provider adapter folders, and current official provider
documentation rechecked on 2026-07-05.

## Implementation Status Matrix

| Capability | Claude | Codex | Gemini | Repo-local Evidence |
| --- | --- | --- | --- | --- |
| Shared entry route | Implemented | Implemented | Implemented | `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, [provider notes](../../../00.agent-governance/providers/agents-md.md) |
| Provider notes | Implemented | Implemented | Implemented | [Claude](../../../00.agent-governance/providers/claude.md), [Codex](../../../00.agent-governance/providers/codex.md), [Gemini](../../../00.agent-governance/providers/gemini.md) |
| Agent catalog adapter | Implemented | Implemented | Partially Implemented | `.claude/agents/`, `.codex/agents/`, `.agents/agents/`; Gemini uses pointer/reference-index adapters. |
| Skills/functions adapter | Implemented | Implemented | Partially Implemented | `.claude/skills/`, `.codex/skills/`, `.agents/skills/`; Gemini uses pointer/reference-index adapters. |
| First-class subagents in official product | Implemented | Implemented | Not Implemented / Needs Revalidation | Claude and Codex official docs document subagents; official Gemini CLI docs reviewed here describe ReAct/MCP/context and tools, not first-class subagent parity. |
| Programmatic hooks | Implemented | Implemented | Not Implemented / Behavioral | Claude and Codex repo adapters plus official docs support hooks; Gemini provider notes record behavioral parity only. |
| Context file model | Implemented | Implemented | Implemented | CLAUDE.md, AGENTS.md, GEMINI.md, Gemini context configuration docs, Stage 00 loading sequence. |
| MCP/tool integration | Implemented | Implemented | Implemented | Provider notes and official docs support tool/MCP integration; repository policy keeps tool use bounded by approval rules. |
| Sandbox / approval boundary | Partially Implemented | Implemented | Partially Implemented | Codex has explicit sandbox/approval model; Claude/Gemini rely on provider settings plus Stage 00 approval boundaries. |
| Model policy mapping | Implemented | Implemented | Implemented | [Subagent protocol](../../../00.agent-governance/subagent-protocol.md) and provider adapters. |
| Hook parity validation | Partially Implemented | Partially Implemented | Not Implemented / Behavioral | Structural checks exist; semantic parity across all hook behavior is not fully automated. |

## Findings

- Claude and Codex have the closest match between repository adapter design and
  current official product features: both support native subagents and hooks.
- Gemini participates in the common workspace through `.agents/` pointer
  adapters, shared context loading, MCP/tools, and behavioral contracts.
- Gemini should remain labeled partial for first-class subagents and hooks
  until official Gemini sources document equivalent native primitives.
- The repository has strong shape parity but weaker semantic parity checks
  across generated or mirrored provider files.

## Gap / Follow-up

| Gap | Status | Follow-up Direction |
| --- | --- | --- |
| Gemini first-class subagent parity | Not Implemented / Needs Revalidation | Recheck official Gemini CLI and Gemini Code Assist docs before changing status. |
| Gemini programmatic hook parity | Not Implemented / Behavioral | Keep manual behavioral contract and document provider limitation. |
| Provider adapter semantic drift | Partially Implemented | Add a validator that extracts critical clauses from provider adapters and Stage 00 sources. |
| Provider source freshness | Partially Implemented | Add scheduled source revalidation notes or a dated provider capability review task. |

## Automation Impact

Automation should focus on provider adapter drift detection: compare catalog
names, model values, scope imports, rule links, hook contract clauses, and
critical provider-specific limitations in one generated report.

## Source Rules

- Official provider feature claims must cite current official provider docs.
- Repo-local adapter claims must cite Stage 00 and provider adapter paths.
- Do not infer Gemini first-class subagents from `.agents/` pointer adapters.

## Sources

- [Provider comparison research](../../research/2026-07-05-agentic-research-pack-refresh/provider-implementation-comparison.md) - research baseline.
- [Provider capability matrix](../../../00.agent-governance/rules/provider-capability-matrix.md) - repo-local capability mapping.
- [Subagent protocol](../../../00.agent-governance/subagent-protocol.md) - role and model policy mapping.
- [Claude provider notes](../../../00.agent-governance/providers/claude.md) - Claude adapter contract.
- [Codex provider notes](../../../00.agent-governance/providers/codex.md) - Codex adapter contract.
- [Gemini provider notes](../../../00.agent-governance/providers/gemini.md) - Gemini adapter contract.
- [Claude subagents docs](https://code.claude.com/docs/en/sub-agents) - official Claude subagent criteria.
- [Claude hooks docs](https://code.claude.com/docs/en/hooks) - official Claude hook criteria.
- [Codex subagents docs](https://developers.openai.com/codex/subagents) - official Codex subagent criteria.
- [Codex hooks docs](https://developers.openai.com/codex/hooks) - official Codex hook criteria.
- [Gemini CLI docs](https://developers.google.com/gemini-code-assist/docs/gemini-cli) - official Gemini ReAct/MCP/context criteria.

## Maintenance

- **Owner**: Agentic Workflow Specialist.
- **Review Cadence**: Review after provider docs, provider adapters, model
  policy, or sync script changes.
- **Update Trigger**: Update when a provider adds/removes native subagents,
  hooks, model controls, or context mechanisms.

## Related Documents

- [Audit pack README](./README.md)
- [Implementation overview](./implementation-overview.md)
- [Workspace rules/environment audit](./workspace-rules-environment-implementation.md)
- [Research pack](../../research/2026-07-05-agentic-research-pack-refresh/README.md)
