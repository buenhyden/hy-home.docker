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
per-provider mechanics that express that choice.

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

### Out of Scope

- Changing any model value, reasoning effort, or provider adapter.
- The Model Policy table itself (owned by `subagent-protocol.md`).
- Active policy, runbooks, incident timelines, or runtime configuration truth.
- Proving provider model availability on any date.

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
  defaults to `high` on `opus-4.8`; `xhigh` is the recommended level for coding
  and high-autonomy agentic work.
- **Codex mechanics**: `.codex/agents/*.toml` carry the literal model identifier
  plus a required `model_reasoning_effort`. `workflow-supervisor` uses `xhigh`;
  default workers use `medium`; an approved task may raise a worker to `high`;
  repetitive formatting-only work may drop to `low` through a task-specific
  override. Codex accepts `minimal`, `low`, `medium`, `high`, and `xhigh`, with a
  default of `medium`.
- **Gemini mechanics**: The Antigravity IDE manages reasoning effort strictly
  through model selection. `gemini-3.1-pro` is mandated for high-effort work
  (planning, complex refactors); `gemini-3.5-flash` handles standard or low-effort
  work (repetitive edits, text classification).
- **Enforcement**: The name/model/scope mapping is machine-checked by
  `scripts/validation/check-repo-contracts.sh`; provider adapters must keep
  parity with the Stage 00 catalog.

## Task-Characteristic to Configuration Mapping

| Task characteristic                         | Tier       | Claude       | Codex effort                  | Gemini             |
| ------------------------------------------- | ---------- | ------------ | ----------------------------- | ------------------ |
| Routing, arbitration, final synthesis       | Supervisor | `opus-4.8`   | `xhigh`                       | `gemini-3.1-pro`   |
| Planning, architecture, complex refactoring | Supervisor | `opus-4.8`   | `xhigh`                       | `gemini-3.1-pro`   |
| Scoped implementation within one domain     | Worker     | `sonnet-4.6` | `medium` (`high` if approved) | `gemini-3.5-flash` |
| Doc organizing, summarization, review       | Worker     | `sonnet-4.6` | `medium`                      | `gemini-3.5-flash` |
| Repetitive, formatting-only editing         | Worker     | `sonnet-4.6` | `low` (task override)         | `gemini-3.5-flash` |

The tier column is fixed by the role (only `workflow-supervisor` is Supervisor),
so in practice task characteristics drive the effort column: the same Worker
model spends more or less reasoning effort depending on how demanding the scoped
task is.

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
set of tasks whose accuracy outweighs cost, and it removes per-invocation
model-shopping from worker agents. The second axis, reasoning effort, is where
task characteristics still vary the configuration at run time, most visibly in
the Codex adapter's `model_reasoning_effort` and in Gemini's model-as-effort
selection.

## Application Notes for This Workspace

- Read tier as a property of the role. If a task needs Supervisor-tier judgment,
  route it to `workflow-supervisor` rather than raising a worker's model.
- Vary effort, not model, for a worker whose task is unusually hard: request an
  approved `high` Codex effort for that task instead of promoting the tier.
- Treat any change to a model value, reasoning effort default, or provider
  mapping as a Model Policy change: it is valid only when the policy table,
  adapter generation, generated adapters, validators, and Stage 04 task evidence
  are updated together, per the change protocol.
- Keep provider model identifiers native to each surface; never copy one
  provider's model name onto another provider's adapter.
- Record any model-selection decision as active-stage work, not inside this
  reference.

## Potential Follow-up / Gap

- A future note could document a lightweight decision aid for choosing an
  approved Codex `high` effort override, so worker effort escalation stays
  evidence-backed rather than ad hoc.
- Provider model baselines change; the concrete identifiers and effort defaults
  cited here must be rechecked against `subagent-protocol.md` before reuse.

## Source Rules

- Prefer the repo-local Model Policy in `subagent-protocol.md` for all tier,
  model, and effort facts; it is the single source of truth.
- Treat external model-selection guidance as background practice, not as
  authority over repo values.
- Re-check external model names, effort levels, and defaults before using them
  for current decisions.

## Sources

- [Subagent protocol](../../../00.agent-governance/subagent-protocol.md) - repo-local Model Policy, tier mapping, reasoning-effort policy, and change protocol
- [Provider capability matrix](../../../00.agent-governance/rules/provider-capability-matrix.md) - vendor feature and boundary SSOT relevant to model configuration
- [Repository contract check](../../../../scripts/validation/check-repo-contracts.sh) - enforces name/model/scope parity across provider adapters
- [Choosing the right Claude model](https://platform.claude.com/docs/en/docs/about-claude/models/choosing-a-model) - capabilities/speed/cost/effort selection guidance and the effort lever
- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents) - subagent model field and alias resolution
- [Codex configuration reference](https://developers.openai.com/codex/config-reference) - `model_reasoning_effort` values and default

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review when the Stage 00 Model Policy, subagent protocol, or
  provider adapter model surfaces change materially
- **Update Trigger**: Update when model tiers, reasoning-effort policy, provider
  model identifiers, or the model-change protocol change

## Related Documents

- [research pack index](./README.md)
- [provider implementation comparison](./provider-implementation-comparison.md)
- [ai agent catalogs](./ai-agent-catalogs.md)
- [harness engineering](./harness-engineering.md)
- [subagent protocol](../../../00.agent-governance/subagent-protocol.md)
