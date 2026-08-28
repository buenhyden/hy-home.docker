---
status: draft
artifact_id: reference:agentic-engineering-research-draft:agent-instructions-vibe-coding
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-28
review_cycle: on-source-change
---

# Agent Instructions and Bounded Generated Work

## Overview

Instructions supply scoped context; configuration supplies native mechanics;
neither alone proves a prompt was loaded or work was accepted. Generated work
is safe only when it stays within the same ownership and review boundaries as
hand-authored work.

## Purpose

Separate instruction layering from configuration, explain progressive skill
discovery, and define a bounded review path for conversational implementation.

## Scope

This leaf covers repository instruction routing and retained provider
capability observations. It excludes personal configuration, prompt contents,
runtime session state, and changes to generated adapters.

## Definitions / Facts

| Claim ID | Claim | Evidence class | State | Workspace target | Implication |
| --- | --- | --- | --- | --- | --- |
| `AIV-001` | The bootstrap policy orders direct user/system authority, Stage 00 policy, Stage 99 document authority, current stage documents, provider adapters, and evidence; generated projections are not policy sources. | tracked configuration | VERIFIED | `docs/00.agent-governance/policies/bootstrap.md` | A prompt or generated adapter cannot override a canonical owner. |
| `AIV-002` | Claude and Codex adapters define different native loading/mechanics while requiring the active Spec and Task for repository changes. | tracked configuration | VERIFIED | `docs/00.agent-governance/providers/{claude.md,codex.md}` | Discover provider-specific syntax after resolving shared authority. |
| `AIV-003` | The retained Codex skills observation says skills support progressive disclosure and explicit or implicit invocation, but it does not prove local discovery or execution. | retained official observation | HISTORICAL VERIFIED | Task 0001 source ledger | Load only needed skill instructions and retain runtime uncertainty. |
| `AIV-004` | Bounded generated work needs an approved scope, a narrow implementation, focused validation, independent review, and escalation after the permitted correction. | advisory synthesis grounded in tracked contract | ADVISORY | `docs/00.agent-governance/providers/registry.yaml` | Do not accept generated output merely because it appears plausible. |
| `AIV-005` | Retained instruction observations distinguish Claude instruction/memory hierarchy and imports from Codex `AGENTS.override.md`/`AGENTS.md` global-to-project-root-to-CWD discovery with one file per directory. | retained official observation | HISTORICAL VERIFIED | retained dated instruction analysis | Apply progressive discovery without treating either mechanism as proof of local loading. |

### Instruction layers and generated-work boundary

| Layer | Responsibility | Evidence limit |
| --- | --- | --- |
| Direct task authority | Sets the immediate request and higher-priority constraints. | Not a repository runtime proof. |
| Canonical policy and role | Defines shared ownership, permissions, and completion criteria. | Tracked definition only. |
| Root entry and provider adapter | Routes bootstrap and native syntax. | Presence does not prove loading. |
| Skill body | Supplies task-specific instructions through progressive discovery. | Discovery/invocation remains unobserved. |
| Native configuration/hooks | Encodes provider mechanics. | Configuration is not execution. |
| Prompt-generated output | Proposed work requiring normal validation and review. | Never self-authenticates. |

A bounded conversational loop begins by discovering the applicable authority
and only the relevant skill material. It then produces the smallest scoped
change, checks it with the named gate, and gives an independent reviewer the
exact diff and evidence. Missing authority, a protected surface, source
insufficiency, or a failed narrow correction is an escalation point—not an
invitation to keep prompting.

The retained sources distinguish the native discovery mechanisms: Claude's
memory documentation was observed for instruction/memory hierarchy capability,
while Codex's AGENTS.md documentation was observed for discovery/order/size
capability. They inform a provider-neutral progressive-discovery practice but
do not establish that this repository loaded either file in a live session.

## Sources

| Source ID | Claim IDs | Title / publisher | URL or path | Class | Revision / observed | Accessed at | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `AIV-SRC-001` | `AIV-001` | Agent Bootstrap Policy / workspace | [bootstrap policy](../../../00.agent-governance/policies/bootstrap.md) | tracked configuration | `bbe8d9f35b5b57f0fdd647504f4015f651a4d58f` | 2026-08-28 | Authority routing does not prove compliance. |
| `AIV-SRC-002` | `AIV-002`, `AIV-004` | Claude and Codex provider adapters; registry / workspace | [Claude](../../../00.agent-governance/providers/claude.md); [Codex](../../../00.agent-governance/providers/codex.md); [registry](../../../00.agent-governance/providers/registry.yaml) | tracked configuration | `bbe8d9f35b5b57f0fdd647504f4015f651a4d58f` | 2026-08-28 | Local declarations cannot prove a provider accepted them. |
| `AIV-SRC-003` | `AIV-003` | Codex skills / OpenAI | [official page](https://learn.chatgpt.com/docs/build-skills) | retained official observation | retrieval-time page | 2026-08-08T16:07:00+09:00 | Mutable historical capability; no local skill run inferred. |
| `AIV-SRC-004` | `AIV-005` | Claude Code memory / Anthropic | [official page](https://code.claude.com/docs/en/memory) | retained official observation | retained dated leaf C-MEM row; version not recorded | 2026-08-14 | Historical hierarchy/import mechanics; no local loading inferred. |
| `AIV-SRC-005` | `AIV-005` | Codex AGENTS.md / OpenAI | [official page](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | retained official observation | retained dated leaf O-INSTR row; version not recorded | 2026-08-14 | Historical global-to-CWD discovery mechanics; no local loading inferred. |

## Scope Application

| Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
| --- | --- | --- | --- | --- |
| agentic | applies | Resolve instruction layers before work. | Inspect bootstrap precedence, then the matching adapter and selected skill body. | Loading unobserved. |
| architecture | applies | Route generated design claims to owners. | Review source and authority. | No architecture decision. |
| common | applies | Keep projections subordinate to policy. | Inspect canonical source first. | No enforcement proof. |
| docs | applies | Review generated prose and links. | Run focused metadata/link checks. | Plausibility is insufficient. |
| infra | applies | Escalate runtime-affecting prompts. | Require explicit approval. | No environment access. |
| ops | applies | Hand off operational generation to ops. | Preserve sanitized evidence. | No runbook execution. |
| qa | applies | Require independent review after checks. | Inspect exact diff, named validation gate, and reviewer evidence. | No self-acceptance. |
| security | applies | Reject prompts seeking secrets or bypasses. | Confirm excluded-material boundary. | No security execution. |

## Maintenance

Update this analysis when the bootstrap, adapters, skill contract, or retained
observation changes. Keep instruction discovery distinct from proof of loading.

## Related Documents

- [Provider comparison](./provider-implementation-comparison.md)
- [Loop engineering](./loop-engineering.md)
- [Research pack README](./README.md)
