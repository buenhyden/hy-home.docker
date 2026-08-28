---
status: draft
artifact_id: reference:agentic-engineering-research-draft:harness-engineering
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-28
review_cycle: on-source-change
---

# Harness Engineering

## Overview

An agent harness is the controlled boundary around a task: it selects context,
role, tools, authority, provider translation, feedback, and evidence. This is
advisory synthesis, not evidence that any native hook, model, or CI job ran.

## Purpose

Describe a provider-neutral construction that can be inspected locally without
confusing a tracked declaration with runtime or remote enforcement.

## Scope

This leaf covers the registered harness layers and their inspection targets.
It excludes provider-private state, credentials, live services, and changes to
Stage 00, adapters, scripts, or generated surfaces.

## Definitions / Facts

Configuration establishes an intended binding; execution evidence requires a
separately authorized observed run. A permission profile grants only the
declared action class, not ownership of an arbitrary path or external state.

| Claim ID | Claim | Evidence class | State | Workspace target | Implication |
| --- | --- | --- | --- | --- | --- |
| `HE-001` | The local registry defines eight harness layers: canonical contract, role/skill routing, permission boundary, provider/model policy, semantic events, controlled validation, tracked CI, and sanitized evidence. | tracked configuration | VERIFIED | `docs/00.agent-governance/providers/registry.yaml` | Inspect the named owner and gate before extending a harness. |
| `HE-002` | The registry separates canonical sources from generated adapters and records Claude and Codex as supported/adopted while their `runtime_acceptance` remains `needs_revalidation`. | tracked configuration | VERIFIED | `docs/00.agent-governance/providers/{registry.yaml,claude.md,codex.md}` | Adapter presence does not prove loading, acceptance, or execution. |
| `HE-003` | Official hook documentation observed on 2026-08-08 describes lifecycle/configuration capability; it does not establish this repository's active interception. | retained official observation | HISTORICAL VERIFIED | Task 0001 source ledger | Treat provider hooks as historical capability evidence only. |
| `HE-004` | The registry requires command, result, rollback, and skipped-check fields and prohibits auth files, credentials, raw logs, secret values, shell history, and tokens. | tracked configuration | VERIFIED | `docs/00.agent-governance/providers/registry.yaml` | Record value-free evidence and escalate when proof would require excluded material. |
| `HE-005` | Retained hook observations distinguish Claude command/HTTP/prompt/agent/MCP-tool handlers across 31 events from Codex command hooks across 11 events, with Codex project hooks trust-gated and its main-thread `SessionEnd` advisory. | retained official observation | HISTORICAL VERIFIED | retained dated provider comparison | Translate feedback semantics per native adapter; do not infer that either hook fired locally. |

### Construction and inspection targets

1. Start from the canonical contract in `registry.yaml`, then inspect the role
   and skill sources named by its patterns; generated adapters may translate
   syntax but cannot define lifecycle, policy, or completion criteria.
2. Resolve a role's work profile and permission profile before selecting tools.
   Read-only discovery and workspace-write implementation are distinct from
   approval for protected, runtime, remote, or secret-bearing work.
3. Inspect provider adapters at `providers/claude.md` and `providers/codex.md`
   for native paths. Claude names `.claude/agents/`, `.claude/skills/`, and
   `.claude/settings.json`; Codex names `.codex/agents/*.toml`, shared
   `.agents/skills/*/SKILL.md`, and `.codex/hooks.json`.
4. Treat `semantic_events` as declared mapping data. The registry contains
   seven Claude events including `SessionEnd` and six Codex events without it.
   A historical upstream Codex `SessionEnd` observation is not local adoption.
5. Run only the authorized, smallest validation gate. Tracked CI is a layer,
   not proof of a hosted execution. Attach sanitized evidence and hand off to
   an independent reviewer before a completion claim.

The retained observations make the feedback boundary concrete. A provider may
offer a handler shape or event, yet the local harness must still decide whether
its result is advisory, a native block, or a repository gate. The local Codex
six-event registry intentionally remains the inspection target for this draft;
the historical upstream `SessionEnd` observation identifies a revalidation gap,
not an extra active event.

