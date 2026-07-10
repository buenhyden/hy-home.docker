---
status: active
---

<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-model-landscape.md -->

# Reference: Provider Model Landscape at the 2026-07-10 Cutoff

## Overview

This reference records the lifecycle-relevant Claude, OpenAI/Codex, and Gemini
catalogs at the evidence cutoff **2026-07-10 10:00 KST (01:00 UTC)**. Retrieval
date is 2026-07-10. It preserves provider-native names and maturity terms before
making a deliberately narrow cross-provider normalization.

## Purpose

The inventory gives provider, agent-catalog, and task-selection research one
cutoff-bound source. It prevents a mutable current catalog, a moving alias, or a
post-cutoff announcement from silently changing a historical comparison.

## Repository Role

This Stage 90 document is advisory evidence. The current workspace model-policy
SSoT remains the Model Policy in `subagent-protocol.md`; this reference neither
changes that policy nor proves that a configured model was available to a
particular account, region, product surface, or provider adapter.

## Scope

### In Scope

- Official first-party model catalogs, model IDs/aliases, lifecycle pages,
  release notes/changelogs, and CLI model-configuration surfaces.
- Models shown by each provider's cutoff-relevant catalog, including provider
  preview/experimental/latest, deprecated, retired, and shut-down equivalents.
- A normalized lifecycle only where the provider's own term supports it.
- Task-fit analysis inferred from official capability descriptions and the
  workspace task taxonomy.

### Out of Scope

- Benchmark ranking, observed workspace quality, account entitlement, price
  comparison, regional rollout, or undocumented capability claims.
- Any active policy, adapter, generator, validator, runtime, or CI change.
- Models found only in announcements after the cutoff.

## Definitions / Facts

- **Cutoff disposition** states whether the row is included at the cutoff and
  whether its state is dated proof or only a mutable retrieval-time view.
- **`historical state unverified`** means an official mutable page was retrieved
  on 2026-07-10 but does not prove its exact contents at 01:00 UTC.
- **Model row** is one official catalog card/model page. A card may carry
  multiple exact endpoints when the provider presents them as one family.
- **No maturity parity**: `Active`, an unqualified OpenAI listing, Gemini
  `Stable`, `Preview`, `Experimental`, `Latest`, `Deprecated`, Claude `Legacy`,
  `Deprecated`, and `Retired` are not treated as interchangeable labels.

## Source Rules

- Use direct official pages only. Anthropic evidence uses `platform.claude.com`
  and `code.claude.com`; Google evidence uses `ai.google.dev` and the official
  Gemini CLI site.
- The required OpenAI Docs MCP tools were not exposed in this live agent
  session. Following the `openai-docs` skill fallback, OpenAI research is
  restricted to `developers.openai.com`; this is an official-web fallback, not
  Docs MCP evidence.
- The OpenAI latest-model guide was fetched before the all-models and
  deprecations pages. Model pages are linked directly from the inventory.
- Mutable retrieval state is not backdated. A dated changelog/deprecation entry
  may establish a release or transition before the cutoff; otherwise the row
  says `historical state unverified`.
- No post-cutoff announcement is included. A calendar-day entry dated before
  2026-07-10 is included, while its exact time remains unstated when the source
  gives no time of day.

## Coverage Summary

| Provider | Model rows | Provider-native lifecycle totals | Normalized lifecycle totals | Cutoff exceptions |
| --- | ---: | --- | --- | --- |
| Anthropic | 17 | Active 9; limited availability 1; Deprecated 1; Retired 6 | stable 9; deprecated 7; not normalized (limited) 1 | 13 mutable status-table rows carry `historical state unverified`; dated release/deprecation notes corroborate transitions |
| OpenAI | 93 | Listed without maturity label 45; Latest alias 1; Deprecated 47 | not normalized (listed) 45; not normalized (latest alias) 1; deprecated 47 | 46 non-deprecated listing states carry `historical state unverified`; dated changelog establishes releases but not the exact mutable listing state |
| Google | 35 | Stable 11; Preview 18; Experimental 1; Deprecated 1; Shut down 4 | stable 11; preview 18; not normalized (experimental) 1; deprecated 5 | Main catalog says last updated 2026-07-09 UTC; exact time is not shown |
| **Total** | **145** | — | stable 20; preview 18; deprecated 59; not normalized 48 | No row lacks a lifecycle or cutoff disposition |

## Cross-provider Terminology Map

| Provider-native term | Normalized lifecycle | Rule |
| --- | --- | --- |
| Claude `Active` | `stable` | Anthropic defines Active as fully supported and recommended. This does not imply Gemini GA semantics. |
| Claude limited availability | not normalized | Access scope is not a maturity term. |
| Claude `Legacy` | `deprecated` only after a deprecation notice; otherwise not normalized | Anthropic says Legacy may be deprecated later. No Legacy row is relabeled without a notice. |
| Claude `Deprecated` / `Retired` | `deprecated` | The normalized bucket means leaving/left service; provider-native state retains whether requests still work. |
| OpenAI unqualified all-models listing | not normalized | “Available” is not an official stable/GA label. |
| OpenAI `Latest` alias | not normalized | A mutable alias is version behavior, not maturity. |
| OpenAI `Deprecated` / shut down | `deprecated` | Provider-native state retains whether shutdown has occurred. |
| Gemini `Stable` | `stable` | Google explicitly defines stable model strings. |
| Gemini `Preview` | `preview` | Google explicitly defines Preview and its shorter notice boundary. |
| Gemini `Latest` | not normalized | The alias may point to stable, preview, or experimental. |
| Gemini `Experimental` | not normalized | Google explicitly says Experimental is unstable; it is not collapsed into Preview. |
| Gemini `Deprecated` / `Shut down` | `deprecated` | Provider-native state preserves endpoint availability. |

## Workspace-policy Comparison

| Tier | Stage 00 Claude value | Catalog finding | Stage 00 OpenAI/Codex value | Catalog finding | Stage 00 Gemini value | Catalog finding | Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Supervisor | `opus-4.8` (Claude Code alias `opus`) | `claude-opus-4-8` is Active; alias resolution is a Claude Code surface | `gpt-5.5` | listed without a maturity label | `gemini-3.1-pro` | Official API ID is `gemini-3.1-pro-preview`; the policy value omits provider `-preview` | Policy unchanged; Gemini value is an unsupported availability gap pending the full approved-change protocol |
| Worker | `sonnet-4.6` (Claude Code alias `sonnet`) | `claude-sonnet-4-6` is Active, although Sonnet 5 is newer | `gpt-5.4-mini` | listed without a maturity label | `gemini-3.5-flash` | Stable/GA | Policy unchanged; newer/different models do not authorize automatic replacement |
| Effort | Claude effort is provider/model specific | Opus 4.8 documents `high` default; other controls remain provider-native | supervisor `xhigh`; workers `medium`, approved `high`, formatting-only `low` | Codex config accepts a model and reasoning-effort fields; support remains model-specific | Antigravity selects model rather than a separate workspace effort field | API thinking controls are not assumed to equal Antigravity policy | Preserve distinct controls; no false parity |

## Provider Catalogs

### Anthropic / Claude

Anthropic defines `Active`, `Legacy`, `Deprecated`, and `Retired`. Its status
page is mutable and omits the newer Fable 5, Mythos 5, and Sonnet 5 rows that are
documented by dated June release notes; those releases are added from the
official changelog rather than inferred from the status table.

