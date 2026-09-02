---
title: "Reference: Provider Model Landscape at the Evidence Cutoff"
type: references/research-member
layer: reference
status: active
owner: "@buenhyden"
artifact_id: RES-0002-m0013
parent_ids: [RES-0002]
created: 2026-08-23
updated: 2026-08-30
reviewed_at: 2026-08-28
review_cycle: on-source-change
---

# Reference: Provider Model Landscape at the Evidence Cutoff

## Overview

The workspace model registry is a dated policy input, not an evergreen list of
everything a provider sells. At Task 4 baseline
`1cd9bc2830db710585348e8ef38b0318cc7f5a10`, the typed contract records 3
providers, 5 work profiles, and 11 exact model IDs: 5 Claude, 4 Codex, and 2
Gemini. Every model keeps separate provider-lifecycle, repository-disposition,
runtime-acceptance, entitlement, default-eligibility, and activation axes.

Anthropic and OpenAI/Codex model/configuration pages were reopened at
`2026-08-08T16:18:04+09:00`. Those current observations supplement but do not
rewrite the registry's fixed `2026-07-26T20:08:18+09:00` retrieval/cutoff.

The same pages were reopened again at `2026-08-14T13:40:00+09:00` for this
deepening pass, together with the Claude Code subagent and effort references.
Direct re-read of `contracts/provider-models.yaml` at repository commit
`ece3eda9c3e1a603c6495dd55caba7df1c29ef6c` (2026-08-14) confirms the tracked
contract itself is byte-identical in cutoff, provider count, profile count,
and model count to the Task 4 baseline; only the layered current-observation
evidence below is new. The 2026-08-14 pass also surfaces a control-value
discrepancy between the tracked Codex reasoning-control enum and the current
Codex configuration reference (see "Reasoning-control value drift" below),
which is recorded as `UNVERIFIED` rather than silently resolved.

## Purpose

Record the current official Claude and Codex landscape relevant to the local
registry, explain provider-native model/effort/fallback mechanics, and prevent
catalog presence or configuration from being mistaken for live availability.

## Repository Role

This Stage 90 reference is an evidence map. Exact allowed defaults and controls
remain owned by `contracts/provider-models.yaml` and the human routing view in
`subagent-protocol.md`. This document changes neither.

## Scope

### In scope

- Dated official model/configuration facts for Claude and Codex.
- The complete tracked 11-model registry and its six status axes.
- Provider-native effort, selection, alias, fallback, and entitlement limits.

### Out of scope

- Ranking providers, predicting cost/latency, or claiming benchmark parity.
- Calling a provider, inspecting account entitlements, or changing adapters.
- Backdating current observations into the fixed registry cutoff.

## Definitions / Facts

### Six independent status axes

| Axis                   | Question answered                              | Current workspace interpretation                                       |
| ---------------------- | ---------------------------------------------- | ---------------------------------------------------------------------- |
| Provider lifecycle     | How does the owner publish the model?          | Stable, preview, limited availability, or another owner-defined state. |
| Repository disposition | What may this repository do with it?           | Default, candidate, or catalog-only.                                   |
| Runtime acceptance     | Did the active runtime accept the exact value? | `needs_revalidation` for every registered model.                       |
| Entitlement            | May the active account/organization use it?    | `needs_revalidation` for every registered model.                       |
| Default eligibility    | May a work profile select it?                  | True only for registered defaults.                                     |
| Activation eligibility | May this evidence activate it now?             | False for all 11 models.                                               |

### Complete tracked registry

