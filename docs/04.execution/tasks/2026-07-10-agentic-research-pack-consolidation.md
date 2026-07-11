---
status: active
---

<!-- Target: docs/04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md -->

# Task: Agentic Research Pack Consolidation

## Overview

This document tracks the source research, canonical document changes,
supersession work, logical commits, reviews, and verification evidence for the
agentic research pack consolidation defined by Spec 122 and its implementation
plan.

## Inputs

- **Parent Spec**:
  [Agentic Research Pack Consolidation](../../03.specs/122-agentic-research-pack-consolidation/spec.md)
- **Parent Plan**:
  [Agentic Research Pack Consolidation Plan](../plans/2026-07-10-agentic-research-pack-consolidation.md)
- **Canonical Research Pack**:
  [Agentic Engineering Research Pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- **Duplicate Pack**:
  [2026-07-07 Update](../../90.references/research/2026-07-07-agentic-research-pack-update/README.md)

## Working Rules

- Use tracked repo-local files and active stage documents for workspace truth.
- Use official vendor, standards, original-paper, and official-repository
  sources for external research.
- Apply the provider-model cutoff at 2026-07-10 10:00 KST (01:00 UTC).
- Record source metadata and concise evidence; do not paste raw pages, raw
  command output, diagnostics, shell history, or secret material.
- Keep Stage 90 advisory and record active-policy/runtime changes as follow-up
  gaps.
- Use one sequential implementer and one task-scoped review gate per task.
- Commit each clean reviewed task as one logical unit.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-ARC-001 | Refresh workspace baseline, spec-driven SDLC, document roles, and source evidence | doc | VAL-ARC-002, VAL-ARC-007, VAL-ARC-009 | PLN-ARC-001 | Category/role coverage, validators, commit range, task review | Documentation implementer | Done |
| T-ARC-002 | Add cutoff-bound provider model landscape and refresh task selection | doc/eval | VAL-ARC-003, VAL-ARC-004 | PLN-ARC-002 | Model/lifecycle totals, cutoff exceptions, provider sources, validators, task review | Documentation implementer | Done |
| T-ARC-003 | Consolidate harness, loop, provider implementation, and AI agent catalogs | doc | VAL-ARC-002, VAL-ARC-005 | PLN-ARC-003 | Capability sources, stale-claim disposition, validators, task review | Documentation implementer | Done |
| T-ARC-004 | Refresh QA/CI/formatting and automation/pipeline/workflow research | doc | VAL-ARC-002, VAL-ARC-008 | PLN-ARC-004 | Gate/job inventory, evidence classes, validators, task review | Documentation implementer | Done |
| T-ARC-005 | Refresh Docker Compose/infrastructure and security-governance research | doc/security | VAL-ARC-002, VAL-ARC-008 | PLN-ARC-005 | Rechecked Compose evidence, security status/gap matrix, validators, task review | Documentation implementer | Done |
| T-ARC-006 | Finalize indexes and supersede the duplicate pack; keep lifecycle closure pending broad review | doc/eval | VAL-ARC-001, VAL-ARC-005, VAL-ARC-006, VAL-ARC-007, VAL-ARC-008, VAL-ARC-009, VAL-ARC-010 | PLN-ARC-006 | Coverage/disposition matrix, final checks, Task 6 review; whole-branch review and closure remain open | Workflow supervisor | Ready for Review |

## Phase View

### Phase 1: Workspace and Lifecycle Baseline

- [x] T-ARC-001 Refresh workspace baseline, SDLC, document roles, and evidence.

### Phase 2: Provider and Agent Research

- [x] T-ARC-002 Add provider model landscape and task-selection analysis.
- [x] T-ARC-003 Consolidate harness, loop, provider, and AI agent research
      (**Done**; final independent review PASS / APPROVED).

### Phase 3: Quality, Infrastructure, and Security

- [x] T-ARC-004 Refresh QA/CI/formatting and automation research
      (**Done**; final independent review PASS / APPROVED).
- [x] T-ARC-005 Refresh Compose/infrastructure and security research
      (**Done**; final independent review PASS / APPROVED).

### Phase 4: Consolidation Closure

- [ ] T-ARC-006 Supersede the duplicate pack and prepare provisional evidence
      (**Ready for Review**; Task 6 independent verdict, broad review, and
      lifecycle closure remain pending).

## Source Evidence Contract

Each task appends a source ledger with these exact fields:

Rows are added only after a task verifies the source. A mutable page that cannot
prove an applicable model cutoff must use `historical state unverified`.

| Source URL / repo path | Owner / source class | Supported claim | Published / updated | Retrieved | Cutoff disposition | Caveat | Task |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax> | GitHub / official mutable documentation | A workflow is YAML automation composed of jobs and steps with triggers and permissions. | Not shown | 2026-07-10 | Not applicable (non-model source) | Mutable page; retrieval-time syntax only, not proof of remote enforcement. | T-ARC-001 |
| <https://csrc.nist.gov/pubs/sp/800/218/final> | NIST / official standard publication page | SSDF v1.1 provides high-level secure-development practices integrable into an SDLC. | 2022-02 | 2026-07-10 | Not applicable (non-model source) | Framework comparison only; no workspace control mapping or adoption. | T-ARC-001 |
| <https://github.github.com/spec-kit/> | GitHub / official mutable project documentation | Current core flow is Spec → Plan → Tasks → Implement, with each Markdown artifact feeding the next. | 2026-05-27 | 2026-07-10 | Not applicable (non-model source) | Page displays “Last updated: May 27, 2026”; mutable retrieval-time content only, and no Spec Kit runtime or policy is adopted. | T-ARC-001 |
| <https://github.com/github/spec-kit/blob/main/spec-driven.md> | GitHub / official repository document | Specifications provide implementation context and a constitution supplies cross-phase principles. | Not shown | 2026-07-10 | Not applicable (non-model source) | `main` is mutable; retrieval-time content only. | T-ARC-001 |
| <https://www.iso.org/standard/63712.html> | ISO / official standards metadata | ISO/IEC/IEEE 12207:2017 identifies software lifecycle-process framing. | 2017-11 | 2026-07-10 | Not applicable (non-model source) | Page now marks the edition withdrawn; historical metadata only, not a current normative basis. | T-ARC-001 |
| <https://www.iso.org/standard/72089.html> | ISO / official standards metadata | ISO/IEC/IEEE 29148:2018 supplies requirements-engineering framing. | 2018-11 | 2026-07-10 | Not applicable (non-model source) | Public metadata/summary is not full standard text; page says the standard is to be revised. | T-ARC-001 |
| <https://www.iso.org/standard/74393.html> | ISO / official standards metadata | ISO/IEC/IEEE 42010:2022 supplies architecture-description framing. | 2022-11 | 2026-07-10 | Not applicable (non-model source) | Public metadata/summary is not full standard text; repo ARD scope is narrower. | T-ARC-001 |
| <https://adr.github.io/> | ADR community / curated primary practice hub | An ADR captures one architectural decision, rationale, trade-offs, and consequences. | Not shown | 2026-07-10 | Not applicable (non-model source) | Curated mutable page, not a workspace mandate. | T-ARC-001 |
| <https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions> | Michael Nygard / original practice article | Original ADR practice records status, context, decision, and consequences. | 2011-11-15 | 2026-07-10 | Not applicable (non-model source) | Original essay is practice guidance, not a standard. | T-ARC-001 |
| <https://sre.google/sre-book/managing-incidents/> | Google SRE / official book chapter | Incident command separates command, operations, communications, planning, and live state. | Not shown on page | 2026-07-10 | Not applicable (non-model source) | Book guidance; page has no visible update date and is not adopted incident policy. | T-ARC-001 |
| <https://sre.google/sre-book/postmortem-culture/> | Google SRE / official book chapter | A reviewed blameless postmortem records impact, mitigation, root causes, and preventive actions. | Not shown on page | 2026-07-10 | Not applicable (non-model source) | Book guidance; page has no visible update date and is not adopted policy. | T-ARC-001 |
| <https://csrc.nist.gov/pubs/sp/800/61/r3/final> | NIST / official standard publication page | SP 800-61 Rev. 3 frames incident response as a CSF 2.0 Community Profile. | 2025-04 | 2026-07-10 | Not applicable (non-model source) | Supersedes Rev. 2; comparison only, with no formal workspace mapping. | T-ARC-001 |
| <https://www.pagerduty.com/resources/learn/what-is-a-runbook/> | PagerDuty / vendor practice guide | A runbook is detailed repeatable operational how-to guidance and may be manual or automated. | Not shown | 2026-07-10 | Not applicable (non-model source) | Redirects to `/resources/automation/learn/what-is-a-runbook/`; mutable vendor guidance, not policy. | T-ARC-001 |
| <https://keepachangelog.com/en/1.1.0/> | Keep a Changelog / official convention page | Changelogs communicate notable human-readable changes and maintain an Unreleased section. | 2019-02-15 (v1.1.0) | 2026-07-10 | Not applicable (non-model source) | Convention only; site content includes later maintenance updates. | T-ARC-001 |
| <https://semver.org/> | Semantic Versioning / official specification page | MAJOR, MINOR, and PATCH communicate incompatible, compatible feature, and compatible fix changes. | Not shown (2.0.0) | 2026-07-10 | Not applicable (non-model source) | Requires a declared public API; does not define workspace release approval. | T-ARC-001 |
| <https://platform.claude.com/docs/en/about-claude/models/overview> | Anthropic / official mutable model catalog | Current Claude names, IDs/surfaces, Fable general availability, Sonnet 5 current-model placement, and a statement that Mythos Preview is offered separately. | No visible page date | 2026-07-10 | Included; dated releases corroborated separately; historical state unverified where only current-page state exists | Conflicts with the Mythos Preview scheduled-retirement statement; does not prove account availability. | T-ARC-002 |
| <https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions> | Anthropic / official model-ID guide | Dateless 4.6+ IDs are pinned; older convenience aliases may resolve to dated snapshots. | No visible page date | 2026-07-10 | Included; versioning rule | Mutable guide; not a lifecycle status table. | T-ARC-002 |
| <https://platform.claude.com/docs/en/about-claude/model-deprecations> | Anthropic / official lifecycle page | Seven literal Active rows, one Deprecated row, five Retired rows, dated transitions, and a statement Mythos Preview “will be retired” June 30. | Through 2026-06-05 notice | 2026-07-10 | Included; six Deprecated/Retired transitions dated before cutoff; seven Active states historical state unverified | No dated Mythos retirement-completion statement; partner-operated platform schedules differ. | T-ARC-002 |
| <https://platform.claude.com/docs/en/release-notes/overview> | Anthropic / official changelog | Dated Fable 5, Mythos 5, Sonnet 5, Opus 4.8, and retirement evidence. | Latest visible entry 2026-07-08 | 2026-07-10 | Included; no post-cutoff entry used | Changelog dates give no time of day. | T-ARC-002 |
| <https://code.claude.com/docs/en/configuration> | Anthropic / official Claude Code configuration | Claude Code model, fallback, advisor, teammate, and available-model surfaces. | No visible page date | 2026-07-10 | Included as surface evidence | Does not prove account model availability or API ID maturity. | T-ARC-002 |
| <https://developers.openai.com/api/docs/guides/latest-model> | OpenAI / official latest-model guide | GPT-5.6 family, native reasoning/tool features, and latest model guidance. | Current page includes a `Jul 9` family release | 2026-07-10 | Retrieval-time context only for GPT-5.6; exact cutoff inclusion historical state unverified | Official-web fallback because Docs MCP was not exposed; no release time or timezone. | T-ARC-002 |
| <https://developers.openai.com/api/docs/models/all> | OpenAI / official mutable model catalog | 93 retrieval-time model cards and explicit Deprecated labels. | No visible page date | 2026-07-10 | Structural coverage 93; exact-cutoff-qualified subset 90 | 46 non-deprecated and five deprecated alias/card states are historical state unverified; listed is not normalized to stable/GA. | T-ARC-002 |
| <https://developers.openai.com/api/docs/deprecations> | OpenAI / official lifecycle page | Deprecated, shut down/sunset, Legacy definitions and dated model/snapshot transitions. | Latest model notice 2026-06-11 | 2026-07-10 | Included; dated notices precede cutoff where the exact model/alias matches | `gpt-audio-mini` and `gpt-4o-mini-tts` entries date snapshots, not the mutable aliases. | T-ARC-002 |
| <https://developers.openai.com/api/docs/changelog> | OpenAI / official changelog | Unzoned `Jul 9` GPT-5.6 entry and July 6 Realtime 2.1 release. | `Jul 9` | 2026-07-10 | GPT-5.6 retained structurally but excluded from exact-cutoff-qualified count | An unzoned July 9 time can fall after 2026-07-10 01:00 UTC; official-web fallback route. | T-ARC-002 |
| <https://developers.openai.com/codex/config-reference> | OpenAI / official Codex configuration entry point | Model and reasoning-effort configuration surface. | No visible page date | 2026-07-10 | Included as surface evidence | Redirected to current ChatGPT Learn docs; does not establish API/Codex entitlement. | T-ARC-002 |
| <https://github.com/openai/openai-go/commit/ee32400f70d6d16c583978c574806648bdeecd91> | OpenAI / official OpenAI-owned SDK commit | Adds exact `gpt-4o-transcribe-diarize` support on the audio transcriptions endpoint. | 2025-10-16 (included in `openai-go` v3.4.0) | 2026-07-10 | Included; exact-ID endpoint existence before cutoff | Immutable existence evidence only; it is not used as the model's launch date or lifecycle state. | T-ARC-002 |
| <https://openai.com/index/new-models-and-developer-products-announced-at-devday/> | OpenAI / official dated product announcement | Names `tts-1` and `tts-1-hd` as the two TTS model variants. | 2023-11-06 | 2026-07-10 | Included; both exact IDs existed before cutoff | Establishes existence, not retrieval-time listing state or lifecycle maturity. | T-ARC-002 |
| <https://openai.com/index/introducing-gpt-oss/> | OpenAI / official dated release announcement | Names and releases `gpt-oss-120b` and `gpt-oss-20b`. | 2025-08-05 | 2026-07-10 | Included; both exact IDs existed before cutoff | Open-weight release does not imply hosted API availability or a stable/GA lifecycle label. | T-ARC-002 |
| <https://openai.com/index/new-embedding-models-and-api-updates/> | OpenAI / official dated product announcement | Names `text-embedding-3-small` and `text-embedding-3-large`. | 2024-01-25 | 2026-07-10 | Included; both exact IDs existed before cutoff | Establishes existence, not retrieval-time listing state or lifecycle maturity. | T-ARC-002 |
| <https://openai.com/index/new-and-improved-embedding-model/> | OpenAI / official dated product announcement | Names `text-embedding-ada-002` as the new embedding model. | 2022-12-15 | 2026-07-10 | Included; exact ID existed before cutoff | Establishes existence, not retrieval-time listing state or lifecycle maturity. | T-ARC-002 |
| <https://ai.google.dev/gemini-api/docs/models> | Google / official model catalog | 35 official catalog cards, exact IDs, Stable/Preview/Experimental terms, and previous-model cards. | Last updated 2026-07-09 UTC | 2026-07-10 | Included; page date precedes cutoff date | Exact update time is not shown; `latest` aliases remain mutable. | T-ARC-002 |
| <https://ai.google.dev/gemini-api/docs/deprecations> | Google / official lifecycle page | Release/shutdown schedules and recommended replacements. | Last updated 2026-07-02 UTC | 2026-07-10 | Included; dated before cutoff | Shutdown date can coexist with Stable maturity. | T-ARC-002 |
| <https://ai.google.dev/gemini-api/docs/changelog> | Google / official changelog | Dated releases, redirects, deprecations, and shutdown evidence. | Through cutoff-relevant 2026-06-30 model entries | 2026-07-10 | Included; no post-cutoff entry used | Mutable log; dates have no time of day. | T-ARC-002 |
| <https://google-gemini.github.io/gemini-cli/docs/get-started/configuration.html> | Google / official Gemini CLI configuration | CLI model/configuration surface. | No visible page date | 2026-07-10 | Included as surface evidence | Does not prove Gemini API or Antigravity model availability. | T-ARC-002 |
| <https://code.claude.com/docs/en/overview> | Anthropic / official mutable Claude Code documentation | Current product, instruction, tool, MCP, automation, and multi-agent surface. | No visible page date | 2026-07-10 | Not applicable (non-model source) | Retrieval-time documentation; feature-specific maturity labels and version notes take precedence. | T-ARC-003 |
| <https://code.claude.com/docs/en/sub-agents> | Anthropic / official mutable Claude Code documentation | Custom subagent context, schema, tools, permissions, MCP, skills, hooks, memory, foreground/background, and worktree isolation. | No visible page date; page contains feature-specific version notes | 2026-07-10 | Not applicable (non-model source) | Current behavior only; local Claude agents remain workspace projections. | T-ARC-003 |
| <https://code.claude.com/docs/en/hooks> | Anthropic / official mutable Claude Code documentation | Command, HTTP, and prompt lifecycle hooks; agent hooks are marked experimental. | No visible page date | 2026-07-10 | Not applicable (non-model source) | Hook configuration does not prove complete enforcement or runtime enablement. | T-ARC-003 |
| <https://code.claude.com/docs/en/configuration> | Anthropic / official mutable Claude Code documentation | User/project/local/managed configuration layers. | No visible page date | 2026-07-10 | Not applicable (non-model source) | Tracked project settings do not prove user/managed configuration. | T-ARC-003 |
| <https://code.claude.com/docs/en/permissions> | Anthropic / official mutable Claude Code documentation | Allow/ask/deny rules and permission modes. | No visible page date | 2026-07-10 | Not applicable (non-model source) | Native permissions complement and do not replace repository approval boundaries. | T-ARC-003 |
| <https://code.claude.com/docs/en/security> | Anthropic / official mutable Claude Code documentation | Security and sandbox/permission framing. | No visible page date | 2026-07-10 | Not applicable (non-model source) | Local files cannot prove that optional sandbox controls are enabled. | T-ARC-003 |
| <https://code.claude.com/docs/en/mcp> | Anthropic / official mutable Claude Code documentation | MCP configuration and tool integration. | No visible page date | 2026-07-10 | Not applicable (non-model source) | Does not prove locally installed servers, credentials, or transports. | T-ARC-003 |
| <https://developers.openai.com/codex/guides/agents-md> | OpenAI / official mutable Codex documentation | Global and project `AGENTS.md` discovery and precedence. | No visible page date | 2026-07-10 | Not applicable (non-model source) | Retrieved through official Docs MCP after the local manual helper rejected a response missing `x-content-sha256`. | T-ARC-003 |
| <https://developers.openai.com/codex/subagents> | OpenAI / official mutable Codex documentation | Current custom-agent required fields, optional runtime fields, parallel execution, sandbox inheritance, and approval propagation. | No visible page date | 2026-07-10 | Not applicable (non-model source) | Tracked TOMLs omit current required description/instructions; documentation does not prove adapter compatibility. | T-ARC-003 |
| <https://developers.openai.com/codex/hooks> | OpenAI / official mutable Codex documentation | Current hook event list and interception limitations. | No visible page date | 2026-07-10 | Not applicable (non-model source) | Tracked `SessionEnd` lacks current official-list support; Pre/Post interception is not universal. | T-ARC-003 |
| <https://developers.openai.com/codex/config-reference> | OpenAI / official mutable Codex documentation | Configuration layers, MCP, model/effort, agent, and opt-in telemetry fields. | No visible page date | 2026-07-10 | Not applicable (non-model source) | Current documentation; global operator configuration remains unknown. | T-ARC-003 |
| <https://learn.chatgpt.com/docs/agent-approvals-security> | OpenAI / official mutable Codex security documentation | Sandbox and approval separation, protected paths, filesystem/network profiles, and beta permission profiles. | No visible page date | 2026-07-10 | Not applicable (non-model source) | Beta/current labels are retrieval-time; repository metadata is not a permission profile. | T-ARC-003 |
| <https://google-gemini.github.io/gemini-cli/docs/get-started/configuration.html> and <https://google-gemini.github.io/gemini-cli/docs/cli/gemini-md.html> | Google / official mutable Gemini CLI documentation | Settings layers, approval/model surfaces, and hierarchical `GEMINI.md` context/imports. | No visible page date | 2026-07-10 | Not applicable (non-model source) | Does not prove local `.gemini` settings or Antigravity behavior; context discovery is not enforcement. | T-ARC-003 |
| <https://google-gemini.github.io/gemini-cli/docs/tools/mcp-server.html> | Google / official mutable Gemini CLI documentation | MCP server/tool configuration and include/exclude controls. | No visible page date | 2026-07-10 | Not applicable (non-model source) | Does not establish installed servers, credentials, transports, or local enablement. | T-ARC-003 |
| <https://google-gemini.github.io/gemini-cli/docs/cli/sandbox.html> | Google / official mutable Gemini CLI documentation | Optional Seatbelt and container sandboxing, disabled by default. | No visible page date | 2026-07-10 | Not applicable (non-model source) | Described capability is not evidence that the workspace enables it. | T-ARC-003 |
| <https://github.com/google-gemini/gemini-cli/blob/main/docs/core/subagents.md> and <https://github.com/google-gemini/gemini-cli/discussions/25562> | Google / official Gemini CLI repository documentation and announcement | Built-in/custom subagents; project/user `.gemini/agents/*.md`; required `name`/`description`; optional tools, inline MCP, model, turn, and timeout controls; isolated context and parallel delegation. | Public support announced in v0.38.1 on 2026-04-16 | 2026-07-10 | Included; dated announcement precedes the evidence date | Current mutable schema may evolve; no tracked `.gemini/agents` proves workspace adoption, and `.agents` is a separate Antigravity/reference surface. | T-ARC-003 |
| <https://github.com/google-gemini/gemini-cli/blob/main/docs/reference/configuration.md>, <https://github.com/google-gemini/gemini-cli/blob/main/docs/hooks/writing-hooks.md>, <https://github.com/google-gemini/gemini-cli/blob/main/docs/reference/commands.md>, <https://github.com/google-gemini/gemini-cli/discussions/17790>, and <https://github.com/google-gemini/gemini-cli/discussions/17812> | Google / official Gemini CLI repository documentation and announcements | Synchronous command hooks under `.gemini` for tool, agent, session, model, and tool-selection events; `.gemini/hooks` examples and `/hooks` management. | Hooks announced with v0.26.0 on 2026-01-28; official weekly announcement says enabled by default | 2026-07-10 | Included; dated announcements precede the evidence date | Event names/input-output semantics differ by provider; no tracked `.gemini/settings.json` or hooks prove local enablement or parity. | T-ARC-003 |
| <https://google-gemini.github.io/gemini-cli/docs/>, <https://google-gemini.github.io/gemini-cli/docs/cli/checkpointing.html>, and <https://google-gemini.github.io/gemini-cli/docs/cli/telemetry.html> | Google / official mutable Gemini CLI documentation | CLI/headless operation, optional default-off shadow-Git checkpointing, and opt-in local/GCP OTLP telemetry. | No visible page date | 2026-07-10 | Not applicable (non-model source) | Provider checkpointing is not shared rollback; telemetry may be disabled and remains privacy/secret constrained. | T-ARC-003 |
| <https://arxiv.org/abs/2210.03629> | Princeton/Google / original ReAct paper | Interleaved reasoning traces and environment actions as a research loop pattern. | 2022-10-06; revised 2023-03-10 | 2026-07-10 | Not applicable (non-model source) | Research foundation only; no repository authority, retry, or evidence policy is adopted from it. | T-ARC-003 |
| <https://arxiv.org/abs/2303.11366> | Northeastern/MIT / original Reflexion paper | Verbal feedback and episodic memory across trials without weight updates. | 2023-03-20; revised 2023-10-10 | 2026-07-10 | Not applicable (non-model source) | Research foundation only; workspace memory remains advisory. | T-ARC-003 |
| <https://github.com/msitarzewski/agency-agents/tree/9f3e401ccd09aa0ee0ef8e015226d0647908e01e> | agency-agents / pinned upstream repository | Point-in-time catalog, agent definitions, integration structure, and MIT-licensed distribution. | Commit 2026-07-09 | 2026-07-10 | Not applicable (non-model source) | Community source; upstream “production-ready” claims are self-claims, not independent evaluation. | T-ARC-003 |
| <https://github.com/msitarzewski/agency-agents/blob/9f3e401ccd09aa0ee0ef8e015226d0647908e01e/README.md> | agency-agents / pinned upstream README | “230+” agents, 17 observed division headings, multi-tool install/conversion, global-directory targets, and desktop auto-update claim. | Commit 2026-07-09 | 2026-07-10 | Not applicable (non-model source) | Counts are point-in-time; README claims do not authorize installation or import. | T-ARC-003 |
| <https://github.com/msitarzewski/agency-agents/blob/9f3e401ccd09aa0ee0ef8e015226d0647908e01e/integrations/codex/README.md> | agency-agents / pinned upstream integration documentation | Converter maps name, description, and Markdown body to minimal Codex TOML fields. | Commit 2026-07-09 | 2026-07-10 | Not applicable (non-model source) | Upstream conversion pattern is comparative only and was not executed. | T-ARC-003 |
| <https://github.com/msitarzewski/agency-agents/blob/9f3e401ccd09aa0ee0ef8e015226d0647908e01e/integrations/gemini-cli/README.md> | agency-agents / pinned upstream integration documentation | Upstream maps Markdown agents to `~/.gemini/agents/`; official Gemini CLI documentation independently confirms that user-level directory and the project-level `.gemini/agents/` surface. | Commit 2026-07-09 | 2026-07-10 | Not applicable (non-model source) | Native target corroboration does not authorize installation, prove upstream converter fidelity, or establish workspace adoption. | T-ARC-003 |
| `scripts/operations/sync-provider-surfaces.sh` | Workspace / tracked generator | Generates Codex agent TOMLs and Gemini/Antigravity agent/skill pointers; `--check` detects drift. | Baseline `1a80b698` | 2026-07-10 | Not applicable (repo-local source) | Generation proves projection parity, not provider-native schema acceptance or runtime enforcement. | T-ARC-003 |
| `scripts/hooks/post-tool-validate.sh` | Workspace / tracked hook implementation | Whitespace/newline normalization plus conditional shell/YAML checks, `git diff --check`, and repository validators. | Baseline `1a80b698` | 2026-07-10 | Not applicable (repo-local source) | It does not run `prettier --check` and is selective by changed-file type. | T-ARC-003 |
| `docker-compose.yml` | Workspace / tracked runtime source | Root network definitions: ordinary `infra_net` bridge and three external networks. | Baseline `1a80b698` | 2026-07-10 | Not applicable (repo-local source) | Definition does not prove external-network existence, live connectivity, or egress policy. | T-ARC-003 |
| `docs/00.agent-governance/agents/README.md` and `docs/00.agent-governance/subagent-protocol.md` | Workspace / canonical governance | Fifteen canonical roles, provider projection model, handoff boundary, and active model tiers. | Baseline `1a80b698` | 2026-07-10 | Not applicable (repo-local source) | Active policy remains unchanged; provider runtime compatibility requires separate evidence. | T-ARC-003 |
| <https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax> | GitHub / official mutable documentation | Class: CI/remote. Workflows are YAML automation made of one or more jobs; the syntax defines triggers, permissions, job IDs, dependencies, and steps. | Not shown | 2026-07-11 | Not applicable (non-model source) | Retrieval-time syntax only; it does not prove that tracked jobs ran or are remotely required. | T-ARC-004 |
| <https://docs.github.com/en/actions/reference/security/secure-use> | GitHub / official mutable documentation | Class: CI/remote security. Supports least-privilege token permissions, caution for untrusted input/secrets, and full-SHA action pinning. | Not shown | 2026-07-11 | Not applicable (non-model source) | Guidance only; no remote setting, scanner result, or workspace control adoption is proved. | T-ARC-004 |
| <https://pre-commit.com/> | pre-commit / official mutable documentation | Class: local/CI. A configured multi-language hook set can run at Git stages or in CI; hook IDs, file filters, stages, and `SKIP` determine execution. | Page showed pre-commit 4.6.0 at retrieval | 2026-07-11 | Not applicable (non-model source) | Upstream capability does not prove installation, every hook run, or this repository's local-runner count. | T-ARC-004 |
| <https://editorconfig.org/> | EditorConfig / official project site | Class: local/editor. EditorConfig files and plugins support consistent coding style across editors and IDEs. | Not shown | 2026-07-11 | Not applicable (non-model source) | File presence does not prove every editor/plugin applies the settings. | T-ARC-004 |
| <https://spec.editorconfig.org/> | EditorConfig / official specification 0.17.2 | Class: local/editor. Defines hierarchical file search, `root`, section precedence, and supported style pairs. | Version 0.17.2 shown | 2026-07-11 | Not applicable (non-model source) | Specification behavior is editor-core behavior, not a standalone repository blocking gate. | T-ARC-004 |
| <https://prettier.io/docs> | Prettier / official stable documentation | Class: local/CI capability. Prettier parses and reprints supported inputs to a consistent style. | Stable docs; no visible page date | 2026-07-11 | Not applicable (non-model source) | The tracked shared post-tool hook does not invoke Prettier, and configuration alone is not execution evidence. | T-ARC-004 |
| <https://prettier.io/docs/cli> | Prettier / official stable CLI documentation | Class: local/CI capability. The CLI's check mode reports unformatted files and uses non-zero exit codes suitable for CI. | Stable docs; no visible page date | 2026-07-11 | Not applicable (non-model source) | Upstream command behavior is not an adopted or tracked shared gate in this workspace. | T-ARC-004 |
| <https://dora.dev/guides/dora-metrics/> | DORA / official mutable guide | Class: remote operational measurement. Current model groups change lead time, deployment frequency, failed deployment recovery time, change fail rate, and deployment rework rate into throughput/instability. | Last updated 2026-01-05 | 2026-07-11 | Not applicable (non-model source) | Best applied to one application/service at a time; this task collected no production deployment or recovery data. | T-ARC-004 |
| <https://martinfowler.com/bliki/ContinuousDelivery.html> | Martin Fowler / original practice article | Class: pipeline/delivery comparison. Continuous delivery emphasizes releasability, fast automated production-readiness feedback, builds/tests, and a deployment pipeline. | Published 2013-05-30; updated 2014-08-12 | 2026-07-11 | Not applicable (non-model source) | Practice framing only; tracked CI checks do not prove production deployability or continuous deployment. | T-ARC-004 |
| <https://docs.docker.com/compose/> | Docker / official mutable documentation | Compose application and workflow overview for services, networks, volumes, configs, and secrets. | Not shown | 2026-07-11 | Not applicable (non-model source) | Overview capability does not prove the workspace's rendered or live state. | T-ARC-005 |
| <https://docs.docker.com/reference/compose-file/> | Docker / official mutable reference | Compose services/resources syntax including profiles, networks, volumes, secrets, and healthchecks. | Not shown | 2026-07-11 | Not applicable (non-model source) | Syntax reference only; examples are not workspace mandates. | T-ARC-005 |
| <https://docs.docker.com/reference/compose-file/include/> | Docker / official mutable documentation | Each include loads an application model with its own project directory and copies resources after base-file merge. | Not shown | 2026-07-11 | Not applicable (non-model source) | Includes can recurse; conflicts and transitive trust require resolved-config review. | T-ARC-005 |
| <https://docs.docker.com/compose/how-tos/profiles/> | Docker / official mutable documentation | Unassigned services are enabled by default; assigned services require profile activation. | Not shown | 2026-07-11 | Not applicable (non-model source) | Profile assignment is activation behavior, not isolation or production readiness. | T-ARC-005 |
| <https://docs.docker.com/compose/how-tos/networking/> | Docker / official mutable documentation | Service-name DNS, custom/internal networks, external pre-existing networks, and cross-project reachability. | Not shown | 2026-07-11 | Not applicable (non-model source) | External declarations do not prove host existence, ACLs, egress, or current connectivity. | T-ARC-005 |
| <https://docs.docker.com/compose/how-tos/use-secrets/> | Docker / official mutable documentation | Compose grants named services access to declared secrets as mounted files. | Not shown | 2026-07-11 | Not applicable (non-model source) | Delivery model does not prove rotation, host-file protection, or Vault integration. | T-ARC-005 |
| <https://docs.docker.com/compose/how-tos/startup-order/> | Docker / official mutable documentation | `depends_on` controls order and health conditions can gate readiness. | Not shown | 2026-07-11 | Not applicable (non-model source) | Static key presence does not prove application readiness or every dependency edge. | T-ARC-005 |
| <https://docs.docker.com/compose/how-tos/production/> | Docker / official mutable documentation | Single-server production considerations and optional production-specific override-file pattern. | Not shown | 2026-07-11 | Not applicable (non-model source) | Example guidance is not a workspace mandate or multi-host production design. | T-ARC-005 |
| <https://docs.docker.com/compose/trust-model/> | Docker / official mutable documentation | Compose files are trusted host-affecting input; transitive includes and fully resolved configuration require review. | Not shown | 2026-07-11 | Not applicable (non-model source) | `docker compose config` aids inspection but does not make untrusted content safe. | T-ARC-005 |
| <https://csrc.nist.gov/pubs/sp/800/218/final> | NIST / official standard publication page | SSDF v1.1 supplies high-level secure-development practices integrable into an SDLC. | 2022-02 | 2026-07-11 | Not applicable (non-model source) | Reference framework only; no workspace control mapping, conformity, or adoption is claimed. | T-ARC-005 |
| <https://owaspsamm.org/model/> | OWASP SAMM / official mutable model | SAMM v2 groups fifteen security practices into five business functions for risk-driven maturity improvement. | Version 2; page date not shown | 2026-07-11 | Not applicable (non-model source) | No workspace assessment, target maturity, score, or roadmap was performed. | T-ARC-005 |
| <https://slsa.dev/spec/v1.2/> | SLSA / official approved specification | SLSA v1.2 defines source/build tracks, incremental levels, attestations, and provenance formats. | Version 1.2; publication date not shown | 2026-07-11 | Not applicable (non-model source) | No SLSA level is claimed; tracked image declaration provenance is not build provenance. | T-ARC-005 |
| <https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations> | GitHub / official mutable documentation | Actions can generate and verify build provenance and signed SBOM attestations with explicit permissions. | Not shown | 2026-07-11 | Not applicable (non-model source) | Availability varies by visibility/plan; no tracked workspace attestation workflow exists. | T-ARC-005 |
| <https://docs.github.com/en/rest/dependency-graph/sboms> | GitHub / official mutable API documentation | A repository dependency graph can be exported as an SPDX-compatible SBOM. | API version 2026-03-10 | 2026-07-11 | Not applicable (non-model source) | Remote availability/coverage was not queried; export capability is not a tracked release SBOM. | T-ARC-005 |
| <https://github.com/ossf/scorecard> | OpenSSF / official mutable repository documentation | Scorecard reports automated heuristic security-health checks and their limitations. | Not shown | 2026-07-11 | Not applicable (non-model source) | No workspace scan/score was produced; heuristic detection can be incomplete. | T-ARC-005 |

## T-ARC-001 Evidence

### Status and Scope

Status is **Done**. The implementation is documentation-only; code TDD is not
applicable. The editable scope was exactly this task record and the three
canonical Stage 90 references below. The controller's final independent review
returned Spec Compliance **PASS** and Document Quality **APPROVED** for the exact
reviewed range recorded below.

### Source and Coverage Inventory

- Repo-local baseline: tracked root, docs, Stage 00, templates, scripts, infra,
  Compose, CI workflow, active stage artifacts, and existing research references.
- External baseline: all 13 URLs under the plan's `Spec-driven SDLC and
  document roles` source group plus GitHub Actions workflow syntax and NIST SSDF.
- Workspace comparison map: 25 category rows with the required eight columns.
- Lifecycle matrix: 7 forward/feedback transition records plus a participant
  boundary for Compose, CI, and secure SDLC.
- Document-role matrix: 19 rows, including separate API, agent, data, and test
  supporting contracts.

### Changed Files

- `docs/04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md`
- `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md`
- `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/spec-driven-sdlc.md`
- `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/sdlc-document-roles.md`

### Validation Evidence

The clean pre-edit base passed the same five commands. The final post-edit gate
recorded:

- `git diff --check` — exit 0.
- `bash scripts/knowledge/generate-llm-wiki-index.sh --check` — exit 0; generated
  index reported fresh.
- `bash scripts/validation/check-doc-traceability.sh` — exit 0;
  `catalog_pairs_total=46`, `failures=0`.
- `bash scripts/validation/check-doc-implementation-alignment.sh` — exit 0;
  `stage_docs_total=621`, `repo_local_markdown_links_checked=4807`,
  `failures=0`.
- `bash scripts/validation/check-repo-contracts.sh` — exit 0; four changed
  template-mapped docs normalized, repository `failures=0`.

### Review-Fix Validation Evidence

After addressing I-1 through I-3 and M-1, the review-fix cycle reran every
covering command:

- `git diff --check` — exit 0.
- `bash scripts/knowledge/generate-llm-wiki-index.sh --check` — exit 0; generated
  index reported fresh.
- `bash scripts/validation/check-doc-traceability.sh` — exit 0;
  `catalog_pairs_total=46`, `failures=0`.
- `bash scripts/validation/check-doc-implementation-alignment.sh` — exit 0;
  `stage_docs_total=621`, `repo_local_markdown_links_checked=4807`,
  `failures=0`.
- `bash scripts/validation/check-repo-contracts.sh` — exit 0;
  `changed_template_docs_total=3`, `normalized_changed_template_docs_total=3`,
  repository `failures=0`.

### Commit and Implementer Review Evidence

- Task brief: `.superpowers/sdd/task-1-brief.md`.
- Implementer report: `.superpowers/sdd/task-1-implementer-report.md`.
- Base commit: `341282da13c2ff4aec5c5415dbdde9efeac5b0dd`.
- Initial implementation commit:
  `6136c57da53a6562cf73600d86d7fc1b159b4879`.
- Review-fix commits:
  `96c1c4059c04a1c412a3aea5a7c15eaa8930e98c` and
  `b60fd1f1c4418c6b6b1e36c81c064fb69b10c7b3`.
- Final independent review range:
  `341282da13c2ff4aec5c5415dbdde9efeac5b0dd..b60fd1f1c4418c6b6b1e36c81c064fb69b10c7b3`.
- Implementer spec-compliance self-review: **PASS** — exact category/document
  table columns,
  25 requested categories, required lifecycle flow, 7 transitions, 19 document
  roles, 15 required source records, retrieval dates, and caveats are present.
- Implementer document-quality self-review: **PASS** — template headings,
  relative links,
  English stage language, evidence/policy boundaries, ownership, and source
  caveats are explicit.
- Review method: structured implementer self-review; the task brief prohibited
  subagents. Critical findings: none. One Important broken link to
  `./model-selection.md` was fixed to `./agent-model-selection.md`, then the
  repository-contract gate passed. The matching non-link filename was corrected
  during diff review. Remaining Minor findings: none.
- Initial independent review of `6136c57d`: **Spec Compliance: FAIL** and
  **Document Quality: CHANGES_REQUESTED**. Findings I-1 through I-3 and M-1
  are addressed in a separate review-fix commit.
- Final independent verdicts: **Spec Compliance: PASS** and
  **Document Quality: APPROVED**.
- Final findings: `Critical=0`, `Important=0`, `Minor=0`; all five prior
  findings (I-1, I-2, I-3, M-1, and M-2) are resolved.
- Final review report:
  `.superpowers/sdd/task-1-final-review-report.md` (ignored controller evidence;
  intentionally not part of the tracked documentation commits).

## T-ARC-002 Evidence

### Status and Scope

Status is **Done** because every one of the 145 retrieval-time structural rows
has a lifecycle value and explicit cutoff disposition, and the three rows that
lack exact-cutoff proof are excluded from the 142-row cutoff-qualified subset.
This task is documentation-only; code TDD is not applicable. No active Model
Policy, provider adapter/generator, configuration, runtime, CI, script,
credential, remote state, or unrelated document changed.

The final bounded OpenAI gap search used Docs MCP search/fetch first and then
dated first-party gap sources where the MCP index exposed only mutable current
pages. It rescued all eight rows named by the final independent re-review:
`gpt-4o-transcribe-diarize`, `tts-1`, `tts-1-hd`, `gpt-oss-120b`,
`gpt-oss-20b`, `text-embedding-3-large`, `text-embedding-3-small`, and
`text-embedding-ada-002`. No row in that exact subset remains unrescued; the
three GPT-5.6 rows remain retrieval-only.

### Provider, Model, and Lifecycle Coverage

| Provider | Structural rows | Cutoff-qualified rows | Provider-native structural totals | Normalized structural totals | Cutoff-qualified normalized totals | Cutoff exception |
| --- | ---: | ---: | --- | --- | --- | --- |
| Anthropic | 17 | 17 | Active 7; generally available 1; current/launched 1; limited 1; Deprecated 1; Retired 5; scheduled-retirement/current-offer conflict 1 | stable 9; deprecated 6; not normalized 2 | stable 9; deprecated 6; not normalized 2 | The status table supplies 13 rows: seven Active states are historical state unverified and six dated Deprecated/Retired transitions are proven; Mythos Preview remains a disclosed official-page conflict |
| OpenAI | 93 | 90 | Listed without maturity label 45; Latest alias 1; Deprecated 47 | not normalized 46; deprecated 47 | not normalized 43; deprecated 47 | GPT-5.6 Sol/Terra/Luna are retrieval-only; all final exact-eight gaps have dated first-party existence proof; 46 non-deprecated and five deprecated alias/card states remain historical state unverified for lifecycle/listing state |
| Google | 35 | 35 | Stable 11; Preview 18; Experimental 1; Deprecated 1; Shut down 4 | stable 11; preview 18; not normalized 1; deprecated 5 | stable 11; preview 18; not normalized 1; deprecated 5 | Catalog's last-updated date is 2026-07-09 UTC, wholly before the cutoff |
| **Total** | **145** | **142** | — | stable 20; preview 18; deprecated 58; not normalized 49 | stable 20; preview 18; deprecated 58; not normalized 46 | Three structural rows are not exact-cutoff-qualified |

The inventory uses one row per official provider catalog card. When an official
card groups multiple endpoints (for example Imagen 4), every exact endpoint is
preserved in that row. OpenAI's all-models page contains 93 retrieval-time cards:
46 current or latest rows without a stable/GA label and 47 explicit Deprecated
rows. Sol, Terra, and Luna remain in that structural count but not the
exact-cutoff-qualified subset.

### Workspace Comparison and Gaps

- Stage 00 `subagent-protocol.md` remains the current workspace model-policy
  SSoT; Supervisor/Worker values and reasoning effort were compared, not edited.
- Claude `opus-4.8` / `sonnet-4.6` correspond to Active API IDs through Claude
  Code aliases.
- OpenAI `gpt-5.5` / `gpt-5.4-mini` are listed, but OpenAI does not label those
  unqualified catalog rows Stable/GA and public docs do not prove entitlement.
- Gemini Worker `gemini-3.5-flash` is Stable. The official Pro API ID is
  `gemini-3.1-pro-preview`; Stage 00 `gemini-3.1-pro` is recorded as an
  unsupported-availability gap and remains unchanged.
- An approved future model change must update the Model Policy, adapter
  generator, generated adapters, validators, Stage 04 evidence, and provider
  sync in one task.

### Changed Files

- `docs/04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md`
- `docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md`
- `docs/90.references/llm-wiki/llm-wiki-index.md`
- `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-model-landscape.md`
- `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/agent-model-selection.md`

### Validation Evidence

The clean pre-edit base `ff17d4d40d834bc01faf17faf9dce72e22c77a4e`
passed `git diff --check`, LLM Wiki freshness, provider sync (no drift), and the
full repository-contract gate (`failures=0`). The final controller-finding
remediation results are:

- `git diff --check` — exit 0.
- Targeted cutoff/lifecycle scan from the parent plan — exit 0; matched the
  cutoff, lifecycle terms, uncertainty label, and both required table headings.
- `bash scripts/knowledge/generate-llm-wiki-index.sh --check` — exit 0; generated
  index reported fresh.
- `bash scripts/operations/sync-provider-surfaces.sh --check` — exit 0; no drift.
- `bash scripts/validation/check-repo-contracts.sh` — exit 0;
  `changed_template_docs_total=5`, `normalized_changed_template_docs_total=5`,
  repository `failures=0`.

The controller-finding fix rerun initially exposed the newly tracked provider
reference as missing from the generated LLM Wiki index and coverage snapshot.
The prescribed generators refreshed those two derived artifacts; the full final
gate rerun then passed with the results above.

### Final Exact-ID Remediation Validation Evidence

The final remediation changed exactly this task record,
`provider-model-landscape.md`, and `agent-model-selection.md`; no generated
artifact required another refresh. The final pre-commit gate recorded:

- Exact-ID/date scan — exit 0; all eight remediated rows name a dated
  first-party source before the cutoff, and all five source-ledger records carry
  owner/source class, publication date, retrieval date, cutoff disposition, and
  caveat.
- Catalog census/schema audit — exit 0; Anthropic `17/17`, OpenAI `93/90`,
  Google `35/35`, total `145/142` structural/cutoff-qualified; zero malformed
  rows and zero empty required cells. Structural normalized totals are
  `stable 20; preview 18; deprecated 58; not normalized 49`; qualified totals
  are `stable 20; preview 18; deprecated 58; not normalized 46`.
- GPT-5.6 disposition scan — exit 0; Sol, Terra, and Luna remain retrieval-only
  with exact cutoff inclusion `historical state unverified`.
- `git diff --check` — exit 0.
- Required cutoff/lifecycle scan from the Task 2 brief — exit 0.
- `bash scripts/knowledge/generate-llm-wiki-index.sh --check` — exit 0; fresh.
- `bash scripts/knowledge/generate-llm-wiki-coverage.sh --check` — exit 0;
  fresh.
- `bash scripts/operations/sync-provider-surfaces.sh --check` — exit 0; no
  drift.
- `bash scripts/validation/check-doc-traceability.sh` — exit 0;
  `catalog_pairs_total=46`, `failures=0`.
- `bash scripts/validation/check-doc-implementation-alignment.sh` — exit 0;
  `stage_docs_total=621`, `repo_local_markdown_links_checked=4807`,
  `failures=0`.
- `bash scripts/validation/check-repo-contracts.sh` — exit 0;
  `changed_template_docs_total=3`, `normalized_changed_template_docs_total=3`,
  `failures=0`.
- Full diff from `ff17d4d40d834bc01faf17faf9dce72e22c77a4e` — inspected;
  exactly the three authored Task 2 documents and the two previously approved,
  canonically generated Wiki artifacts are present.

### Commit and Review Evidence

- Task brief: `.superpowers/sdd/task-2-brief.md`.
- Implementer report: `.superpowers/sdd/task-2-implementer-report.md`.
- Base commit: `ff17d4d40d834bc01faf17faf9dce72e22c77a4e`.
- Original implementation range:
  `ff17d4d40d834bc01faf17faf9dce72e22c77a4e..3c029db4be1f4196b77de22599697e33aea02651`
  with subject `docs(research): add provider model landscape`.
- First controller-finding fix commit:
  `5a398988e5b0c433db9f1fb971ab7990bd9b7c84`; full fix review range:
  `ff17d4d40d834bc01faf17faf9dce72e22c77a4e..5a398988e5b0c433db9f1fb971ab7990bd9b7c84`.
- The final independent re-review of that range returned **Spec Compliance:
  FAIL** and **Document Quality: CHANGES_REQUESTED**, with `Critical=0`,
  `Important=1`, and `Minor=1`. The Important finding was the exact eight-row
  cutoff-evidence gap; the Minor finding was this incomplete commit/review
  ledger.
- Final exact-ID remediation content commit:
  `4c7671c40def61e41a2d3b556cb3fb5a09aef4ee`; exact final content review
  range:
  `ff17d4d40d834bc01faf17faf9dce72e22c77a4e..4c7671c40def61e41a2d3b556cb3fb5a09aef4ee`.
- Implementer spec-compliance self-review: **PASS** — exact cutoff, provider
  schemas, complete provider-card inventory, lifecycle/cutoff disposition,
  task-fit inference label, workspace comparison, sources, and maintenance are
  present.
- Implementer document-quality self-review: **PASS** — official facts are
  separated from inference; mutable-state uncertainty and source-route caveats
  are explicit; no benchmark, price, entitlement, or cross-provider parity is
  invented.
- Final independent review of the exact content range returned **Spec
  Compliance: PASS** and **Document Quality: APPROVED**, with `Critical=0`,
  `Important=0`, and `Minor=0`. The reviewer verified direct dated first-party
  evidence for all 8/8 remediated IDs, reproduced the 145 structural / 142
  cutoff-qualified census (`17/17`, `93/90`, `35/35`), and confirmed all prior
  findings resolved.
- Final review report: `.superpowers/sdd/task-2-final-review-report.md` (ignored
  controller evidence; intentionally not part of tracked documentation
  commits).

## T-ARC-003 Evidence

### Status and Scope

Status is **Done**. The initial independent review requested changes; the
remediation fixed all three Important findings, and the final independent
review returned Spec Compliance **PASS** and Document Quality **APPROVED** with
no remaining findings. The work is documentation-only; code TDD and Graphify
refresh are not applicable. The editable tracked scope was exactly this task
record plus the four canonical Stage 90 references listed below. Stage 00,
provider adapters, scripts, Compose, runtime configuration, CI, credentials,
remote state, and unrelated documents were inspected but not changed.

### Source and Coverage Inventory

- Source-ledger additions: 28 records — 7 Anthropic official records, 5 OpenAI
  official records, 6 Google Gemini CLI official evidence records, 2 original
  papers, 4 immutable upstream `agency-agents` records, and 4 tracked workspace
  source records. The six Google records now include direct subagent/hook
  documentation and dated v0.38.1/v0.26.0 announcements while preserving the
  exact ledger count.
- OpenAI route: the fresh local manual helper rejected a response missing
  `x-content-sha256`, so current Codex pages were retrieved through the
  official Docs MCP search/fetch route. Mutable pages are retrieval-time
  evidence only.
- Workspace inventory: 15 canonical agents (one supervisor and fourteen
  workers), 22 tracked skills, three provider entry shims, provider notes,
  Claude/Codex adapters, Gemini/Antigravity pointers and native rules/workflows,
  hook scripts/settings, sync generator, validation scripts, Compose networks,
  and advisory Graphify report.
- Matrix coverage: 14 harness-element rows, 10 exact loop-contract rows, 17
  provider-capability rows, 18 provider official-evidence rows, and 12 external
  catalog-comparison rows. Every required owner/status/confidence field is
  populated.
- `agency-agents` is pinned to
  `9f3e401ccd09aa0ee0ef8e015226d0647908e01e`. Its README reports 230+ agents
  and exposes 17 observed division headings. No installer, converter,
  auto-update path, or imported definition was executed.

### Stale-Claim Disposition

- `post-tool-validate.sh` is recorded as selective whitespace/newline,
  shell/YAML, diff, and repository validation; it does not run
  `prettier --check`.
- `sync-provider-surfaces.sh` already generates Codex TOMLs and
  Gemini/Antigravity agent/skill pointers; auto-scaffolding is not missing.
- Stage 04 plans/tasks are the canonical execution artifacts; generic
  `implementation_plan.md` and `walkthrough.md` names are explicitly rejected.
- Codex `scope`/`source_catalog` metadata is not a strict path/tool allowlist.
  Current official Codex custom-agent requirements also expose a tracked
  description/instructions schema gap.
- Current official Codex hook evidence does not list tracked `SessionEnd` and
  documents incomplete Pre/Post interception coverage.
- Root Compose has an ordinary `infra_net` bridge plus three external
  networks; the prior blanket internal-network claim is rejected.
- Gemini CLI native custom subagents and hooks are established by official
  documentation and pre-evidence-date release announcements. The tracked
  workspace still has no `.gemini/agents`, `.gemini/settings.json`, or
  `.gemini/hooks`; `.agents` remains an Antigravity/reference projection, not
  proof of Gemini CLI adoption or cross-provider parity.
- Official Codex documentation supports project/user MCP configuration, but
  this tracked tree has no `.codex/config.toml`; `.codex/hooks.json`, agent
  TOMLs/skills, Stage 00, and provider notes are the actual tracked surfaces.
- The hook behavior owner is the tracked
  `docs/00.agent-governance/rules/provider-capability-matrix.md` plus its
  provider Hook Parity Contracts. `.claude/settings.json`, `.codex/hooks.json`,
  and `scripts/hooks/` remain separate executable evidence; no
  standalone `hooks.md` owner exists under the rules directory.
- The prior upstream “16 divisions” claim is corrected to 17 observed README
  division headings at the pinned commit; upstream maturity language remains
  a self-claim.

### Initial Review and Remediation State

- Initial review range:
  `1a80b6989304fa7b6a179861a9cad795dd875ca3..6747cbe3585ea2851c60d16704b8f0e6c97f3a91`.
- Initial independent verdicts: **Spec Compliance: FAIL** and **Document
  Quality: CHANGES_REQUESTED**, with `Critical=0`, `Important=3`, and
  `Minor=0`.
- I-1 fixed: all affected claims across the five assigned documents now
  reflect Gemini CLI's official native subagent/schema and hook/event surfaces,
  dated maturity, and the separate Missing workspace `.gemini` adoption gap
  without claiming parity.
- I-2 fixed: the false tracked project Codex config/MCP baseline is replaced by
  an explicit absent `.codex/config.toml` gap and the actual tracked Codex
  adapter/provider surfaces.
- I-3 fixed: the nonexistent hook owner is replaced by the tracked provider
  capability matrix/Hook Parity Contracts, with configuration and scripts kept
  as implementation evidence rather than policy ownership.
- Remediation state at commit `7aa07accc00770dd4e18cd37ddd77d9f92236848`:
  implementation self-review was complete and the task was **Ready for
  Review**; the final independent result is recorded below.

### Final Independent Re-review

- Exact cumulative content-review range:
  `1a80b6989304fa7b6a179861a9cad795dd875ca3..7aa07accc00770dd4e18cd37ddd77d9f92236848`.
- Final verdicts: **Spec Compliance: PASS** and **Document Quality:
  APPROVED**, with `Critical=0`, `Important=0`, and `Minor=0`.
- All three prior Important findings are resolved: Gemini CLI native
  subagents/hooks now have direct official evidence without local-adoption or
  parity overclaim; the absent project `.codex/config.toml` is an explicit
  tracked-state gap; and hook ownership resolves to the existing provider
  capability matrix/Hook Parity Contracts.
- Reviewer-reproduced counts: harness `14`, loop `10`, provider capabilities
  `17`, official provider evidence `18`, catalog concerns `12`, and T-ARC-003
  source records `28`.
- The stale Stage 00 Gemini fallback wording and absent `.gemini` adoption are
  disclosed future policy/adoption work, not a remaining Task 3 research
  defect; no active-policy or adapter change was authorized here.
- Final re-review report: `.superpowers/sdd/task-3-rereview-report.md` (ignored
  controller evidence; intentionally not part of tracked documentation
  commits).

### Changed Files

- `docs/04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md`
- `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/harness-engineering.md`
- `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md`
- `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-implementation-comparison.md`
- `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/ai-agent-catalogs.md`

### Validation Evidence

- `git diff --check` — exit 0.
- Matrix/schema/source count check — exit 0: harness `14/14`, loops `10/10`,
  provider capabilities `17/17`, official evidence ledger `18/18`, catalog
  concerns `12/12`, and T-ARC-003 source records `28/28`.
- Stale-claim disposition scan — exit 0; matches occur only in explicit
  corrections/gap statements, with no stale affirmative claim retained.
- Tracked-path existence check — exit 0: no project `.codex/config.toml` or
  standalone rules `hooks.md`; the provider capability matrix, Codex/Claude
  hook configuration, and shared hook script paths are tracked.
- `bash scripts/knowledge/generate-llm-wiki-index.sh --check` — exit 0; fresh.
- `bash scripts/knowledge/generate-llm-wiki-coverage.sh --check` — exit 0;
  fresh.
- `bash scripts/operations/sync-provider-surfaces.sh --check` — exit 0; no
  drift.
- `bash scripts/validation/check-doc-traceability.sh` — exit 0;
  `catalog_pairs_total=46`, `failures=0`.
- `bash scripts/validation/check-doc-implementation-alignment.sh` — exit 0;
  `stage_docs_total=621`, `repo_local_markdown_links_checked=4807`,
  `failures=0`.
- `bash scripts/validation/check-repo-contracts.sh` — exit 0;
  `changed_template_docs_total=5`, all five normalized,
  `legacy_changed_template_docs_skipped=0`, repository `failures=0`.
- Full diff from `1a80b6989304fa7b6a179861a9cad795dd875ca3` — inspected;
  exactly the five assigned tracked files are present.

### Commit and Review Evidence

- Task brief: `.superpowers/sdd/task-3-brief.md`.
- Implementer report: `.superpowers/sdd/task-3-implementer-report.md`
  (ignored evidence; it records the original implementation and remediation
  fix cycles, commands, and exact hashes).
- Base commit: `1a80b6989304fa7b6a179861a9cad795dd875ca3`.
- Original implementation commit:
  `6747cbe3585ea2851c60d16704b8f0e6c97f3a91`, subject
  `docs(research): consolidate harness and agent research`.
- Remediation commit:
  `7aa07accc00770dd4e18cd37ddd77d9f92236848`, subject
  `docs(research): remediate Task 3 review findings`.
- Remediation range:
  `6747cbe3585ea2851c60d16704b8f0e6c97f3a91..7aa07accc00770dd4e18cd37ddd77d9f92236848`.
- Implementer spec-compliance self-review: **PASS** — required source classes,
  matrix schemas/counts, tracked inventory, stale corrections, status
  vocabulary, owners, confidence, caveats, and no-import boundary are present.
- Implementer document-quality self-review: **PASS** — official fact,
  workspace implementation, inference/gap, and recommendation are separated;
  every reference retains the canonical template headings and direct sources.
- Final independent remediation verdict: **Spec Compliance PASS** and
  **Document Quality APPROVED**, with `Critical=0`, `Important=0`, and
  `Minor=0`, for the exact cumulative range recorded above. All three prior
  Important findings are resolved; T-ARC-003 is **Done**.

## T-ARC-004 Evidence

### Status and Scope

Status is **Done**. The initial independent review of exact range
`505277817eee0de4270bc03ae7fb789ef9d02ad3..0e400ec2022575fcecb35f9054c9a35a8501d7f9`
returned Spec Compliance **FAIL** and Document Quality
**CHANGES_REQUESTED**, with **Critical 0 · Important 2 · Minor 0**. Both
Important findings were remediated in `ef97a8c1`. The final independent
re-review of exact content range
`505277817eee0de4270bc03ae7fb789ef9d02ad3..ef97a8c148359b7ee1af5948921156a3ab1fa1b1`
returned Spec Compliance **PASS** and Document Quality **APPROVED**, with
**Critical 0 · Important 0 · Minor 1**; I-01 and I-02 are resolved. The sole
M-01 source-date metadata finding is corrected in this bookkeeping update.
This implementation is documentation only, so code TDD and domain coverage are
N/A. The tracked editable scope is exactly this task record plus the two
assigned Stage 90 references. Workflows, scripts, hooks, pre-commit/tool
configuration, runtime, provider adapters, credentials, and remote GitHub state
were inspected but not changed.

### Tracked Inventory and Derivation

- Workflow inventory: **6 tracked workflow files and 21 job IDs**. The count is
  derived from mappings directly under each YAML `jobs:` key: 15 in
  `ci-quality.yml`, 1 changelog job, 2 greeting jobs, 1 PR-labeler job, 1 stale
  job, and 1 tech-stack drift job.
- Local runner inventory: **12 executed local script-backed gates**. The count
  is the 12 `run_step` calls in `run_script_backed_gates`; default,
  `--script-backed`, and `--all-profiles` execute all 12. The `--harness` mode
  executes its separate 8 `run_step` calls. The `--list` mode executes 0 gates
  and only lists responsibilities, including `recommend-qa-gates.sh` as **1
  advisory recommendation** that the runner does not execute. The headline
  census remains 12 default/script-backed gates plus 1 non-executed advisory.
- Pre-commit inventory: **23 hook IDs** in `.pre-commit-config.yaml`. It is
  recorded separately because hook stages/file filters and the local runner are
  different execution surfaces.
- Quality matrix: **28 gate rows** using the required Gate/Purpose/Local/CI/
  Evidence class/Blocking/External basis/Gap schema.
- Automation matrix: **17 loop rows** using the required Automation/Trigger/
  Authority/Inputs/Actions/Evidence/Failure/Rollback/External boundary schema.

### Source Route and Corrected Claims

All nine fixed external entry points were opened directly from their official
URLs and revalidated on 2026-07-11. The source ledger records supported claim,
local/CI/remote class, and caveat. Mutable pages provide retrieval-time
comparison only, and no source is adopted policy.

The refresh corrects these tracked-evidence drifts:

- the security job ID is `zizmor`;
- the quality inventory includes `docs-implementation-alignment`,
  `agent-output-eval-fixture-gate`, and `dependency-vulnerability-audit`;
- `run-local-qa-gates.sh` is a 12-gate local subset with explicit
  CI/local-tooling and remote-only responsibility classes, not a complete CI
  reproduction;
- the shared post-tool hook performs basic text normalization and selective
  shell/YAML/diff/repository checks, but does not invoke Prettier;
- `generate-changelog.yml` verifies that a pushed release tag already appears
  in `CHANGELOG.md`; it does not generate or commit the changelog;
- active `docs/00.agent-governance/rules/github-governance.md:147-155` still
  labels that workflow “generate release changelog,” so the reference records
  the live contradiction, Stage 00 canonical owner, separately approved policy
  correction, and residual gap without editing policy or workflow;
- formatting, linting, syntax, type, test, build, coverage, security,
  traceability, eval, and freshness are separate evidence classes; and
- current branch protection/required-check enforcement is remote-only and
  unknown for this task. The tracked 2026-07-04 observation is historical and
  was not promoted to current evidence.

### Initial Findings and Remediation Mapping

| Finding | Initial evidence | Remediation | Disposition |
| --- | --- | --- | --- |
| I-01 — inaccurate local-runner mode mapping | The automation row assigned 12 actions to `--harness`, but tracked functions contain 12 script-backed and 8 harness `run_step` calls. | The two Stage 90 references now state default/`--script-backed`/`--all-profiles` = 12 executed gates, `--harness` = 8, and `--list` = 0 with 1 advisory non-executed recommender. | Resolved; final independent review PASS / APPROVED. |
| I-02 — omitted changelog governance drift | The workflow only verifies pushed-tag coverage, while active Stage 00 governance says “generate release changelog.” | The automation comparison and follow-up sections record the contradiction, name `docs/00.agent-governance/rules/github-governance.md` as canonical owner, and recommend a separately approved Stage 00 correction. No active policy or workflow changed. | Resolved in Task 4; residual Stage 00 gap remains pending separate approval. |

### Changed Files

- `docs/04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md`
- `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md`
- `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/automation-pipeline-workflow.md`

### Validation Evidence

The clean pre-edit base `505277817eee0de4270bc03ae7fb789ef9d02ad3`
passed diff hygiene, document implementation alignment, repository contracts,
LLM Wiki freshness, document traceability, and provider-surface verification.
The stale-phrase scan returned exit 1 with no matches, which is the expected
success condition for that negative scan.

The post-draft covering pass recorded:

- `git diff --check` — exit 0.
- Required stale-phrase scan — exit 1 with no output/matches.
- `bash scripts/validation/check-doc-implementation-alignment.sh` — exit 0;
  `stage_docs_total=621`, `repo_local_markdown_links_checked=4807`,
  `failures=0`.
- `bash scripts/validation/check-repo-contracts.sh` — exit 0;
  `changed_template_docs_total=3`, `normalized_changed_template_docs_total=3`,
  repository `failures=0`.
- `bash scripts/knowledge/generate-llm-wiki-index.sh --check` — exit 0; fresh.
- `bash scripts/validation/check-doc-traceability.sh` — exit 0;
  `catalog_pairs_total=46`, `failures=0`.
- `bash scripts/operations/sync-provider-surfaces.sh` — exit 0; no drift.

The remediation covering pass recorded:

- Tracked runner source recount — 12 `run_step` calls in
  `run_script_backed_gates`, 8 in `run_harness_gates`, and list-only output with
  1 explicitly advisory recommender; the dispatch maps default/
  `--script-backed`/`--all-profiles` to 12, `--harness` to 8, and `--list` to 0.
- Changelog contradiction check — workflow lines 15-42 verify tag coverage;
  active Stage 00 governance lines 147-155 retain the conflicting generation
  label; the Stage 90 gap and separately approved owner route are present.
- Matrix recount — 28 quality rows and 17 automation rows.
- `git diff --check` and original-base
  `505277817eee0de4270bc03ae7fb789ef9d02ad3..HEAD` diff inspection — PASS;
  exactly the three approved Task 4 files changed.
- Required stale-phrase scan — exit 1 with no output/matches.
- `bash scripts/validation/check-doc-implementation-alignment.sh` — exit 0;
  `stage_docs_total=621`, `repo_local_markdown_links_checked=4807`,
  `failures=0`.
- `bash scripts/validation/check-repo-contracts.sh` — exit 0;
  `changed_template_docs_total=3`, `normalized_changed_template_docs_total=3`,
  repository `failures=0`.
- `bash scripts/knowledge/generate-llm-wiki-index.sh --check` and
  `generate-llm-wiki-coverage.sh --check` — exit 0; both generated artifacts
  fresh.
- `bash scripts/validation/check-doc-traceability.sh` — exit 0;
  `catalog_pairs_total=46`, `failures=0`.
- `bash scripts/operations/sync-provider-surfaces.sh --check` — exit 0; no
  drift.

### Commit and Review Evidence

- Task brief: `.superpowers/sdd/task-4-brief.md`.
- Implementer report: `.superpowers/sdd/task-4-implementer-report.md` (ignored
  out-of-band evidence; it records the immutable implementation commit after
  commit creation).
- Base commit: `505277817eee0de4270bc03ae7fb789ef9d02ad3`.
- Original implementation commit:
  `0e400ec2022575fcecb35f9054c9a35a8501d7f9`.
- Initial review range:
  `505277817eee0de4270bc03ae7fb789ef9d02ad3..0e400ec2022575fcecb35f9054c9a35a8501d7f9`.
- Remediation commit:
  `ef97a8c148359b7ee1af5948921156a3ab1fa1b1`.
- Final independent review range:
  `505277817eee0de4270bc03ae7fb789ef9d02ad3..ef97a8c148359b7ee1af5948921156a3ab1fa1b1`.
- Final independent review report:
  `.superpowers/sdd/task-4-rereview-report.md` (ignored out-of-band evidence).
- Logical subject: `docs(research): refresh QA and automation references`.
- Implementer spec-compliance self-review: **PASS** — fixed source set,
  tracked counts/derivation, exact schemas, evidence taxonomy, known-drift
  corrections, one canonical owner per applicable row, remote uncertainty, and
  scope boundaries are present.
- Implementer document-quality self-review: **PASS** — repository evidence,
  external comparison, blocking behavior, status/gap/recommendation, and
  caveats are separated and directly sourced.
- Initial independent spec-compliance verdict: **FAIL**.
- Initial independent document-quality verdict: **CHANGES_REQUESTED**.
- Initial finding counts: **Critical 0 · Important 2 · Minor 0**.
- Final independent spec-compliance verdict: **PASS**.
- Final independent document-quality verdict: **APPROVED**.
- Final finding counts: **Critical 0 · Important 0 · Minor 1**; I-01 and I-02
  are resolved.
- M-01 disposition: corrected in this bookkeeping update by recording DORA as
  `Last updated 2026-01-05` and Fowler as
  `Published 2013-05-30; updated 2014-08-12`.
- Final status: **Done**.

## T-ARC-005 Evidence

### Status and Scope

Status is **Done**. The final independent review of exact content range
`34fc342ebfbc6601bc0e7f4c9ac9ae7aae00c4c6..26fb9d227da49594c04967ccc4830d722463468b`
returned Spec Compliance **PASS** and Document Quality **APPROVED**, with
**Critical 0 · Important 0 · Minor 0**. The implementation is documentation
only, so code TDD and domain coverage are N/A. The exact tracked implementation
scope was this task record plus the two assigned Stage 90 references. Compose,
infrastructure, workflows, scripts, policy, provider/model configuration,
credentials, secrets, runtime, and remote state were inspected read-only and
not changed.

### Tracked Topology and Derivation

- Canonical Compose census: **49 tracked Compose files** — root plus **48 infra
  variants**. The 48 variants comprise **40 canonical**
  `docker-compose.yml`, **5 dev**, **2 cluster**, and **1 v2** file in **40
  service directories**. Forty-eight files contain services; root contains no
  services.
- Root include census: **17 active include entries** plus **20 commented
  optional entries**. Active included leaves contain **60 declared service
  entries before profile resolution**; this is not a simultaneous runtime
  count.
- Canonical generated coverage: **169 declared service entries**, **25 profile
  labels including `default`** (**24 named**), **9 default** service entries,
  and **160 profile-gated** entries. The generator freshness check passed.
- Root identity/network/secret census: one explicit project name
  (`hy-home-infra`); **4 root networks = 1 ordinary bridge, 0 internal, and 3
  external**; **70 root secret declarations**. Runtime external-network
  existence and secret values remain unknown/unread.
- Static service-key census across all 169 entries: **145 healthchecks, 94
  dependencies, 60 restart policies, 39 port declarations, 130 volume
  declarations, and 112 secret declarations**. Root-included leaves contain 55,
  36, 29, 14, 46, and 42 respectively.
- The infrastructure matrix contains **19 concerns: 6 Implemented, 12
  Partially Implemented, 1 Missing, 0 Not Applicable**. It distinguishes
  include entries, variants, services, profiles, project name, ordinary/
  internal/external networks, static declarations, rendered validation, and
  unknown live state.

### Security Controls, Gaps, and Policy Conflict

- The security matrix contains **15 concerns: 3 Implemented, 9 Partially
  Implemented, 3 Missing, 0 Not Applicable**. Active control, reference
  framework, implementation gap, and human/remote approval are separate.
- Tracked workflow evidence: **6 workflows**, **16/16 full-SHA external action
  references**, top-level permissions in all 6, and 15 required `ci-quality`
  jobs including dependency audit, infrastructure security gates, pre-commit,
  and `zizmor`. Remote runs/settings were not queried.
- Canonical security-automation readiness remains **11 controls: 7
  Implemented, 1 Partially Implemented, 3 Gap** under its generated schema.
  The three generated `Gap` records map to shared research status **Missing**:
  SBOM generation, artifact signing/provenance attestation, and OpenSSF
  Scorecard automation. The generated scan covers 6 workflows, 28 scripts, and
  pre-commit.
- Tracked image/version provenance is explicitly narrower than supply-chain
  provenance: **21 curated images = 20 declared-pinned plus 1 approved floating
  exception**. It is not an SBOM, signature, attestation, vulnerability result,
  or SLSA level.
- Unresolved out-of-scope policy tension: owner
  `docs/00.agent-governance/rules/approval-boundaries.md` unconditionally bans
  secret-value reads and names them a Hard Stop, while owner
  `docs/00.agent-governance/scopes/security.md` describes approved concrete
  value reads/writes/rotations under redaction, validation, and recovery
  evidence. This task follows the stricter ban, names both owners, does not
  resolve the conflict, and routes a separately approved Stage 00/security
  policy follow-up.

### Source Inventory

- External source inventory: **16 primary/official sources** revalidated on
  `2026-07-11` — **9 Docker** sources (overview, file reference, include,
  profiles, networking, secrets, startup order, production, trust model) and
  **7 security/supply-chain** sources (NIST SSDF, OWASP SAMM, SLSA, GitHub
  Actions secure use, GitHub artifact attestations, GitHub SBOM API, OpenSSF
  Scorecard).
- Source-ledger additions: **15 Task 5 rows**. The already-ledgered Task 4
  GitHub Actions secure-use row was revalidated and reused rather than
  duplicated. All mutable pages are retrieval-time guidance; no external
  example/framework is adopted as workspace policy.
- Repo-local source classes: root/all infra Compose, canonical generated Compose
  coverage and security/provenance snapshots, infra/operations READMEs, Stage 00
  approval/security/QA/ops governance, `.github/SECURITY.md`, CODEOWNERS,
  workflows/pre-commit, hardening/validation scripts, and the stale/advisory
  Graphify report corroborated against tracked sources.

### Changed Files

- `docs/04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md`
- `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md`
- `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/security-governance.md`

### Validation Evidence

- Clean pre-edit baseline: HEAD
  `34fc342ebfbc6601bc0e7f4c9ac9ae7aae00c4c6`; `git status --short`,
  `git diff --stat`, and `git diff --check` were clean; generated Compose
  coverage was fresh. Graphify was stale at `30df271a` and advisory.
- Structural recount — exit 0: infrastructure matrix 19 rows
  (`6/12/1/0`), security matrix 15 rows (`3/9/3/0`), 19/19 and 15/15
  single existing canonical-owner paths, and 15 Task 5 source-ledger additions.
- `git diff --check` — exit 0.
- `bash scripts/operations/generate-compose-profile-service-coverage.sh --check`
  — exit 0; generated Compose coverage fresh.
- `bash scripts/validation/generate-security-automation-readiness.sh --check`
  — exit 0; generated security readiness fresh.
- `bash scripts/operations/generate-tech-stack-version-provenance.sh --check`
  — exit 0; generated declaration provenance fresh.
- `bash scripts/validation/validate-docker-compose.sh` — exit 0;
  `services_total=5` for the core profile.
- `bash scripts/hardening/check-all-hardening.sh` — exit 0; all 11 tier
  baselines passed.
- `bash scripts/knowledge/generate-llm-wiki-index.sh --check` and
  `generate-llm-wiki-coverage.sh --check` — exit 0; both generated artifacts
  fresh.
- `bash scripts/validation/check-doc-traceability.sh` — exit 0;
  `catalog_pairs_total=46`, `failures=0`.
- `bash scripts/validation/check-doc-implementation-alignment.sh` — exit 0;
  `stage_docs_total=621`, `repo_local_markdown_links_checked=4807`,
  `failures=0`.
- `bash scripts/operations/sync-provider-surfaces.sh --check` — exit 0; no
  provider drift.
- `bash scripts/validation/check-repo-contracts.sh` — exit 0;
  `changed_template_docs_total=3`, all three normalized, repository
  `failures=0`.
- The first repository-contract pass found only three broken new relative
  links. They were corrected in scope, then the complete gate bundle above was
  rerun and passed; no unrelated pre-existing validator failure remains.

### Commit and Review Evidence

- Task brief: `.superpowers/sdd/task-5-brief.md`.
- Implementer report: `.superpowers/sdd/task-5-implementer-report.md` (ignored
  out-of-band evidence; finalized after the implementation commit).
- Final independent review report: `.superpowers/sdd/task-5-review-report.md`
  (ignored out-of-band evidence).
- Base commit: `34fc342ebfbc6601bc0e7f4c9ac9ae7aae00c4c6`.
- Implementation commit: `26fb9d227da49594c04967ccc4830d722463468b`.
- Final independent review range:
  `34fc342ebfbc6601bc0e7f4c9ac9ae7aae00c4c6..26fb9d227da49594c04967ccc4830d722463468b`.
- Logical subject: `docs(research): refresh infrastructure and security references`.
- Implementer spec-compliance self-review: **PASS** — required topology/control
  concerns, exact schemas, recomputed counts, status vocabulary, one existing
  canonical owner per row, primary sources, approval boundaries, unknown-state
  caveats, and policy-conflict disposition are present.
- Implementer document-quality self-review: **PASS** — tracked fact, generated
  evidence, external comparison, current control, implementation gap,
  recommendation, and human/remote authority remain distinguishable; no secret
  value or fabricated review/runtime verdict is present.
- Independent spec-compliance verdict: **PASS**.
- Independent document-quality verdict: **APPROVED**.
- Independent finding counts: **Critical 0 · Important 0 · Minor 0**.
- Reviewer reproduced the tracked topology, the infrastructure matrix at
  **19 rows (`6/12/1/0`)**, the security matrix at **15 rows (`3/9/3/0`)**,
  **34/34 existing canonical-owner paths**, and **16 supported external
  sources**.
- Reviewer confirmed that the secret-read conflict is accurately recorded,
  the stricter no-read boundary was conservatively followed, and resolution is
  correctly assigned to a separate approved policy follow-up.
- Runtime/remote state remains intentionally unknown, and the unresolved
  policy conflict remains an explicit gap rather than a Task 5 review defect.
- Final status: **Done**.

## T-ARC-006 Provisional Evidence

### Status and Lifecycle Boundary

T-ARC-006 is **Ready for Review**. Steps 1-8 produced the coverage audit,
supersession records, routing updates, and provisional validation evidence.
The Task 6 independent verdict has not been issued. Spec 122, its plan, and
this task remain `status: active`; the Phase 4 checkbox, T-ARC-006, every final
Completion Criteria item, the first whole-branch review, lifecycle-closure
commit, and post-closure review remain open.

### Requested-Category and Spec Coverage Audit

Each row below has exactly one primary canonical owner and section. A routing
summary or downstream evidence link does not create a second owner. Provider
and model rows resolve to the official-source ledger/source notes in their
assigned owner rather than restating vendor facts here.

| ID | Original category or Spec criterion | Primary canonical owner and section | Evidence | Ownership / coverage result |
| --- | --- | --- | --- | --- |
| CAT-001 | purpose | [Workspace baseline — Workspace Category Map, `purpose`](../../90.references/research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md#workspace-category-map) | Root README evidence and external sources linked from that reference | Covered; baseline owns the comparative purpose record. |
| CAT-002 | overview | [Workspace baseline — Workspace Category Map, `overview`](../../90.references/research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md#workspace-category-map) | Tracked root/docs/infra/scripts entry points cited there | Covered; baseline owns workspace routing context. |
| CAT-003 | roles | [Workspace baseline — Workspace Category Map, `roles`](../../90.references/research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md#workspace-category-map) | Stage 00 persona/catalog evidence cited there | Covered; role policy remains outside Stage 90. |
| CAT-004 | CI/CD | [Quality reference — Quality Gate Matrix](../../90.references/research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md#quality-gate-matrix) | [Tracked Inventory](../../90.references/research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md#tracked-inventory) and official GitHub sources | Covered; automation doc links but does not own gate facts. |
| CAT-005 | QA | [Quality reference — Workspace Comparison and Ownership](../../90.references/research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md#workspace-comparison-and-ownership) | Exact gate taxonomy and tracked commands | Covered; one quality owner. |
| CAT-006 | formatting | [Quality reference — Quality Gate Matrix](../../90.references/research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md#quality-gate-matrix) | EditorConfig/Prettier primary sources and tracked configuration cited there | Covered; configuration and enforcement remain distinct. |
| CAT-007 | linting | [Quality reference — Quality Gate Matrix](../../90.references/research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md#quality-gate-matrix) | Pre-commit and tracked linter evidence | Covered. |
| CAT-008 | syntax/type checks | [Quality reference — Quality Gate Matrix](../../90.references/research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md#quality-gate-matrix) | Parser, TypeScript, workflow, and Compose gate rows | Covered. |
| CAT-009 | automation | [Automation reference — Automation Loop Matrix](../../90.references/research/2026-07-05-agentic-research-pack-refresh/automation-pipeline-workflow.md#automation-loop-matrix) | Tracked scripts/hooks/workflows and official workflow sources | Covered; quality owns gate semantics, automation owns trigger/action loops. |
| CAT-010 | pipeline | [Automation reference — Tracked Workflow and Job Inventory](../../90.references/research/2026-07-05-agentic-research-pack-refresh/automation-pipeline-workflow.md#tracked-workflow-and-job-inventory) | Six-workflow/21-job census and caveats | Covered; remote enforcement remains unknown. |
| CAT-011 | workflow | [Automation reference — Automation Loop Matrix](../../90.references/research/2026-07-05-agentic-research-pack-refresh/automation-pipeline-workflow.md#automation-loop-matrix) | Trigger, authority, action, evidence, retry, rollback, and external-boundary fields | Covered. |
| CAT-012 | operating contracts | [Document roles — Canonical Document-Role Matrix](../../90.references/research/2026-07-05-agentic-research-pack-refresh/sdlc-document-roles.md#canonical-document-role-matrix) | Guide/Policy/Runbook/Incident/Postmortem/Release rows and source bases | Covered; Stage 05 remains active owner. |
| CAT-013 | templates | [Document roles — Canonical Document-Role Matrix](../../90.references/research/2026-07-05-agentic-research-pack-refresh/sdlc-document-roles.md#canonical-document-role-matrix) | Tracked Stage 99 template paths in each row | Covered; no template mutation. |
| CAT-014 | scripts | [Automation reference — Automation Loop Matrix](../../90.references/research/2026-07-05-agentic-research-pack-refresh/automation-pipeline-workflow.md#automation-loop-matrix) | Scripts README and exact script entry points cited there | Covered; scripts own actions, not policy. |
| CAT-015 | integration guides | [Document roles — Canonical Document-Role Matrix, `Guide`](../../90.references/research/2026-07-05-agentic-research-pack-refresh/sdlc-document-roles.md#canonical-document-role-matrix) | Guide template/path and role basis | Covered. |
| CAT-016 | SDLC | [Spec-driven SDLC — Lifecycle Flow](../../90.references/research/2026-07-05-agentic-research-pack-refresh/spec-driven-sdlc.md#lifecycle-flow) | [Transition Evidence Matrix](../../90.references/research/2026-07-05-agentic-research-pack-refresh/spec-driven-sdlc.md#transition-evidence-matrix) | Covered; Compose/CI/security are participants, not duplicate owners. |
| CAT-017 | governance | [Workspace baseline — Workspace Category Map, `governance`](../../90.references/research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md#workspace-category-map) | Stage 00 hub and NIST/Spec Kit comparison cited there | Covered; active governance remains Stage 00. |
| CAT-018 | system structure | [Workspace baseline — Workspace Category Map, `system structure`](../../90.references/research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md#workspace-category-map) | Root map and tracked implementation entry points | Covered. |
| CAT-019 | rules | [Workspace baseline — Workspace Category Map, `rules`](../../90.references/research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md#workspace-category-map) | Stage 00 hierarchy/provider-adapter evidence | Covered. |
| CAT-020 | security | [Security reference — Security Comparison](../../90.references/research/2026-07-05-agentic-research-pack-refresh/security-governance.md#security-comparison) | [External Framework Position](../../90.references/research/2026-07-05-agentic-research-pack-refresh/security-governance.md#external-framework-position) and tracked control census | Covered; active controls and reference frameworks remain distinct. |
| CAT-021 | Docker Compose/infrastructure | [Compose reference — Infrastructure Comparison](../../90.references/research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md#infrastructure-comparison) | Recomputed topology census and official Docker sources | Covered; tracked Compose remains runtime truth. |
| CAT-022 | AI agents | [AI agent catalogs — Catalog Comparison Matrix](../../90.references/research/2026-07-05-agentic-research-pack-refresh/ai-agent-catalogs.md#catalog-comparison-matrix) | Immutable upstream pin and tracked Stage 00 catalog | Covered; no agent import/adoption. |
| CAT-023 | harness engineering | [Harness reference — Harness Implementation Matrix](../../90.references/research/2026-07-05-agentic-research-pack-refresh/harness-engineering.md#harness-implementation-matrix) | Official provider/framework and tracked harness sources | Covered. |
| CAT-024 | loop engineering | [Loop reference — Loop Contract Matrix](../../90.references/research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md#loop-contract-matrix) | ReAct/Reflexion papers plus tracked loop owners | Covered; research foundations are not authority. |
| CAT-025 | task-characteristic model selection | [Agent model selection — Task-Characteristic to Configuration Mapping](../../90.references/research/2026-07-05-agentic-research-pack-refresh/agent-model-selection.md#task-characteristic-to-configuration-mapping) | Official provider capability sources and Stage 00 taxonomy linked there | Covered; recommendations are explicitly inference. |
| VAL-ARC-001 | only one active canonical pack | [Canonical pack README — Consolidation and Lifecycle Boundary](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md#consolidation-and-lifecycle-boundary) | Parent research README current/superseded routing | Covered; 2026-07-05 is the only current pack. |
| VAL-ARC-002 | every category has the complete comparison record | [Workspace baseline — Workspace Category Map](../../90.references/research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md#workspace-category-map) | 25 rows with the required eight fields; CAT-001 through CAT-025 above route detailed ownership | Covered; no category is unowned. |
| VAL-ARC-003 | cutoff-bound provider model catalog | [Provider model landscape — Provider Catalogs](../../90.references/research/2026-07-05-agentic-research-pack-refresh/provider-model-landscape.md#provider-catalogs) | [Official provider source notes](../../90.references/research/2026-07-05-agentic-research-pack-refresh/provider-model-landscape.md#sources) and T-ARC-002 ledger | Covered; 145 structural / 142 cutoff-qualified with three disclosed exceptions. |
| VAL-ARC-004 | separate model landscape and task selection | [Agent model selection — Repository Role](../../90.references/research/2026-07-05-agentic-research-pack-refresh/agent-model-selection.md#repository-role) | Full catalog link plus inference-only mapping boundary | Covered; no catalog duplication in selection reference. |
| VAL-ARC-005 | verified duplicate content exists once; unsupported content removed | [T-ARC-006 — Duplicate Claim Disposition](#duplicate-claim-disposition) | Thirty-family ledger below and superseded leaf mappings | Covered provisionally; reviewer verdict pending. |
| VAL-ARC-006 | duplicate pack and every child superseded/mapped | [T-ARC-006 — Supersession Result](#supersession-result) | Duplicate README mapping plus five template-compliant leaf records | Covered provisionally; targeted scan evidence recorded below. |
| VAL-ARC-007 | completed Stage 03/04 and audits preserved as history | [Canonical pack README — Consolidation and Lifecycle Boundary](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md#consolidation-and-lifecycle-boundary) | Direct links to completed Spec 104, its Stage 04 plan/task, and both audit packs | Covered; no historical body deleted or copied. |
| VAL-ARC-008 | no active policy/runtime/CI/provider/model/hook/script/secret/remote change | [Spec 122 — Guardrails](../../03.specs/122-agentic-research-pack-consolidation/spec.md#guardrails-if-applicable) | Task 6 changed-file inventory and full diff inspection | Covered provisionally; exact scope is documentation/index output only. |
| VAL-ARC-009 | logical commits and task reviews | [Tasks 1-5 Commit and Review Ledger](#tasks-1-5-commit-and-review-ledger) | Exact ranges and final PASS/APPROVED reports below | Covered for Tasks 1-5; Task 6 review remains pending. |
| VAL-ARC-010 | specified checks pass or unrelated failure recorded | [Provisional Validation Evidence](#provisional-validation-evidence) | Exact Step 6-8 command results | Covered provisionally; lifecycle closure still requires later broad reviews. |

Coverage result: **35/35 rows covered**, **35/35 with one primary canonical
owner/section**, **0 uncovered**, and **0 duplicate primary owners**. Provider
and model facts are owned by the cutoff landscape and its direct official-source
notes; the comparison and selection documents link rather than reproduce the
catalog.

### Duplicate Claim Disposition

The former five leaves were audited as thirty substantive claim families. A
family groups claims that share one evidence basis and destination; mixed
verified/stale material was split so no unsupported statement inherits a valid
disposition.

| ID | Former document / claim family | Disposition | Canonical destination or retained evidence |
| --- | --- | --- | --- |
| DUP-001 | Workspace stage-to-lifecycle mapping | merged | [Lifecycle flow](../../90.references/research/2026-07-05-agentic-research-pack-refresh/spec-driven-sdlc.md#lifecycle-flow) |
| DUP-002 | Spec/evidence transition and validation chain | merged | [Transition Evidence Matrix](../../90.references/research/2026-07-05-agentic-research-pack-refresh/spec-driven-sdlc.md#transition-evidence-matrix) |
| DUP-003 | Claimed DORA outcome attainment from repository controls | unsupported | Not carried; [quality analysis](../../90.references/research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md#analysis) requires production data. |
| DUP-004 | CI and local gate inventory | merged | Corrected [Quality Gate Matrix](../../90.references/research/2026-07-05-agentic-research-pack-refresh/quality-ci-formatting.md#quality-gate-matrix) |
| DUP-005 | Formatter/linter configuration presence | duplicate | Already owned by the same quality matrix; no second body retained. |
| DUP-006 | External security frameworks described as applied workspace controls | unsupported | Not carried; [External Framework Position](../../90.references/research/2026-07-05-agentic-research-pack-refresh/security-governance.md#external-framework-position) preserves comparison-only status. |
| DUP-007 | Secret-delivery and redaction boundary | merged | [Security Comparison](../../90.references/research/2026-07-05-agentic-research-pack-refresh/security-governance.md#security-comparison) and [Infrastructure Comparison](../../90.references/research/2026-07-05-agentic-research-pack-refresh/docker-compose-infrastructure.md#infrastructure-comparison) |
| DUP-008 | Generic execution filenames, signed skip records, and appended raw output assertions | unsupported | Not carried; Stage 04 task evidence and QA scope remain authoritative. |
| DUP-009 | Template, script-purpose, and bootstrap routing | duplicate | Already covered by [Workspace Category Map](../../90.references/research/2026-07-05-agentic-research-pack-refresh/workspace-baseline.md#workspace-category-map). |
| DUP-010 | Future Graphify, delivery-dashboard, and scanner proposals | historical-only | Preserved only by this disposition; no adopted requirement or implementation is claimed. |
| DUP-011 | Four-part harness concept | duplicate | Canonical definitions already exist in [Harness Definitions / Facts](../../90.references/research/2026-07-05-agentic-research-pack-refresh/harness-engineering.md#definitions--facts). |
| DUP-012 | Root shim and contract-validator implementation | merged | [Harness Implementation Matrix](../../90.references/research/2026-07-05-agentic-research-pack-refresh/harness-engineering.md#harness-implementation-matrix) |
| DUP-013 | Blanket network-isolation assertion | unsupported | Not carried; corrected network evidence is in the harness and Compose matrices. |
| DUP-014 | Provider capability and maturity rankings | unsupported | Not carried; [Provider Capability Matrix](../../90.references/research/2026-07-05-agentic-research-pack-refresh/provider-implementation-comparison.md#provider-capability-matrix) uses official provider-specific evidence. |
| DUP-015 | Proposed universal command wrapper | historical-only | Preserved only as a former proposal disposition; no tracked implementation or approval exists. |
| DUP-016 | Automatic destructive rollback on validation failure | unsupported | Not carried; canonical rollback requires evidence and approval. |
| DUP-017 | Claimed provider-hook absence and unverified resource-quota gap | unsupported | Not carried; official capability and local-adoption gaps are separated in the provider/harness references. |
| DUP-018 | Observe/plan/execute/verify loop concept | duplicate | Canonical loop definitions already cover the concept without duplicating ownership. |
| DUP-019 | Four workspace feedback-loop summary | merged | Expanded into the ten-row [Loop Contract Matrix](../../90.references/research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md#loop-contract-matrix). |
| DUP-020 | Proposed diagnostic-parser architecture | historical-only | Preserved only by this disposition; no current implementation is asserted. |
| DUP-021 | Provider self-correction rankings | unsupported | Not carried; official mechanisms and evidence gaps replace rankings. |
| DUP-022 | Unverified terminal-output and circuit-breaker gaps | unsupported | Not carried as current fact; canonical loop gaps require tracked evidence. |
| DUP-023 | Cross-provider parity ratings and delivery-risk scoring | unsupported | Not carried; provider facts remain provider-native and non-ranked. |
| DUP-024 | Claimed compiler projections and enforced adapter restrictions | unsupported | Not carried; generated metadata and native enforcement are explicitly separated. |
| DUP-025 | Claimed shared formatting wrapper behavior | unsupported | Not carried; tracked hook behavior is owned by the quality/harness references. |
| DUP-026 | Claimed absent adapter generation and unsupported context-limit comparison | unsupported | Not carried; generation is tracked and provider context claims require primary evidence. |
| DUP-027 | External catalog breadth and reference-only comparison | merged | [Catalog Comparison Matrix](../../90.references/research/2026-07-05-agentic-research-pack-refresh/ai-agent-catalogs.md#catalog-comparison-matrix) with immutable upstream pin |
| DUP-028 | Unverified upstream structure, orchestration, and sandbox claims | unsupported | Not carried; publisher claims and verified repository facts are separated. |
| DUP-029 | Local catalog and subagent-routing facts | merged | [Workspace Implementation Status](../../90.references/research/2026-07-05-agentic-research-pack-refresh/ai-agent-catalogs.md#workspace-implementation-status) |
| DUP-030 | Claimed missing profile lint/tracing plus proposed local message-log path | unsupported | Not carried; no tracked evidence or approved logging contract supports it. |

Disposition totals: **merged 8 · duplicate 4 · unsupported 15 ·
historical-only 3 = 30/30**. Unsupported claims are absent from the superseded
leaf bodies and were not promoted to current canonical truth.

### Supersession Result

- Duplicate pack README and all five leaves now declare `status: superseded`.
- Every leaf retains its original H1 and the complete Stage 90 reference
  section contract while containing only mapping/lifecycle facts.
- The duplicate README maps all five leaves; the parent research README lists
  one current pack plus a separate `Superseded References` route.
- The canonical README includes the provider model landscape in Structure,
  Current References, and Reading Order, and records the only-active-pack,
  historical-evidence, and policy/runtime boundaries.

### Tasks 1-5 Commit and Review Ledger

| Task | Full task range | Final content review range | Final verdict | Findings / report |
| --- | --- | --- | --- | --- |
| T-ARC-001 | `341282da13c2ff4aec5c5415dbdde9efeac5b0dd..ff17d4d40d834bc01faf17faf9dce72e22c77a4e` | `341282da13c2ff4aec5c5415dbdde9efeac5b0dd..b60fd1f1c4418c6b6b1e36c81c064fb69b10c7b3` | Spec **PASS** / Quality **APPROVED** | `0/0/0`; `.superpowers/sdd/task-1-final-review-report.md` |
| T-ARC-002 | `ff17d4d40d834bc01faf17faf9dce72e22c77a4e..1a80b6989304fa7b6a179861a9cad795dd875ca3` | `ff17d4d40d834bc01faf17faf9dce72e22c77a4e..4c7671c40def61e41a2d3b556cb3fb5a09aef4ee` | Spec **PASS** / Quality **APPROVED** | `0/0/0`; `.superpowers/sdd/task-2-final-review-report.md` |
| T-ARC-003 | `1a80b6989304fa7b6a179861a9cad795dd875ca3..505277817eee0de4270bc03ae7fb789ef9d02ad3` | `1a80b6989304fa7b6a179861a9cad795dd875ca3..7aa07accc00770dd4e18cd37ddd77d9f92236848` | Spec **PASS** / Quality **APPROVED** | `0/0/0`; `.superpowers/sdd/task-3-rereview-report.md` |
| T-ARC-004 | `505277817eee0de4270bc03ae7fb789ef9d02ad3..34fc342ebfbc6601bc0e7f4c9ac9ae7aae00c4c6` | `505277817eee0de4270bc03ae7fb789ef9d02ad3..ef97a8c148359b7ee1af5948921156a3ab1fa1b1` | Spec **PASS** / Quality **APPROVED** | `0` blocking; reviewer M-01 corrected in bookkeeping; `.superpowers/sdd/task-4-rereview-report.md` |
| T-ARC-005 | `34fc342ebfbc6601bc0e7f4c9ac9ae7aae00c4c6..00190fc97b003c9beedc5af79d195532bc181dde` | `34fc342ebfbc6601bc0e7f4c9ac9ae7aae00c4c6..26fb9d227da49594c04967ccc4830d722463468b` | Spec **PASS** / Quality **APPROVED** | `0/0/0`; `.superpowers/sdd/task-5-review-report.md` |

### Cutoff Caveats, Deviations, and Broad-Review Gate

- The model ledger remains fixed at `2026-07-10 10:00 KST (01:00 UTC)`:
  145 structural rows, 142 cutoff-qualified rows, and three GPT-5.6 rows kept
  as retrieval-only context because their unzoned date does not prove the exact
  cutoff. Mutable provider states retain `historical state unverified` where
  applicable; account/region/product entitlement remains unproven.
- Prior approved deviation: Task 2 refreshed the two generated LLM Wiki outputs
  only through their canonical generators after the new model reference became
  tracked. Task 6 follows the same generator-only rule.
- No new content-scope deviation is introduced. Graphify remains stale and
  advisory; this documentation-only task does not refresh it.
- After Task 6 receives PASS/APPROVED, the exact first broad-review package
  command is:

```bash
git diff --binary 940eae305da0c29e10957bdd80c95d5e6530927a..HEAD -- . > .superpowers/sdd/whole-branch-pre-closure.diff
```

That command and the whole-branch reviewer dispatch are Step 10 and were not
run in this task. Lifecycle completion is forbidden until that review is clean.

### Provisional Validation Evidence

Documentation-only TDD and code coverage are not applicable. The final Step
6-8 evidence is:

- `git diff --check` — exit 0.
- `bash scripts/knowledge/generate-llm-wiki-index.sh --check` — exit 0; fresh.
- `bash scripts/knowledge/generate-llm-wiki-coverage.sh --check` — exit 0;
  fresh. Both generated outputs were unchanged; no generated file was
  hand-edited or regenerated.
- `bash scripts/operations/sync-provider-surfaces.sh --check` — exit 0;
  `no drift`.
- `bash scripts/validation/check-doc-traceability.sh` — exit 0;
  `catalog_pairs_total=46`, `failures=0`.
- `bash scripts/validation/check-doc-implementation-alignment.sh` — exit 0;
  `stage_docs_total=621`, `repo_local_markdown_links_checked=4856`,
  `failures=0`.
- `bash scripts/validation/validate-docker-compose.sh` — exit 0;
  `services_total=5` for the core profile.
- `bash scripts/hardening/check-all-hardening.sh` — exit 0; all eleven tier
  baselines passed.
- `bash scripts/validation/check-repo-contracts.sh` — final exit 0;
  `changed_template_docs_total=13`, `normalized_changed_template_docs_total=13`,
  `target_stage_docs_total=724`, `legacy_target_stage_docs_skipped=0`, and
  repository `failures=0`. The first pass reported the duplicate README's
  missing `## Structure` heading; it was fixed in scope and the complete Step 7
  bundle was rerun successfully.
- Duplicate-active scan — exit 1 with no matches, the expected negative result.
- Duplicate-path scan — exit 0; matches are limited to supersession/history
  routing, target comments, plan scope/check instructions, and task/spec
  traceability. No current-reading route presents the duplicate as active.
- Exact stale-phrase scan — exit 0 with six matches, all already present at
  base `00190fc97b003c9beedc5af79d195532bc181dde` in the out-of-scope canonical
  `harness-engineering.md` and `loop-engineering.md`. Every match is an explicit
  negative correction (not a current affirmative claim); the five new
  tombstones add zero matches. Rewording those previously reviewed Task 3
  canonical leaves would exceed the fourteen-file Task 6 scope, so the semantic
  result is recorded rather than hidden.
- Full changed-file and diff review — fourteen always-scoped documentation
  files only; zero generated files; no policy, runtime, CI, provider/model,
  hook, script, secret, credential, operations, remote, or branch-protection
  surface changed.

Graphify remains built from `30df271a` and advisory. No code file changed, so
the graph refresh was skipped under the approved documentation-only scope.
These results make T-ARC-006 reviewable but do not close the lifecycle or
fabricate a reviewer verdict.

## Task Review Evidence Contract

For each task, record:

- task-brief path;
- implementer report path;
- base and head commits;
- covering commands and summarized results;
- spec-compliance verdict;
- document-quality verdict;
- fixed Critical/Important findings and re-review outcome;
- remaining Minor findings for final review.

## Verification Summary

The implementation records final results for:

```bash
git diff --check
bash scripts/knowledge/generate-llm-wiki-index.sh --check
bash scripts/knowledge/generate-llm-wiki-coverage.sh --check
bash scripts/operations/sync-provider-surfaces.sh --check
bash scripts/validation/check-doc-traceability.sh
bash scripts/validation/check-doc-implementation-alignment.sh
bash scripts/validation/validate-docker-compose.sh
bash scripts/hardening/check-all-hardening.sh
bash scripts/validation/check-repo-contracts.sh
```

Plan-authoring checks are recorded in the current progress entry and commit;
task-specific results are added here during execution.

## Deviation Notes

No implementation deviation exists at plan creation. Any later deviation must
name the affected task, plan requirement, reason, approval or evidence owner,
verification impact, and final disposition.

For `T-ARC-001`, no plan or content-scope deviation occurred. The broader
bootstrap progress-log update was not made because the task brief restricted
mutation to the four named documentation targets; the required implementer
report is the explicit out-of-band task artifact. Graphify refresh was not
required because no code file changed. No active policy, runtime, CI, template,
script, provider/model configuration, remote state, or unrelated document was
modified.

For `T-ARC-002`, the controller approved one necessary generated-collateral
scope deviation: the fix commit includes
`docs/90.references/llm-wiki/llm-wiki-index.md` and
`docs/90.references/data/knowledge/llm-wiki-stage-category-coverage.md`. The
new provider reference was untracked when the first implementation's pre-commit
Wiki check ran, so its missing generated entries became observable only after
the first commit made it tracked. Both files were refreshed solely with their
canonical generators and were not hand-edited. Task 6 may regenerate them again
after later research-pack changes.

For `T-ARC-004`, no content-scope deviation occurred. The bootstrap progress
log was not edited because the task brief restricted tracked mutation to the
three named documentation files; the required implementer report is the
explicit out-of-band artifact. Graphify was already stale relative to the base
and remained advisory; no code file changed, and refreshing generated Graphify
artifacts would have expanded the approved scope. No generated artifact became
stale under the covering freshness checks.

For `T-ARC-005`, no content-scope deviation occurred. The bootstrap progress
log was not edited because the task brief restricted tracked mutation to the
three named documentation files; the required implementer report is the
explicit out-of-band artifact. The secret-read policy conflict is recorded but
not resolved because Stage 00 policy edits require separate approval. Graphify
was already stale/advisory and was not refreshed for documentation-only work.
No Compose, infra, workflow, script, policy, configuration, credential, secret,
runtime, provider/model, or remote state changed.

## Related Documents

- **Parent Spec**:
  [Agentic Research Pack Consolidation](../../03.specs/122-agentic-research-pack-consolidation/spec.md)
- **Parent Plan**:
  [Agentic Research Pack Consolidation Plan](../plans/2026-07-10-agentic-research-pack-consolidation.md)
- **Previous Task Evidence**:
  [Agentic Research Pack Refresh](./2026-07-05-agentic-research-pack-refresh.md)
- **Canonical Research Pack**:
  [Agentic Engineering Research Pack](../../90.references/research/2026-07-05-agentic-research-pack-refresh/README.md)
- **Research Category**:
  [Research References](../../90.references/research/README.md)
