---
status: active
---

<!-- Target: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/loop-engineering-implementation.md -->

# Reference: Loop Engineering Implementation

## Overview

This reference audits how feedback loops from the loop-engineering research
baseline are implemented in `hy-home.docker`.

## Purpose

The purpose is to separate implemented loops from partially implemented or
manual loops so follow-up automation can target the right gaps.

## Repository Role

This document supports future planning for agent feedback, validation, memory,
CI, approval, operations, and evaluation loops. It does not define active
workflow policy or replace scripts, CI workflows, provider adapters, or task
evidence.

## Scope

### In Scope

- Agent context and planning loops.
- Subagent/delegation loops.
- Validation and CI loops.
- Memory and evidence loops.
- Human approval loops.
- Eval and semantic feedback loops.
- Operations and incident learning loops.

### Out of Scope

- Implementing new eval jobs or CI gates.
- Changing runtime hooks or provider configuration.
- Changing incident, postmortem, runbook, or operations policy content.
- Secret values, credentials, tokens, private keys, raw logs, shell history, or
  `.env` values.

## Definitions / Facts

- **Loop engineering** means designing feedback cycles that turn observation
  into safer next action: context -> action -> validation -> evidence ->
  memory or follow-up.
- **Human approval loop** means protected state changes require explicit user
  approval and recorded evidence.
- **Eval loop** means a repeatable check of agent output against criteria or
  fixtures, not just a one-time manual review.

## Assessment Method

The audit compared loop-engineering research criteria with Stage 00 workflow
rules, subagent protocol, provider hooks, validation scripts, CI jobs, Stage 04
task evidence, memory/progress, operations docs, and generated reference
indexes.

## Implementation Status Matrix

| Loop | Status | Evidence | Notes |
| --- | --- | --- | --- |
| Bootstrap / context loop | Implemented | `AGENTS.md`, [Stage 00 governance hub](../../../00.agent-governance/README.md), [documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md) | Root shims and Stage 00 define loading sequence, scope, memory, and stage rules. |
| Brainstorm / spec / plan loop | Implemented | [Stage 03 README](../../../03.specs/README.md), [Stage 04 plans README](../../../04.execution/plans/README.md), [audit pack spec](../../../03.specs/105-agentic-engineering-implementation-audit-pack/spec.md) | Design and execution artifacts are routed through canonical stages. |
| Delegation / subagent loop | Partially Implemented | [subagent protocol](../../../00.agent-governance/subagent-protocol.md), `.claude/agents/`, `.codex/agents/`, `.agents/agents/` | Governance and adapters exist; runtime-native parity differs by provider. |
| Hook pre/post edit loop | Partially Implemented | `.claude/hooks/`, `.codex/hooks.json`, [provider notes](../../../00.agent-governance/providers/gemini.md) | Claude/Codex hooks exist; Gemini follows behavioral contract. |
| Local validation loop | Implemented | [scripts README](../../../../scripts/README.md), `scripts/validation/**` | Local checks cover docs, contracts, Compose, hardening, templates, and QA bundles. |
| CI feedback loop | Implemented | `.github/workflows/ci-quality.yml` | CI repeats quality gates on push and pull request. |
| Memory / progress loop | Implemented | [progress memory](../../../00.agent-governance/memory/progress.md), [memory README](../../../00.agent-governance/memory/README.md) | Agents must review and update progress memory during repository work. |
| Generated index freshness loop | Implemented | `scripts/knowledge/generate-llm-wiki-index.sh`, `docs/90.references/llm-wiki/llm-wiki-index.md` | LLM Wiki freshness is checked by repo contracts. |
| Human approval loop | Implemented | [approval boundaries](../../../00.agent-governance/rules/approval-boundaries.md), task approved-surface evidence | Protected surfaces and hard stops require explicit approval and evidence. |
| Operations learning loop | Partially Implemented | `docs/05.operations/**`, [documentation protocol](../../../00.agent-governance/rules/documentation-protocol.md), [HAFE guide](../../../05.operations/guides/00-workspace/harness-agent-first-engineering.md), incidents structure | Operations docs, postmortem routing, and manual gap-to-stage routing exist; not every audit gap has generated closure review or operational feedback evidence. |
| Eval / semantic scoring loop | Partially Implemented | [loop research](../../research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md), scripts/CI surface | Research and QA concepts exist, but general-purpose agent-output eval is not a full CI gate. |