| Provider | Exact model ID              | Owner lifecycle           | Repository disposition | Work-profile use                          | Current mutable-source observation                                                                                          |
| -------- | --------------------------- | ------------------------- | ---------------------- | ----------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Claude   | `claude-fable-5`            | Stable                    | Candidate              | None                                      | Official overview calls it generally available and suited to long-running agents; Claude Code does not make it the default. |
| Claude   | `claude-haiku-4-5-20251001` | Stable                    | Default                | Routine validation                        | Official overview lists it as the fastest current row and the only current row without adaptive thinking.                   |
| Claude   | `claude-mythos-5`           | Limited availability      | Catalog-only           | None                                      | Official overview limits it to approved Project Glasswing customers; public documentation is not entitlement.               |
| Claude   | `claude-opus-5`             | Stable                    | Default                | Adversarial review, supervision           | Official overview recommends it for complex agentic coding and enterprise work.                                             |
| Claude   | `claude-sonnet-5`           | Stable                    | Default                | Complex implementation, evidence research | Official overview describes a speed/intelligence balance.                                                                   |
| Codex    | `gpt-5.3-codex-spark`       | Preview                   | Catalog-only           | None                                      | Codex models page describes a text-only research preview available to ChatGPT Pro users.                                    |
| Codex    | `gpt-5.6-luna`              | Stable                    | Catalog-only           | None                                      | Codex page positions it for clear, repeatable, high-volume tasks.                                                           |
| Codex    | `gpt-5.6-sol`               | Stable                    | Default                | Review, implementation, supervision       | Codex page positions it for complex open-ended coding, research, and cybersecurity.                                         |
| Codex    | `gpt-5.6-terra`             | Stable                    | Default                | Evidence research, routine validation     | Codex page positions it as the everyday balanced model.                                                                     |
| Gemini   | `gemini-3.5-flash-lite`     | Stable at contract cutoff | Default                | Evidence research, routine validation     | Not reopened in Task 4; current provider state remains bounded by the dated tracked source.                                 |
| Gemini   | `gemini-3.6-flash`          | Stable at contract cutoff | Default                | Review, implementation, supervision       | Not reopened in Task 4; current provider state remains bounded by the dated tracked source.                                 |

All eleven rows retain `needs_revalidation` runtime acceptance and entitlement,
and `runtime_activation_eligible: false`. The table reports source and policy
state only.

### Full vendor catalog versus the registered subset

The 2026-08-14 reopen of the Anthropic models overview shows the vendor
catalog is materially larger than the 5 Claude rows this repository tracks.
The current page lists 4 "current" Claude models (Fable 5, Opus 5, Sonnet 5,
Haiku 4.5) plus an accordion of 6 "legacy" models still served over the API:
Opus 4.8, Opus 4.7, Opus 4.6, Sonnet 4.6, Sonnet 4.5, and Opus 4.5. None of
the 6 legacy IDs (`claude-opus-4-8`, `claude-opus-4-7`, `claude-opus-4-6`,
`claude-sonnet-4-6`, `claude-sonnet-4-5-20250929`, `claude-opus-4-5-20251101`)
appear in `provider-models.yaml`. That is expected under this repository's
curated-registry design (Scope: In scope), not a gap, but it means "vendor
still serves it" and "repository can select it" are disjoint sets that must
never be conflated.

The vendor page also documents `claude-mythos-preview` as a distinct
invitation-only model inside Project Glasswing, separate from the tracked
`claude-mythos-5` row. `provider-models.yaml` has no row for
`claude-mythos-preview`. This is a genuine current-catalog delta the tracked
registry has not evaluated; it is named here as an intake candidate, not
adopted, consistent with the pack's router character.

On the Codex side, the current models page documents 4 current-generation
IDs matching the tracked registry (`gpt-5.6-sol`, `gpt-5.6-terra`,
`gpt-5.6-luna`, `gpt-5.3-codex-spark`) plus a "previous generation" tier
(`gpt-5.5`, `gpt-5.4`, `gpt-5.4-mini`) and an already-deprecated tier
(`gpt-5.2`, `gpt-5.3-codex`) for ChatGPT-authenticated Codex users. The page
states `gpt-5.4` and `gpt-5.4-mini` retire from Codex with ChatGPT sign-in on
2026-08-31, with `gpt-5.6-terra` and `gpt-5.6-luna` named as their
replacements. None of the previous-generation or deprecated IDs are tracked
in `provider-models.yaml`, so the 2026-08-31 retirement carries no direct
repository risk; it is recorded because a future registry refresh that adds
one of the retiring IDs as a stopgap default would need this date.

### Catalog evidence-reading rules

The retiring pack's 145-row vendor catalog carried a `Caveat` column that is a
separate claim family from the identity columns beside it. Measured over the
catalog: 145 cells, 96 non-trivial, 70 distinct strings, 51 of them occurring
once. Most are not facts about one model but reading rules that generalise well
past the row they sit in, so they are carried here deduplicated into twenty
families rather than as 96 cells. The per-row identity data is not carried; it is
re-derivable from the vendor pages the `Sources` section names.

1. **A mutable alias is not a maturity claim.** `latest` does not mean stable,
   and an alias stays mutable even when its current target is Stable.
