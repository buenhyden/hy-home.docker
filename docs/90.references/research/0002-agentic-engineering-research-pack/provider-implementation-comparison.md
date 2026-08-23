---
status: draft
artifact_id: reference:agentic-engineering-research:provider-implementation-comparison
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-19
review_cycle: on-source-change
---

# Reference: Claude and Codex Implementation Comparison

## Overview

Claude Code and Codex can implement the same semantic governance while using
different instruction discovery, agent schemas, model controls, hook payloads,
permissions, and settings layers. Common construction therefore means one
provider-neutral contract plus generated or translated native adapters. It does
not mean copying one provider's field names into the other.

This reference satisfies REQ-04 and REQ-05 at tracked baseline
`9a6e09ca06d99ae8234199443974c978640f3ae6`. Provider observations were
reopened from official pages on 2026-08-08; local facts were re-derived from
tracked contracts, adapters, hooks, scripts, and tests.

## Purpose

Compare current upstream Claude/Codex harness and loop mechanisms with the
workspace's tracked adoption, build the required common construction matrix,
and distinguish translation gaps, irreducibly native behavior, local
configuration, repository enforcement, and unverified runtime/remote state.

## Repository Role

This Stage 90 comparison is advisory. It does not change provider policy,
declare live compatibility, or authorize adapter/hook/configuration changes.
Stage 00 remains the canonical contract; provider-native files remain adapters.

## Scope

### In scope

- Claude hooks, subagents, settings, memory/instructions, and model controls.
- Codex hooks, subagents, AGENTS.md, configuration, and model controls.
- Local role/function projections, instruction shims, hooks, dispatcher,
  skills, effort/reasoning overlays, validators, and gaps.
- The exact Spec 137 common construction matrix and all fourteen scope
  implications.

### Out of scope

- User-global config, hook trust state, account entitlement, billing, private
  memory, transcripts, telemetry, installed MCP state, or credentials.
- Live provider invocation, performance/cost evaluation, remote CI, or branch
  protection proof.
- Fixing stale provider contracts or generated surfaces in this Task.

## Definitions / Facts

### Comparison method

- **Upstream capability** means an official vendor page documents the feature
  at retrieval time.
- **Provider-neutral contract** means the semantic owner is tracked outside a
  provider adapter.
- **Tracked state** means the repository contains a definition or
  configuration at the named baseline.
- **Execution/enforcement evidence** means a local command, validator, or
  decision path was inspected or run; a generated file alone is not execution.
- **Runtime/remote proof** requires a separately authorized observation and is
  unverified here.

### Current upstream construction

| Concern              | Claude official observation                                                                                                                                 | Codex official observation                                                                                                        | Evidence boundary                                                                                  |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Instructions         | `CLAUDE.md`/`CLAUDE.local.md`, hierarchical discovery, `.claude/rules/`, imports, and auto memory                                                           | `AGENTS.override.md`/`AGENTS.md`, global then project root-to-CWD discovery, one file per directory, 32 KiB default combined cap  | Instructions shape context; neither page proves this repository's session loaded or followed them. |
| Settings             | Managed, CLI, local, project, user precedence; project `.claude/settings.json` is shareable                                                                 | CLI, project, profile, user, system, built-in precedence; project `.codex/` layers require trust                                  | Tracked project files do not reveal user, managed, trust, or live override state.                  |
| Custom agents        | Markdown body plus YAML frontmatter; required name/description and optional tools, model, permissions, turns, skills, MCP, hooks, memory, effort, isolation | Standalone TOML; required `name`, `description`, `developer_instructions`; agent file acts as a spawned-session config layer      | Schema presence does not prove native acceptance in the installed/runtime version.                 |
| Delegation           | Separate subagent context with agent-specific controls                                                                                                      | ChatGPT/Codex orchestrates child threads; current local releases respond to direct or applicable instruction-triggered delegation | No provider run was executed for this research unit.                                               |
| Model control        | Per-agent `model`; `effort` can override session effort with model-dependent `low` through `max` choices                                                    | Per-agent `model` and `model_reasoning_effort`; current subagent page lists `low`, `medium`, `high`, `xhigh`, `max`, `ultra`      | Product/model controls are mutable and do not prove entitlement or task quality.                   |
| Hooks                | Command, HTTP, prompt, agent, and MCP-tool handlers across 31 named lifecycle events                                                                        | Command hooks across 11 named events; project hooks are trust-gated                                                               | Event count is not local coverage, parity, or blocking depth.                                      |
| Session end          | Native `SessionEnd` event                                                                                                                                   | Native main-thread `SessionEnd`; no subagent firing; output is advisory                                                           | Local Codex contract is stale and does not wire it.                                                |
| Permission/isolation | Settings permissions, permission mode, sandbox/worktree isolation                                                                                           | Parent sandbox/approval context plus per-agent overrides; live parent overrides can be reapplied to children                      | Repository authority remains separate and may be narrower.                                         |

