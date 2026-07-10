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
| T-ARC-003 | Consolidate harness, loop, provider implementation, and AI agent catalogs | doc | VAL-ARC-002, VAL-ARC-005 | PLN-ARC-003 | Capability sources, stale-claim disposition, validators, task review | Documentation implementer | Ready for Review |
| T-ARC-004 | Refresh QA/CI/formatting and automation/pipeline/workflow research | doc | VAL-ARC-002, VAL-ARC-008 | PLN-ARC-004 | Gate/job inventory, evidence classes, validators, task review | Documentation implementer | Todo |
| T-ARC-005 | Refresh Docker Compose/infrastructure and security-governance research | doc/security | VAL-ARC-002, VAL-ARC-008 | PLN-ARC-005 | Rechecked Compose evidence, security status/gap matrix, validators, task review | Documentation implementer | Todo |
| T-ARC-006 | Finalize indexes, supersede duplicate pack, close lifecycle and validation | doc/eval | VAL-ARC-001, VAL-ARC-005, VAL-ARC-006, VAL-ARC-007, VAL-ARC-008, VAL-ARC-009, VAL-ARC-010 | PLN-ARC-006 | Coverage/disposition matrix, final checks, whole-branch review, closure commit | Workflow supervisor | Todo |

## Phase View

### Phase 1: Workspace and Lifecycle Baseline

- [x] T-ARC-001 Refresh workspace baseline, SDLC, document roles, and evidence.

### Phase 2: Provider and Agent Research

- [x] T-ARC-002 Add provider model landscape and task-selection analysis.
- [ ] T-ARC-003 Consolidate harness, loop, provider, and AI agent research
      (**Ready for Review**; independent verdict pending).

### Phase 3: Quality, Infrastructure, and Security

- [ ] T-ARC-004 Refresh QA/CI/formatting and automation research.
- [ ] T-ARC-005 Refresh Compose/infrastructure and security research.

### Phase 4: Consolidation Closure

- [ ] T-ARC-006 Supersede the duplicate pack, close indexes/lifecycle, and
      record final evidence.

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
| <https://google-gemini.github.io/gemini-cli/docs/get-started/configuration.html> | Google / official mutable Gemini CLI documentation | Settings layers, tool controls, approval modes, and model/config surfaces. | No visible page date | 2026-07-10 | Not applicable (non-model source) | Does not prove local `.gemini` settings or Antigravity behavior. | T-ARC-003 |
| <https://google-gemini.github.io/gemini-cli/docs/cli/gemini-md.html> | Google / official mutable Gemini CLI documentation | Hierarchical `GEMINI.md` context, imports, and configurable context filenames. | No visible page date | 2026-07-10 | Not applicable (non-model source) | Context discovery is not tool/permission enforcement. | T-ARC-003 |
| <https://google-gemini.github.io/gemini-cli/docs/tools/mcp-server.html> | Google / official mutable Gemini CLI documentation | MCP server/tool configuration and include/exclude controls. | No visible page date | 2026-07-10 | Not applicable (non-model source) | Does not establish installed servers or native subagents/hooks. | T-ARC-003 |
| <https://google-gemini.github.io/gemini-cli/docs/cli/sandbox.html> | Google / official mutable Gemini CLI documentation | Optional Seatbelt and container sandboxing, disabled by default. | No visible page date | 2026-07-10 | Not applicable (non-model source) | Described capability is not evidence that the workspace enables it. | T-ARC-003 |
| <https://google-gemini.github.io/gemini-cli/docs/cli/checkpointing.html> | Google / official mutable Gemini CLI documentation | Optional shadow-Git checkpointing, disabled by default. | No visible page date | 2026-07-10 | Not applicable (non-model source) | Provider checkpointing is not a shared repository rollback contract. | T-ARC-003 |
| <https://google-gemini.github.io/gemini-cli/docs/cli/telemetry.html> | Google / official mutable Gemini CLI documentation | Opt-in telemetry and local/GCP OTLP metrics. | No visible page date | 2026-07-10 | Not applicable (non-model source) | Telemetry may be disabled and remains privacy/secret constrained. | T-ARC-003 |
| <https://arxiv.org/abs/2210.03629> | Princeton/Google / original ReAct paper | Interleaved reasoning traces and environment actions as a research loop pattern. | 2022-10-06; revised 2023-03-10 | 2026-07-10 | Not applicable (non-model source) | Research foundation only; no repository authority, retry, or evidence policy is adopted from it. | T-ARC-003 |
| <https://arxiv.org/abs/2303.11366> | Northeastern/MIT / original Reflexion paper | Verbal feedback and episodic memory across trials without weight updates. | 2023-03-20; revised 2023-10-10 | 2026-07-10 | Not applicable (non-model source) | Research foundation only; workspace memory remains advisory. | T-ARC-003 |
| <https://github.com/msitarzewski/agency-agents/tree/9f3e401ccd09aa0ee0ef8e015226d0647908e01e> | agency-agents / pinned upstream repository | Point-in-time catalog, agent definitions, integration structure, and MIT-licensed distribution. | Commit 2026-07-09 | 2026-07-10 | Not applicable (non-model source) | Community source; upstream “production-ready” claims are self-claims, not independent evaluation. | T-ARC-003 |
| <https://github.com/msitarzewski/agency-agents/blob/9f3e401ccd09aa0ee0ef8e015226d0647908e01e/README.md> | agency-agents / pinned upstream README | “230+” agents, 17 observed division headings, multi-tool install/conversion, global-directory targets, and desktop auto-update claim. | Commit 2026-07-09 | 2026-07-10 | Not applicable (non-model source) | Counts are point-in-time; README claims do not authorize installation or import. | T-ARC-003 |
| <https://github.com/msitarzewski/agency-agents/blob/9f3e401ccd09aa0ee0ef8e015226d0647908e01e/integrations/codex/README.md> | agency-agents / pinned upstream integration documentation | Converter maps name, description, and Markdown body to minimal Codex TOML fields. | Commit 2026-07-09 | 2026-07-10 | Not applicable (non-model source) | Upstream conversion pattern is comparative only and was not executed. | T-ARC-003 |
| <https://github.com/msitarzewski/agency-agents/blob/9f3e401ccd09aa0ee0ef8e015226d0647908e01e/integrations/gemini-cli/README.md> | agency-agents / pinned upstream integration documentation | Upstream claims Markdown agent installation under `~/.gemini/agents/`. | Commit 2026-07-09 | 2026-07-10 | Not applicable (non-model source) | Third-party integration claim was not independently established by assigned official Gemini CLI entry points. | T-ARC-003 |
| `scripts/operations/sync-provider-surfaces.sh` | Workspace / tracked generator | Generates Codex agent TOMLs and Gemini/Antigravity agent/skill pointers; `--check` detects drift. | Baseline `1a80b698` | 2026-07-10 | Not applicable (repo-local source) | Generation proves projection parity, not provider-native schema acceptance or runtime enforcement. | T-ARC-003 |
| `scripts/hooks/post-tool-validate.sh` | Workspace / tracked hook implementation | Whitespace/newline normalization plus conditional shell/YAML checks, `git diff --check`, and repository validators. | Baseline `1a80b698` | 2026-07-10 | Not applicable (repo-local source) | It does not run `prettier --check` and is selective by changed-file type. | T-ARC-003 |
| `docker-compose.yml` | Workspace / tracked runtime source | Root network definitions: ordinary `infra_net` bridge and three external networks. | Baseline `1a80b698` | 2026-07-10 | Not applicable (repo-local source) | Definition does not prove external-network existence, live connectivity, or egress policy. | T-ARC-003 |
| `docs/00.agent-governance/agents/README.md` and `docs/00.agent-governance/subagent-protocol.md` | Workspace / canonical governance | Fifteen canonical roles, provider projection model, handoff boundary, and active model tiers. | Baseline `1a80b698` | 2026-07-10 | Not applicable (repo-local source) | Active policy remains unchanged; provider runtime compatibility requires separate evidence. | T-ARC-003 |

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