2. **Snapshot and alias schedules are separate.** A dated snapshot can be
   Deprecated while its alias is not, snapshot evidence does not date an alias
   transition, and deprecated snapshot status must not be transferred to the
   current alias.
3. **A product or marketing surface is not an API identity.** A product alias, a
   policy alias, a family marketing name, and a managed-agent label are each
   distinct from the API model ID.
4. **Availability is not maturity.** Invitation-only access, an open-weight
   release, and an Experimental label each establish that something exists
   without establishing that it is generally available or production-suitable.
5. **Existence evidence is not lifecycle state.** An announcement, an SDK commit,
   or an API listing proves that a thing existed by a date; none proves its
   current lifecycle state, its launch date, or a product entitlement.
6. **A mutable page does not prove a state at an instant.** A status page or
   listing read after a cutoff is not evidence of the state at that cutoff,
   particularly where the page shows no exact update time.
7. **Stable maturity and a scheduled lifecycle end coexist.** A provider-native
   `stable` or `preview` token inside an ID does not override a Deprecated or
   scheduled-retirement state recorded elsewhere.
8. **First-party dates do not govern partner schedules.** Cloud marketplace and
   partner lifecycles run separately from the first-party one.
9. **Feature removal is not model deprecation.** A removed mode, an ended
   legacy-tool support, and a separate fine-tuning transition each retire less
   than the model.
10. **A redirect does not revive maturity.** Following a redirect reaches a
    different endpoint; it does not restore the lifecycle state of the one that
    was redirected away.
11. **A specialized model is not a general worker.** Media, robotics, and other
    specialized models are not general task-selection defaults.
12. **An unzoned calendar day is cutoff-qualified only when its whole range
    precedes the cutoff instant.** This is the rule that produces the
    structural-versus-qualified split rather than any individual vendor fact.
    **Correction.** The retiring pack applied a `historical state unverified`
    marker to rows failing this test, meaning the official evidence retrieved
    on its access date does not prove the exact state at the cutoff instant,
    because the page is mutable, the event lacks a cutoff-safe timestamp, or
    official pages conflict. That marker is a convention of that pack, not a
    value in any typed contract, and it must not be cited as one.
13. **Absent replacement or shutdown data is itself a finding.** A deprecation
    entry with no named replacement, or with no shutdown date, records an
    evidence gap rather than an absence of risk.
14. **Retention and data-handling constraints ride with the model.** A model may
    require a retention window that rules out zero-data-retention use.
15. **An agent endpoint is not interchangeable with a base model.** Corrected
    2026-08-19: this family previously added "Some agent endpoints are not
    generative models at all", which merged two distinct source classes and
    attributed an embeddings property to agent endpoints. The retiring catalog
    records them separately — `Agent endpoint is not interchangeable with a base
    model` on the deep-research rows, and `Not a generative agent model` on
    `gemini-embedding-2` and the `text-embedding-3` rows, which are Embeddings
    API entries rather than agent endpoints. Read them as two rules: an agent
    endpoint is a distinct surface from the base model it wraps, and an
    embeddings entry is not a generative model at all.
16. **One official card may group several exact endpoints.** Card granularity is
    a presentation choice, so a single card is not evidence that the endpoints
    it groups share an identity or a schedule.
17. **A normalized lifecycle label is derived, not the provider's own.** Where
    this catalog records `Stable`, that normalization rests on the dated launch
    plus current-model placement and is not the provider's own `Active` status.
18. **The catalog asserts no performance ranking.** No row claims benchmark
    superiority over another, and none should be read as implying one.
19. **Presence in the catalog is not endorsement.** An alias retained as a
    historical identifier, a preview suffix recorded for exactness, and a former
    workspace worker value are each catalogued without being a current default
    or locally proven as available.
20. **An informal descriptor is not a lifecycle label.** Wording such as
    "older" on a vendor page is description, not a deprecation state.

**Mythos Preview carries an unresolved official conflict.** The vendor lifecycle
page schedules `claude-mythos-preview` for retirement on 2026-06-30 while the
current overview still presents it as separately offered, and no dated
completion notice or endpoint evidence resolves the two. Its availability at the
cutoff is therefore `UNVERIFIED`, and the row is retained structurally rather
than normalized. This is recorded because Spec 137's guardrail for a conflict
between external and local documents is to record the conflict and its evidence
class, not to pick a side; the intake-candidate framing above states the delta
but not the conflict.

