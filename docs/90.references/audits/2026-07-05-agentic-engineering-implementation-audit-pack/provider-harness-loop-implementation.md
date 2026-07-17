---
status: active
artifact_id: audit:agentic-engineering-implementation:provider-harness-loop
artifact_type: audit
parent_ids: [audit:agentic-engineering-implementation:overview]
supersedes: [audit:agentic-engineering-implementation-2026-07-07:harness-loop]
reviewed_at: 2026-07-12
review_cycle: per-remediation-task
---

<!-- Target: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/provider-harness-loop-implementation.md -->

# Reference: Provider Harness and Loop Implementation

## Overview

This reference assesses every `PIC-*` provider criterion against tracked
Claude, Codex, Gemini/Antigravity, and Stage 00 surfaces at baseline `507cd505`
on 2026-07-11.

## Purpose

Keep three claims separate: a provider-native feature documented by an
official source, its tracked workspace adoption, and active repository policy.

## Repository Role

This is advisory provider-maintenance evidence. Stage 00 and provider runtime
files remain authoritative; the fixed model catalog remains bound to the
2026-07-10 10:00 KST cutoff.

## Scope

### In Scope

- `PIC-01` through `PIC-17`, tracked provider adapters, current primary-source
  capability evidence, model literals, sync, and eval-fixture adoption.

### Out of Scope

- Provider/model/adapter mutation, user-global configuration, account
  entitlement, credentials, live network state, or remote provider settings.

## Definitions / Facts

- Stage 00 owns 14 roles (one supervisor and thirteen workers) and 22
  functions. The renderer emits 14 role adapters in each of `.claude`,
  `.codex`, `.gemini`, and `.agents`; function skills intentionally project to
  22 Claude and 22 shared `.agents` directories.
- Current work profiles map supervision to Claude Opus 4.8, Codex GPT-5.6, and
  Gemini 3.5 Flash; complex implementation to Sonnet 5, GPT-5.6, and Gemini 3.5
  Flash; and read-heavy work to Haiku 4.5, GPT-5.6 Terra, and Gemini 3.1
  Flash-Lite. Exact provider controls remain distinct.
- One typed seven-event contract renders seven Claude mappings, six Codex
  native mappings plus explicit unsupported `SessionEnd`, and seven Gemini
  mappings. All tracked bindings are configured-not-executed, so local parity
  does not prove provider runtime acceptance.

## Assessment Method

Provider facts use the fixed-cutoff ledger and the separate typed retrieval at
`2026-07-16T01:17:36+09:00`.
Workspace status uses only tracked files and reproduced sync/eval commands.
Mutable official pages are retrieval-time evidence, not historical cutoff
proof. Graphify was stale/advisory and was not used as authority.

## Audit Criteria