Status is **Ready for Review**. The independent spec-compliance and
document-quality verdicts are pending, so the phase checkbox remains open and
this task is not `Done`. The work is documentation-only; code TDD and Graphify
refresh are not applicable. The editable tracked scope is exactly this task
record plus the four canonical Stage 90 references listed below. Stage 00,
provider adapters, scripts, Compose, runtime configuration, CI, credentials,
remote state, and unrelated documents were inspected but not changed.

### Source and Coverage Inventory

- Source-ledger additions: 28 records — 7 Anthropic official pages, 5 OpenAI
  official pages, 6 Google Gemini CLI official pages, 2 original papers, 4
  immutable upstream `agency-agents` records, and 4 tracked workspace source
  records.
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
- Gemini CLI capability gaps are labeled “not established by assigned official
  sources,” and `.agents` is distinguished from tracked `.gemini` CLI config.
- The prior upstream “16 divisions” claim is corrected to 17 observed README
  division headings at the pinned commit; upstream maturity language remains
  a self-claim.

### Changed Files

- `docs/04.execution/tasks/2026-07-10-agentic-research-pack-consolidation.md`
- `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/harness-engineering.md`
- `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/loop-engineering.md`
- `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-implementation-comparison.md`
- `docs/90.references/research/2026-07-05-agentic-research-pack-refresh/ai-agent-catalogs.md`

### Validation Evidence

- `git diff --check` — exit 0.
- Matrix schema/count check — exit 0: harness `14/14`, loops `10/10`,
  provider capabilities `17/17`, and catalog concerns `12/12`.
- Stale-claim disposition scan — exit 0; matches occur only in explicit
  corrections/gap statements, with no stale affirmative claim retained.
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
  (ignored evidence; exact implementation commit is added after commit).
- Base commit: `1a80b6989304fa7b6a179861a9cad795dd875ca3`.
- Implementation subject:
  `docs(research): consolidate harness and agent research`. The immutable head
  and exact review range are pending commit and will be handed to the
  independent reviewer through the ignored implementer report.
- Implementer spec-compliance self-review: **PASS** — required source classes,
  matrix schemas/counts, tracked inventory, stale corrections, status
  vocabulary, owners, confidence, caveats, and no-import boundary are present.
- Implementer document-quality self-review: **PASS** — official fact,
  workspace implementation, inference/gap, and recommendation are separated;
  every reference retains the canonical template headings and direct sources.
- Independent verdict: **PENDING**. The task must remain **Ready for Review**
  until a separate reviewer records spec-compliance and document-quality
  verdicts for the exact committed range.

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
