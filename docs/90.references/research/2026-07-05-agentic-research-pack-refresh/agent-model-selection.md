---
status: active
artifact_id: reference:agentic-research:agent-model-selection
artifact_type: reference
parent_ids: [spec:123-agentic-engineering-audit-remediation]
reviewed_at: 2026-07-16
review_cycle: on-source-change
---

<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/agent-model-selection.md -->

# Reference: Task-Characteristic AI Agent Model Selection

## Overview

This reference explains how an agent's model and reasoning effort are chosen to
match a task's characteristics in `hy-home.docker`. It connects the repo-local
Model Policy in `subagent-protocol.md` to the general engineering practice of
right-sizing a model to task complexity, latency tolerance, and cost, and to the
per-provider mechanics that express that choice. The provider landscape's 145
retrieval-time structural rows and 142 exact-cutoff-qualified rows, with their
lifecycle and exact-ID existence evidence, are maintained in
[`provider-model-landscape.md`](./provider-model-landscape.md) at the fixed
**2026-07-10 10:00 KST (01:00 UTC)** cutoff.

## Purpose

The research packs name the Supervisor and Worker model tiers but do not explain
how to select a model for a given task. This reference closes that gap: it makes
the two selection axes explicit (which tier/model, and how much reasoning effort)
and shows how each provider adapter encodes them, so that agent authors and
reviewers can reason about model configuration without re-deriving it.

## Repository Role

This reference supports `subagent-protocol.md`, `rules/provider-capability-matrix.md`,
and the provider adapter surfaces (`.claude/agents/`, `.codex/agents/`,
`.gemini/agents/`, `.agents/`). It is advisory background only. It does not set model policy, change
any agent's model or reasoning effort, or authorize a provider adapter change;
the Model Policy table and the change protocol in `subagent-protocol.md` remain
the single source of truth.

## Scope

### In Scope

- The two model-selection axes: tier/model choice and reasoning effort.
- The mapping from task characteristics to Supervisor or Worker tier.
- Per-provider mechanics for expressing tier and effort (Claude, Codex, Gemini).
- How the choice is enforced and what a change to it requires.
- The external right-sizing practice that motivates the policy.
- Cutoff-bound catalog gaps that affect the literal configured values.

### Out of Scope

- Changing any model value, reasoning effort, or provider adapter.
- The Model Policy table itself (owned by `subagent-protocol.md`).
- Active policy, runbooks, incident timelines, or runtime configuration truth.
- Replacing the complete provider inventory in `provider-model-landscape.md`.
- Proving account, region, or product-surface entitlement.

## Definitions / Facts

- **Two selection axes**: Model configuration has two independent levers. The
  first is **tier/model** (which model runs the agent). The second is
  **reasoning effort** (how much deliberation the same model spends on a task).
  Tuning effort is often a better lever than switching models, because it trades
  intelligence for latency and cost within one model.
- **Work profiles** (`subagent-protocol.md`): The repo defines supervision,
  complex-implementation, and read-heavy-repetitive profiles. Profiles bind an
  exact provider model and native effort/thinking control to task
  characteristics; they do not imply cross-provider capability equivalence.
- **Single-Supervisor rule**: `workflow-supervisor` is the only Supervisor-tier
  role; every other catalog agent is Worker tier. This makes tier selection a
  property of the role, not a per-invocation decision.
- **Current profile mapping**: Supervision resolves to Claude
  `claude-opus-4-8`, Codex `gpt-5.6`, and Gemini `gemini-3.5-flash`.
  Complex implementation resolves to `claude-sonnet-5`, `gpt-5.6`, and
  `gemini-3.5-flash`. Read-heavy/repetitive work resolves to
  `claude-haiku-4-5-20251001`, `gpt-5.6-terra`, and
  `gemini-3.1-flash-lite`.