### Claude current-model comparison (2026-08-14 vendor table)

| Model            | Claude API ID               | Pricing (in/out per MTok) | Context window | Adaptive thinking | Extended thinking (`thinking.type`) | Reliable knowledge cutoff |
| ---------------- | --------------------------- | ------------------------- | -------------- | ----------------- | ----------------------------------- | ------------------------- |
| Claude Fable 5   | `claude-fable-5`            | $10 / $50                 | 1M tokens      | Yes, always on    | No                                  | Jan 2026                  |
| Claude Opus 5    | `claude-opus-5`             | $5 / $25                  | 1M tokens      | Yes               | No                                  | May 2026                  |
| Claude Sonnet 5  | `claude-sonnet-5`           | $2 / $10                  | 1M tokens      | Yes               | No                                  | Jan 2026                  |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | $1 / $5                   | 200k tokens    | No                | Yes                                 | Feb 2025                  |

Claude Mythos 5 "shares Claude Fable 5's specs and pricing" per the vendor
page and is not broken out separately in the comparison table. Haiku 4.5 is
confirmed as the only current-generation row with extended thinking instead
of adaptive thinking and without an adaptive-thinking toggle, matching this
leaf's prior claim; the vendor table now also shows Haiku 4.5 is the only
current row with a sub-1M context window (200k tokens) and the only one with
a pre-2026 reliable knowledge cutoff. Every current model ID is a pinned
snapshot: dateless IDs from the Claude 4.6 generation onward are fixed
releases, not evergreen aliases, per the vendor page's explicit note.

### Effort mechanics per model family

The 2026-08-14 reopen of the Claude Code model-configuration reference
resolves exactly which effort levels each model family supports, closing a
gap this leaf previously left implicit:

| Model family                         | Supported `effort` levels                   | Default                               | Downgrade behavior when an unsupported level is requested                                                                           |
| ------------------------------------ | ------------------------------------------- | ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Fable 5                              | `low`, `medium`, `high`, `xhigh`, `max`     | `high`                                | N/A (supports the full ladder)                                                                                                      |
| Opus 5, Sonnet 5, Opus 4.8, Opus 4.7 | `low`, `medium`, `high`, `xhigh`, `max`     | `high` (Opus 4.7 defaults to `xhigh`) | N/A (supports the full ladder)                                                                                                      |
| Opus 4.6, Sonnet 4.6                 | `low`, `medium`, `high`, `max` (no `xhigh`) | `high`                                | Claude Code falls back to the highest supported level at or below the requested one, for example `xhigh` runs as `high` on Opus 4.6 |

`provider-models.yaml` records `supported_reasoning_controls` for
`claude-opus-5` and `claude-sonnet-5` as exactly `high`, `low`, `max`,
`medium`, `xhigh` — a 5-value set that matches the vendor page exactly for
those two model families. This is a positive cross-check: the tracked
registry's Claude reasoning-control enum has not drifted from the current
vendor documentation.

`ultracode`, offered in the `/effort` menu, is confirmed as a Claude Code
session setting rather than a model effort value: it sends `xhigh` to the
model and additionally has Claude orchestrate dynamic workflows; it cannot be
set through `effortLevel` in settings or through
`CLAUDE_CODE_EFFORT_LEVEL`, and it is session-only. This is consistent with,
and now more precisely sourced than, the leaf's prior warning against
copying Codex's Max/Ultra controls into `model_reasoning_effort` by analogy.

### Reasoning-control value drift (Codex, `UNVERIFIED`)

The 2026-08-14 reopen of the Codex configuration reference documents
`model_reasoning_effort` as accepting exactly `minimal | low | medium | high
| xhigh`, five values, with `xhigh` noted as model-dependent. The tracked
registry's `supported_reasoning_controls` for `gpt-5.6-sol`, `gpt-5.6-terra`,
and `gpt-5.6-luna` instead lists six values: `high`, `low`, `max`, `medium`,
`none`, `xhigh` — it includes `max` and `none`, both absent from the current
vendor documentation, and omits `minimal`, which the current vendor
documentation includes. This is flagged `UNVERIFIED`: it is not clear
whether the tracked enum reflects an earlier Codex configuration schema, a
different exposure surface (product UI reasoning levels versus the
`model_reasoning_effort` config field), or a documentation change since the
registry's `2026-07-26T20:08:18+09:00` cutoff. Observation that would settle
it: re-open the exact `reasoning_source_url` cited per Codex model row in
`provider-models.yaml` and diff its enumerated values against both this
leaf's citation and the registry's `repository_reasoning_controls`
(currently `high`/`xhigh` for `gpt-5.6-sol`, `low`/`medium` for
`gpt-5.6-terra`) to confirm neither configured value falls outside the
current vendor-documented set.

