---
status: superseded
artifact_id: reference:agentic-research:agent-model-selection
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-07
review_cycle: on-source-change
---


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
- **Work profiles** (`subagent-protocol.md`): The repo defines
  `adversarial-review`, `complex-implementation`, `evidence-research`,
  `long-horizon-supervision`, and `routine-validation`. Profiles bind an exact
  provider model and native effort/thinking control to task characteristics;
  they do not imply cross-provider capability equivalence.
- **Single-Supervisor rule**: `workflow-supervisor` is the only Supervisor-tier
  role; every other catalog agent is Worker tier. This makes tier selection a
  property of the role, not a per-invocation decision.
- **Current profile mapping**: `adversarial-review` resolves to
  `claude-opus-5` / `high`, `gpt-5.6-sol` / `xhigh`, and
  `gemini-3.6-flash` / `high`; `complex-implementation` resolves to
  `claude-sonnet-5` / `high`, `gpt-5.6-sol` / `high`, and
  `gemini-3.6-flash` / `high`; `evidence-research` resolves to
  `claude-sonnet-5` / `low`, `gpt-5.6-terra` / `medium`, and
  `gemini-3.5-flash-lite` / `medium`; `long-horizon-supervision` resolves to
  `claude-opus-5` / `xhigh`, `gpt-5.6-sol` / `xhigh`, and
  `gemini-3.6-flash` / `high`; and `routine-validation` resolves to
  `claude-haiku-4-5-20251001` with no effort key, `gpt-5.6-terra` / `low`,
  and `gemini-3.5-flash-lite` / `minimal`.
- **Claude mechanics**: `.claude/agents/*.md` carry exact model IDs and only
  the supported per-model effort surface. Opus 5 and Sonnet 5 use configured
  effort; Haiku 4.5 omits the effort key. That omission is correct against the
  source rather than a rendering shortcut: the official effort page's supported
  model list names `claude-fable-5`, `claude-mythos-5`,
  `claude-mythos-preview`, `claude-opus-5`, `claude-opus-4-8`,
  `claude-opus-4-7`, `claude-opus-4-6`, `claude-sonnet-5`, `claude-sonnet-4-6`,
  and `claude-opus-4-5-20251101`, and does not name
  `claude-haiku-4-5-20251001`. The subagent frontmatter field is `effort` with
  values `low`, `medium`, `high`, `xhigh`, and `max`; it "Overrides the session
  effort level", defaults to inheriting from the session, and its "available
  levels depend on the model". Claude controls are not normalized to Codex or
  Gemini values.
- **Codex mechanics**: `.codex/agents/*.toml` carry the exact model identifier
  plus `model_reasoning_effort`, whose documented values are `low`, `medium`,
  `high`, `xhigh`, `max`, and `ultra`. The workspace uses `high` or `xhigh` for
  Sol and `medium` or `low` for Terra, so it configures four of the six
  available values and never selects `max` or `ultra`. OpenAI documents Sol,
  Terra, and Luna as the current GPT-5.6 family, with `gpt-5.6` documented as
  an alias for Sol, and the workspace records the selected exact IDs as
  `stable`. Public catalog presence still does not prove Codex product
  acceptance, entitlement, or runtime activation.
- **Gemini mechanics**: `.gemini/agents/*.md` select `gemini-3.6-flash` for
  adversarial, complex, and supervision work and `gemini-3.5-flash-lite` for
  evidence and routine work. Both are documented as generally available and
  production-ready. The paired `high`, `medium`, and `minimal` values are
  Gemini API thinking-level values. The Gemini CLI subagent file schema is
  limited to `name`, `description`, `kind`, `tools`, `mcpServers`, `model`,
  `temperature`, `max_turns`, and `timeout_mins`, with no reasoning or thinking
  field, so those values are not per-agent file controls. The contract records
  their real destination as
  `modelConfigs.overrides[].modelConfig.generateContentConfig.thinkingConfig.thinkingLevel`,
  a settings-level or API path rather than an agent-file key. `.agents` remains
  the shared compatibility projection and is not treated as Gemini native
  configuration.
