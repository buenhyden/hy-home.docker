---
status: active
artifact_id: audit:agentic-engineering-implementation:provider-harness-loop
artifact_type: audit
parent_ids: [audit:agentic-engineering-implementation:overview]
supersedes: [audit:agentic-engineering-implementation-2026-07-07:harness-loop]
reviewed_at: 2026-07-11
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

- Claude, Codex, and `.agents` each expose 15 tracked role names; each provider
  skill surface exposes 22 tracked skill names.
- Claude role aliases are `opus` for the supervisor and `sonnet` for workers,
  mapped by policy to `opus-4.8` and `sonnet-4.6`.
- Codex uses `gpt-5.5` with `xhigh` for the supervisor and `gpt-5.4-mini` with
  `medium` for workers.
- `.agents` uses `gemini-3.1-pro` for the supervisor and
  `gemini-3.5-flash` for workers. The canonical research identifies the
  supervisor literal as unsupported/uncertain; this audit does not change it.
- Official Gemini CLI sources now document native agents and hooks. The
  workspace has no tracked `.gemini/agents`, `.gemini/settings.json`, or
  `.gemini/hooks`; `.agents` remains an Antigravity/reference projection.

## Assessment Method

Provider facts use Task 2's official evidence ledger revalidated on 2026-07-11.
Workspace status uses only tracked files and reproduced sync/eval commands.
Mutable official pages are retrieval-time evidence, not historical cutoff
proof. Graphify was stale/advisory and was not used as authority.

## Audit Criteria