### Fallback mechanics decomposition

The 2026-08-14 reopen of the Claude Code model-configuration reference shows
Claude Code implements two independent fallback mechanisms that this leaf
previously treated as one "fallback" concept:

| Mechanism                              | Trigger                                                                                                                                                 | Configuration                                                | Scope and limits                                                                                                                                                                                      |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Availability-based fallback chains     | Primary model overloaded, unavailable, or a non-retryable server error; never triggered by auth, billing, rate-limit, request-size, or transport errors | `--fallback-model` flag or `fallbackModel` array in settings | Capped at 3 models after duplicate removal; applies for the current turn only, then reverts to the primary model on the next message                                                                  |
| Automatic (safety-classifier) fallback | A cybersecurity- or biology-content classifier flags a Fable 5 or Opus 5 request                                                                        | Not user-configured; built into Fable 5 and Opus 5           | Fable 5: biology flag re-runs on Opus 5, cybersecurity flag re-runs on Opus 4.8. Opus 5: cybersecurity flag re-runs on Opus 4.8; biology flag ends in refusal (Opus 5 has no biology fallback target) |

Both mechanisms respect `availableModels`: an availability-chain entry
outside the allowlist is dropped before the walk starts, and a
safety-classifier fallback target outside the allowlist does not run,
ending the flagged request in a refusal instead. Neither mechanism is
configured anywhere in this repository's tracked contract, so this leaf's
prior statement that "the current typed contract has no automatic fallback
graph" remains accurate for both senses of "fallback" now that they are
distinguished. Codex's cited configuration source documents neither
mechanism.

### Provider-native selection and reasoning

| Concern           | Claude Code                                                                                                        | Codex                                                                                                                    | Workspace rule                                                                                         |
| ----------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ |
| Model selection   | Full ID or mutable family/special alias; session, startup, environment, and settings precedence.                   | `model` in shared local config or `--model`; recommended model may apply when unset.                                     | Generated agents use exact IDs from the typed work profile.                                            |
| Reasoning control | `low`, `medium`, `high`, `xhigh`, `max`; `ultracode` is a session orchestration setting, not a model effort value. | Product UI/CLI exposes Low through Max and an Ultra delegation mode; config reference documents model effort separately. | Local adapters use only `low`, `medium`, `high`, or `xhigh`; names are not cross-provider equivalents. |
| Default           | Current Claude models generally default to `high`; model/organization restrictions can clamp or substitute.        | Codex page states the default Power setting is Sol with medium reasoning.                                                | A configured value is not proof the runtime applied it.                                                |
| Alias risk        | Family aliases update and can resolve differently by provider; full names pin the configured target.               | `gpt-5.6` is a product alias while local profiles use `-sol` or `-terra`.                                                | Keep exact native IDs in generated adapters.                                                           |
| Fallback          | Claude Code supports ordered availability fallback chains and some safety-triggered fallback.                      | No workspace model fallback graph is defined by the cited Codex config source.                                           | The current typed contract has no automatic fallback graph; do not invent one.                         |

The Codex product's Max and Ultra controls must not be copied into
`model_reasoning_effort` by analogy: Ultra is explicitly a delegated
multi-agent mode. Likewise, the same effort label across Claude, Codex, and
Gemini does not establish equal compute, quality, cost, or latency.

### Local construction and verification state

- `provider-models.yaml` owns the 11 exact rows and 15 provider/profile cells.
- `agent-catalog.yaml` assigns each of 14 roles exactly one work profile.
- The renderer maps that profile into 14 Claude, 14 Codex, and 14 Gemini
  native role adapters plus the compatibility projection.
- Validators check allowed IDs/control values and projection parity.
- The repository has observed Claude and Codex CLI versions, but no tracked
  observation proves exact-model acceptance, execution, substitution, or
  entitlement. Gemini CLI observation is unavailable in the contract.

### Control and eligibility boundary