## Findings

- The repository has strong structural loops: context loading, stage-gated
  design and plan handoff, validation scripts, CI repetition, progress memory,
  generated-index freshness, and approval boundaries.
- The repository has partial semantic loops: subagent result review, provider
  adapter semantic parity, agent-output evals, and operations-to-governance
  learning depend on task evidence and human judgment more than automated
  scoring.
- Loop maturity is intentionally conservative where providers differ. Gemini
  can participate through shared context and pointer adapters, but native
  hooks/subagents should not be claimed.

## Gap / Follow-up

| Gap | Impact | Follow-up Direction |
| --- | --- | --- |
| Agent-output eval loop is not generalized. | Regression risk remains for agent behavior that passes structural checks. | Create small eval fixtures for common docs, provider, and infra tasks. |
| Provider semantic parity loop is partial. | Adapter files may drift in behavioral detail even when catalog parity passes. | Add diff/extraction checks for critical clauses. |
| Operations learning loop is selective. | Audit findings may not consistently become policies, runbooks, or backlog items. | Manual gap-to-stage routing now exists in Stage 00; add a recurring audit closure review or generated routing report if stronger automation is needed. |
| Gemini behavioral parity loop is manual. | Gemini users must remember hook-equivalent obligations. | Keep explicit Gemini gap rows and revalidate official docs periodically. |

## Automation Impact

Future loop automation should focus on semantic checks: provider-adapter clause
diffing, automated audit-gap routing, agent-output eval fixtures, and a generated loop
coverage matrix that is refreshed from repository paths.

## Source Rules

- Loop implementation claims must cite repo-local scripts, CI, provider notes,
  Stage 00 governance, Stage 04 evidence, operations docs, or generated-index
  maintenance scripts.
- External loop-engineering papers and vendor docs remain criteria sources,
  not active policy.

## Sources

- [Loop engineering research](../../research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md) - criteria source.
- [Stage 00 governance hub](../../../00.agent-governance/README.md) - context, workflow, memory, and policy loop evidence.
- [Subagent protocol](../../../00.agent-governance/subagent-protocol.md) - delegation loop evidence.
- [Approval boundaries](../../../00.agent-governance/rules/approval-boundaries.md) - human approval loop evidence.
- [scripts README](../../../../scripts/README.md) - local validation, hook, and generated-index loops.
- [CI quality workflow](../../../../.github/workflows/ci-quality.yml) - remote CI feedback loop.
- [HAFE guide](../../../05.operations/guides/00-workspace/harness-agent-first-engineering.md) - operational audit usage loop.
- [Task evidence](../../../04.execution/tasks/2026-07-05-agentic-engineering-implementation-audit-pack.md) - audit execution loop evidence.
- [ReAct paper](https://arxiv.org/abs/2210.03629) - external reason/action loop concept.
- [Reflexion paper](https://arxiv.org/abs/2303.11366) - external verbal feedback and memory loop concept.

## Maintenance

- **Owner**: Agentic Workflow Specialist / QA Engineer.
- **Review Cadence**: Review after provider, hook, CI, validation, operations,
  or task-evidence workflow changes.
- **Update Trigger**: Update when new eval automation, provider-native loops,
  or operational feedback loops are introduced.

## Related Documents

- [Audit pack README](./README.md)
- [Implementation overview](./implementation-overview.md)
- [Harness implementation audit](./harness-engineering-implementation.md)
- [Research pack](../../research/2026-07-05-agentic-research-pack-refresh/README.md)
- [Audit pack task evidence](../../../04.execution/tasks/2026-07-05-agentic-engineering-implementation-audit-pack.md)