### Measured local adoption

| Surface             | Claude                                                                               | Codex                                                                                                                                                                                         | Shared/canonical state                                               | Proof limit                                                                                                              |
| ------------------- | ------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Root instructions   | `CLAUDE.md` uses four `@` imports                                                    | `AGENTS.md` tells the agent to load four owners in three steps                                                                                                                                | Stage 00 files are common                                            | Claude transcludes; Codex prose requests tool loading. No live context inspection.                                       |
| Role adapters       | 14 Markdown/YAML agents                                                              | 14 TOML agents                                                                                                                                                                                | 14 Stage 00 roles, one supervisor + 13 workers                       | Renderer/validator parity, not runtime acceptance.                                                                       |
| Function bodies     | 24 `.claude/skills/*/SKILL.md`; all 14 roles declare skills                          | 24 shared `.agents/skills/*/SKILL.md`; official Codex guidance documents name/description/path discovery and loads full `SKILL.md` when selected; zero role TOMLs contain `[[skills.config]]` | 24 canonical function records                                        | Official capability plus filesystem projection does not prove this runtime listed, selected, or invoked any local skill. |
| Model overlays      | 14 model fields; effort distribution: 11 `high`, one `low`, one `xhigh`, one omitted | 14 model and 14 `model_reasoning_effort` fields                                                                                                                                               | Five work profiles select provider-native values                     | Entitlement and actual spawned model are unverified.                                                                     |
| Permission overlays | `permissionMode` per role plus project allow/deny settings                           | `sandbox_mode` per role; no tracked project `.codex/config.toml`                                                                                                                              | Two permission profiles and approval boundaries                      | Active provider/user overrides are unverified.                                                                           |
| Hook configuration  | 7 events in `.claude/settings.json`                                                  | 6 events in `.codex/hooks.json`                                                                                                                                                               | Seven semantic events and one shared dispatcher                      | Native firing not observed; 20 cells configured-not-executed, one unsupported.                                           |
| Stop gate           | `blocking` response                                                                  | first `block`, then `continue: false` on active retry                                                                                                                                         | Shared target-doc and uncommitted-work logic                         | Local decision code and tests; no native session executed.                                                               |
| Eval/review         | Same repository fixtures and review rules                                            | Same repository fixtures and review rules                                                                                                                                                     | 11 synthetic fixtures, 16 regressions, independent reviewer contract | No live cross-model evaluation.                                                                                          |

### Corrected local drift

1. **Codex `SessionEnd`:** current official documentation supports the event,
   but `provider-models.yaml` records `native_event: null`, `unsupported`, and
   `not_applicable`; `.codex/hooks.json` omits it; `providers/codex.md` and
   parity reporting repeat the stale limitation. This is an upstream-supported
   local contract/adoption gap, not an irreducible provider limitation.
2. **Semantic-binding depth:** seven events × three providers creates 21
   cells. Twenty are `configured-not-executed`; the stale Codex `session-end`
   cell is `unsupported`. The predecessor statement that all 21 are configured
   is false.
3. **Claude effort overlays:** the Claude provider prose says generated Sonnet
   and Opus adapters emit selected `high` effort. The actual profile-backed
   distribution is 11 high, `doc-writer` low, `workflow-supervisor` xhigh, and
   `drift-detector` with no effort field. The generated adapters match the
   typed work profiles; the prose is stale.
4. **Loop counts:** the only canonical machine-readable retry controls are
   four typed loops. The predecessor's ten prose patterns are an analytical
   taxonomy, not ten additional enforced loop objects, and the phrase
   “remaining six” incorrectly enumerated seven patterns.
