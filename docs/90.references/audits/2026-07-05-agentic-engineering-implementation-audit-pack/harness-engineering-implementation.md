---
status: active
artifact_id: audit:agentic-engineering-implementation:harness-engineering
artifact_type: audit
parent_ids: [audit:agentic-engineering-implementation:overview]
reviewed_at: 2026-07-12
review_cycle: per-remediation-task
---

<!-- Target: docs/90.references/audits/2026-07-05-agentic-engineering-implementation-audit-pack/harness-engineering-implementation.md -->

# Reference: Harness Engineering Implementation

## Overview

This reference assesses every `HAR-*` criterion in the canonical harness
research against tracked workspace evidence at baseline `507cd505` on
2026-07-11. It is advisory Stage 90 evidence, not active harness policy.

## Purpose

Distinguish a provider feature from repository adoption, and distinguish both
from Stage 00 policy or an inference about live runtime behavior.

## Repository Role

This report feeds approved Stage 03/04 follow-up. Stage 00, provider adapters,
scripts, CI, and runtime configuration remain authoritative for behavior.

## Scope

### In Scope

- Instruction discovery, subagents, tools/MCP, lifecycle interception,
  isolation/approval, model routing, and evaluation/evidence.
- Tracked `.claude`, `.codex`, and `.agents` surfaces and canonical validators.

### Out of Scope

- Provider, model-policy, hook, CI, script, runtime, secret, or remote changes.
- Claims about user-global configuration, account entitlement, or live egress.

## Definitions / Facts

- States use `Implemented`, `Partial`, `Missing`, `Not Applicable`, and
  `Needs Revalidation` exactly.
- Enforcement depth is `0` absent, `1` documented, `2` partially applied,
  `3` automated/enforced, and `4` measured with a closed feedback loop.
- The tracked tree contains 14 canonical roles (one supervisor and thirteen
  workers), 22 functions, and 14 generated role adapters on each of the
  Claude, Codex, Gemini, and shared compatibility surfaces. Function skills
  intentionally project to 22 Claude and 22 shared `.agents` directories;
  Gemini consumes the canonical functions through generated agents rather than
  a duplicate `.gemini/skills` tree. `sync-provider-surfaces.sh --check`
  reports three providers and zero drift; this does not prove native runtime
  acceptance or account entitlement.

## Assessment Method

The audit read the canonical `HAR-01` through `HAR-07` research rows, Stage 00
governance, provider notes, all tracked role/model literals, hook definitions,
the sync generator, and the agent-output fixture runner. Graphify was built
from older commit `30df271a` and was used only for navigation; every finding
below is corroborated by tracked source.

## Audit Criteria

| Criterion ID | External criterion | Workspace evidence | Status | Enforcement depth | Disposition | Canonical owner | Automation impact | Verification | Confidence |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- | --- |
| HAR-01 | Discover hierarchical provider instructions with explicit precedence. | Thin `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` shims route to `docs/00.agent-governance/rules/bootstrap.md`; provider sync validates projections. | Implemented | 3 | Retain | Stage 00 bootstrap and provider notes | Existing sync/contracts; add no parallel instruction layer. | `bash scripts/operations/sync-provider-surfaces.sh --check`; inspect root shims. | High: direct tracked evidence; loading still does not prove compliance. |
| HAR-02 | Use native isolated subagents with bounded schema, tools, model, and handoff. | Stage 00 defines one supervisor and thirteen workers; the renderer emits 14 strict native role adapters for Claude, Codex, and Gemini plus 14 shared compatibility adapters. Schema and drift checks pass, while live provider acceptance remains unproved. | Partial | 3 | Retain | Stage 00 subagent protocol plus provider adapters | Retain synchronized lifecycle/schema projections and provider semantic checks; require separate native acceptance evidence. | Compare `subagent-protocol.md` with all four role directories, run provider sync `--check`, and inspect current PIC evidence. | High for tracked parity; live provider acceptance is unobserved. |
| HAR-03 | Bound tools/MCP by native controls and repository authority. | Approval/environment rules and canonical scripts bound actions, but tracked role metadata is not a tool/path allowlist and no shared tracked project MCP baseline exists. | Partial | 2 | Improve | Stage 00 approval boundaries and provider configuration owners | Candidate denied-action/tool-boundary tests; do not inspect or overwrite user-global config. | Inspect `approval-boundaries.md`, role adapters, and tracked provider config paths. | High for policy; runtime MCP/permissions are unknown. |
| HAR-04 | Intercept lifecycle events without inventing cross-provider event parity. | One typed seven-event contract renders seven Claude and seven Gemini native mappings plus six Codex native mappings; Codex `SessionEnd` is explicitly unsupported. Repository checks validate the tracked commands and semantics, but live interception evidence is absent. | Partial | 3 | Retain | Stage 00 hook contract and provider adapters | Retain generated hook-parity semantics and the explicit unsupported-event boundary; do not infer live interception. | Run provider sync and hook-parity checks; inspect `.claude/settings.json`, `.codex/hooks.json`, `.gemini/settings.json`, and provider notes. | High for tracked configuration; live provider interception is unobserved. |
| HAR-05 | Separate sandbox isolation, approval, network, and repository authority. | Stage 00 documents protected actions and environment constraints; provider settings expose different controls. Tracked files cannot prove the executing sandbox profile, unattended mode, egress, or user-global settings. | Partial | 2 | Improve | Stage 00 environment and approval rules | Record actual execution mode in task evidence where available; do not infer global state. | Inspect `environment-constraints.md`, `approval-boundaries.md`, and task evidence. | Medium-high: policy is direct; runtime mode is intentionally unobserved. |
| HAR-06 | Select exact models and provider-native reasoning controls with coupled validation. | The typed policy maps complex implementation to Claude Sonnet 5, Codex GPT-5.6, and Gemini 3.5 Flash; supervision to Opus 4.8, GPT-5.6, and Gemini 3.5 Flash; and read-heavy work to Haiku 4.5, GPT-5.6 Terra, and Gemini 3.1 Flash-Lite. Exact provider-native effort/thinking values, fallbacks, source records, renderer output, and repository validators are coupled. Availability and entitlement remain separately unverified rather than weakening the tracked contract. | Implemented | 3 | Retain | `subagent-protocol.md` and provider-model contract | Preserve atomic contract/renderer/adapter/validator/evidence updates and approved rollback edges. | Run model-contract, provider-sync, and repository-contract checks; inspect exact adapter literals. | High for tracked policy and controls; runtime availability is explicitly out of scope. |
| HAR-07 | Connect deterministic validation, task evidence, and semantic evaluation. | The harness validator, CI/local routing, Stage 04 evidence, eight versioned fixtures, ten synthetic regressions, exact thresholds, and value-free bounded evaluator form a deterministic corrective loop. The suite makes no live model-quality claim. | Implemented | 4 | Retain | QA scope and Stage 04 task owner | Retain the calibrated synthetic eval and independent review loop; add live/model comparative evaluation only under a separate approved contract. | `bash scripts/validation/run-agent-output-eval-fixtures.sh --check-fixtures --check-regressions`; `bash scripts/validation/validate-harness.sh`. | High: exact markers require fixtures `8/8` and regressions `10/10`. |