- **Enforcement**: The typed provider-model contract, deterministic renderer,
  provider sync, strict native-schema checks, and repository contracts enforce
  exact model/profile/control coupling across all four adapter surfaces. There
  is no active fallback graph or implicit model substitution. This validation
  does not prove provider availability or entitlement.
- **Catalog/cutoff boundary**: The linked landscape has 145 structural rows from
  the 2026-07-10 retrieval, but only 142 have evidence proving release or
  existence before 01:00 UTC. GPT-5.6 Sol, Terra, and Luna remain retrieval-time
  context because their official changelog entry says only `Jul 9`, without a
  time or timezone. Eight other OpenAI rows are cutoff-qualified by dated
  first-party exact-ID evidence added in the final remediation: one OpenAI-owned
  SDK support commit and four OpenAI release announcements. Their mutable
  listing/lifecycle state remains separately `historical state unverified`.
- **Cutoff versus retrieval**: The historical cutoff remains immutable at
  2026-07-10 10:00 KST, including its 145/142 ledger and three retrieval-only
  GPT-5.6 rows. The current Stage 00 contract facts were retrieved at
  `2026-07-26T20:08:18+09:00`; official external pages were separately
  revalidated at `2026-08-07T12:45:40+09:00`. Those later observations support
  the current five-profile/11-model contract, not a rewrite of the historical
  cutoff ledger.

## Exact Model-Approval Evidence Contract

These criteria are advisory inputs to any later exact-value approval gate.
Provider facts establish what a surface documents, workspace policy establishes
what is currently configured, and task-fit inference remains an eval hypothesis.
Passing this table does not itself authorize a model or adapter change.

| Criterion                            | Provider fact required                                                                                                                 | Workspace policy evidence                                                                                         | Task-fit / evaluation evidence                                                                                     | Reject or hold when                                                                                              |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| AMS-01 — Exact identifier            | Direct official model page, dated release/existence evidence, and provider-native lifecycle label for the exact ID or documented alias | Current Stage 00 literal, adapter target, generator mapping, and validator expectation                            | N/A; identity is not a quality inference                                                                           | Only a family nickname, moving alias, secondary source, or `historical state unverified` existence is available. |
| AMS-02 — Product surface             | Official evidence for the exact API, CLI, IDE, agent, region/account, or partner surface being proposed                                | The concrete provider adapter and invocation surface are named                                                    | Representative execution on the same surface when public docs cannot prove entitlement                             | Catalog presence is being used to infer Codex/Claude Code/Antigravity/account availability.                      |
| AMS-03 — Lifecycle and cutoff        | Provider-native maturity/deprecation state plus a cutoff-safe timestamp when the decision is historical                                | Proposed baseline date and rollback model remain explicit                                                         | Migration/churn risk is part of the rubric for Preview, deprecated, scheduled-shutdown, or mutable aliases         | A later announcement would need to be backdated, or lifecycle state is mutable and material to approval.         |
| AMS-04 — Capability and tools        | Official context, modality, reasoning-control, tool, coding, and agent support for the exact model/surface                             | Required role, tools, sandbox, approvals, and reasoning policy are enumerated                                     | Fixtures exercise every capability the task actually depends on                                                    | Capability is inferred from family branding, another endpoint, or another provider surface.                      |
| AMS-05 — Reasoning control           | Official supported effort/thinking values and defaults for the proposed model/surface                                                  | Exact Supervisor/Worker effort and approved override path are named                                               | Same task set is compared at the proposed effort, including latency/token observations where allowed               | Effort values are copied across providers or unsupported values are accepted by schema but ignored at runtime.   |
| AMS-06 — Task fit                    | Provider descriptions are cited only as hypotheses, not benchmarks                                                                     | Role taxonomy and task class identify why the current tier is insufficient or should remain                       | Versioned representative tasks, baseline, scorer/rubric, failure cases, privacy boundary, and reviewer calibration | Selection rests on provider prose, anecdote, or unmeasured “newer is better” reasoning.                          |
| AMS-07 — Coupled change and rollback | Current provider deprecation/migration guidance is recorded                                                                            | Stage 00, generator, generated adapters, validators, Stage 04 evidence, and provider sync are one atomic proposal | Regression threshold, rollback literal, and post-change verification are defined before mutation                   | Any coupled surface, rollback path, or independent review is absent.                                             |