| Provider | Official name | Model ID / alias | Provider-native status | Normalized lifecycle | Release / cutoff evidence | Availability surfaces | Context / modalities | Reasoning control | Tool / agent / coding characteristics | Cutoff disposition | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Anthropic | Claude Fable 5 | `claude-fable-5` | generally available | stable | Released 2026-06-09; access restored 2026-07-01 | Claude API; Claude Platform on AWS; Bedrock; Google Cloud; Microsoft Foundry | 1M; text/image input, text output | adaptive thinking always on | Long-running-agent positioning; tool support is model-page specific | Included; dated before cutoff | Requires 30-day retention; no zero-data-retention support |
| Anthropic | Claude Mythos 5 | `claude-mythos-5` | limited availability | not normalized (limited) | Released 2026-06-09; access restored 2026-07-01 | Project Glasswing; approved customers | 1M; text/image input, text output | adaptive thinking always on | Defensive-cybersecurity limited offering | Included; dated before cutoff | Invitation-only; availability is not maturity |
| Anthropic | Claude Sonnet 5 | `claude-sonnet-5` | current / generally released | stable | Released 2026-06-30 | Claude API and documented partner surfaces | 1M; text/image input, text output | adaptive thinking default; manual extended thinking removed | Same documented tools/platform features as Sonnet 4.6 except Priority Tier | Included; dated before cutoff | Changelog is dated; exact release time is not shown |
| Anthropic | Claude Opus 4.8 | `claude-opus-4-8`; Claude Code `opus` | Active | stable | Released 2026-05-28; status table Active | Claude API; Claude Platform on AWS; Bedrock; Google Cloud; Microsoft Foundry; Claude Code | 1M; text/image input, text output | effort defaults `high`; adaptive thinking | Computer use; advisor; task budgets; agentic coding description | Included; dated release; status historical state unverified | Claude Code alias is a product surface, not the API ID |
| Anthropic | Claude Opus 4.7 | `claude-opus-4-7` | Active | stable | Released 2026-04-16; status table Active | Claude API and documented partner surfaces | Model page; high-resolution image input documented | `xhigh` effort documented; adaptive thinking | Agentic coding; task budgets; computer-use support documented | Included; dated release; status historical state unverified | Fast mode was deprecated 2026-06-25; model itself was not |
| Anthropic | Claude Opus 4.6 | `claude-opus-4-6` | Active | stable | Released 2026-02-05; status table Active | Claude API and documented partner surfaces | 1M GA; text/image input, text output | effort; adaptive thinking recommended | Complex agentic/long-horizon positioning | Included; dated release; status historical state unverified | Fast mode removal is not model deprecation |
| Anthropic | Claude Opus 4.5 | `claude-opus-4-5-20251101`; `claude-opus-4-5` alias | Active | stable | Status table Active | Claude API and documented partner surfaces | Model page; text/image input, text output | effort public beta at release | Professional software engineering and advanced-agent description | Included; historical state unverified | Mutable status page does not prove exact cutoff state |
| Anthropic | Claude Opus 4.1 | `claude-opus-4-1-20250805`; `claude-opus-4-1` alias | Deprecated | deprecated | Deprecated 2026-06-05; retirement 2026-08-05 | Claude API until retirement; partner schedules may differ | Not re-established for task selection | Not re-established | Do not select for new work | Included as Deprecated at cutoff | First-party dates do not govern Bedrock/Google Cloud schedules |
| Anthropic | Claude Opus 4 | `claude-opus-4-20250514`; `claude-opus-4-0` alias | Retired | deprecated | Deprecated 2026-04-14; retired 2026-06-15 | Unavailable on first-party API | — | — | Historical only | Included as Retired at cutoff | Partner schedules may differ |
| Anthropic | Claude Sonnet 4.6 | `claude-sonnet-4-6`; Claude Code `sonnet` | Active | stable | Released 2026-02-17; status table Active | Claude API; Claude Code; documented partner surfaces | 1M GA; text/image input, text output | adaptive/extended thinking documented | Agentic search; code execution, web/tool features documented | Included; dated release; status historical state unverified | Policy alias is not the API ID |
| Anthropic | Claude Sonnet 4.5 | `claude-sonnet-4-5-20250929`; `claude-sonnet-4-5` alias | Active | stable | Status table Active | Claude API and documented partner surfaces | 200k after 1M beta retirement; text/image input, text output | Model page | Tool support is model-page specific | Included; historical state unverified | Mutable status page does not prove exact cutoff state |
| Anthropic | Claude Sonnet 4 | `claude-sonnet-4-20250514`; `claude-sonnet-4-0` alias | Retired | deprecated | Deprecated 2026-04-14; retired 2026-06-15 | Unavailable on first-party API | — | — | Historical only | Included as Retired at cutoff | Partner schedules may differ |
| Anthropic | Claude Sonnet 3.7 | `claude-3-7-sonnet-20250219`; `claude-3-7-sonnet-latest` alias | Retired | deprecated | Deprecated 2025-10-28; retired 2026-02-19 | Unavailable on first-party API | — | — | Historical only | Included as Retired at cutoff | Alias retained only as historical identifier here |
| Anthropic | Claude Haiku 4.5 | `claude-haiku-4-5-20251001`; `claude-haiku-4-5` alias | Active | stable | Status table Active | Claude API and documented partner surfaces | 200k; text/image input, text output | Extended thinking documented | Fast/current Haiku; tool support is model-page specific | Included; historical state unverified | Mutable status page does not prove exact cutoff state |
| Anthropic | Claude Haiku 3.5 | `claude-3-5-haiku-20241022`; `claude-3-5-haiku-latest` alias | Retired | deprecated | Deprecated 2025-12-19; retired 2026-02-19 | Unavailable on first-party API | — | — | Historical only | Included as Retired at cutoff | — |
| Anthropic | Claude Haiku 3 | `claude-3-haiku-20240307` | Retired | deprecated | Deprecated 2026-02-19; retired 2026-04-20 | Unavailable on first-party API | — | — | Historical only | Included as Retired at cutoff | — |
| Anthropic | Claude Mythos Preview | `claude-mythos-preview` | Retired | deprecated | Preview released 2026-04-07; retired 2026-06-30 | Unavailable; replaced by limited Mythos 5 | — | — | Historical defensive-cybersecurity preview | Included as Retired at cutoff | Preview maturity and limited access were distinct |

### OpenAI / Codex

OpenAI's all-models page calls the catalog “available” but does not assign a
stable/GA status to an unqualified listing. Those rows therefore remain
`not normalized (listed)`. The page's explicit `Deprecated` label is retained.
`gpt-5.6-*` (July 9) and `gpt-realtime-2.1*` (July 6) precede the cutoff; no
later announcement is included. Exact account/Codex-surface availability is not
inferred from API documentation.

