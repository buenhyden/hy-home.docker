---
status: draft
artifact_id: reference:agentic-engineering-research:provider-model-landscape
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-08
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

| Axis | Question answered | Current workspace interpretation |
| --- | --- | --- |
| Provider lifecycle | How does the owner publish the model? | Stable, preview, limited availability, or another owner-defined state. |
| Repository disposition | What may this repository do with it? | Default, candidate, or catalog-only. |
| Runtime acceptance | Did the active runtime accept the exact value? | `needs_revalidation` for every registered model. |
| Entitlement | May the active account/organization use it? | `needs_revalidation` for every registered model. |
| Default eligibility | May a work profile select it? | True only for registered defaults. |
| Activation eligibility | May this evidence activate it now? | False for all 11 models. |

### Complete tracked registry

| Provider | Exact model ID | Owner lifecycle | Repository disposition | Work-profile use | Current mutable-source observation |
| --- | --- | --- | --- | --- | --- |
| Claude | `claude-fable-5` | Stable | Candidate | None | Official overview calls it generally available and suited to long-running agents; Claude Code does not make it the default. |
| Claude | `claude-haiku-4-5-20251001` | Stable | Default | Routine validation | Official overview lists it as the fastest current row and the only current row without adaptive thinking. |
| Claude | `claude-mythos-5` | Limited availability | Catalog-only | None | Official overview limits it to approved Project Glasswing customers; public documentation is not entitlement. |
| Claude | `claude-opus-5` | Stable | Default | Adversarial review, supervision | Official overview recommends it for complex agentic coding and enterprise work. |
| Claude | `claude-sonnet-5` | Stable | Default | Complex implementation, evidence research | Official overview describes a speed/intelligence balance. |
| Codex | `gpt-5.3-codex-spark` | Preview | Catalog-only | None | Codex models page describes a text-only research preview available to ChatGPT Pro users. |
| Codex | `gpt-5.6-luna` | Stable | Catalog-only | None | Codex page positions it for clear, repeatable, high-volume tasks. |
| Codex | `gpt-5.6-sol` | Stable | Default | Review, implementation, supervision | Codex page positions it for complex open-ended coding, research, and cybersecurity. |
| Codex | `gpt-5.6-terra` | Stable | Default | Evidence research, routine validation | Codex page positions it as the everyday balanced model. |
| Gemini | `gemini-3.5-flash-lite` | Stable at contract cutoff | Default | Evidence research, routine validation | Not reopened in Task 4; current provider state remains bounded by the dated tracked source. |
| Gemini | `gemini-3.6-flash` | Stable at contract cutoff | Default | Review, implementation, supervision | Not reopened in Task 4; current provider state remains bounded by the dated tracked source. |

All eleven rows retain `needs_revalidation` runtime acceptance and entitlement,
and `runtime_activation_eligible: false`. The table reports source and policy
state only.

### Provider-native selection and reasoning

| Concern | Claude Code | Codex | Workspace rule |
| --- | --- | --- | --- |
| Model selection | Full ID or mutable family/special alias; session, startup, environment, and settings precedence. | `model` in shared local config or `--model`; recommended model may apply when unset. | Generated agents use exact IDs from the typed work profile. |
| Reasoning control | `low`, `medium`, `high`, `xhigh`, `max`; `ultracode` is a session orchestration setting, not a model effort value. | Product UI/CLI exposes Low through Max and an Ultra delegation mode; config reference documents model effort separately. | Local adapters use only `low`, `medium`, `high`, or `xhigh`; names are not cross-provider equivalents. |
| Default | Current Claude models generally default to `high`; model/organization restrictions can clamp or substitute. | Codex page states the default Power setting is Sol with medium reasoning. | A configured value is not proof the runtime applied it. |
| Alias risk | Family aliases update and can resolve differently by provider; full names pin the configured target. | `gpt-5.6` is a product alias while local profiles use `-sol` or `-terra`. | Keep exact native IDs in generated adapters. |
| Fallback | Claude Code supports ordered availability fallback chains and some safety-triggered fallback. | No workspace model fallback graph is defined by the cited Codex config source. | The current typed contract has no automatic fallback graph; do not invent one. |

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