The fixed historical cutoff ledger holds GPT-5.6 Sol/Terra/Luna at AMS-01 because
their unzoned `Jul 9` changelog entry does not prove release before 01:00 UTC.
The current typed policy separately selects exact stable Sol and Terra IDs
while retaining `needs_revalidation` entitlement and runtime acceptance. Those
axes are independent: a current lifecycle fact cannot backdate a historical
cutoff, and a configured default cannot prove live activation.

## Task-Characteristic to Configuration Mapping

This table is **analysis inferred from official capability descriptions plus
the workspace task taxonomy**. It does not rank providers or guarantee a
workspace result. The complete inference matrix, including specialized models,
lives in `provider-model-landscape.md`.

| Task characteristic                         | Required capabilities                               | Claude option                              | OpenAI/Codex option       | Gemini option                      | Latency/cost consideration                                | Evidence basis                                                   | Confidence                                    |
| ------------------------------------------- | --------------------------------------------------- | ------------------------------------------ | ------------------------- | ---------------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------- | --------------------------------------------- |
| Adversarial correctness and policy review   | Deep inspection, challenge, edge cases              | `claude-opus-5`, `high`                    | `gpt-5.6-sol`, `xhigh`    | `gemini-3.6-flash`, `high`         | Capability is prioritized; no cross-provider cost rank    | Stage 00 `adversarial-review` profile plus official descriptions | High for policy; Medium for equivalence       |
| Planning, architecture, and final synthesis | Long-horizon reasoning, synthesis, tools            | `claude-opus-5`, `xhigh`                   | `gpt-5.6-sol`, `xhigh`    | `gemini-3.6-flash`, `high`         | Capability is prioritized; no price claim                 | Stage 00 `long-horizon-supervision` profile                      | High for policy; Medium for live availability |
| Scoped complex implementation               | Coding, tools, bounded execution                    | `claude-sonnet-5`, `high`                  | `gpt-5.6-sol`, `high`     | `gemini-3.6-flash`, `high`         | Exact controls are provider-native; no numeric comparison | Stage 00 `complex-implementation` profile plus model pages       | High for tracked policy                       |
| Source-grounded research and synthesis      | Instruction following, context, structured evidence | `claude-sonnet-5`, `low`                   | `gpt-5.6-terra`, `medium` | `gemini-3.5-flash-lite`, `medium`  | No provider cost rank; evaluate representative research   | Stage 00 `evidence-research` profile                             | High for tracked policy                       |
| Routine validation and classification       | Low-latency bounded repetition                      | `claude-haiku-4-5-20251001`; no effort key | `gpt-5.6-terra`, `low`    | `gemini-3.5-flash-lite`, `minimal` | Right-sized profile is the approved workspace lever       | Stage 00 `routine-validation` profile                            | High for tracked policy                       |

## Configured Value Versus Provider Default

A configuration that restates a provider default is not the same intervention
as one that moves off it, and the two are indistinguishable in the profile
table above. This comparison was derived on 2026-08-07 from the official
effort and thinking-level documentation for the exact configured models. It
changes no value; it states which of the fifteen provider cells actually
diverge from what the provider would do unconfigured.