5. **Configured versus executed:** provider/model acceptance remains
   `needs_revalidation`; every supported semantic binding remains
   `configured-not-executed`. Renderer and contract tests prove consistency,
   not provider loading, hook firing, model selection, or remote behavior.

## Common Construction Matrix

The columns below reproduce Spec 137's required semantic construction view.
“Translation required” names the adapter work. “Irreducibly provider-native”
identifies behavior that should remain native instead of being normalized into
false parity.

| Semantic capability              | Provider-neutral contract                                    | Claude native                                                   | Codex native                                                                                                                           | Shared implementation                        | Translation required                                                                                                                             | Irreducibly provider-native                                           | Tracked state                                                                                                            | Execution/enforcement evidence                                   | Gap                                                                                                                                                                                                                                    |
| -------------------------------- | ------------------------------------------------------------ | --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Instruction entry and precedence | Bootstrap, provider overlay, scope, JIT stage evidence       | `CLAUDE.md`, imports, hierarchy, `.claude/rules/`               | `AGENTS.md`/override hierarchy, root-to-CWD concatenation                                                                              | Stage 00 documents and concise root shims    | Render/import for Claude; explicit load sequence for Codex                                                                                       | Claude `@` transclusion; Codex fallback/size/trust rules              | Both shims tracked; no nested local rule files used                                                                      | Metadata/repo checks validate files and links                    | Codex does not automatically transclude the four Stage 00 bodies named in prose.                                                                                                                                                       |
| Settings and trust               | Provider config may narrow behavior but not own policy       | JSON scopes and managed/local/project precedence                | TOML/hooks layers and project trust                                                                                                    | Approval and environment rules               | Map semantic permission/event choices into each schema                                                                                           | Managed settings and hook trust stores                                | Claude settings and Codex hooks tracked; no project Codex config                                                         | JSON syntax and provider-surface tests                           | User/managed layers and Codex trust state unverified.                                                                                                                                                                                  |
| Role catalog                     | 14 canonical agent records                                   | `.claude/agents/*.md`                                           | `.codex/agents/*.toml`                                                                                                                 | Renderer consumes Stage 00 agent bodies      | YAML frontmatter/Markdown versus escaped TOML developer instructions                                                                             | Native file schemas and spawn lifecycle                               | 14 + 14 adapters, name-set parity                                                                                        | Renderer and contract tests                                      | Runtime acceptance remains `needs_revalidation`.                                                                                                                                                                                       |
| Function/skill catalog           | 24 canonical function records                                | 24 native skill projections; role `skills` list                 | Skill directories with required `SKILL.md`; initial discovery uses name, description, and path, then loads the full file when selected | Canonical function Markdown and renderer     | Claude attaches named skills to roles; Codex exposes skill directories for explicit `/skills` or `$` selection and implicit description matching | Provider discovery, context-budget omission, and invocation lifecycle | 24 + 24 files; 14 Claude attachments; 24 shared `.agents` projections; zero Codex role-level `[[skills.config]]` entries | Deterministic renderer tests; official Codex capability verified | Role-level attachment is not required for general Codex skill discovery. This Task did not run Codex to prove all 24 local projections were listed, selected, or invoked; the documented initial-list context budget may omit entries. |
| Model selection                  | Five work profiles and status axes                           | `model`                                                         | `model`                                                                                                                                | One profile selection per role/provider      | Exact provider IDs, never aliases copied across vendors                                                                                          | Entitlement, model availability, provider fallback behavior           | 14 fields each; 11-model registry                                                                                        | Contract/renderer tests                                          | Live selected model and quality unverified.                                                                                                                                                                                            |
| Reasoning control                | Profile-specific native control                              | `effort`; omitted for null profile                              | `model_reasoning_effort`                                                                                                               | Work-profile intent                          | Translate semantic depth to allowed native values                                                                                                | Model-dependent Claude effort; Codex product/runtime levels           | Claude 11 high/1 low/1 xhigh/1 omitted; Codex 14 fields                                                                  | Tests reject schema/policy drift                                 | Claude prose stale; runtime overrides and entitlement unverified.                                                                                                                                                                      |
| Delegation/orchestration         | One supervisor, 13 workers, scope and handoff contract       | Native subagents and optional worktree isolation                | Native child threads and orchestration controls                                                                                        | Stage 00 roles and subagent protocol         | Provider-native spawn/task envelopes and result transport                                                                                        | Thread UI, background behavior, nested-agent controls                 | Catalog/projections tracked                                                                                              | Name/schema tests only                                           | No live delegation or depth/concurrency evidence in this Task.                                                                                                                                                                         |
| Tool and filesystem boundary     | Permission profile, approval boundary, path ownership        | `tools`, `disallowedTools`, `permissionMode`, sandbox/isolation | spawned-session config, `sandbox_mode`, parent approvals                                                                               | Shared governance and task ownership         | Tool names and decision payloads differ                                                                                                          | Provider sandbox engines and live overrides                           | Role adapters and Claude settings tracked                                                                                | Static validation and scoped shell sandbox for this Task         | Provider metadata does not prove path enforcement.                                                                                                                                                                                     |
| Semantic hooks                   | Seven event meanings and honest capability/adoption/depth    | Seven configured native events                                  | Six configured native events                                                                                                           | Shared dispatcher and post-tool validator    | Map event name, matcher, payload, timeout, decision schema                                                                                       | Event vocabularies, handler types, trust, timeouts                    | 20 configured-not-executed cells; one unsupported Codex cell                                                             | Contract and native-surface tests                                | Codex `SessionEnd` contract/adoption is stale; native firing unverified.                                                                                                                                                               |
| Pre/post action feedback         | `pre-tool` advisory context and `post-tool` validation       | `PreToolUse` / `PostToolUse`                                    | `PreToolUse` / `PostToolUse`                                                                                                           | Same dispatcher/validator behavior           | Parse provider payload and emit native response keys                                                                                             | Hosted-tool coverage and provider matcher semantics                   | Configured on both                                                                                                       | Script tests and local changed-path routing                      | Not every provider tool is intercepted; no native run proof.                                                                                                                                                                           |
| Stop/completion gate             | Target-doc contract plus logical-commit boundary             | blocking Stop response                                          | block then bounded hard stop using `stop_hook_active`                                                                                  | Same underlying checks                       | Translate decision/retry payload                                                                                                                 | Provider continuation semantics                                       | Configured on both; semantic modes differ                                                                                | Dispatcher code, contract tests, scoped repo checks              | Retry bound depends on provider payload semantics.                                                                                                                                                                                     |
| Session closure                  | Optional sanitized end reminder                              | `SessionEnd`                                                    | Official `SessionEnd`, main thread only, advisory                                                                                      | Shared dispatcher has a session-end handler  | Add a Codex contract binding/config entry with provider timeout/schema through canonical change                                                  | Trigger timing and advisory result semantics                          | Claude configured; Codex absent/stale                                                                                    | No native execution evidence                                     | Requires separate Stage 00/provider fix and revalidation; not changed here.                                                                                                                                                            |
| Evaluation and evidence          | Four typed loops, four evidence fields, independent reviewer | Can invoke shared checks through tools/hooks                    | Can invoke shared checks through tools/hooks                                                                                           | 11 fixtures, 16 regressions, Stage 04 ledger | Only invocation/result transport differs                                                                                                         | Provider outputs, latency, cost, telemetry                            | Synthetic catalog and tests tracked                                                                                      | Deterministic scorer/fixture tests and Task checks               | No live comparative provider baseline or remote enforcement.                                                                                                                                                                           |
| Memory/context continuity        | Canonical lifecycle evidence plus bounded advisory memory    | CLAUDE.md and auto memory                                       | AGENTS.md plus product memory features outside this unit                                                                               | Stage 04/Stage 00 evidence owners            | Provider memory must link to, not copy/override, canonical state                                                                                 | Native auto-memory/storage/retention behavior                         | Repository memory contract tracked; private state excluded                                                               | Repository contract checks bounded files                         | Provider-private memory and cross-session behavior unverified.                                                                                                                                                                         |