## Scope Implications

| Scope | Application and disposition |
| --- | --- |
| `agentic` | Own the typed registry, renderer, and native-control parity; status axes must remain separate. |
| `architecture` | Model changes affecting system design require an approved architecture/lifecycle owner; no current typed agent record owns this scope. |
| `backend` | No current application surface; future inference/runtime choices need their own Spec and are not implied by agent defaults. |
| `common` | Shared review uses the registered profile only; no ad hoc alias or cross-provider effort translation. |
| `docs` | Dated mutable-source facts and cutoff history must remain explicit; this reference cannot promote a model. |
| `entry` | Gateway/runtime model routing is outside this agent-adapter registry and needs infra ownership if introduced. |
| `frontend` | Current Storybook fixture does not justify a product model policy; future UI agents use an approved typed profile. |
| `infra` | Provider, gateway, environment, and secret changes require separate approval and runtime evidence. |
| `meta` | Model identifiers and status axes are typed contract data; schema changes route through Stage 00 and validators. |
| `mobile` | Not applicable to the current corpus; no mobile model/runtime inference is made. |
| `ops` | Availability, rate limits, fallback events, and costs are operational observations, not derivable from configured IDs. |
| `product` | Provider descriptions are hypotheses for evaluation, not product acceptance or procurement decisions. |
| `qa` | Synthetic fixtures validate semantics, not comparative model quality; live evaluation needs approved representative tasks. |
| `security` | Limited-access/security-specialized labels do not grant use; model/provider changes preserve approval, privacy, and supply-chain review. |

## Sources

| Source | Accessed | Class | Verification state |
| --- | --- | --- | --- |
| [Anthropic models overview](https://platform.claude.com/docs/en/about-claude/models/overview) | 2026-08-08T16:18:04+09:00 | External mutable | Original docs URL redirected here; HTTP 200; IDs, lifecycle, capability, context, and reasoning facts. |
| [Claude Code model configuration](https://code.claude.com/docs/en/model-config) | 2026-08-08T16:18:04+09:00 | External mutable | HTTP 200; aliases, precedence, restrictions, effort, and fallback mechanics. |
| [Codex models](https://learn.chatgpt.com/docs/models) | 2026-08-08T16:18:04+09:00 | External mutable | HTTP 200; Sol/Terra/Luna/Spark, product reasoning, and retirement facts. |
| [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) | 2026-08-08T16:18:04+09:00 | External mutable | HTTP 200; exact configuration fields and project-scope limits. |
| [Provider model contract](../../../00.agent-governance/contracts/provider-models.yaml) | 2026-08-08 | Workspace tracked | Complete 11-model registry at Task 4 baseline; fixed cutoff `2026-07-26T20:08:18+09:00`. |
| [Subagent protocol](../../../00.agent-governance/subagent-protocol.md) | 2026-08-08 | Workspace tracked | Human work-profile routing and coupled change protocol. |
| [Graphify report](../../../../graphify-out/GRAPH_REPORT.md) | 2026-08-08 | Workspace stale/advisory | Stale at `f8a72211`; corroborated against tracked owners. |

## Maintenance

Reopen mutable provider pages and parse the complete typed registry when any
model, lifecycle, alias, reasoning control, work profile, renderer, or
validator changes. Preserve old cutoff evidence; append a new dated
observation rather than rewriting history.

## Related Documents

- [Agent model selection](./agent-model-selection.md)
- [Provider implementation comparison](./provider-implementation-comparison.md)
- [Agent instructions](./agent-instructions-vibe-coding.md)
- [Scope application matrix](./scope-application-matrix.md)
- [Execution Task](../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md)