| Criterion ID | External criterion | Workspace evidence | Status | Enforcement depth | Disposition | Canonical owner | Automation impact | Verification | Confidence |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| PIC-01 | Preserve native hierarchical project-instruction discovery. | Root shims delegate to Stage 00; Claude/Codex/Gemini discovery syntax remains provider-specific. | Implemented | 3 | Retain | Stage 00 bootstrap and provider notes | Existing sync/contracts. | Inspect root shims; provider sync check. | High. |
| PIC-02 | Support bounded custom agents/subagents without conflating provider surfaces. | Fifteen names project across Claude, Codex, and `.agents`; Gemini CLI native agents are not locally wired. | Partial | 2 | Improve | Stage 00 subagent protocol | Native compatibility/adoption checks are candidates. | Compare role directories and current official ledger. | High. |
| PIC-03 | Emit provider-valid custom-agent schema. | Provider sync has no drift across all projected roles/skills and preserves the canonical lifecycle contract; Claude definitions are native-rich, Codex TOMLs remain locally validated projections without live native acceptance evidence, and `.agents` remains pointer-based rather than `.gemini` definitions. | Partial | 2 | Fix | Provider generation logic and Stage 00 catalog | Retain synchronized schema semantics and validators; native acceptance and `.gemini` adoption require separate evidence. | Run `sync-provider-surfaces.sh --check`; inspect representative adapters and provider notes. | High for tracked sync; native acceptance is unobserved. |
| PIC-04 | Map desired lifecycle behavior to supported native hook types. | The fresh hook-parity matrix records seven Claude native wrappers, seven Codex native dispatches, and seven Gemini behavioral reminders while preserving one canonical lifecycle contract. No tracked native Gemini hook adapter exists. | Partial | 2 | Fix | Stage 00 hook contract and provider adapters | Retain provider-specific parity generation and the reminder/native-adoption distinction. | Run provider hook parity `--check`; inspect hook configs/scripts and provider notes. | High for tracked configuration. |
| PIC-05 | Validate actual interception coverage and blocking semantics. | Generated parity and repository contracts validate tracked event/config semantics, but local configuration does not prove provider-native acceptance, live blocking, or Gemini interception. | Partial | 2 | Fix | Provider hook validator owner | Retain semantic/event coverage checks; add live/native verification only under separately approved scope. | Run parity/contracts checks and compare tracked configs with current provider notes. | High for tracked semantics; live interception remains unproved. |
| PIC-06 | Respect user/project/managed configuration layers. | Tracked project adapters coexist with user-owned provider config; no audit read or mutation of global config occurred. | Partial | 1 | Retain | Provider configuration owner | Explicit non-automation: global operator state is outside repo authority. | Tracked config inventory. | High for absence; global state unknown by design. |
| PIC-07 | Separate native permission/confirmation from repository authorization. | Stage 00 approval boundaries are explicit; provider modes differ and tracked metadata does not prove enforcement. | Partial | 2 | Improve | Stage 00 approval boundaries | Candidate denied-action evidence for high-risk workflows. | Inspect approval policy and provider settings. | High for policy; runtime modes unknown. |
| PIC-08 | Record actual filesystem sandbox mode rather than infer optional support. | Environment constraints exist, but tracked files cannot prove the executing provider's active sandbox/profile. | Needs Revalidation | 1 | Improve | Executing task/provider owner | Record scoped runtime mode when exposed; do not add a guessed repository default. | Task runtime evidence plus provider configuration, when authorized. | Medium: deliberate evidence gap. |
| PIC-09 | Record network/egress boundary separately from sandbox and approval. | Policy requires approval for networked mutations; tracked provider files and Compose declarations do not prove live egress. | Needs Revalidation | 1 | Retain | Executing environment owner | Non-automation unless a scoped network test is approved. | Authorized runtime observation only. | Medium. |
| PIC-10 | Configure MCP per provider/scope without exposing global credentials. | Providers support MCP, but there is no shared tracked project MCP baseline and installed/global servers are unknown. | Needs Revalidation | 1 | Retain | Provider/user configuration owner | Explicit non-automation: do not inventory user-global credentials/config. | Tracked-file scan for project config; authorized provider inspection only. | High for tracked absence; global state unknown. |
| PIC-11 | Use shell/file/web tools under canonical authority and QA gates. | Canonical scripts and approval rules exist; role metadata does not enforce a uniform native tool allowlist. | Partial | 2 | Improve | Stage 00 task/approval owners | Candidate task-specific tool/denial checks. | Inspect task brief, role adapter, scripts, and task evidence. | High. |
| PIC-12 | Bound headless/noninteractive automation to trigger authority. | Scripts and CI workflows exist; remote writes remain approval-gated and provider batch modes are not adopted as policy. | Partial | 2 | Retain | Workflow/CI owner | Existing workflow validation; no autonomous remote expansion. | Inspect workflows, scripts, and approval rules. | High. |
| PIC-13 | Treat checkpoint/resume as provider state, not repository rollback. | Git/worktree/task evidence define repository recovery; no uniform tracked provider checkpoint/resume contract exists. | Partial | 2 | Improve | Git workflow and Stage 04 task owner | Improve restart evidence before adding provider checkpoint automation. | Inspect git workflow, task evidence, and provider notes. | High. |
| PIC-14 | Observe execution with redaction-safe evidence. | Diffs, CI/SARIF, commands, and task evidence exist; no unified provider trace backend is tracked and opt-in telemetry state is unknown. | Partial | 2 | Retain | QA/task evidence owner | Explicit non-automation unless actionable telemetry use and privacy controls are approved. | Tracked telemetry/config scan and task evidence review. | High. |
| PIC-15 | Generate provider adapters without equating generation with native compatibility. | T-AER-010 completed provider sync and semantic-parity validation: no drift for 15 roles and 22 skills per surface, fresh 7/7/7 hook parity, and changed/new metadata validation in the existing CI job. Native schema/event acceptance and `.gemini` adoption remain unproved. | Partial | 3 | Fix | Provider sync generator/validator owner | Retain sync, semantic parity, hook parity, and CI definition checks without equating them with native compatibility. | Provider sync/parity freshness, workflow checks, and T-AER-010 PASS/APPROVED evidence. | High for tracked definitions; native/live acceptance remains unobserved. |
| PIC-16 | Select exact models/reasoning while separating policy from availability. | All tracked literals match current Stage 00 policy and validators; current provider facts do not prove entitlement, and the Gemini supervisor ID requires approved resolution. | Partial | 3 | Improve | `subagent-protocol.md` model policy | Preserve literals until AMS-01..07 and coupled rollback evidence pass. | Model-literal `rg`, provider sync, repo contracts. | High for tracked values; medium for provider acceptance. |
| PIC-17 | Integrate provider execution with repository evaluation evidence. | Deterministic QA, independent review, and 3/3 fixture freshness exist; no adopted general semantic scorer/baseline/threshold. | Partial | 3 | Improve | QA/eval owner | Retain fixture check; future scored eval requires approved design. | Eval fixture check and task review ledger. | High. |

## Findings

- Current official facts correct the old claim that Gemini CLI lacks native
  subagents/hooks. Local adoption is still absent, so workspace parity remains
  partial rather than implemented.
- Structural sync is depth 3, but it cannot validate native schema acceptance,
  complete hook interception, or account/model availability.
- `PIC-08`, `PIC-09`, and `PIC-10` remain `Needs Revalidation` because the
  required facts are live/user-global, not because provider documentation is
  absent.

## Gap / Follow-up

| Gap | Action | Boundary |
| --- | --- | --- |
| Provider-native schema and hook acceptance | Fix | Tracked provider/governance/generator/validator parity is current; verify live native acceptance only through separate approved scope. |
| Gemini CLI native surface decision | Improve | Separate approved task; do not rewrite `.agents` pointer semantics in this audit. |
| Exact Gemini supervisor model evidence | Improve | Preserve current policy until AMS evidence and exact rollback value are approved. |
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