| Criterion | Profile                    | Provider | Configured                                 | Documented default                 | Diverges?      |
| --------- | -------------------------- | -------- | ------------------------------------------ | ---------------------------------- | -------------- |
| CVD-01    | `adversarial-review`       | Claude   | `claude-opus-5` / `high`                   | API default `high`                 | No             |
| CVD-02    | `adversarial-review`       | Codex    | `gpt-5.6-sol` / `xhigh`                    | Product default Medium             | Yes            |
| CVD-03    | `adversarial-review`       | Gemini   | `gemini-3.6-flash` / `high`                | Default thinking level `medium`    | Yes            |
| CVD-04    | `complex-implementation`   | Claude   | `claude-sonnet-5` / `high`                 | API and Claude Code default `high` | No             |
| CVD-05    | `complex-implementation`   | Codex    | `gpt-5.6-sol` / `high`                     | Product default Medium             | Yes            |
| CVD-06    | `complex-implementation`   | Gemini   | `gemini-3.6-flash` / `high`                | Default thinking level `medium`    | Yes            |
| CVD-07    | `evidence-research`        | Claude   | `claude-sonnet-5` / `low`                  | Default `high`                     | Yes, downward  |
| CVD-08    | `evidence-research`        | Codex    | `gpt-5.6-terra` / `medium`                 | Product default Medium             | No             |
| CVD-09    | `evidence-research`        | Gemini   | `gemini-3.5-flash-lite` / `medium`         | Default thinking level `minimal`   | Yes, upward    |
| CVD-10    | `long-horizon-supervision` | Claude   | `claude-opus-5` / `xhigh`                  | Default `high`                     | Yes            |
| CVD-11    | `long-horizon-supervision` | Codex    | `gpt-5.6-sol` / `xhigh`                    | Product default Medium             | Yes            |
| CVD-12    | `long-horizon-supervision` | Gemini   | `gemini-3.6-flash` / `high`                | Default thinking level `medium`    | Yes            |
| CVD-13    | `routine-validation`       | Claude   | `claude-haiku-4-5-20251001`, no effort key | Effort unsupported on this model   | Not applicable |
| CVD-14    | `routine-validation`       | Codex    | `gpt-5.6-terra` / `low`                    | Product default Medium             | Yes, downward  |
| CVD-15    | `routine-validation`       | Gemini   | `gemini-3.5-flash-lite` / `minimal`        | Default thinking level `minimal`   | No             |

Four findings follow, and each is a fact about this workspace rather than a
recommendation.

- **Two Claude cells are behavioral no-ops.** Official guidance states that
  "Setting `effort` to `"high"` produces exactly the same behavior as omitting
  the `effort` parameter entirely." CVD-01 and CVD-04 therefore configure the
  default explicitly. That is defensible as pinning against a future default
  change, but it should not be read as the workspace raising effort for
  adversarial review or complex implementation. Only CVD-07 and CVD-10 move
  Claude off its default at all.
- **Claude's real supervisor signal is `xhigh`, not the tier.** CVD-10 is the
  single Claude cell configured above default, and the supervisor and the
  adversarial reviewer share the same model. The distinction between the two
  Supervisor-tier and Worker-tier roles on Claude is carried entirely by that
  one effort step.
- **Codex diverges in four of five profiles.** Its product default is Medium,
  so every profile except `evidence-research` is a deliberate move. This is the
  provider where the workspace's configuration does the most work, and also the
  provider whose effort names differ by surface: the product ladder's lowest
  step is Low in the CLI and Light in the desktop app, web, and IDE.
- **Gemini's evidence profile is the one upward step on a light model.** CVD-09
  raises Flash-Lite from `minimal` to `medium`, which matches the official
  guidance to use `medium` or `high` for autonomous subagents on Flash-Lite
  that need tool calls and multi-step reasoning. The choice is independently
  corroborated rather than inferred.

## Repository Investigation for Model Changes

Anything that alters a value in the table above must resolve the following in
this workspace before the change protocol can be satisfied. These are gaps in
observability, not objections to a particular model.

1. **Runtime substitution is unobservable.** Claude Code checks a subagent's
   model against an organization `availableModels` allowlist and, when a family
   alias is blocked, runs the subagent on the newest permitted version of that
   family; for other blocked values it falls back to the inherited model. No
   tracked repository file can see this happen, so a validated exact model ID
   is not proof of the model that ran.
2. **Entitlement remains unproven for all three providers.** The contract
   records `local_runtime_acceptance: needs_revalidation` for Claude, Codex,
   and Gemini alike, and `local_cli_observation: unavailable` for Gemini with a
   null CLI version. Two of the three have an observed CLI version; none has an
   observed model acceptance.
3. **No comparative evaluation exists.** The 11 fixtures and 16 synthetic
   regressions score repository semantics, not model quality. Changing a
   profile on task-fit grounds currently has no baseline to beat, which is what
   AMS-06 is guarding against.
4. **Effort is not a token budget.** Official guidance calls effort "a
   behavioral signal, not a strict token budget", and notes that changing it
   between requests invalidates prompt caching. Any argument for stepping a
   profile down on cost grounds needs measurement, and none is tracked here.

## Analysis