### Environment prerequisites

An implementation needs an approved objective, a known repository state,
the applicable Spec and Task, a canonical owner, and a permission-compatible
worktree. Runtime proof additionally needs separate concrete-target approval,
pre-check, rollback, post-check, and a redacted record. None was sought here.

## Sources

| Source ID | Claim IDs | Title / publisher | URL or path | Class | Revision / observed | Accessed at | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `HE-SRC-001` | `HE-001`, `HE-004` | Provider registry / workspace | [registry](../../../00.agent-governance/providers/registry.yaml) | tracked configuration | `bbe8d9f35b5b57f0fdd647504f4015f651a4d58f` | 2026-08-28 | Declared controls do not prove execution. |
| `HE-SRC-002` | `HE-002` | Provider registry / workspace | [registry](../../../00.agent-governance/providers/registry.yaml) | tracked configuration | `bbe8d9f35b5b57f0fdd647504f4015f651a4d58f` | 2026-08-28 | Adoption and acceptance flags are registry fields, not adapter proof. |
| `HE-SRC-003` | `HE-002` | Claude and Codex provider adapters / workspace | [Claude](../../../00.agent-governance/providers/claude.md); [Codex](../../../00.agent-governance/providers/codex.md) | tracked configuration | `bbe8d9f35b5b57f0fdd647504f4015f651a4d58f` | 2026-08-28 | Native paths are configuration surfaces only. |
| `HE-SRC-004` | `HE-003` | Claude Code hooks / Anthropic | [official page](https://code.claude.com/docs/en/hooks) | retained official observation | retrieval-time page | 2026-08-08T15:48:51+09:00 | Historical hook lifecycle/configuration capability; no local execution inferred. |
| `HE-SRC-005` | `HE-003` | Codex hooks / OpenAI | [official page](https://learn.chatgpt.com/docs/hooks) | retained official observation | retrieval-time page | 2026-08-08T15:48:51+09:00 | Historical page included advisory main-thread `SessionEnd`; local Codex registry does not adopt it. |
| `HE-SRC-006` | `HE-005` | Claude Code hooks / Anthropic | [official page](https://code.claude.com/docs/en/hooks) | retained official observation | retained dated leaf C-HOOK row; version not recorded | 2026-08-14 | Retained detail records handler/event behavior; no local firing inferred. |
| `HE-SRC-007` | `HE-005` | Codex hooks / OpenAI | [official page](https://learn.chatgpt.com/docs/hooks) | retained official observation | retained dated leaf O-HOOK row; version not recorded | 2026-08-14 | Retained detail records trust/advisory behavior; no local firing inferred. |

## Scope Application

| Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
| --- | --- | --- | --- | --- |
| agentic | applies | Route changes through the eight layers. | Inspect `registry.yaml` harness layers/events and the role/skill source named by its patterns. | No runtime proof. |
| architecture | applies | Bind an agent change to its owner artifact. | Review scoped design evidence. | No architecture decision created. |
| common | applies | Preserve shared canonical sources. | Compare adapters with canonical sources, then use documented adapter parity check when authorized. | Parity requires a separate gate. |
| docs | applies | Record only evidence-backed claims. | Check source mappings. | This leaf is advisory. |
| infra | applies | Seek approval before environment observation. | Use concrete-target pre/post checks. | No service was run. |
| ops | applies | Escalate operational proof to its owner. | Review sanitized handoff. | No incident or telemetry. |
| qa | applies | Use the smallest registered gate. | Inspect the registry gate and record the scoped command/exit. | CI configuration is not CI execution. |
| security | applies | Keep sensitive evidence excluded. | Inspect evidence fields. | Control effectiveness unverified. |

## Maintenance

Revisit when the registry, adapters, or retained source record changes. Do not
convert a capability observation into a current runtime claim without approval.

## Related Documents

- [Research pack README](./README.md)
- [Loop engineering](./loop-engineering.md)
- [Provider comparison](./provider-implementation-comparison.md)