### The construction recipe: Stage 00's Canonical Adapter Model

`providers/agents-md.md` §5 (re-read directly 2026-08-14) states the exact
mechanism this workspace already uses to answer "what does it take to build
one common environment, ruleset, and system across providers." It is a
two-tier model, not a two-provider one — Claude, Codex, and Gemini all sit in
Tier 2:

- **Tier 1 — Stage 00 canonical catalog**: `agents/agents/` (roles),
  `agents/functions/` (skills), and `contracts/provider-models.yaml`
  (provider/model/event facts) are the only place a capability is defined.
  The agent and function **name sets** defined there are authoritative, and
  every provider adapter must expose exactly those name sets.
- **Tier 2 — provider runtime adapters**: Claude exposes native Markdown
  agents/skills, Codex exposes native TOML agents plus hook compatibility,
  Gemini exposes native Markdown agents, settings, and one thin event-name
  adapter. None of the three is canonical; each is a translation.

Five adapter rules make the recipe concrete and falsifiable rather than
aspirational:

| Rule              | What it requires                                                                                                                 | Enforcement in this workspace                                                                                                                                                       |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Name-set parity   | Agent/function name sets identical across Stage 00 and every active projection                                                   | `scripts/validation/check-repo-contracts.sh` and `sync-provider-surfaces.sh` per `providers/agents-md.md`                                                                           |
| Role parity       | Each adapter points back to its Stage 00 entry and preserves scope/role intent                                                   | Renderer/contract tests (name-set only; not a semantic-intent check)                                                                                                                |
| Policy parity     | Adapters may change syntax/frontmatter/hook mechanics but not create separate governance, QA, template, model, or workflow rules | No automated semantic-drift detector observed; relies on the "hand-authored policy in generated adapters" prohibition in `.claude/CLAUDE.md`/`.codex/README.md`-equivalent guidance |
| Model parity      | Only the model identifiers and controls `provider-models.yaml` allows                                                            | Renderer/contract tests plus the per-provider "never carry [other vendor] model names" rule in each `providers/*.md`                                                                |
| Validation parity | `check-repo-contracts.sh` and `sync-provider-surfaces.sh` detect drift                                                           | Both scripts are tracked and referenced; this Task did not re-run them as fresh evidence                                                                                            |