The repo policy is a disciplined instance of the general right-sizing practice.
External guidance frames model choice as a balance of capabilities, speed, and
cost, and treats effort as a lever that is often preferable to switching models:
start from a capable model for complex reasoning and lower effort or downgrade as
the workflow is optimized, or start from a fast, cheap model for high-volume,
straightforward tasks and upgrade only for specific capability gaps. Sub-agent
tasks are explicitly called out as a good fit for the fast, economical tier.

The workspace resolves the first axis structurally through one supervisor and
thirteen workers, each assigned one of five typed work profiles. The second
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

## Corrections to Stale Claims

- **Corrected 2026-08-07.** Earlier text described the Codex TOML effort
  surface only through the product ladder. The subagent documentation names six
  accepted `model_reasoning_effort` values — `low`, `medium`, `high`, `xhigh`,
  `max`, `ultra` — and the workspace uses four of them. The product-versus-API
  divergence still holds: the product ladder has `Ultra` and no `none`, while
  the API exposes `none`, `low`, `medium`, `high`, `xhigh`, and `max` with no
  `ultra`.
- **Refined 2026-08-07.** "Haiku 4.5 omits the unsupported effort key" is now
  backed by the official supported-model list rather than asserted. That list
  does not include `claude-haiku-4-5-20251001`.
- **Refined 2026-08-07.** The Gemini thinking-value claim now cites the exact
  contract field path rather than describing it as "settings-level". The
  subagent file schema was re-verified and contains no thinking field; it does
  contain `temperature`, which the earlier description did not mention.
- **Added 2026-08-07.** `gpt-5.6` is documented as an alias for GPT-5.6 Sol.
  Because the workspace configures the exact ID `gpt-5.6-sol`, the alias is not
  in use and no moving-alias risk applies to the current contract.
- **Added 2026-08-07.** Two of the five Claude profile values restate the
  provider default rather than change it. See CVD-01 and CVD-04.
- **Unchanged 2026-08-07.** The fixed historical cutoff ledger, its 145/142
  split, the three retrieval-only GPT-5.6 rows, and the
  `2026-07-26T20:08:18+09:00` contract timestamp are not revised by this pass.
  Later provider observations describe current state only and cannot be
  backdated into the 2026-07-10 10:00 KST cutoff.

## Potential Follow-up / Gap

- The historical GPT-5.6 rows remain cutoff-unverified; that historical state
  is separate from the current contract's stable provider lifecycle.
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
- [Provider capability matrix](../../../00.agent-governance/policies/provider-capability-matrix.md) - vendor feature and boundary SSOT relevant to model configuration
- [Repository contract check](../../../../scripts/validation/check-repo-contracts.sh) - enforces name/model/scope parity across provider adapters
- [Provider model landscape](./provider-model-landscape.md) - 145-row structural catalog, 142-row exact-cutoff-qualified subset, dated exact-ID remediation evidence, lifecycle normalization, official sources, and task-fit inference
- [Choosing a Claude model](https://platform.claude.com/docs/en/about-claude/models/choosing-a-model) - provider capability/speed/effort guidance
- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents) - subagent model field and alias resolution
- [OpenAI model catalog](https://developers.openai.com/api/docs/models) - Sol, Terra, Luna, the `gpt-5.6` alias, and current reasoning controls
- [Codex manual snapshot](https://learn.chatgpt.com/docs/models) - Codex model-selection and reasoning-effort product guidance
- [Gemini latest models](https://ai.google.dev/gemini-api/docs/latest-model) - Gemini 3.6 Flash and Gemini 3.5 Flash-Lite GA state, their `medium` and `minimal` default thinking levels, and the guidance to raise Flash-Lite to `medium` or `high` for autonomous tool-calling subagents
- [Claude effort parameter](https://platform.claude.com/docs/en/build-with-claude/effort) - the supported-model list, the five effort levels, the statement that `high` equals omitting the parameter, and the note that effort is a behavioral signal rather than a token budget
- [Gemini CLI subagents](https://github.com/google-gemini/gemini-cli/blob/main/docs/core/subagents.md) - the subagent frontmatter field list, which contains no reasoning or thinking key
- [Provider model contract](../../../00.agent-governance/contracts/provider-models.yaml) - the five work profiles, the exact per-provider model and control values, and the `native_reasoning_field` paths

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
