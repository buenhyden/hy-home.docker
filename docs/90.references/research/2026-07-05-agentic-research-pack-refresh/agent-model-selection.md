---
status: active
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
lifecycle evidence, are maintained in
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
`.agents/`). It is advisory background only. It does not set model policy, change
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
- **Tier model** (`subagent-protocol.md`): The repo defines two tiers.
  **Supervisor (top spec)** covers routing, final decisions, synthesis,
  planning, architecture, and refactoring. **Worker (right-sized)** covers scoped
  task execution, repetitive editing, doc organizing, and summarization.
- **Single-Supervisor rule**: `workflow-supervisor` is the only Supervisor-tier
  role; every other catalog agent is Worker tier. This makes tier selection a
  property of the role, not a per-invocation decision.
- **Provider-equivalent mapping**: Supervisor resolves to Claude `opus-4.8`,
  Gemini `gemini-3.1-pro`, and GPT/Codex `gpt-5.5`. Worker resolves to Claude
  `sonnet-4.6`, Gemini `gemini-3.5-flash`, and GPT/Codex `gpt-5.4-mini`. The
  Model Policy baseline date is 2026-05-29.
- **Claude mechanics**: `.claude/agents/*.md` carry the Claude Code aliases
  `opus` (Supervisor) and `sonnet` (Worker), which resolve to `opus-4.8` and
  `sonnet-4.6`. Claude expresses reasoning effort with an effort parameter that
  defaults to `high` on `opus-4.8`. Provider-native effort behavior is not
  normalized to the Codex effort policy.
- **Codex mechanics**: `.codex/agents/*.toml` carry the literal model identifier
  plus a required `model_reasoning_effort`. `workflow-supervisor` uses `xhigh`;
  default workers use `medium`; an approved task may raise a worker to `high`;
  repetitive formatting-only work may drop to `low` through a task-specific
  override. These are workspace values; model support remains model-specific.
- **Gemini mechanics**: The Antigravity IDE manages reasoning effort strictly
  through model selection. `gemini-3.1-pro` is mandated for high-effort work
  (planning, complex refactors); `gemini-3.5-flash` handles standard or low-effort
  work (repetitive edits, text classification).
- **Enforcement**: The name/model/scope mapping is machine-checked by
  `scripts/validation/check-repo-contracts.sh`; provider adapters must keep
  parity with the Stage 00 catalog. This validation does not prove provider
  availability.
- **Catalog/cutoff boundary**: The linked landscape has 145 structural rows from
  the 2026-07-10 retrieval, but only 142 have evidence proving release or
  existence before 01:00 UTC. GPT-5.6 Sol, Terra, and Luna remain retrieval-time
  context because their official changelog entry says only `Jul 9`, without a
  time or timezone.
- **Cutoff finding**: At the cutoff, `gemini-3.5-flash` is an official Stable
  model ID. The official Pro ID is `gemini-3.1-pro-preview`; the workspace
  Supervisor value `gemini-3.1-pro` lacks `-preview` and is recorded as an
  unsupported-availability gap, not silently corrected here.

## Task-Characteristic to Configuration Mapping

This table is **analysis inferred from official capability descriptions plus
the workspace task taxonomy**. It does not rank providers or guarantee a
workspace result. The complete inference matrix, including specialized models,
lives in `provider-model-landscape.md`.

| Task characteristic | Required capabilities | Claude option | OpenAI/Codex option | Gemini option | Latency/cost consideration | Evidence basis | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Routing, arbitration, final synthesis | Long-horizon reasoning, synthesis, tools | Policy `opus-4.8` via `opus` | Policy `gpt-5.5`, `xhigh` | Policy `gemini-3.1-pro`; official API ID gap noted | Capability is prioritized; no cross-provider cost rank | Stage 00 policy plus official descriptions | High for policy; Medium for equivalence |
| Planning, architecture, complex refactoring | Reasoning, coding, context, verification | Policy `opus-4.8` via `opus` | Policy `gpt-5.5`, `xhigh` | Policy `gemini-3.1-pro`; official ID is Preview | Capability is prioritized; no price claim | Stage 00 policy plus cutoff catalog | High for policy; Medium for availability |
| Scoped implementation within one domain | Coding, tools, bounded execution | Policy `sonnet-4.6` via `sonnet` | Policy `gpt-5.4-mini`, `medium` (`high` only if approved) | Policy `gemini-3.5-flash` | Mini/Flash official descriptions emphasize efficiency | Stage 00 Worker taxonomy plus model pages | High |
| Doc organizing, summarization, review | Instruction following, context, structured output | Policy `sonnet-4.6` | Policy `gpt-5.4-mini`, `medium` | Policy `gemini-3.5-flash` | No provider cost rank; evaluate representative docs | Stage 00 taxonomy | High |
| Repetitive formatting-only editing | Low-latency bounded edits | Policy `sonnet-4.6` | Policy `gpt-5.4-mini`, task override `low` | Policy `gemini-3.5-flash` | Lower effort is the approved workspace lever | Stage 00 reasoning policy | High |

## Analysis

The repo policy is a disciplined instance of the general right-sizing practice.
External guidance frames model choice as a balance of capabilities, speed, and
cost, and treats effort as a lever that is often preferable to switching models:
start from a capable model for complex reasoning and lower effort or downgrade as
the workflow is optimized, or start from a fast, cheap model for high-volume,
straightforward tasks and upgrade only for specific capability gaps. Sub-agent
tasks are explicitly called out as a good fit for the fast, economical tier.

The workspace resolves the first axis structurally: because only
`workflow-supervisor` is Supervisor tier, top-spec models are reserved for
orchestration, planning, architecture, and refactoring, and all scoped execution
runs on the right-sized Worker tier. This keeps the expensive model on the small
set of tasks where the policy prioritizes capability, and it removes
per-invocation model-shopping from worker agents. The second axis, reasoning
effort, is where
task characteristics still vary the configuration at run time, most visibly in
the Codex adapter's `model_reasoning_effort` and in Gemini's model-as-effort
selection.

## Application Notes for This Workspace

- Read tier as a property of the role. If a task needs Supervisor-tier judgment,
  route it to `workflow-supervisor` rather than raising a worker's model.
- Vary effort, not model, for a worker whose task is unusually hard: request an
  approved `high` Codex effort for that task instead of promoting the tier.
- Treat any change to a model value, reasoning effort default, or provider
  mapping as a Model Policy change. The exact approved-change surfaces are the
  Stage 00 Model Policy, provider adapter generator, generated adapters,
  validators, Stage 04 evidence, and provider sync. All must be updated together
  under the change protocol.
- Keep provider model identifiers native to each surface; never copy one
  provider's model name onto another provider's adapter.
- Record any model-selection decision as active-stage work, not inside this
  reference.
- Treat the `gemini-3.1-pro` literal as a tracked gap until an approved task
  supplies the concrete value, role, provider evidence, and validation path.
- Treat newer catalog entries as candidates for evaluation, not automatic
  replacements for the current Supervisor or Worker values.

## Potential Follow-up / Gap

- The Gemini Supervisor string is unsupported by the official cutoff catalog;
  the official API page exposes `gemini-3.1-pro-preview` instead.
- Account/product availability for the configured Claude and OpenAI/Codex values
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
- [Provider model landscape](./provider-model-landscape.md) - 145-row structural catalog, 142-row exact-cutoff-qualified subset, lifecycle normalization, official sources, and task-fit inference
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