- **Claude mechanics**: `.claude/agents/*.md` carry exact model IDs and only
  the supported per-model effort surface. Opus 4.8 and Sonnet 5 use adaptive
  thinking with configured effort; Haiku 4.5 uses extended thinking and omits
  the unsupported effort key. Claude controls are not normalized to Codex or
  Gemini values.
- **Codex mechanics**: `.codex/agents/*.toml` carry the exact model identifier
  plus `model_reasoning_effort`. Supervision uses `xhigh`, complex work uses
  `high`, and read-heavy work uses `low`. GPT-5.6 is provider-listed without a
  provider maturity label, so the workspace records it as
  `unclassified-listed`, not `stable`.
- **Gemini mechanics**: `.gemini/agents/*.md` use `gemini-3.5-flash` with
  `high` for supervision/complex work and `gemini-3.1-flash-lite` with
  `minimal` for read-heavy work. `.agents` remains the shared compatibility
  projection and is not treated as Gemini native configuration.
- **Enforcement**: The typed provider-model contract, deterministic renderer,
  provider sync, strict native-schema checks, and repository contracts enforce
  model/profile/control/fallback coupling across all four adapter surfaces.
  This validation does not prove provider availability or entitlement.
- **Catalog/cutoff boundary**: The linked landscape has 145 structural rows from
  the 2026-07-10 retrieval, but only 142 have evidence proving release or
  existence before 01:00 UTC. GPT-5.6 Sol, Terra, and Luna remain retrieval-time
  context because their official changelog entry says only `Jul 9`, without a
  time or timezone. Eight other OpenAI rows are cutoff-qualified by dated
  first-party exact-ID evidence added in the final remediation: one OpenAI-owned
  SDK support commit and four OpenAI release announcements. Their mutable
  listing/lifecycle state remains separately `historical state unverified`.
- **Cutoff versus retrieval**: The historical cutoff remains immutable at
  2026-07-10 10:00 KST. The typed current-state registry was retrieved at
  `2026-07-16T01:17:36+09:00`; it cannot backdate GPT-5.6's unzoned `Jul 9`
  changelog entry. GPT-5.6 Sol/Terra/Luna therefore remain cutoff-unverified
  even though current official pages list them. Gemini 3.5 Flash and 3.1
  Flash-Lite are Stable; the exact Pro preview ID remains
  `gemini-3.1-pro-preview` and is non-default.

## Exact Model-Approval Evidence Contract

These criteria are advisory inputs to any later exact-value approval gate.
Provider facts establish what a surface documents, workspace policy establishes
what is currently configured, and task-fit inference remains an eval hypothesis.
Passing this table does not itself authorize a model or adapter change.

| Criterion | Provider fact required | Workspace policy evidence | Task-fit / evaluation evidence | Reject or hold when |
| --- | --- | --- | --- | --- |
| AMS-01 — Exact identifier | Direct official model page, dated release/existence evidence, and provider-native lifecycle label for the exact ID or documented alias | Current Stage 00 literal, adapter target, generator mapping, and validator expectation | N/A; identity is not a quality inference | Only a family nickname, moving alias, secondary source, or `historical state unverified` existence is available. |
| AMS-02 — Product surface | Official evidence for the exact API, CLI, IDE, agent, region/account, or partner surface being proposed | The concrete provider adapter and invocation surface are named | Representative execution on the same surface when public docs cannot prove entitlement | Catalog presence is being used to infer Codex/Claude Code/Antigravity/account availability. |
| AMS-03 — Lifecycle and cutoff | Provider-native maturity/deprecation state plus a cutoff-safe timestamp when the decision is historical | Proposed baseline date and rollback model remain explicit | Migration/churn risk is part of the rubric for Preview, deprecated, scheduled-shutdown, or mutable aliases | A later announcement would need to be backdated, or lifecycle state is mutable and material to approval. |
| AMS-04 — Capability and tools | Official context, modality, reasoning-control, tool, coding, and agent support for the exact model/surface | Required role, tools, sandbox, approvals, and reasoning policy are enumerated | Fixtures exercise every capability the task actually depends on | Capability is inferred from family branding, another endpoint, or another provider surface. |
| AMS-05 — Reasoning control | Official supported effort/thinking values and defaults for the proposed model/surface | Exact Supervisor/Worker effort and approved override path are named | Same task set is compared at the proposed effort, including latency/token observations where allowed | Effort values are copied across providers or unsupported values are accepted by schema but ignored at runtime. |
| AMS-06 — Task fit | Provider descriptions are cited only as hypotheses, not benchmarks | Role taxonomy and task class identify why the current tier is insufficient or should remain | Versioned representative tasks, baseline, scorer/rubric, failure cases, privacy boundary, and reviewer calibration | Selection rests on provider prose, anecdote, or unmeasured “newer is better” reasoning. |
| AMS-07 — Coupled change and rollback | Current provider deprecation/migration guidance is recorded | Stage 00, generator, generated adapters, validators, Stage 04 evidence, and provider sync are one atomic proposal | Regression threshold, rollback literal, and post-change verification are defined before mutation | Any coupled surface, rollback path, or independent review is absent. |