The practical answer to "what does it take": one canonical name/role/function
registry that every adapter must name-match; one typed model/event/permission
contract that every adapter must translate rather than reinterpret; and a
renderer plus a drift validator that make the first two machine-checkable
instead of aspirational. What it does **not** take, per this same section, is
uniform native syntax — Claude's YAML-frontmatter Markdown, Codex's TOML, and
Gemini's Markdown-with-different-fields are accepted as permanently
irreducible, and the matrix explicitly warns against "normalizing[ing]" them
into false parity (see the Common Construction Matrix above).

### Exact per-event capability and adoption matrix

Re-derived directly from `contracts/provider-models.yaml` `semantic_events`
(all 7 events × 3 providers = 21 cells; no field estimated or rounded):

| Event                | Claude native / mode                     | Codex native / mode                      | Gemini native / mode                   |
| -------------------- | ---------------------------------------- | ---------------------------------------- | -------------------------------------- |
| `session-start`      | `SessionStart`, advisory                 | `SessionStart`, advisory                 | `SessionStart`, advisory               |
| `pre-tool`           | `PreToolUse`, advisory (can block)       | `PreToolUse`, advisory (can block)       | `BeforeTool`, advisory (can block)     |
| `post-tool`          | `PostToolUse`, advisory                  | `PostToolUse`, advisory                  | `AfterTool`, advisory                  |
| `pre-compaction`     | `PreCompact`, advisory (can block)       | `PreCompact`, advisory (can block)       | `PreCompress`, advisory (cannot block) |
| `user-prompt-intake` | `UserPromptSubmit`, advisory (can block) | `UserPromptSubmit`, advisory (can block) | `BeforeAgent`, advisory (can block)    |
| `stop`               | `Stop`, **blocking**                     | `Stop`, **retry**                        | `AfterAgent`, **deny-retry**           |
| `session-end`        | `SessionEnd`, advisory                   | `null`, **unsupported**                  | `SessionEnd`, advisory                 |

Every "advisory" cell has `runtime_depth: configured-not-executed` and every
"blocking"/"retry"/"deny-retry" cell in the `stop` row is the sole exception
where `repository_hook_mode` differs from `advisory`. Timeout units also
differ by provider construction, not by choice: Claude and Codex declare
seconds (Claude 10–30s per event, Codex a uniform 600s), Gemini declares
milliseconds (a uniform 60000ms) — a native-schema difference the shared
dispatcher does not need to reconcile because timeouts are provider-enforced,
not repository-enforced.

### Construction rule