The local contract maps `effort` to Claude and `model_reasoning_effort` to
Codex. Those fields describe different native schemas. The 2026-08-14 retained
Claude observation says that an unsupported effort request is resolved by that
provider's own compatibility behavior; it does not authorize a local fallback.
The retained Codex configuration page documented `minimal`, `low`, `medium`,
`high`, and model-dependent `xhigh`, while the tracked Codex rows additionally
contain historical `none` and `max`. This mismatch is deliberately
`UNVERIFIED`, rather than evidence of a fallback or a runtime defect.

The registry's model rows must pass three distinct checks before promotion:
official-source revalidation, entitlement revalidation, and runtime
revalidation. A provider catalog can therefore contain a model that this
repository cannot select; conversely, an existing row is not proof that a
particular user, organization, or session can use it.

### Static profile bindings

The five current tracked-only mappings are below. They are declarations, not
public-entitlement assertions: `adversarial-review` maps to Claude
`claude-opus-5` / `effort: high` and Codex `gpt-5.6-sol` /
`model_reasoning_effort: xhigh`; `complex-implementation` maps to
`claude-sonnet-5` / `high` and `gpt-5.6-sol` / `high`; `evidence-research`
maps to `claude-sonnet-5` / `low` and `gpt-5.6-terra` / `medium`;
`long-horizon-supervision` maps to `claude-opus-5` / `xhigh` and
`gpt-5.6-sol` / `xhigh`; and `routine-validation` maps to
`claude-haiku-4-5-20251001` / no native effort value and `gpt-5.6-terra` /
`low`. The final profile is a useful boundary: a null Claude control is not a
request to invent one.

### Evidence-reading rules

The retained provider-catalog analysis supplies three durable reading rules.
An alias or marketing family is not necessarily an exact API identity; a
provider lifecycle label does not establish account availability; and a
catalogue row does not assert a benchmark ranking. These rules avoid turning a
mutable product page into a claim about local execution. They also mean that
the registry's five rows are a curated routing input, not a claim to enumerate
all provider offerings.

## Scope Implications

| Scope          | Application and disposition                                                                                                              |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `agentic`      | Own the typed registry, renderer, and native-control parity; status axes must remain separate.                                           |
| `architecture` | Model changes affecting system design require an approved architecture/lifecycle owner; no current typed agent record owns this scope.   |
| `backend`      | No current application surface; future inference/runtime choices need their own Spec and are not implied by agent defaults.              |
| `common`       | Shared review uses the registered profile only; no ad hoc alias or cross-provider effort translation.                                    |
| `docs`         | Dated mutable-source facts and cutoff history must remain explicit; this reference cannot promote a model.                               |
| `entry`        | Gateway/runtime model routing is outside this agent-adapter registry and needs infra ownership if introduced.                            |
| `frontend`     | Current Storybook fixture does not justify a product model policy; future UI agents use an approved typed profile.                       |
| `infra`        | Provider, gateway, environment, and secret changes require separate approval and runtime evidence.                                       |
| `meta`         | Model identifiers and status axes are typed contract data; schema changes route through Stage 00 and validators.                         |
| `mobile`       | Not applicable to the current corpus; no mobile model/runtime inference is made.                                                         |
| `ops`          | Availability, rate limits, fallback events, and costs are operational observations, not derivable from configured IDs.                   |
| `product`      | Provider descriptions are hypotheses for evaluation, not product acceptance or procurement decisions.                                    |
| `qa`           | Synthetic fixtures validate semantics, not comparative model quality; live evaluation needs approved representative tasks.               |
| `security`     | Limited-access/security-specialized labels do not grant use; model/provider changes preserve approval, privacy, and supply-chain review. |

## Sources