The fixed cutoff ledger currently holds GPT-5.6 Sol/Terra/Luna at AMS-01 because
their unzoned `Jul 9` changelog entry does not prove release before 01:00 UTC.
The current typed policy may select those exact listed IDs while retaining
`historical-state-unverified`, `needs_revalidation` entitlement, and
`needs_revalidation` runtime acceptance. The exact Gemini Pro preview ID remains
catalog-only. Those boundaries are evidence states, not authorization to infer
live availability.

## Task-Characteristic to Configuration Mapping

This table is **analysis inferred from official capability descriptions plus
the workspace task taxonomy**. It does not rank providers or guarantee a
workspace result. The complete inference matrix, including specialized models,
lives in `provider-model-landscape.md`.

| Task characteristic | Required capabilities | Claude option | OpenAI/Codex option | Gemini option | Latency/cost consideration | Evidence basis | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Routing, arbitration, final synthesis | Long-horizon reasoning, synthesis, tools | `claude-opus-4-8`, `high` | `gpt-5.6`, `xhigh` | `gemini-3.5-flash`, `high` | Capability is prioritized; no cross-provider cost rank | Stage 00 typed supervision profile plus official descriptions | High for policy; Medium for equivalence |
| Planning, architecture, complex refactoring | Reasoning, coding, context, verification | `claude-opus-4-8`, `high` | `gpt-5.6`, `xhigh` | `gemini-3.5-flash`, `high` | Capability is prioritized; no price claim | Stage 00 supervision profile plus cutoff/current boundary | High for policy; Medium for live availability |
| Scoped implementation within one domain | Coding, tools, bounded execution | `claude-sonnet-5`, `high` | `gpt-5.6`, `high` | `gemini-3.5-flash`, `high` | Exact controls are provider-native; no numeric comparison | Stage 00 complex-implementation profile plus model pages | High for tracked policy |
| Doc organizing, summarization, review | Instruction following, context, structured output | `claude-haiku-4-5-20251001` | `gpt-5.6-terra`, `low` | `gemini-3.1-flash-lite`, `minimal` | No provider cost rank; evaluate representative docs | Stage 00 read-heavy profile | High for tracked policy |
| Repetitive formatting-only editing | Low-latency bounded edits | `claude-haiku-4-5-20251001` | `gpt-5.6-terra`, `low` | `gemini-3.1-flash-lite`, `minimal` | Right-sized profile is the approved workspace lever | Stage 00 read-heavy profile | High for tracked policy |

## Analysis

The repo policy is a disciplined instance of the general right-sizing practice.
External guidance frames model choice as a balance of capabilities, speed, and
cost, and treats effort as a lever that is often preferable to switching models:
start from a capable model for complex reasoning and lower effort or downgrade as
the workflow is optimized, or start from a fast, cheap model for high-volume,
straightforward tasks and upgrade only for specific capability gaps. Sub-agent
tasks are explicitly called out as a good fit for the fast, economical tier.