The common environment is achievable at the semantic layer: canonical roles,
functions, work profiles, permissions, event meanings, loop bounds, validation,
and evidence can share owners. Native instruction loading, file schemas,
settings precedence, trust, sandboxes, payloads, timeouts, and memory remain
provider-specific. The renderer should translate those differences and the
validator should detect drift; neither should claim live provider acceptance.

### Carried source-evidence claims

Source-evidence claims carried forward from the superseded 2026-07-05
research pack on 2026-08-19. Each states what the upstream evidence supports
and, where it matters more, what it does not.

- **The Codex skills pattern has no confirming official source.** Both candidate official pages, `https://learn.chatgpt.com/docs/skills` and `https://learn.chatgpt.com/docs/agent-configuration/skills`, returned HTTP 404 at the recorded revalidation, so the `native_skill_pattern: .agents/skills/**/SKILL.md` value recorded for Codex has no confirming official source and is not treated as established. The per-agent `[[skills.config]]` field remains verified, because it appears on the Codex subagents page. The 404 observation is dated and was not re-fetched here; it is `UNVERIFIED` as a current network fact and carried as the recorded observation.

## Scope Implications

This table applies the [scope application matrix](./scope-application-matrix.md)
to provider construction explicitly.

| Scope          | Provider-comparison implication                                                                      | Disposition / route                                                                            |
| -------------- | ---------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `agentic`      | Owns semantic contracts and native adapter translations.                                             | Implemented definitions; close drift through Stage 00 plus renderer/tests, not this reference. |
| `architecture` | Records why a capability is common, translated, or irreducibly native.                               | Partial; ADR/Spec route, no typed agent.                                                       |
| `backend`      | Provider tool/runtime comparison applies after a backend exists.                                     | Not Applicable now; future approved surface required.                                          |
| `common`       | Independent review checks parity, correctness, and false equivalence.                                | Partial; route through `code-reviewer`.                                                        |
| `docs`         | Owns sourced comparison, mutable-page dates, direct links, and migration evidence.                   | Implemented locally; independent Task 3 review pending.                                        |
| `entry`        | Provider networking or gateway actions require infra ownership and runtime evidence.                 | Partial; no edge/runtime proof.                                                                |
| `frontend`     | Browser/UI provider claims bind only to a real frontend test surface.                                | Partial; Storybook fixture is not product-wide proof.                                          |
| `infra`        | Sandbox, filesystem, network, Compose, and MCP reach must be measured per runtime.                   | Definitions exist; active runtime unverified.                                                  |
| `meta`         | Typed registries and deterministic rendering prevent adapter drift.                                  | Partial; route through docs/Stage 00 because typed meta agent is absent.                       |
| `mobile`       | Native device/provider comparisons need an approved mobile surface.                                  | Not Applicable; none tracked.                                                                  |
| `ops`          | Runtime availability, telemetry, incident, rollback, and provider outages need operational evidence. | Partial; no live observation.                                                                  |
| `product`      | Chooses acceptable provider capability, cost, latency, and lock-in trade-offs.                       | Partial; human/Stage 01 decision required.                                                     |
| `qa`           | Validates schema parity, hooks, fixtures, regressions, and provider-specific behavior.               | Extensive static/local evidence; live comparative eval unverified.                             |
| `security`     | Trust, approvals, sandboxing, hook code, MCP, data handling, and secrets require least privilege.    | Partial; private/secret/runtime/remote state excluded.                                         |

## Sources

All nine minimum official pages were reopened 2026-08-08
(`2026-08-08T15:48:51+09:00`); a second pass reopened the highest-value pages
2026-08-14 (LLM-mediated fetch, noted per-row) to extract schema/precedence
detail not previously recorded. All returned HTTP 200 with no redirect and no
stable revision identifier; every vendor row is external mutable.