| Criterion ID | External criterion | Workspace evidence | Status | Enforcement depth | Disposition | Canonical owner | Automation impact | Verification | Confidence |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| PIC-01 | Preserve native hierarchical project-instruction discovery. | Root shims delegate to Stage 00; Claude/Codex/Gemini discovery syntax remains provider-specific. | Implemented | 3 | Retain | Stage 00 bootstrap and provider notes | Existing sync/contracts. | Inspect root shims; provider sync check. | High. |
| PIC-02 | Support bounded custom agents/subagents without conflating provider surfaces. | Four distinct role surfaces each contain 14 generated adapters sourced from the same typed catalog. Claude, Codex, and Gemini receive native schemas; `.agents` remains the shared compatibility surface. | Partial | 3 | Retain | Stage 00 subagent protocol | Keep provider schemas distinct and obtain live acceptance evidence separately. | Compare all four role directories, renderer output, and current official ledger. | High for tracked parity; live provider behavior is unobserved. |
| PIC-03 | Emit provider-valid custom-agent schema. | The renderer emits strict Claude Markdown, Codex TOML with required description/instructions, Gemini Markdown, and shared compatibility Markdown for all 14 roles. Schema/drift checks pass for three providers, while live native acceptance remains unproved. | Partial | 3 | Retain | Provider renderer and Stage 00 catalog | Retain synchronized native-schema validators; test live acceptance only in separately approved scope. | Run `sync-provider-surfaces.sh --check`; inspect representative adapters and provider notes. | High for tracked schema and zero drift; native acceptance is unobserved. |
| PIC-04 | Map desired lifecycle behavior to supported native hook types. | The generated parity contract records seven Claude mappings, six Codex native mappings plus unsupported `SessionEnd`, and seven Gemini mappings. Commands are rendered to provider-native settings while one canonical semantic event set is preserved. | Partial | 3 | Retain | Stage 00 hook contract and provider adapters | Preserve explicit N/A mappings and provider-specific event names. | Run provider sync and hook-parity checks; inspect all three hook configs/wrappers. | High for tracked configuration; provider execution is unobserved. |
| PIC-05 | Validate actual interception coverage and blocking semantics. | Repository contracts validate native event sets, matchers, timeouts, commands, blocking capabilities, and the Gemini deny/retry mapping. All bindings remain configured-not-executed, so local configuration does not prove live blocking or interception. | Partial | 3 | Retain | Provider hook validator owner | Retain semantic/event coverage checks; add live/native verification only under separately approved scope. | Run parity/contracts checks and compare tracked configs with current provider notes. | High for tracked semantics; live interception remains unproved. |
| PIC-06 | Respect user/project/managed configuration layers. | Tracked project adapters coexist with user-owned provider config; no audit read or mutation of global config occurred. | Partial | 1 | Retain | Provider configuration owner | Explicit non-automation: global operator state is outside repo authority. | Tracked config inventory. | High for absence; global state unknown by design. |
| PIC-07 | Separate native permission/confirmation from repository authorization. | Stage 00 approval boundaries are explicit; provider modes differ and tracked metadata does not prove enforcement. | Partial | 2 | Improve | Stage 00 approval boundaries | Candidate denied-action evidence for high-risk workflows. | Inspect approval policy and provider settings. | High for policy; runtime modes unknown. |
| PIC-08 | Record actual filesystem sandbox mode rather than infer optional support. | Environment constraints exist, but tracked files cannot prove the executing provider's active sandbox/profile. | Needs Revalidation | 1 | Improve | Executing task/provider owner | Record scoped runtime mode when exposed; do not add a guessed repository default. | Task runtime evidence plus provider configuration, when authorized. | Medium: deliberate evidence gap. |
| PIC-09 | Record network/egress boundary separately from sandbox and approval. | Policy requires approval for networked mutations; tracked provider files and Compose declarations do not prove live egress. | Needs Revalidation | 1 | Retain | Executing environment owner | Non-automation unless a scoped network test is approved. | Authorized runtime observation only. | Medium. |
| PIC-10 | Configure MCP per provider/scope without exposing global credentials. | Providers support MCP, but there is no shared tracked project MCP baseline and installed/global servers are unknown. | Needs Revalidation | 1 | Retain | Provider/user configuration owner | Explicit non-automation: do not inventory user-global credentials/config. | Tracked-file scan for project config; authorized provider inspection only. | High for tracked absence; global state unknown. |
| PIC-11 | Use shell/file/web tools under canonical authority and QA gates. | Canonical scripts and approval rules exist; role metadata does not enforce a uniform native tool allowlist. | Partial | 2 | Improve | Stage 00 task/approval owners | Candidate task-specific tool/denial checks. | Inspect task brief, role adapter, scripts, and task evidence. | High. |
| PIC-12 | Bound headless/noninteractive automation to trigger authority. | Scripts and CI workflows exist; remote writes remain approval-gated and provider batch modes are not adopted as policy. | Partial | 2 | Retain | Workflow/CI owner | Existing workflow validation; no autonomous remote expansion. | Inspect workflows, scripts, and approval rules. | High. |
| PIC-13 | Treat checkpoint/resume as provider state, not repository rollback. | Git/worktree/task evidence define repository recovery; no uniform tracked provider checkpoint/resume contract exists. | Partial | 2 | Improve | Git workflow and Stage 04 task owner | Improve restart evidence before adding provider checkpoint automation. | Inspect git workflow, task evidence, and provider notes. | High. |
| PIC-14 | Observe execution with redaction-safe evidence. | Diffs, CI/SARIF, commands, and task evidence exist; no unified provider trace backend is tracked and opt-in telemetry state is unknown. | Partial | 2 | Retain | QA/task evidence owner | Explicit non-automation unless actionable telemetry use and privacy controls are approved. | Tracked telemetry/config scan and task evidence review. | High. |
| PIC-15 | Generate provider adapters without equating generation with native compatibility. | The Stage 00-only renderer reports three providers and zero drift across 14 native/shared role adapters per surface, 22 Claude/shared function skills, provider settings/hooks, exact schema checks, and changed/new metadata validation. Generation still does not prove native runtime acceptance. | Partial | 3 | Retain | Provider renderer/validator owner | Retain sync, semantic parity, hook parity, and CI definition checks without equating them with native compatibility. | Provider sync/parity freshness, workflow checks, and T-AGHC Task 3-4 review evidence. | High for tracked definitions; native/live acceptance remains unobserved. |
| PIC-16 | Select exact models/reasoning while separating policy from availability. | Exact supervision, complex, and read-heavy profiles plus provider-native controls, fallbacks, renderer literals, and validators are coupled. GPT-5.6 cutoff qualification, entitlement, and provider runtime acceptance remain unverified. | Partial | 3 | Retain | `subagent-protocol.md` and provider-model contract | Preserve atomic change/rollback protocol and keep runtime availability a separate evidence state. | Model-contract check, adapter literals, provider sync, and repo contracts. | High for tracked values; provider acceptance remains unobserved. |
| PIC-17 | Integrate provider execution with repository evaluation evidence. | Deterministic QA, independent review, eight exact fixtures, ten synthetic regressions, calibrated thresholds, and value-free bounded scoring are routed through local/CI harness gates. They do not call or benchmark live provider models. | Partial | 4 | Retain | QA/eval owner | Retain the synthetic semantic gate; design live provider comparison separately if approved. | Eval `8/8` and regression `10/10` markers plus task review ledger. | High for repository semantics; live model quality is unverified. |