The workspace resolves the first axis structurally through one supervisor and
thirteen workers, each assigned one of three typed work profiles. The second
axis remains provider-native: Claude effort/thinking, Codex reasoning effort,
and Gemini thinking level are independently validated rather than presented as
equivalent. This removes per-invocation model shopping while retaining an
explicit, reviewed profile-change path.

## Application Notes for This Workspace

- Read the work profile as a property of the role. If a task needs supervisor judgment,
  route it to `workflow-supervisor` rather than raising a worker's model.
- Use only the provider-native control allowed by the typed profile. A harder
  task is rerouted or changed through the coupled policy protocol, not silently
  given an unsupported or cross-provider effort value.
- Treat any change to a model value, reasoning effort default, or provider
  mapping as a Model Policy change. The exact approved-change surfaces are the
  Stage 00 Model Policy, provider adapter generator, generated adapters,
  validators, Stage 04 evidence, and provider sync. All must be updated together
  under the change protocol.
- Keep provider model identifiers native to each surface; never copy one
  provider's model name onto another provider's adapter.
- Record any model-selection decision as active-stage work, not inside this
  reference.
- Treat newer catalog entries as candidates for evaluation, not automatic
  replacements for the current Supervisor or Worker values.

## Potential Follow-up / Gap

- GPT-5.6 is current and provider-listed but its unzoned release entry remains
  cutoff-unverified and OpenAI does not label the listing Stable/GA.
- Account/product availability for the configured Claude, OpenAI/Codex, and Gemini values
  is not proven by repository validators or public model catalogs.
- There is no workspace cross-provider eval establishing task-quality, latency,
  or cost equivalence for the provider mapping.

## Source Rules

- Prefer the repo-local Model Policy in `subagent-protocol.md` for all tier,
  model, and effort facts; it is the single source of truth.
- Use `provider-model-landscape.md` for the full structural catalog,
  cutoff-qualified subset, and lifecycle evidence, not a partial list copied
  into this analysis.
- Treat external model-selection guidance as background practice, not as
  authority over repo values.
- Re-check external model names, effort levels, and defaults before using them
  for current decisions.

## Sources

- [Subagent protocol](../../../00.agent-governance/subagent-protocol.md) - repo-local Model Policy, tier mapping, reasoning-effort policy, and change protocol
- [Provider capability matrix](../../../00.agent-governance/rules/provider-capability-matrix.md) - vendor feature and boundary SSOT relevant to model configuration
- [Repository contract check](../../../../scripts/validation/check-repo-contracts.sh) - enforces name/model/scope parity across provider adapters
- [Provider model landscape](./provider-model-landscape.md) - 145-row structural catalog, 142-row exact-cutoff-qualified subset, dated exact-ID remediation evidence, lifecycle normalization, official sources, and task-fit inference
- [Choosing a Claude model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model) - provider capability/speed/effort guidance
- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents) - subagent model field and alias resolution
- [Codex configuration reference](https://developers.openai.com/codex/config-reference) - `model_reasoning_effort` values and default
- [Gemini models](https://ai.google.dev/gemini-api/docs/models) - official IDs, Stable/Preview/Experimental terms, and capability cards

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when the Stage 00 Model Policy, subagent protocol, or
  provider adapter model surfaces change materially
- **Update Trigger**: Update when model tiers, reasoning-effort policy, provider
  model identifiers, the cutoff catalog, or the model-change protocol change

## Related Documents

- [research pack index](./README.md)
- [provider model landscape](./provider-model-landscape.md)
- [provider implementation comparison](./provider-implementation-comparison.md)
- [ai agent catalogs](./ai-agent-catalogs.md)
- [harness engineering](./harness-engineering.md)
- [subagent protocol](../../../00.agent-governance/subagent-protocol.md)