| ID | Source | Verification |
| --- | --- | --- |
| C-HOOK | [Claude hooks](https://code.claude.com/docs/en/hooks) | Re-verified 2026-08-14: 31 events, 5 handler types, exact blocking/advisory split, 6 config scopes. |
| C-AGENT | [Claude subagents](https://code.claude.com/docs/en/sub-agents) | Verified 2026-08-08: frontmatter schema, model, effort, permissions, skills, hooks, memory, isolation. |
| C-SET | [Claude settings](https://code.claude.com/docs/en/settings) | Re-verified 2026-08-14: exact 5-level precedence, permission-merge-across-scopes rule, `autoMode` schema. |
| C-MEM | [Claude memory](https://code.claude.com/docs/en/memory) | Re-verified 2026-08-14: full load order, `@import` 4-hop limit, "delivered as user message, not system prompt." |
| O-HOOK | [Codex hooks](https://learn.chatgpt.com/docs/hooks) | Re-verified 2026-08-14: 11-event blocking/advisory split, `stop_hook_active`, main-thread `SessionEnd`. |
| O-AGENT | [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | Re-verified 2026-08-14: TOML fields incl. `skills.config`, reasoning-effort set (`low`–`ultra`), sandbox inheritance. |
| O-INSTR | [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | Re-verified 2026-08-14: discovery order, `AGENTS.override.md`, 32 KiB cap, "prepended not transcluded." |
| O-CONFIG | [Codex config basics](https://learn.chatgpt.com/docs/config-file/config-basic) | Verified 2026-08-08: CLI/project/profile/user/system/default precedence, trusted-project gate. |
| O-MODEL | [Codex models](https://learn.chatgpt.com/docs/models) | Verified 2026-08-08: model/reasoning controls; entitlement not inferred. |
| O-SKILL | [Codex build skills](https://learn.chatgpt.com/docs/build-skills) | Verified 2026-08-08: `SKILL.md` discovery, `/skills`/`$` selection, implicit matching. |
| G-HOOK | [Gemini CLI hooks reference](https://geminicli.com/docs/hooks/reference/) | New 2026-08-14: event list; header/table count mismatch (11 rows vs "12 Total") marked `UNVERIFIED`. |
| G-AGENT | [Gemini CLI subagents](https://geminicli.com/docs/core/subagents/) | New 2026-08-14: frontmatter schema, tool allowlist, no-recursive-subagent rule. |
| WS-CATALOG | [Agent catalog](../../../00.agent-governance/contracts/agent-catalog.yaml) | Re-read 2026-08-14: 14 agents, 24 functions, typed eval fields, per-agent work profiles. |
| WS-PROVIDER | [Provider/model contract](../../../00.agent-governance/contracts/provider-models.yaml) | Re-read 2026-08-14: 3-provider list, all 21 `semantic_events` cells, `local_cli_observation` per provider. |
| WS-MATRIX | [Provider capability matrix](../../../00.agent-governance/rules/provider-capability-matrix.md) | Re-read 2026-08-14: 3-column Claude/Codex/Gemini matrix; source for the Supported/Unsupported/Deferred table. |
| WS-ADAPTER | [`providers/agents-md.md`](../../../00.agent-governance/providers/agents-md.md) §5 | Re-read 2026-08-14: Tier 1/Tier 2 Canonical Adapter Model and the five adapter rules. |
| WS-CLAUDE | [Claude provider notes](../../../00.agent-governance/providers/claude.md) | Tracked mutable; stale uniform-high effort sentence identified. |
| WS-CODEX | [Codex provider notes](../../../00.agent-governance/providers/codex.md) | Tracked mutable; stale `SessionEnd` limitation identified. |
| WS-GEMINI | [Gemini provider notes](../../../00.agent-governance/providers/gemini.md) | Read 2026-08-14: `AfterAgent` deny-retry mechanism, `.gemini/` runtime surface description. |
| WS-GRAPH | [Graphify report](../../../../graphify-out/GRAPH_REPORT.md) | Stale/advisory at `f8a72211`; every lead corroborated against tracked owners. |

## Maintenance

Reopen all cited official pages and re-derive catalogs, adapters, skills, model
controls, hook/event cells, dispatcher behavior, tests, and runtime status when
any owner changes. Record redirects/unavailability as observations, never
silently reuse an earlier retrieval, and keep local adoption gaps separate from
provider limitations.

## Related Documents

- [Harness engineering](./harness-engineering.md)
- [Loop engineering](./loop-engineering.md)
- [Workspace baseline](./workspace-baseline.md)
- [Scope application matrix](./scope-application-matrix.md)
- [Subagent protocol](../../../00.agent-governance/subagent-protocol.md)
- [Spec 137](../../../03.specs/137-agentic-research-pack-rebuild/spec.md)
- [Execution Task](../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md)