| Source                                                                                        | Accessed                  | Class                    | Verification state                                                                                         |
| --------------------------------------------------------------------------------------------- | ------------------------- | ------------------------ | ---------------------------------------------------------------------------------------------------------- |
| [Anthropic models overview](https://platform.claude.com/docs/en/about-claude/models/overview) | 2026-08-08T16:18:04+09:00 | External mutable         | Original docs URL redirected here; HTTP 200; IDs, lifecycle, capability, context, and reasoning facts.     |
| [Claude Code model configuration](https://code.claude.com/docs/en/model-config)               | 2026-08-08T16:18:04+09:00 | External mutable         | HTTP 200; aliases, precedence, restrictions, effort, and fallback mechanics.                               |
| [Codex models](https://learn.chatgpt.com/docs/models)                                         | 2026-08-08T16:18:04+09:00 | External mutable         | HTTP 200; Sol/Terra/Luna/Spark, product reasoning, and retirement facts.                                   |
| [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)  | 2026-08-08T16:18:04+09:00 | External mutable         | HTTP 200; exact configuration fields and project-scope limits.                                             |
| Provider model contract (retired path: `../../../00.agent-governance/contracts/provider-models.yaml`)        | 2026-08-08                | Workspace tracked        | Complete 11-model registry at Task 4 baseline; fixed cutoff `2026-07-26T20:08:18+09:00`.                   |
| Subagent protocol (retired path: `../../../00.agent-governance/subagent-protocol.md`)                        | 2026-08-08                | Workspace tracked        | Human work-profile routing and coupled change protocol.                                                    |
| [Graphify report](../../../../graphify-out/GRAPH_REPORT.md)                                   | 2026-08-08                | Workspace stale/advisory | Stale at `f8a72211`; corroborated against tracked owners.                                                  |
| [Anthropic models overview](https://platform.claude.com/docs/en/about-claude/models/overview) | 2026-08-14T13:40:00+09:00 | External mutable         | Re-read; HTTP 200; full current/legacy model comparison tables, pricing, `claude-mythos-preview` row.      |
| [Claude Code model configuration](https://code.claude.com/docs/en/model-config)               | 2026-08-14T13:40:00+09:00 | External mutable         | Re-read; HTTP 200; per-family effort ladder, `ultracode`, availability chains, safety-classifier fallback. |
| [Codex models](https://learn.chatgpt.com/docs/models)                                         | 2026-08-14T13:40:00+09:00 | External mutable         | Re-read; HTTP 200; previous-generation/deprecated tiers and 2026-08-31 retirement date.                    |
| [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)  | 2026-08-14T13:40:00+09:00 | External mutable         | Re-read; HTTP 200; `model_reasoning_effort` five-value enum, source of the flagged drift.                  |
| [Claude Code subagents reference](https://code.claude.com/docs/en/sub-agents)                 | 2026-08-14T13:40:00+09:00 | External mutable         | HTTP 200; subagent `model`/`effort` frontmatter fields and model-resolution precedence order.              |
| Provider model contract (retired path: `../../../00.agent-governance/contracts/provider-models.yaml`)        | 2026-08-14                | Workspace tracked        | Re-read at commit `ece3eda9c3e1a603c6495dd55caba7df1c29ef6c`; cutoff, counts, and rows unchanged.          |

## Scope Application

| Scope | Disposition | Investigation / adoption condition | Verification | Caveat |
| --- | --- | --- | --- | --- |
| agentic | applies | `eval-engineer` compares `registry.yaml` native control fields before a promotion. | Re-read the five work-profile bindings. | Runtime acceptance is unobserved. |
| architecture | applies | Architecture owner records a decision only if routing semantics change. | Review the approving ADR/Spec path. | No decision is created here. |
| common | applies | `code-reviewer` checks cross-provider terms are not treated as equivalent. | Inspect claim/source rows. | No benchmark comparison exists. |
| docs | applies | `doc-writer` maintains this advisory source mapping. | Reconcile IDs in README. | Links are not provider proof. |
| infra | applies | `infra-implementer` assesses a concrete provider environment's compatibility/capacity before adoption. | Review an approved target-specific record. | No environment was observed. |
| ops | applies | `incident-responder` owns availability/fallback policy evidence for an operational provider use. | Inspect an approved runbook or incident record. | No fallback graph is configured. |
| qa | applies | `qa-engineer` defines representative evaluation before default promotion. | Inspect an approved evaluation record. | No live comparison was run. |
| security | applies | `security-auditor` checks entitlement-sensitive promotion evidence. | Review value-free approval evidence. | Account state was not inspected. |

## Maintenance

Reopen mutable provider pages and parse the complete typed registry when any
model, lifecycle, alias, reasoning control, work profile, renderer, or
validator changes. Preserve old cutoff evidence; append a new dated
observation rather than rewriting history.

## Related Documents

- [Agent model selection](./m0002-agent-model-selection.md)
- [Provider implementation comparison](./m0012-provider-implementation-comparison.md)
- [Agent instructions](./m0001-agent-instructions-vibe-coding.md)
- [Scope application matrix](./m0015-scope-application-matrix.md)
- Execution Task (retired path: `../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md`)