| Provider | Official name | Model ID / alias | Provider-native status | Normalized lifecycle | Release / cutoff evidence | Availability surfaces | Context / modalities | Reasoning control | Tool / agent / coding characteristics | Cutoff disposition | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OpenAI | [GPT-5.6 Sol](https://developers.openai.com/api/docs/models/gpt-5.6-sol) | `gpt-5.6-sol`; `gpt-5.6` alias | Listed; frontier | not normalized (listed) | Changelog 2026-07-09 | Responses; Chat Completions; Batch | 1M; text/image input, text output | Configurable; `max` documented | Programmatic tool calling; multi-agent beta; professional-work positioning | Included; release dated before cutoff; listing historical state unverified | Changelog gives no time of day |
| OpenAI | [GPT-5.6 Terra](https://developers.openai.com/api/docs/models/gpt-5.6-terra) | `gpt-5.6-terra` | Listed; frontier | not normalized (listed) | Changelog 2026-07-09 | Responses; Chat Completions; Batch | Model page; text/image input, text output | Configurable | GPT-5.6 tool/coding family; balance positioning | Included; release dated before cutoff; listing historical state unverified | No benchmark or account availability inferred |
| OpenAI | [GPT-5.6 Luna](https://developers.openai.com/api/docs/models/gpt-5.6-luna) | `gpt-5.6-luna` | Listed; frontier | not normalized (listed) | Changelog 2026-07-09 | Responses; Chat Completions; Batch | Model page; text/image input, text output | Configurable | GPT-5.6 family; high-volume positioning | Included; release dated before cutoff; listing historical state unverified | No price claim carried forward |
| OpenAI | [GPT-5.5](https://developers.openai.com/api/docs/models/gpt-5.5) | `gpt-5.5` | Listed; frontier | not normalized (listed) | Released 2026-04-24 | Responses; Chat Completions | 1M; text/image input, text output | Defaults `medium` per changelog | Structured outputs, function calling, tools, computer use, shell, apply patch, skills, MCP, web search | Included; listing historical state unverified | API listing does not prove Codex entitlement |
| OpenAI | [GPT-5.5 Pro](https://developers.openai.com/api/docs/models/gpt-5.5-pro) | `gpt-5.5-pro` | Listed; frontier | not normalized (listed) | All-models and model page | Responses | Model page | Pro-mode control is provider-native | Higher-compute GPT-5.5 variant | Included; historical state unverified | No benchmark superiority asserted |
| OpenAI | [GPT-5.4](https://developers.openai.com/api/docs/models/gpt-5.4) | `gpt-5.4` | Listed; frontier | not normalized (listed) | Released 2026-03-05 | Responses; Chat Completions | 1M; multimodal input documented | Configurable | Tool search, computer use, compaction; coding/professional-work positioning | Included; release before cutoff; listing historical state unverified | — |
| OpenAI | [GPT-5.4 Pro](https://developers.openai.com/api/docs/models/gpt-5.4-pro) | `gpt-5.4-pro` | Listed; frontier | not normalized (listed) | Released 2026-03-05 | Responses | Model page | Pro variant | Tougher-problem positioning | Included; release before cutoff; listing historical state unverified | — |
| OpenAI | [GPT-5.4 mini](https://developers.openai.com/api/docs/models/gpt-5.4-mini) | `gpt-5.4-mini` | Listed; frontier | not normalized (listed) | Released 2026-03-17 | Responses; Chat Completions | Model page | Model-specific | Tool search, computer use, compaction; coding and subagent positioning | Included; release before cutoff; listing historical state unverified | Workspace Worker value; availability not locally proven |
| OpenAI | [GPT-5.4 nano](https://developers.openai.com/api/docs/models/gpt-5.4-nano) | `gpt-5.4-nano` | Listed; frontier | not normalized (listed) | Released 2026-03-17 | Responses; Chat Completions | Model page | Model-specific | Compaction; simple high-volume positioning; no tool search/computer use per changelog | Included; release before cutoff; listing historical state unverified | — |
| OpenAI | [GPT Image 2](https://developers.openai.com/api/docs/models/gpt-image-2) | `gpt-image-2` | Listed; image | not normalized (listed) | Released 2026-04-21 | Images; Batch | Text/image input; image output | Not a reasoning-selection control | Image generation and editing | Included; release before cutoff; listing historical state unverified | — |
| OpenAI | [GPT Image 1.5](https://developers.openai.com/api/docs/models/gpt-image-1.5) | `gpt-image-1.5` | Deprecated | deprecated | Deprecated 2026-06-02; shutdown 2026-12-01 | Images until shutdown | Text/image input; image output | — | Previous image generation/editing | Included as Deprecated at cutoff | Replacement `gpt-image-2` |
| OpenAI | [chatgpt-image-latest](https://developers.openai.com/api/docs/models/chatgpt-image-latest) | `chatgpt-image-latest` | Deprecated; mutable alias | deprecated | Deprecated 2026-06-02; shutdown 2026-12-01 | Images until shutdown | Text/image input; image output | — | Previous ChatGPT image model | Included as Deprecated at cutoff | `latest` does not mean stable |
| OpenAI | [GPT Image 1](https://developers.openai.com/api/docs/models/gpt-image-1) | `gpt-image-1` | Deprecated | deprecated | All-models label; shutdown path documented | Images | Text/image input; image output | — | Previous image generation/editing | Included as Deprecated; exact alias state historical state unverified | Snapshot schedule may differ from alias label |
| OpenAI | [gpt-image-1-mini](https://developers.openai.com/api/docs/models/gpt-image-1-mini) | `gpt-image-1-mini` | Deprecated | deprecated | Deprecated 2026-06-02; shutdown 2026-12-01 | Images until shutdown | Text/image input; image output | — | Cost-efficient previous image variant | Included as Deprecated at cutoff | Replacement `gpt-image-2` |
| OpenAI | [DALL·E 3](https://developers.openai.com/api/docs/models/dall-e-3) | `dall-e-3` | Deprecated; shut down | deprecated | Shut down 2026-05-12 | Unavailable | Text input; image output | — | Historical image generation | Included as shut down at cutoff | All-models retains Deprecated card |
| OpenAI | [DALL·E 2](https://developers.openai.com/api/docs/models/dall-e-2) | `dall-e-2` | Deprecated; shut down | deprecated | Shut down 2026-05-12 | Unavailable | Text/image input; image output | — | Historical image generation/editing | Included as shut down at cutoff | All-models retains Deprecated card |
| OpenAI | [GPT-Realtime-2.1](https://developers.openai.com/api/docs/models/gpt-realtime-2.1) | `gpt-realtime-2.1` | Listed; realtime/audio | not normalized (listed) | Released 2026-07-06 | Realtime API | Realtime text/audio | Configurable reasoning documented | Tool use; realtime voice | Included; release before cutoff; listing historical state unverified | — |
| OpenAI | [GPT-Realtime-2.1 mini](https://developers.openai.com/api/docs/models/gpt-realtime-2.1-mini) | `gpt-realtime-2.1-mini` | Listed; realtime/audio | not normalized (listed) | Released 2026-07-06 | Realtime API | Realtime text/audio | Reasoning model | Lower-latency realtime voice positioning | Included; release before cutoff; listing historical state unverified | — |
| OpenAI | [GPT-Realtime-2](https://developers.openai.com/api/docs/models/gpt-realtime-2) | `gpt-realtime-2` | Listed; realtime/audio | not normalized (listed) | Released 2026-05-07 | Realtime API | Realtime text/audio | Configurable reasoning | Speech-to-speech agents | Included; release before cutoff; listing historical state unverified | — |
| OpenAI | [GPT-Realtime-Translate](https://developers.openai.com/api/docs/models/gpt-realtime-translate) | `gpt-realtime-translate` | Listed; realtime/audio | not normalized (listed) | Released 2026-05-07 | Realtime translation | Streaming speech in/out | — | Streaming speech translation | Included; release before cutoff; listing historical state unverified | Specialized model, not a general worker |
| OpenAI | [GPT-Realtime-Whisper](https://developers.openai.com/api/docs/models/gpt-realtime-whisper) | `gpt-realtime-whisper` | Listed; realtime/audio | not normalized (listed) | Released 2026-05-07 | Realtime transcription | Streaming audio input; text output | — | Streaming speech-to-text | Included; release before cutoff; listing historical state unverified | — |
| OpenAI | [GPT-Realtime-1.5](https://developers.openai.com/api/docs/models/gpt-realtime-1.5) | `gpt-realtime-1.5` | Listed; realtime/audio | not normalized (listed) | Released 2026-02-23 | Realtime API | Text/audio input and output | Model page | Voice workflows | Included; release before cutoff; listing historical state unverified | — |
| OpenAI | [GPT-Realtime](https://developers.openai.com/api/docs/models/gpt-realtime) | `gpt-realtime` | Listed; realtime/audio | not normalized (listed) | All-models and model page | Realtime API | Text/audio input and output | Model page | Realtime model | Included; historical state unverified | Mutable alias behavior not treated as maturity |
| OpenAI | [gpt-audio-1.5](https://developers.openai.com/api/docs/models/gpt-audio-1.5) | `gpt-audio-1.5` | Listed; audio | not normalized (listed) | Released 2026-02-23 | Chat Completions | Audio/text input and output | Model page | Voice model | Included; release before cutoff; listing historical state unverified | — |
| OpenAI | [gpt-audio](https://developers.openai.com/api/docs/models/gpt-audio) | `gpt-audio` | Listed; audio | not normalized (listed) | All-models and model page | Chat Completions | Audio/text input and output | Model page | Audio workflows | Included; historical state unverified | Mutable listing does not prove exact cutoff state |
| OpenAI | [GPT-4o Transcribe](https://developers.openai.com/api/docs/models/gpt-4o-transcribe) | `gpt-4o-transcribe` | Listed; transcription | not normalized (listed) | All-models and model page | Audio/transcription API surfaces | Audio input; text output | — | Speech-to-text | Included; historical state unverified | — |
| OpenAI | [GPT-4o mini Transcribe](https://developers.openai.com/api/docs/models/gpt-4o-mini-transcribe) | `gpt-4o-mini-transcribe` | Listed; transcription | not normalized (listed) | All-models and model page | Audio/transcription API surfaces | Audio input; text output | — | Speech-to-text | Included; historical state unverified | Alias snapshot may change |
| OpenAI | [GPT-4o Transcribe Diarize](https://developers.openai.com/api/docs/models/gpt-4o-transcribe-diarize) | `gpt-4o-transcribe-diarize` | Listed; transcription | not normalized (listed) | All-models and model page | Transcription | Audio input; diarized text output | — | Speaker diarization | Included; historical state unverified | — |
| OpenAI | [TTS-1](https://developers.openai.com/api/docs/models/tts-1) | `tts-1` | Listed; speech | not normalized (listed) | All-models and model page | Speech API | Text input; audio output | — | Text-to-speech, speed positioning | Included; historical state unverified | — |
| OpenAI | [TTS-1 HD](https://developers.openai.com/api/docs/models/tts-1-hd) | `tts-1-hd` | Listed; speech | not normalized (listed) | All-models and model page | Speech API | Text input; audio output | — | Text-to-speech, quality positioning | Included; historical state unverified | — |
| OpenAI | [Whisper](https://developers.openai.com/api/docs/models/whisper-1) | `whisper-1` | Listed; transcription | not normalized (listed) | All-models and model page | Audio API | Audio input; text output | — | General speech recognition | Included; historical state unverified | — |
| OpenAI | [GPT-Realtime mini](https://developers.openai.com/api/docs/models/gpt-realtime-mini) | `gpt-realtime-mini` | Listed; realtime/audio | not normalized (listed) | Current alias listed; older snapshot deprecation documented | Realtime API | Text/audio input and output | Model page | Cost-efficient realtime | Included; historical state unverified | Do not transfer deprecated snapshot status to current alias |
| OpenAI | [gpt-audio-mini](https://developers.openai.com/api/docs/models/gpt-audio-mini) | `gpt-audio-mini` | Deprecated | deprecated | All-models label; older snapshot shutdown 2026-07-23 | Chat Completions until applicable shutdown | Audio/text input and output | — | Previous small audio model | Included as Deprecated at cutoff | Alias/snapshot schedule is page-specific |
| OpenAI | [GPT-4o Audio](https://developers.openai.com/api/docs/models/gpt-4o-audio-preview) | `gpt-4o-audio-preview` | Deprecated; shut down | deprecated | Shut down 2026-05-07 | Unavailable | Audio/text input and output | — | Historical audio preview | Included as shut down at cutoff | — |
| OpenAI | [GPT-4o mini Audio](https://developers.openai.com/api/docs/models/gpt-4o-mini-audio-preview) | `gpt-4o-mini-audio-preview` | Deprecated; shut down | deprecated | Shut down 2026-05-07 | Unavailable | Audio/text input and output | — | Historical audio preview | Included as shut down at cutoff | — |
| OpenAI | [GPT-4o Realtime](https://developers.openai.com/api/docs/models/gpt-4o-realtime-preview) | `gpt-4o-realtime-preview` | Deprecated; shut down | deprecated | Shut down 2026-05-07 | Unavailable | Realtime text/audio | — | Historical realtime preview | Included as shut down at cutoff | — |
| OpenAI | [GPT-4o mini Realtime](https://developers.openai.com/api/docs/models/gpt-4o-mini-realtime-preview) | `gpt-4o-mini-realtime-preview` | Deprecated; shut down | deprecated | Shut down 2026-05-07 | Unavailable | Realtime text/audio | — | Historical realtime preview | Included as shut down at cutoff | — |
| OpenAI | [GPT-4o mini TTS](https://developers.openai.com/api/docs/models/gpt-4o-mini-tts) | `gpt-4o-mini-tts` | Deprecated | deprecated | All-models label; 2025-03-20 snapshot shutdown 2026-07-23 | Speech API | Text input; audio output | — | Previous text-to-speech model | Included as Deprecated at cutoff | Current alias and dated snapshot must not be conflated |
| OpenAI | [gpt-oss-120b](https://developers.openai.com/api/docs/models/gpt-oss-120b) | `gpt-oss-120b` | Listed; open-weight | not normalized (listed) | All-models and model page | Self-hosted/open-weight distribution | Model page | Reasoning model family | Open-weight model | Included; historical state unverified | API availability is not implied by open weights |
| OpenAI | [gpt-oss-20b](https://developers.openai.com/api/docs/models/gpt-oss-20b) | `gpt-oss-20b` | Listed; open-weight | not normalized (listed) | All-models and model page | Self-hosted/open-weight distribution | Model page | Reasoning model family | Lower-latency open-weight positioning | Included; historical state unverified | — |
| OpenAI | [text-embedding-3-large](https://developers.openai.com/api/docs/models/text-embedding-3-large) | `text-embedding-3-large` | Listed; embedding | not normalized (listed) | All-models and model page | Embeddings API | Text input; vector output | — | Embeddings | Included; historical state unverified | Not a generative agent model |
| OpenAI | [text-embedding-3-small](https://developers.openai.com/api/docs/models/text-embedding-3-small) | `text-embedding-3-small` | Listed; embedding | not normalized (listed) | All-models and model page | Embeddings API | Text input; vector output | — | Embeddings | Included; historical state unverified | Not a generative agent model |
| OpenAI | [text-embedding-ada-002](https://developers.openai.com/api/docs/models/text-embedding-ada-002) | `text-embedding-ada-002` | Listed; older embedding | not normalized (listed) | All-models and model page | Embeddings API | Text input; vector output | — | Embeddings | Included; historical state unverified | “Older” is a description, not a deprecation label |
| OpenAI | [GPT-5.3-Codex](https://developers.openai.com/api/docs/models/gpt-5.3-codex) | `gpt-5.3-codex` | Listed | not normalized (listed) | Released 2026-02-24 | Responses API | Model page | Model-specific | Agentic coding | Included; release before cutoff; listing historical state unverified | API model listing does not prove Codex product entitlement |
| OpenAI | [GPT-5.2](https://developers.openai.com/api/docs/models/gpt-5.2) | `gpt-5.2` | Listed; previous frontier | not normalized (listed) | Released 2025-12-11 | Responses; Chat Completions | Multimodal/model page | Configurable; `xhigh` introduced | Coding, tool calling, context management | Included; release before cutoff; listing historical state unverified | — |
| OpenAI | [GPT-5.2 Pro](https://developers.openai.com/api/docs/models/gpt-5.2-pro) | `gpt-5.2-pro` | Listed; previous pro | not normalized (listed) | All-models and model page | Responses | Model page | Pro variant | Professional-work positioning | Included; historical state unverified | — |
| OpenAI | [GPT-5.1](https://developers.openai.com/api/docs/models/gpt-5.1) | `gpt-5.1` | Listed | not normalized (listed) | Released 2025-11-13 | Responses; Chat Completions | Model page | Configurable; provider documented default at release | Coding and agentic-workflow positioning | Included; release before cutoff; listing historical state unverified | — |
| OpenAI | [GPT-5](https://developers.openai.com/api/docs/models/gpt-5) | `gpt-5` | Listed; previous | not normalized (listed) | All-models and model page | Responses; Chat Completions | Model page | Configurable | Coding and agentic tasks | Included; historical state unverified | Dated original snapshot is separately Deprecated |
| OpenAI | [GPT-5 mini](https://developers.openai.com/api/docs/models/gpt-5-mini) | `gpt-5-mini` | Listed | not normalized (listed) | All-models and model page | Responses; Chat Completions | Model page | Model-specific | High-volume/cost-sensitive positioning | Included; historical state unverified | Dated original snapshot is separately Deprecated |
| OpenAI | [GPT-5 nano](https://developers.openai.com/api/docs/models/gpt-5-nano) | `gpt-5-nano` | Listed | not normalized (listed) | All-models and model page | Responses; Chat Completions | Model page | Model-specific | Fast/high-volume positioning | Included; historical state unverified | Dated original snapshot is separately Deprecated |
| OpenAI | [GPT-5 Pro](https://developers.openai.com/api/docs/models/gpt-5-pro) | `gpt-5-pro` | Listed | not normalized (listed) | Released 2025-10-06 | Responses | Model page | Pro variant | Higher-compute GPT-5 variant | Included; release before cutoff; listing historical state unverified | Dated original snapshot is separately Deprecated |
| OpenAI | [o3-pro](https://developers.openai.com/api/docs/models/o3-pro) | `o3-pro` | Listed | not normalized (listed) | All-models and model page | Responses | Model page | Reasoning model | Higher-compute o3 variant | Included; historical state unverified | Dated snapshot is separately Deprecated |
| OpenAI | [o3](https://developers.openai.com/api/docs/models/o3) | `o3` | Listed; succeeded by GPT-5 | not normalized (listed) | All-models and model page | Responses | Model page | Reasoning model | Complex-task positioning | Included; historical state unverified | Dated snapshot is separately Deprecated |
| OpenAI | [GPT-4.1](https://developers.openai.com/api/docs/models/gpt-4.1) | `gpt-4.1` | Listed | not normalized (listed) | All-models and model page | Responses; Chat Completions | Model page | Non-reasoning description | General model | Included; historical state unverified | — |
| OpenAI | [GPT-4.1 mini](https://developers.openai.com/api/docs/models/gpt-4.1-mini) | `gpt-4.1-mini` | Listed | not normalized (listed) | All-models and model page | Responses; Chat Completions | Model page | Non-reasoning description | Smaller/faster variant | Included; historical state unverified | — |
| OpenAI | [omni-moderation](https://developers.openai.com/api/docs/models/omni-moderation-latest) | `omni-moderation-latest` | Listed; moderation | not normalized (listed) | All-models and model page | Moderations API | Text/image input; classification output | — | Safety classification | Included; historical state unverified | Mutable `latest` suffix is not maturity |
| OpenAI | [GPT-4o mini](https://developers.openai.com/api/docs/models/gpt-4o-mini) | `gpt-4o-mini` | Listed | not normalized (listed) | All-models and model page | Responses; Chat Completions | Model page | Model-specific | Focused-task positioning | Included; historical state unverified | — |
| OpenAI | [GPT-5.3 Chat](https://developers.openai.com/api/docs/models/gpt-5.3-chat-latest) | `gpt-5.3-chat-latest` | Deprecated | deprecated | Deprecated 2026-05-08; shutdown 2026-08-10 | API until shutdown | Model page | Model-specific | ChatGPT snapshot | Included as Deprecated at cutoff | `latest` is a mutable alias |
| OpenAI | [GPT-5.2 Chat](https://developers.openai.com/api/docs/models/gpt-5.2-chat-latest) | `gpt-5.2-chat-latest` | Deprecated | deprecated | Deprecated 2026-05-08; shutdown 2026-08-10 | API until shutdown | Model page | Model-specific | ChatGPT snapshot | Included as Deprecated at cutoff | `latest` is a mutable alias |
| OpenAI | [GPT-5.2-Codex](https://developers.openai.com/api/docs/models/gpt-5.2-codex) | `gpt-5.2-codex` | Deprecated | deprecated | Deprecated 2026-04-22; shutdown 2026-07-23 | Responses until shutdown | Model page | Model-specific | Long-horizon agentic coding | Included as Deprecated at cutoff | — |
| OpenAI | [Sora 2](https://developers.openai.com/api/docs/models/sora-2) | `sora-2` | Deprecated | deprecated | Deprecated 2026-03-24; shutdown 2026-09-24 | Videos API until shutdown | Text/image input; video/audio output per model page | — | Video generation | Included as Deprecated at cutoff | No recommended replacement listed |
| OpenAI | [Sora 2 Pro](https://developers.openai.com/api/docs/models/sora-2-pro) | `sora-2-pro` | Deprecated | deprecated | Deprecated 2026-03-24; shutdown 2026-09-24 | Videos API until shutdown | Text/image input; video/audio output per model page | — | Video generation | Included as Deprecated at cutoff | No recommended replacement listed |
| OpenAI | [o3-deep-research](https://developers.openai.com/api/docs/models/o3-deep-research) | `o3-deep-research` | Deprecated | deprecated | Deprecated 2026-04-22; shutdown 2026-07-23 | API until shutdown | Model page | Reasoning model | Deep-research specialization | Included as Deprecated at cutoff | — |
| OpenAI | [o4-mini-deep-research](https://developers.openai.com/api/docs/models/o4-mini-deep-research) | `o4-mini-deep-research` | Deprecated | deprecated | Deprecated 2026-04-22; shutdown 2026-07-23 | API until shutdown | Model page | Reasoning model | Deep-research specialization | Included as Deprecated at cutoff | — |
| OpenAI | [GPT-4.1 nano](https://developers.openai.com/api/docs/models/gpt-4.1-nano) | `gpt-4.1-nano` | Deprecated | deprecated | Deprecated 2026-04-22; shutdown 2026-10-23 | API until shutdown | Model page | Non-reasoning description | Small general model | Included as Deprecated at cutoff | — |
| OpenAI | [o4-mini](https://developers.openai.com/api/docs/models/o4-mini) | `o4-mini` | Deprecated | deprecated | Deprecated 2026-04-22; shutdown 2026-10-23 | API until shutdown | Model page | Reasoning model | Previous small reasoning model | Included as Deprecated at cutoff | — |
| OpenAI | [o1-pro](https://developers.openai.com/api/docs/models/o1-pro) | `o1-pro` | Deprecated | deprecated | Deprecated 2026-04-22; shutdown 2026-10-23 | API until shutdown | Model page | Reasoning model | Previous higher-compute o1 | Included as Deprecated at cutoff | — |
| OpenAI | [computer-use-preview](https://developers.openai.com/api/docs/models/computer-use-preview) | `computer-use-preview` | Deprecated | deprecated | Deprecated 2026-04-22; shutdown 2026-07-23 | Responses until shutdown | Screenshot/image interaction | Model page | Computer-use specialization | Included as Deprecated at cutoff | `preview` name plus Deprecated current state |
| OpenAI | [GPT-4o mini Search Preview](https://developers.openai.com/api/docs/models/gpt-4o-mini-search-preview) | `gpt-4o-mini-search-preview` | Deprecated | deprecated | Deprecated 2026-04-22; shutdown 2026-07-23 | Chat Completions until shutdown | Model page | — | Web-search specialization | Included as Deprecated at cutoff | — |
| OpenAI | [GPT-4o Search Preview](https://developers.openai.com/api/docs/models/gpt-4o-search-preview) | `gpt-4o-search-preview` | Deprecated | deprecated | Deprecated 2026-04-22; shutdown 2026-07-23 | Chat Completions until shutdown | Model page | — | Web-search specialization | Included as Deprecated at cutoff | — |
| OpenAI | [GPT-4.5 Preview](https://developers.openai.com/api/docs/models/gpt-4.5-preview) | `gpt-4.5-preview` | Deprecated; shut down | deprecated | Deprecated 2025-04-14; shut down 2025-07-14 | Unavailable | Model page | — | Historical preview | Included as shut down at cutoff | — |
| OpenAI | [o3-mini](https://developers.openai.com/api/docs/models/o3-mini) | `o3-mini` | Deprecated | deprecated | Deprecated 2026-04-22; shutdown 2026-10-23 | API until shutdown | Model page | Reasoning model | Previous small reasoning model | Included as Deprecated at cutoff | — |
| OpenAI | [o1](https://developers.openai.com/api/docs/models/o1) | `o1` | Deprecated | deprecated | Deprecated 2026-04-22; shutdown 2026-10-23 | API until shutdown | Model page | Reasoning model | Previous o-series model | Included as Deprecated at cutoff | — |
| OpenAI | [o1-mini](https://developers.openai.com/api/docs/models/o1-mini) | `o1-mini` | Deprecated; shut down | deprecated | Shut down 2025-10-27 | Unavailable | Model page | Reasoning model | Historical small reasoning model | Included as shut down at cutoff | — |
| OpenAI | [o1 Preview](https://developers.openai.com/api/docs/models/o1-preview) | `o1-preview` | Deprecated; shut down | deprecated | Shut down 2025-07-28 | Unavailable | Model page | Reasoning model | Historical reasoning preview | Included as shut down at cutoff | — |
| OpenAI | [GPT-4o](https://developers.openai.com/api/docs/models/gpt-4o) | `gpt-4o` | Deprecated | deprecated | All-models label; dated snapshot shutdown 2026-10-23 | API subject to alias/snapshot schedule | Model page | Model-specific | Previous general model | Included as Deprecated; exact alias state historical state unverified | Snapshot and alias schedules differ |
| OpenAI | [GPT-4 Turbo](https://developers.openai.com/api/docs/models/gpt-4-turbo) | `gpt-4-turbo` | Deprecated | deprecated | Deprecated 2026-04-22; shutdown 2026-10-23 | API until shutdown | Model page | — | Previous general model | Included as Deprecated at cutoff | — |
| OpenAI | [babbage-002](https://developers.openai.com/api/docs/models/babbage-002) | `babbage-002` | Deprecated | deprecated | Deprecated 2025-09-26; shutdown 2026-09-28 | API until shutdown | Text | — | Base model | Included as Deprecated at cutoff | Fine-tuning training had an earlier separate transition |
| OpenAI | [ChatGPT-4o](https://developers.openai.com/api/docs/models/chatgpt-4o-latest) | `chatgpt-4o-latest` | Deprecated; shut down | deprecated | Shut down 2026-02-17 | Unavailable | Model page | — | Historical ChatGPT snapshot | Included as shut down at cutoff | `latest` historical identifier |
| OpenAI | [GPT-5.1-Codex](https://developers.openai.com/api/docs/models/gpt-5.1-codex) | `gpt-5.1-codex` | Deprecated | deprecated | Deprecated 2026-04-22; shutdown 2026-07-23 | Responses until shutdown | Model page | Model-specific | Agentic coding | Included as Deprecated at cutoff | — |
| OpenAI | [GPT-5.1-Codex-Max](https://developers.openai.com/api/docs/models/gpt-5.1-codex-max) | `gpt-5.1-codex-max` | Deprecated | deprecated | Deprecated 2026-04-22; shutdown 2026-07-23 | Responses until shutdown | Model page | Model-specific | Long-running agentic coding | Included as Deprecated at cutoff | — |
| OpenAI | [GPT-5.1-Codex mini](https://developers.openai.com/api/docs/models/gpt-5.1-codex-mini) | `gpt-5.1-codex-mini` | Deprecated | deprecated | Deprecated 2026-04-22; shutdown 2026-07-23 | Responses until shutdown | Model page | Model-specific | Smaller coding variant | Included as Deprecated at cutoff | — |
| OpenAI | [GPT-5-Codex](https://developers.openai.com/api/docs/models/gpt-5-codex) | `gpt-5-codex` | Deprecated | deprecated | Deprecated 2026-04-22; shutdown 2026-07-23 | Responses until shutdown | Model page | Model-specific | Agentic coding | Included as Deprecated at cutoff | — |
| OpenAI | [codex-mini-latest](https://developers.openai.com/api/docs/models/codex-mini-latest) | `codex-mini-latest` | Deprecated; shut down | deprecated | Shut down 2026-02-12 | Unavailable | Model page | Reasoning model | Historical Codex CLI model | Included as shut down at cutoff | Legacy local-shell support ended with model |
| OpenAI | [davinci-002](https://developers.openai.com/api/docs/models/davinci-002) | `davinci-002` | Deprecated | deprecated | Deprecated 2025-09-26; shutdown 2026-09-28 | API until shutdown | Text | — | Base model | Included as Deprecated at cutoff | Fine-tuning training had an earlier separate transition |
| OpenAI | [GPT-3.5 Turbo](https://developers.openai.com/api/docs/models/gpt-3.5-turbo) | `gpt-3.5-turbo` | Deprecated | deprecated | Deprecated snapshots; shutdown dates vary | API subject to snapshot schedule | Text | — | Legacy chat model | Included as Deprecated; exact alias state historical state unverified | Preserve snapshot-specific schedules |
| OpenAI | [GPT-4](https://developers.openai.com/api/docs/models/gpt-4) | `gpt-4` | Deprecated | deprecated | Deprecated 2026-04-22; shutdown 2026-10-23 | API until shutdown | Model page | — | Previous general model | Included as Deprecated at cutoff | — |
| OpenAI | [GPT-4 Turbo Preview](https://developers.openai.com/api/docs/models/gpt-4-turbo-preview) | `gpt-4-turbo-preview` | Deprecated; shut down | deprecated | Snapshot shut down 2026-03-26 | Unavailable | Model page | — | Historical preview | Included as shut down at cutoff | Alias pointed to a dated snapshot |
| OpenAI | [GPT-5.1 Chat](https://developers.openai.com/api/docs/models/gpt-5.1-chat-latest) | `gpt-5.1-chat-latest` | Deprecated | deprecated | Deprecated 2026-04-22; shutdown 2026-07-23 | API until shutdown | Model page | Model-specific | ChatGPT snapshot | Included as Deprecated at cutoff | `latest` historical identifier |
| OpenAI | [GPT-5 Chat](https://developers.openai.com/api/docs/models/gpt-5-chat-latest) | `gpt-5-chat-latest` | Deprecated | deprecated | Deprecated 2026-04-22; shutdown 2026-07-23 | API until shutdown | Model page | Model-specific | ChatGPT snapshot | Included as Deprecated at cutoff | `latest` historical identifier |
| OpenAI | [text-moderation](https://developers.openai.com/api/docs/models/text-moderation-latest) | `text-moderation-latest`; `text-moderation-007` | Deprecated; shut down | deprecated | Shut down 2025-10-27 | Unavailable | Text input; classification output | — | Historical moderation | Included as shut down at cutoff | — |
| OpenAI | [text-moderation-stable](https://developers.openai.com/api/docs/models/text-moderation-stable) | `text-moderation-stable` | Deprecated; shut down | deprecated | Shut down 2025-10-27 | Unavailable | Text input; classification output | — | Historical moderation | Included as shut down at cutoff | Provider-native `stable` in ID does not override Deprecated state |
| OpenAI | [Chat Latest](https://developers.openai.com/api/docs/models/chat-latest) | `chat-latest` | Latest alias; ChatGPT model | not normalized (latest alias) | All-models mutable alias | ChatGPT-oriented; not recommended for API use | Model behind alias may change | Model-specific | Chat-oriented | Included; historical state unverified | Mutable alias; not a stable model ID |

### Google / Gemini

Google defines `Stable`, `Preview`, `Latest`, and `Experimental`, and separately
tracks deprecation/shutdown. The catalog reports “Last updated 2026-07-09 UTC,”
which is before the cutoff date but does not expose the update time. The table
uses one row per official catalog card; exact endpoints are grouped only where
the official model card groups them.

| Provider | Official name | Model ID / alias | Provider-native status | Normalized lifecycle | Release / cutoff evidence | Availability surfaces | Context / modalities | Reasoning control | Tool / agent / coding characteristics | Cutoff disposition | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Google | [Gemini 3.5 Flash](https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash) | `gemini-3.5-flash`; `gemini-flash-latest` points here | Stable / GA | stable | Released 2026-05-19; model page updated 2026-06-24 | Gemini API; AI Studio; Gemini CLI subject to its auth/surface | 1,048,576 input; text/image/video/audio/PDF in, text out | Thinking supported | Code execution, function calling, search, file search, computer use Preview; agentic/coding positioning | Included; dated before cutoff | `latest` alias is mutable even though target is Stable |
| Google | [Gemini 3.1 Flash-Lite](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-lite) | `gemini-3.1-flash-lite` | Stable / GA | stable | Released 2026-05-07 | Gemini API; AI Studio | 1,048,576 input; text/image/video/audio/PDF in, text out | Thinking supported | Code execution, function calling, search, file search; lightweight-agentic positioning | Included; dated before cutoff | Shutdown date 2027-05-07 is listed separately |
| Google | [Nano Banana 2 / Gemini 3.1 Flash Image](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-image) | `gemini-3.1-flash-image` | Stable / GA | stable | Released 2026-05-28 | Gemini API; AI Studio | Multimodal input; image output | Model-page specific | Image generation and editing | Included; dated before cutoff | Family marketing name is not an alias string |
| Google | [Nano Banana 2 Lite / Gemini 3.1 Flash Lite Image](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-lite-image) | `gemini-3.1-flash-lite-image` | Stable / GA | stable | Released 2026-06-30 | Gemini API; AI Studio | Multimodal input; image output | Model-page specific | Low-latency image generation/editing | Included; dated before cutoff | — |
| Google | [Nano Banana Pro / Gemini 3 Pro Image](https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-image) | `gemini-3-pro-image` | Stable / GA | stable | Released 2026-05-28 | Gemini API; AI Studio | Multimodal input; image output | Reasoning core described | Contextual image generation/editing | Included; dated before cutoff | — |
| Google | [Gemini 3.1 Pro](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-pro-preview) | `gemini-3.1-pro-preview`; `gemini-3.1-pro-preview-customtools` | Preview | preview | Released 2026-02-19 | Gemini API; AI Studio | Model page; multimodal | Thinking/model-page controls | Complex problem solving, agentic and coding; custom-tools endpoint documented | Included; dated before cutoff | Workspace `gemini-3.1-pro` omits required `-preview` |
| Google | [Gemini 3 Flash](https://ai.google.dev/gemini-api/docs/models/gemini-3-flash-preview) | `gemini-3-flash-preview` | Preview | preview | Released 2025-12-17 | Gemini API; AI Studio | Model page; multimodal | Thinking/model-page controls | Agentic coding and multimodal tool features | Included; dated before cutoff | Replacement target is Stable `gemini-3.5-flash` |
| Google | [Gemini 3.5 Live Translate](https://ai.google.dev/gemini-api/docs/models/gemini-3.5-live-translate-preview) | `gemini-3.5-live-translate-preview` | Preview | preview | Catalog updated 2026-07-09 UTC | Live API | Realtime speech input/output | — | Streaming speech translation | Included; catalog update before cutoff date | Exact update time is not shown |
| Google | [Gemini 3.1 Flash Live](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-live-preview) | `gemini-3.1-flash-live-preview` | Preview | preview | Released 2026-03-26 | Live API | Realtime audio-to-audio | Model-page specific | Voice-first dialogue; tool use per Live API | Included; dated before cutoff | — |
| Google | [Gemini 3.1 Flash TTS](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-tts-preview) | `gemini-3.1-flash-tts-preview` | Preview | preview | Released 2026-04-15 | Gemini API speech generation | Text input; audio output | — | Expressive/steerable speech | Included; dated before cutoff | — |
| Google | [Gemini Omni Flash](https://ai.google.dev/gemini-api/docs/models/gemini-omni-flash) | `gemini-omni-flash-preview` | Preview | preview | Released 2026-06-30; page updated 2026-06-30 | Interactions API | 1,048,576 context; text/image/video in, video out | — | Conversational video generation/editing | Included; dated before cutoff | Specialized media model, not a general worker |
| Google | [Gemini 2.5 Flash](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash) | `gemini-2.5-flash` | Stable; shutdown scheduled 2026-10-16 | stable | Released 2025-06-17 | Gemini API; AI Studio | Model page; multimodal | Thinking supported | Low-latency/high-volume reasoning | Included at cutoff | Stable maturity and scheduled lifecycle end coexist |
| Google | [Nano Banana / Gemini 2.5 Flash Image](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-image) | `gemini-2.5-flash-image` | Stable; shutdown scheduled 2026-10-02 | stable | Released 2025-10-02 | Gemini API; AI Studio | Multimodal input; image output | Model-page specific | Image generation/editing | Included at cutoff | Stable maturity and scheduled lifecycle end coexist |
| Google | [Gemini 2.5 Flash Live](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-native-audio-preview-12-2025) | `gemini-2.5-flash-native-audio-preview-12-2025` | Preview | preview | Released 2025-12-12 | Live API | Realtime native audio | Model-page specific | Conversational agents; function calling | Included at cutoff | Deprecation table recommends 3.1 Flash Live but gives no shutdown date |
| Google | [Gemini 2.5 Flash TTS](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-preview-tts) | `gemini-2.5-flash-preview-tts` | Preview | preview | Released 2025-05-20 | Gemini API speech generation | Text input; audio output | — | Low-latency speech generation | Included at cutoff | No shutdown date announced |
| Google | [Gemini 2.5 Flash-Lite](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-lite) | `gemini-2.5-flash-lite` | Stable; shutdown scheduled 2026-10-16 | stable | Released 2025-07-22 | Gemini API; AI Studio | Model page; multimodal | Model-page specific | Fast/budget-friendly multimodal positioning | Included at cutoff | Stable maturity and scheduled lifecycle end coexist |
| Google | [Gemini 2.5 Pro](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-pro) | `gemini-2.5-pro` | Stable; shutdown scheduled 2026-10-16 | stable | Released 2025-06-17 | Gemini API; AI Studio | Model page; multimodal | Deep reasoning described | Complex tasks and coding | Included at cutoff | Stable maturity and scheduled lifecycle end coexist |
| Google | [Gemini 2.5 Pro TTS](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-pro-preview-tts) | `gemini-2.5-pro-preview-tts` | Preview | preview | Released 2025-05-20 | Gemini API speech generation | Text input; audio output | — | High-fidelity structured speech generation | Included at cutoff | No shutdown date announced |
| Google | [Veo 3.1](https://ai.google.dev/gemini-api/docs/models/veo-3.1-generate-preview) | `veo-3.1-generate-preview`; `veo-3.1-fast-generate-preview` | Preview | preview | Released 2025-10-15 | Gemini API media generation | Text/image input; video/audio output | — | Video generation | Included at cutoff | Gemini Enterprise Agent Platform GA models are a separate surface |
| Google | [Veo 3.1 Lite](https://ai.google.dev/gemini-api/docs/models/veo-3.1-lite-generate-preview) | `veo-3.1-lite-generate-preview` | Preview | preview | Released 2026-03-31 | Gemini API media generation | Text/image input; video output | — | Efficient video generation | Included; dated before cutoff | — |
| Google | [Imagen 4](https://ai.google.dev/gemini-api/docs/models/imagen) | `imagen-4.0-generate-001`; `imagen-4.0-ultra-generate-001`; `imagen-4.0-fast-generate-001` | Deprecated | deprecated | Deprecated 2026-06-15; shutdown 2026-08-17 | Gemini API until shutdown | Text input; image output | — | Image generation | Included as Deprecated at cutoff | Three official endpoints grouped by one official card |
| Google | [Lyria 3 Pro](https://ai.google.dev/gemini-api/docs/models/lyria-3-pro-preview) | `lyria-3-pro-preview` | Preview | preview | Released 2026-03-25 | Gemini API music generation | Text/image input; audio output | — | Full-length music generation | Included; dated before cutoff | Specialized media model |
| Google | [Lyria 3 Clip](https://ai.google.dev/gemini-api/docs/models/lyria-3-clip-preview) | `lyria-3-clip-preview` | Preview | preview | Released 2026-03-25 | Gemini API music generation | Text/image input; audio output | — | Short music clips/loops | Included; dated before cutoff | Specialized media model |
| Google | [Lyria RealTime](https://ai.google.dev/gemini-api/docs/models/lyria-realtime-exp) | `lyria-realtime-exp` | Experimental | not normalized (experimental) | Released 2025-05-20 | Realtime music API surface | Streaming music output | — | Realtime music generation | Included at cutoff | Google says Experimental is unstable and not generally suitable for production |
| Google | [Gemini 2.5 Computer Use](https://ai.google.dev/gemini-api/docs/models/gemini-2.5-computer-use-preview-10-2025) | `gemini-2.5-computer-use-preview-10-2025` | Preview | preview | Released 2025-10-07 | Gemini API computer-use tool | Screenshot/image interaction | Model-page specific | UI action automation | Included at cutoff | Specialized model, not general task-selection default |
| Google | [Deep Research](https://ai.google.dev/gemini-api/docs/models/deep-research-preview-04-2026) | `deep-research-preview-04-2026` | Preview | preview | Released 2026-04-21 | Gemini managed-agent/Interactions surface | Agent result modalities per model page | Agent-managed reasoning | Autonomous planning, source research, synthesis | Included; dated before cutoff | Agent endpoint is not interchangeable with a base model |
| Google | [Deep Research Max](https://ai.google.dev/gemini-api/docs/models/deep-research-max-preview-04-2026) | `deep-research-max-preview-04-2026` | Preview | preview | Released 2026-04-21 | Gemini managed-agent/Interactions surface | Agent result modalities per model page | Agent-managed reasoning | Comprehensive research-agent variant | Included; dated before cutoff | Agent endpoint is not interchangeable with a base model |
| Google | [Antigravity Agent](https://ai.google.dev/gemini-api/docs/models/antigravity-preview-05-2026) | `antigravity-preview-05-2026` | Preview | preview | Released 2026-05-19 | Gemini managed-agent surface | Managed sandbox/files/web | Agent-managed reasoning | Plans, runs code, manages files, browses web in isolated Linux sandbox | Included; dated before cutoff | Managed agent, not the Antigravity IDE model-selection label |
| Google | [Gemini Embedding 2](https://ai.google.dev/gemini-api/docs/models/gemini-embedding-2) | `gemini-embedding-2` | Stable / GA | stable | Released 2026-04-22 | Embeddings API | Text/image/video/audio/PDF input; vector output | — | Multimodal embeddings/RAG | Included; dated before cutoff | Not a generative agent model |
| Google | [Gemini Embedding](https://ai.google.dev/gemini-api/docs/models/gemini-embedding-001) | `gemini-embedding-001` | Stable endpoint; shutdown scheduled 2026-07-14 | stable | Released 2025-07-14; deprecation schedule before cutoff | Embeddings API until shutdown | Text input; vector output | — | Embeddings/RAG | Included at cutoff | Scheduled shutdown is four days after cutoff; migrate to Embedding 2 |
| Google | [Gemini Robotics-ER 1.6](https://ai.google.dev/gemini-api/docs/models/gemini-robotics-er-1.6-preview) | `gemini-robotics-er-1.6-preview` | Preview | preview | Released 2026-04-14 | Gemini API robotics surface | Multimodal/physical-space input per model page | Model-page specific | Embodied reasoning and multi-step physical planning | Included; dated before cutoff | Specialized robotics model |
| Google | [Gemini 2.0 Flash](https://ai.google.dev/gemini-api/docs/models/gemini-2.0-flash) | `gemini-2.0-flash`; `gemini-2.0-flash-001` | Shut down | deprecated | Shut down 2026-06-01 | Unavailable | — | — | Historical general model | Included as shut down at cutoff | Two exact endpoints grouped by official family card |
| Google | [Gemini 2.0 Flash-Lite](https://ai.google.dev/gemini-api/docs/models/gemini-2.0-flash-lite) | `gemini-2.0-flash-lite`; `gemini-2.0-flash-lite-001` | Shut down | deprecated | Shut down 2026-06-01 | Unavailable | — | — | Historical lightweight model | Included as shut down at cutoff | Two exact endpoints grouped by official family card |
| Google | [Gemini 3.1 Flash-Lite Preview](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-lite-preview) | `gemini-3.1-flash-lite-preview` | Shut down | deprecated | Shut down 2026-05-25 | Alias/card redirects toward Stable replacement | — | — | Historical preview | Included as shut down at cutoff | Use `gemini-3.1-flash-lite` |
| Google | [Gemini 3 Pro Preview](https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-preview) | `gemini-3-pro-preview` | Shut down | deprecated | Shut down 2026-03-09 | Alias redirects to `gemini-3.1-pro-preview` | — | — | Historical reasoning preview | Included as shut down at cutoff | Redirect does not revive original endpoint maturity |

## Task-fit Analysis (Inference, Not Provider Fact)

The following recommendations are **analysis inferred from official capability
descriptions plus the workspace task taxonomy**. They are candidates for
evaluation, not benchmark rankings, provider guarantees, or permission to
change Stage 00 policy. Relative latency/cost wording is used only where an
official model description explicitly positions the option that way; no prices
or measured workspace results are supplied.

| Task characteristic | Required capabilities | Claude option | OpenAI/Codex option | Gemini option | Latency/cost consideration | Evidence basis | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Supervisor routing, architecture, final synthesis | Long-horizon reasoning, tool use, large context, synthesis | Workspace `opus` → Claude Opus 4.8 | Workspace `gpt-5.5` at `xhigh` | Official API candidate `gemini-3.1-pro-preview`; workspace string is an availability gap | Top-tier choices prioritize capability; no cross-provider cost rank is established | Stage 00 taxonomy plus official agentic/professional/complex-task descriptions | High for workspace routing; Medium for cross-provider equivalence |
| Scoped coding implementation and subagents | Code generation, tools, patch/shell or provider-agent surface, bounded task execution | Workspace `sonnet` → Claude Sonnet 4.6 | Workspace `gpt-5.4-mini` at `medium`; `gpt-5.3-codex` is a separate code-specialized API option | Workspace `gemini-3.5-flash` | Mini/Flash descriptions explicitly emphasize efficiency; no numeric comparison | Official coding/subagent descriptions plus Worker taxonomy | High for configured values; Medium for alternatives |
| High-volume classification, extraction, or routing | Low latency, structured output, multimodal input when needed | Claude Haiku 4.5 candidate; not workspace default | GPT-5.4 nano candidate; no tool search/computer use per changelog | Gemini 3.1 Flash-Lite candidate | Providers position these options for speed/high volume; no price rank | Official model cards | Medium |
| UI automation | Image/screenshot understanding, action tools, safety controls | Claude Opus 4.8 with documented computer use | GPT-5.4/5.4 mini with built-in computer use; deprecated `computer-use-preview` excluded | Gemini 3.5 Flash computer-use support is Preview; specialized 2.5 Computer Use is Preview | Preview/specialized surfaces increase migration risk; latency/cost not compared | Official tool/model pages and lifecycle status | Medium |
| Evidence-backed web research | Tool use, search, long context, source synthesis | Current Claude with web search/fetch; model support must be checked | Current GPT-5 family with web search; deprecated deep-research models excluded | Deep Research / Max managed-agent previews or Gemini 3.5 Flash with search | Managed preview agents trade stability for specialized orchestration; no cost rank | Official capability descriptions and lifecycle pages | Medium |
| Image, voice, video, embedding, or moderation workload | Modality-specific input/output and endpoint contract | Use Claude only where its current multimodal/tool contract matches; no media generator inferred | Select the listed specialized image/audio/realtime/embedding/moderation model, respecting deprecation | Select the exact Stable/Preview/Experimental media or embedding endpoint | Specialized endpoints are not interchangeable with general workers; check lifecycle first | Official specialized model cards | High for specialization boundary; Low for untested quality |

## Workspace Implementation Status

| Research category | Workspace current state | External primary-source finding | Comparison | Status | Gap | Recommendation | Canonical owner | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Model-policy SSoT | Stage 00 defines two tiers and coupled change surfaces | Provider catalogs change independently | Policy is deliberately slower than catalogs | Implemented | Provider availability is not continuously proven | Keep Stage 00 as SSoT and revalidate before approved changes | `subagent-protocol.md` | Stage 00 Model Policy; this cutoff ledger | High |
| Claude mapping | `opus-4.8` / `sonnet-4.6` via Claude Code aliases | Both API IDs are Active; newer models also exist | Current policy is supported but not newest-model tracking | Implemented | Alias/account resolution is not validated by repo checks | Preserve values unless full change protocol is approved | Stage 00 + adapter generator | Claude model and lifecycle pages | High |
| OpenAI/Codex mapping | `gpt-5.5` / `gpt-5.4-mini` with effort controls | Both are listed; OpenAI does not label them stable/GA | Configuration is catalog-consistent, maturity remains unnormalized | Partially Implemented | Repo validators cannot prove entitlement/availability | Add provider evidence to any future approved change task | Stage 00 + Codex generator/validator | OpenAI official-web fallback; Codex config reference | Medium |
| Gemini mapping | `gemini-3.1-pro` / `gemini-3.5-flash` | Flash is Stable; official Pro ID is `gemini-3.1-pro-preview` | Worker matches; Supervisor string lacks `-preview` | Partially Implemented | Unsupported literal availability for Supervisor value | Record as gap; do not edit without policy, generator, adapters, validators, Stage 04 evidence, and provider sync | Stage 00 + Gemini generator/validator | Google model cards and deprecations | High |
| Task-fit evaluation | Role taxonomy fixes Supervisor/Worker defaults | Providers expose many specialized/current models | Catalog descriptions are not workspace eval results | Missing | No cross-provider task fixture proves recommendations | Evaluate representative tasks before any model-policy proposal | Eval owner + workflow supervisor | Inference table above | High |

## Sources

### Anthropic source notes

- [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview) — current names, IDs, surfaces, latest-model context/modalities, and reasoning notes; mutable page, retrieval state only where a dated release note is absent.
- [Model IDs and versioning](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions) — pinned IDs versus pre-4.6 convenience aliases; no visible page date.
- [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations) — provider lifecycle definitions and dated status/retirement history; mutable status table, partner schedules separate.
- [Claude Platform release notes](https://platform.claude.com/docs/en/release-notes/overview) — dated releases through 2026-07-08; retrieval 2026-07-10.
- [Claude Code settings](https://code.claude.com/docs/en/configuration) — `model`, available-model, fallback, advisor, and teammate configuration surfaces; mutable product docs.

### OpenAI source notes

- [Latest-model guide](https://developers.openai.com/api/docs/guides/latest-model) — required first fetch; GPT-5.6 family guidance and provider-native controls; mutable page.
- [All models](https://developers.openai.com/api/docs/models/all) — 93 official catalog cards and explicit Deprecated labels; mutable page, exact cutoff listing state is `historical state unverified` for 46 non-deprecated rows.
- [Deprecations](https://developers.openai.com/api/docs/deprecations) — provider definitions of Deprecated, shut down/sunset, and Legacy plus dated model transitions through 2026-06-11.
- [API changelog](https://developers.openai.com/api/docs/changelog) — dated releases, including GPT-5.6 on 2026-07-09 and Realtime 2.1 on 2026-07-06; dates have no time of day.
- [Codex configuration reference](https://developers.openai.com/codex/config-reference) — model and reasoning-effort configuration surface; redirected at retrieval to the current ChatGPT Learn documentation.

### Google source notes

- [Gemini models](https://ai.google.dev/gemini-api/docs/models) — 35 catalog cards, exact maturity terms, naming-pattern definitions, and previous-model cards; page says last updated 2026-07-09 UTC.
- [Gemini deprecations](https://ai.google.dev/gemini-api/docs/deprecations) — release/shutdown schedules and replacements; page says last updated 2026-07-02 UTC.
- [Gemini API release notes](https://ai.google.dev/gemini-api/docs/changelog) — dated releases and shutdown announcements through the cutoff-relevant catalog state; mutable log.
- [Gemini CLI configuration](https://google-gemini.github.io/gemini-cli/docs/get-started/configuration.html) — CLI model/config surface; does not prove API or Antigravity availability.

## Maintenance

- **Owner**: Documentation maintainers with Stage 00 model-policy owners
- **Evidence Cutoff**: 2026-07-10 10:00 KST (01:00 UTC)
- **Retrieved**: 2026-07-10
- **Review Cadence**: On provider lifecycle announcement or workspace Model Policy proposal
- **Update Trigger**: Rebuild a new explicitly dated ledger; never silently rewrite this cutoff as if a mutable current page proved historical state

## Related Documents

- [task-characteristic model selection](./agent-model-selection.md)
- [research pack index](./README.md)
- [provider implementation comparison](./provider-implementation-comparison.md)
- [subagent protocol](../../../00.agent-governance/subagent-protocol.md)
- [consolidation task evidence](../../../04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md)