## Findings

- Gemini native agents, settings, and hook wrappers are generated and
  validator-backed. Live Gemini acceptance and interception remain unobserved,
  so provider parity remains partial rather than absent.
- Structural sync is depth 3, but it cannot validate native schema acceptance,
  complete hook interception, or account/model availability.
- `PIC-08`, `PIC-09`, and `PIC-10` remain `Needs Revalidation` because the
  required facts are live/user-global, not because provider documentation is
  absent.

## Gap / Follow-up

| Gap | Action | Boundary |
| --- | --- | --- |
| Provider-native schema and hook acceptance | Fix | Tracked provider/governance/generator/validator parity is current; verify live native acceptance only through separate approved scope. |
| Gemini CLI native runtime acceptance | Improve | Keep `.gemini` native adapters and `.agents` compatibility semantics distinct; validate live acceptance only in separate approved scope. |
| Provider model runtime evidence | Improve | Preserve the typed profiles and fallbacks; verify entitlement and runtime acceptance only in separate approved scope. |
| Live sandbox/network/MCP facts | Retain unknown state | Observe only within an authorized executing task; never persist secrets. |

## Automation Impact

Retain provider no-drift, semantic lifecycle parity, hook-parity generation,
and existing CI definition checks. Treat live native-schema/event acceptance as
separate evidence. Do not automate user-global configuration or credential
discovery.

## Source Rules

- Provider facts, workspace adoption, and repository policy are separate columns
  conceptually even when summarized in one row.
- The fixed model cutoff is 2026-07-10 10:00 KST. Retrieval-time provider
  documentation must not be backdated into that catalog.
- No mutable source establishes unobserved account entitlement or runtime mode.

## Sources

- [Provider comparison research and official evidence ledger](../../research/2026-07-05-agentic-research-pack-refresh/provider-implementation-comparison.md)
- [Provider model landscape](../../research/2026-07-05-agentic-research-pack-refresh/provider-model-landscape.md)
- [Subagent protocol](../../../00.agent-governance/subagent-protocol.md)
- [Provider capability matrix](../../../00.agent-governance/rules/provider-capability-matrix.md)
- [Claude notes](../../../00.agent-governance/providers/claude.md)
- [Codex notes](../../../00.agent-governance/providers/codex.md)
- [Gemini notes](../../../00.agent-governance/providers/gemini.md)

## Maintenance

- **Owner**: Agentic Workflow Specialist.
- **Review Cadence**: Monthly during provider release velocity, otherwise quarterly.
- **Update Trigger**: Provider schema/event/default, tracked adapter, or model-policy changes.

## Related Documents

- [Audit pack README](./README.md)
- [Harness audit](./harness-engineering-implementation.md)
- [Loop audit](./loop-engineering-implementation.md)
- [Agent instruction/catalog/model audit](./agent-instructions-catalog-vibe-models.md)