## Findings

- Structural projection, deterministic validation, and the calibrated synthetic
  evaluator now close a measured depth-4 repository loop. Native compatibility,
  live permission evidence, entitlement, and comparative model quality remain
  separate unverified surfaces.
- Provider facts in the research pack do not change Stage 00 policy. In
  particular, native Gemini CLI agents/hooks do not make `.agents` a native
  `.gemini` implementation.

## Gap / Follow-up

| Gap | Owner | Follow-up boundary |
| --- | --- | --- |
| Native agent-schema acceptance and tracked/live hook-event compatibility | Separate provider/runtime verification | Current Stage 00, generator, adapter, validator, and parity evidence is synchronized; retain Partial until native/live acceptance is observed. |
| Gemini CLI native adoption versus Antigravity pointer behavior | Future approved provider task | Decide explicitly; do not relabel pointers as native adoption. |
| Live or comparative model-quality scoring | QA/eval follow-up | The deterministic synthetic scorer is implemented; define a separate versioned dataset, privacy boundary, and provider-runtime contract before any live comparison. |
| Runtime sandbox, entitlement, MCP, and egress facts | Executing task/provider owner | Record scoped observations only; leave unobserved global state unknown. |

## Automation Impact

Retain structural sync, exact fixture/regression scoring, and typed harness
routing. Improve native-schema/event acceptance and live comparative scoring
only through approved active-stage work; no audit-only runtime automation is
introduced here.

## Source Rules

- Provider features come from the current primary-source ledger in the
  canonical research pack; mutable pages prove retrieval-time facts only.
- Workspace adoption comes from tracked files and command results.
- Stage 00 policy is neither inferred from provider features nor changed by
  this audit.

## Sources

- [Harness research](../../research/2026-07-05-agentic-research-pack-refresh/harness-engineering.md)
- [Provider comparison research](../../research/2026-07-05-agentic-research-pack-refresh/provider-implementation-comparison.md)
- [Harness implementation map](../../../00.agent-governance/harness-implementation-map.md)
- [Subagent protocol](../../../00.agent-governance/subagent-protocol.md)
- [Approval boundaries](../../../00.agent-governance/rules/approval-boundaries.md)

## Maintenance

- **Owner**: Agentic Workflow Specialist.
- **Review Cadence**: After Stage 00, provider adapter, hook, model, or eval changes.
- **Update Trigger**: Any `HAR-*` criterion evidence or enforcement depth changes.

## Related Documents

- [Audit pack README](./README.md)
- [Loop implementation audit](./loop-engineering-implementation.md)
- [Provider implementation audit](./provider-harness-loop-implementation.md)
- [Agent instruction/catalog/model audit](./agent-instructions-catalog-vibe-models.md)
