---
status: active
artifact_id: reference:agentic-research:provider-implementation-comparison
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-07
review_cycle: on-source-change
---


# Reference: Claude, Codex, and Gemini Provider Implementation Comparison

## Overview

Claude Code, OpenAI Codex, and Gemini CLI expose overlapping agentic coding
features, but their schemas, defaults, lifecycle coverage, and maturity labels
are not interchangeable. This reference compares current official
documentation originally retrieved on 2026-07-10 and currently revalidated at
`2026-08-07T12:45:40+09:00` with the tracked provider adapters at baseline
`ab3a047511c2bf9b5a95ebac737f3ebdb5589384`.

A second, narrower revalidation at `2026-08-07T17:39:18+09:00` re-derived the
Claude and Codex instruction, model-control, hook, and adapter facts against
tracked files at commit `82fc20dafc86b80393352ce53c86efb29748722a` and against
current official Claude and Codex documentation. It added the
[Claude and Codex harness and loop implementation status](#claude-and-codex-harness-and-loop-implementation-status)
and [common Claude/Codex environment](#common-claudecodex-environment-method-elements-and-current-status)
sections, and it corrected two tracked policy statements that disagreed with the
generated adapters they describe.

## Purpose

Keep Stage 00 provider-neutral while making provider-specific mechanics,
adapter drift, and evidence gaps visible.

## Repository Role

This reference informs provider notes and adapter maintenance. It does not
change `.claude/`, `.codex/`, `.agents/`, model policy, permissions, hooks, or
global provider configuration.

## Scope

This section states the evidence method that bounds every claim below.

- Official vendor documentation or official repositories are primary.
- “Unknown” means the assigned current official entry points did not establish
  the capability; it does not mean the provider can never support it.
- Mutable pages support retrieval-time claims only. They do not prove the
  feature existed at a historical cutoff unless a dated release source says so.
- OpenAI claims were revalidated against official OpenAI documentation.
- Graphify was advisory and stale relative to the baseline. Adapter claims were
  checked directly against tracked files and the generator/validator scripts.
- Provider model inventory and cutoff history are owned by
  [provider-model-landscape.md](./provider-model-landscape.md), not duplicated
  here.

## Definitions / Facts

- A **provider-neutral substrate** is the canonical role, rule, approval, QA,
  and evidence contract shared before native adaptation.
- A **provider adapter** translates that substrate into documented native
  files/events without becoming a second policy source.
- **Current provider capability** means documented at external revalidation at
  `2026-08-07T12:45:40+09:00`. **Current workspace adoption** means tracked
  surfaces rechecked against the 2026-07-26 typed contracts. Neither is a claim
  about the fixed 2026-07-10 10:00 KST model cutoff or live account
  entitlement.
- **Unknown** means the assigned official sources did not establish the
  capability.

## Provider Capability Matrix

Evidence IDs in provider cells resolve to the official evidence ledger below.
Provider cells are facts, the workspace column is tracked policy/implementation,
and the final column records normalization gaps or task-fit caveats.

| Criterion                            | Claude                                                                                                                                        | Codex                                                                                                                                                           | Gemini                                                                                                                                                                                            | Workspace common contract                                                                                                                                                                   | Gap / caveat                                                                                                                                                                                      |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PIC-01 — Project instructions        | Hierarchical `CLAUDE.md` and memory/import surfaces (`C1`)                                                                                    | `AGENTS.md` discovery from global then root-to-CWD, with nearer files winning (`O1`)                                                                            | Hierarchical `GEMINI.md`, `@` imports, and configurable context filenames (`G1`)                                                                                                                  | Thin root shims route to Stage 00.                                                                                                                                                          | Preserve provider discovery syntax; loaded context is not enforcement.                                                                                                                            |
| PIC-02 — Custom agents/subagents     | Separate context, prompt, tools, permissions, skills/MCP, memory, hooks, foreground/background, and optional worktree isolation (`C2`)        | Built-in/custom agents with parallel app/CLI/IDE operation and inherited sandbox/approval propagation (`O2`)                                                    | Built-in/custom subagents with independent context loops, specialized tools, named/automatic delegation, and parallel execution (`G4`)                                                            | `agents/README.md` plus `subagent-protocol.md` own 14 roles and handoffs; native adapters exist on all three provider surfaces.                                                             | Generation and schema checks do not prove live provider acceptance. `.agents` remains compatibility/shared skills rather than Gemini native configuration.                                        |
| PIC-03 — Custom-agent schema         | Markdown frontmatter/body can declare name, description, tools, model, permissions, skills, hooks, memory, MCP, and isolation (`C2`)          | TOML requires `name`, `description`, and `developer_instructions`; model/effort/sandbox/MCP/skills fields are optional (`O2`)                                   | `.gemini/agents/*.md` requires name/description and can declare kind, tools, MCP, model, temperature, turns, and timeouts (`G4`)                                                                  | Stage 00 owns canonical role/scope/model metadata; the renderer emits strict provider-native fields and validators reject drift.                                                            | Native schema conformance is tracked; metadata still does not prove runtime permission enforcement or provider acceptance.                                                                        |
| PIC-04 — Lifecycle hooks             | Command, HTTP, prompt, MCP-tool, and agent handlers span 31 documented events, 15 of them blocking; agent handlers remain experimental (`C3`) | Command hooks document 11 events including `SessionEnd` and `SubagentStart` (`O3`)                                                                              | Synchronous command hooks are configured under `.gemini` and cover tool, agent, session, compression, model, and tool-selection events (`G5`)                                                     | Stage 00 owns seven semantic events; generated Claude and Gemini mappings cover seven and Codex covers six.                                                                                 | Normalize behavior, not event names; configured mappings do not prove live interception.                                                                                                          |
| PIC-05 — Hook coverage               | Matchers, inputs, outputs, and blocking semantics vary by handler/event (`C3`)                                                                | Interception covers documented shell, patch, and MCP paths, not hosted tools or every execution/web path; async command hooks are parsed but unsupported (`O3`) | `BeforeTool`, `AfterTool`, `BeforeAgent`, `AfterAgent`, `SessionStart`, `SessionEnd`, `PreCompress`, `BeforeModel`, `AfterModel`, `BeforeToolSelection`, and `Notification` are documented (`G5`) | Typed mappings preserve provider-specific outputs, blocking modes, and time units; parity freshness is validator-backed.                                                                    | Tracked completeness is not complete runtime enforcement. The Codex six-mapping binding predates upstream `SessionEnd` support and is now a repository-side gap.                                  |
| PIC-06 — Configuration layers        | User, project, local, managed settings, and permissions (`C4`)                                                                                | User/project config with trusted-project loading and layered `config.toml` (`O4`)                                                                               | System, user, workspace, and other settings layers with `.gemini/settings.json` (`G1`)                                                                                                            | Repository adapters coexist with user-owned global configuration.                                                                                                                           | Never infer or overwrite global operator configuration from tracked files.                                                                                                                        |
| PIC-07 — Permissions/confirmation    | Allow/ask/deny rules and permission modes restrict tools and Bash patterns (`C5`)                                                             | Approval policy is separate from sandbox; permission profiles add path/network controls (`O4`, `O5`)                                                            | Tool allow/exclude settings and default/auto-edit/YOLO confirmation modes (`G1`, `G3`)                                                                                                            | `approval-boundaries.md` remains authoritative.                                                                                                                                             | Native settings cannot grant repository authority; unattended modes can remove prompts.                                                                                                           |
| PIC-08 — Filesystem sandbox          | Optional sandbox complements permissions and can isolate filesystem/network access (`C5`, `C6`)                                               | `workspace-write`, read-only, and full-access modes are configurable independently from approval (`O5`)                                                         | Optional Seatbelt or container sandbox; disabled by default (`G2`)                                                                                                                                | `environment-constraints.md` plus the actual executing provider mode.                                                                                                                       | Record actual runtime mode; documentation of an optional control is not local implementation evidence.                                                                                            |
| PIC-09 — Network boundary            | Permissions/sandbox and managed settings can constrain access (`C5`, `C6`)                                                                    | Sandbox network access and approvals are independently configurable (`O5`)                                                                                      | Sandbox profiles, confirmation, and MCP settings govern network/tool paths (`G1`–`G3`)                                                                                                            | Approval rules plus actual provider/Compose runtime state.                                                                                                                                  | Root Compose includes ordinary and external networks; provider docs do not prove live egress.                                                                                                     |
| PIC-10 — MCP                         | Project/user MCP servers and subagent MCP configuration (`C7`)                                                                                | MCP servers can be configured globally/project-locally and selected by agent TOMLs (`O2`, `O4`)                                                                 | `mcpServers` supports server/tool inclusion/exclusion; subagents can declare inline MCP (`G3`, `G4`)                                                                                              | Stage 00/provider notes plus tracked adapters; no shared tracked project MCP baseline.                                                                                                      | `.gemini/settings.json` exists for generated hooks, but neither it nor tracked role schemas prove installed global servers, credentials, or enablement. Project Codex MCP config is still absent. |
| PIC-11 — Shell/file/web tools        | Built-in reads, edits, shell, web, and MCP extensibility (`C1`, `C7`)                                                                         | Local shell/file changes, web/MCP, and sandboxed execution (`O4`, `O5`)                                                                                         | Built-in file/shell/web tools and MCP (`G3`, `G4`)                                                                                                                                                | Canonical scripts and change-type QA gates.                                                                                                                                                 | Provider tool names do not define ownership, authority, or completion evidence.                                                                                                                   |
| PIC-12 — Noninteractive automation   | CLI/headless use, hooks, CI patterns, and scheduled workflows (`C1`, `C3`)                                                                    | Noninteractive execution and parallel/batch workflows; CSV batch mode is experimental (`O2`, `O4`)                                                              | Headless mode, hooks, and parallel subagents (`G4`–`G6`)                                                                                                                                          | Tracked scripts and GitHub workflows.                                                                                                                                                       | Automation authority is limited to the initiating trigger; remote writes remain approval-gated.                                                                                                   |
| PIC-13 — Checkpoint/resume           | Foreground/background subagents and optional worktree isolation (`C2`)                                                                        | Subagent threads inherit sandbox and propagate approvals (`O2`)                                                                                                 | Shadow-Git checkpointing is optional and disabled by default (`G6`)                                                                                                                               | Git history, Stage 04 evidence, and Stage 05 runbooks.                                                                                                                                      | Provider state is not repository rollback; resume must refresh current diff and authority.                                                                                                        |
| PIC-14 — Telemetry/observability     | Hooks, transcripts, and provider logs expose selected lifecycle observations (`C3`)                                                           | OpenTelemetry is opt-in and configurable (`O4`)                                                                                                                 | Local/GCP OTLP telemetry and tool/API metrics are opt-in (`G6`)                                                                                                                                   | Command output, diffs, CI logs, SARIF, and task evidence.                                                                                                                                   | No unified trace backend is tracked; telemetry may be disabled and must respect redaction rules.                                                                                                  |
| PIC-15 — Provider adapter generation | Fourteen generated native Markdown agents plus 24 Claude skills/settings are present.                                                         | Fourteen generated strict TOML agents plus hooks and 24 shared skills are present.                                                                              | Fourteen generated native agents/settings/hooks are distinct from `.agents` compatibility and shared skills.                                                                                      | The Stage 00-only renderer reports three providers and zero drift across 14 roles, 24 functions, settings, hooks, and indexes.                                                              | Generation plus strict schema checks still do not prove provider runtime acceptance.                                                                                                              |
| PIC-16 — Model selection/reasoning   | Agents select a model or inherit; effort behavior is model-specific (`C2`)                                                                    | Agent TOMLs select exact model and reasoning effort (`O2`, `O4`)                                                                                                | CLI configuration selects a model; API thinking and Antigravity selection are distinct surfaces (`G1`)                                                                                            | `subagent-protocol.md` owns five exact active profiles across the 11-model registry, with no active fallback graph or implicit substitution; the cutoff landscape owns historical evidence. | Model labels and provider prose do not prove product acceptance, entitlement, quality, cost, or cross-provider equivalence.                                                                       |
| PIC-17 — Evaluation integration      | Hooks/subagents can invoke tests but do not create a repository semantic eval contract (`C2`, `C3`)                                           | Skills/agents/hooks can invoke eval tooling (`O2`–`O4`)                                                                                                         | Headless/tools/hooks/subagents can invoke checks (`G3`–`G5`)                                                                                                                                      | QA scope, deterministic validators, 11 exact fixtures, 16 synthetic regressions, calibrated thresholds, and independent review form a repository-semantic gate.                             | The gate is synthetic and makes no live cross-provider model-quality claim.                                                                                                                       |

## Official Evidence Ledger

| Provider      | Surface                                              | Official URL                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | Documented maturity                                                                                                                                  | Cutoff relevance                                                  | Workspace adapter                                                                                                                                                            | Confidence / evidence gap                                                              |
| ------------- | ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Claude (`C1`) | Overview, instructions, memory, automation           | [Claude Code overview](https://code.claude.com/docs/en/overview), [memory](https://code.claude.com/docs/en/memory)                                                                                                                                                                                                                                                                                                                                                                      | Current documentation; individual preview labels apply where stated                                                                                  | Mutable pages support retrieval-time state only                   | Root `CLAUDE.md` and `.claude/`                                                                                                                                              | High                                                                                   |
| Claude (`C2`) | Custom subagents                                     | [Subagents](https://code.claude.com/docs/en/sub-agents)                                                                                                                                                                                                                                                                                                                                                                                                                                 | Current first-class feature; page contains feature-specific version notes                                                                            | Current behavior, not historical cutoff proof                     | `.claude/agents/*.md`                                                                                                                                                        | High                                                                                   |
| Claude (`C3`) | Hooks                                                | [Hooks](https://code.claude.com/docs/en/hooks)                                                                                                                                                                                                                                                                                                                                                                                                                                          | Command/HTTP/prompt hooks current; agent hooks explicitly experimental                                                                               | Current behavior                                                  | `.claude/settings.json` and repo scripts                                                                                                                                     | High                                                                                   |
| Claude (`C4`) | Configuration                                        | [Settings](https://code.claude.com/docs/en/settings)                                                                                                                                                                                                                                                                                                                                                                                                                                    | Current documentation                                                                                                                                | Current behavior                                                  | `.claude/settings.json`                                                                                                                                                      | High                                                                                   |
| Claude (`C5`) | Permissions                                          | [Permissions](https://code.claude.com/docs/en/permissions)                                                                                                                                                                                                                                                                                                                                                                                                                              | Current documentation                                                                                                                                | Current behavior                                                  | Stage 00 approvals plus Claude settings                                                                                                                                      | High                                                                                   |
| Claude (`C6`) | Security/sandbox                                     | [Security](https://code.claude.com/docs/en/security), [sandboxing](https://code.claude.com/docs/en/sandboxing)                                                                                                                                                                                                                                                                                                                                                                          | Current docs; sandbox configuration is optional                                                                                                      | Current behavior                                                  | Environment/approval rules; actual global config unknown                                                                                                                     | Medium: local files cannot prove runtime enablement                                    |
| Claude (`C7`) | MCP                                                  | [MCP](https://code.claude.com/docs/en/mcp)                                                                                                                                                                                                                                                                                                                                                                                                                                              | Current documentation                                                                                                                                | Current behavior                                                  | Provider/user configuration                                                                                                                                                  | High                                                                                   |
| Claude (`C8`) | Instruction files, imports, rules, AGENTS.md interop | [Memory](https://code.claude.com/docs/en/memory)                                                                                                                                                                                                                                                                                                                                                                                                                                        | Current documentation; no displayed publication or last-updated date                                                                                 | Retrieval-time state only, re-fetched `2026-08-07T17:39:18+09:00` | Root `CLAUDE.md` and its four `@path` imports; no `.claude/rules/`                                                                                                           | High for documented behavior; the page is mutable and undated                          |
| Codex (`O1`)  | Project instructions                                 | [AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md)                                                                                                                                                                                                                                                                                                                                                                                                         | Current documentation                                                                                                                                | Current behavior                                                  | Root `AGENTS.md` and nested instruction chain                                                                                                                                | High                                                                                   |
| Codex (`O2`)  | Subagents/custom-agent schema                        | [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)                                                                                                                                                                                                                                                                                                                                                                                                               | Current first-class feature; `multi_agent` is documented Stable                                                                                      | Current behavior                                                  | Fourteen tracked strict `.codex/agents/*.toml` adapters include the required native description and developer-instruction fields; schema/drift validation passes             | High for tracked schema adoption; live CLI acceptance remains unobserved               |
| Codex (`O3`)  | Hooks/events/coverage                                | [Hooks](https://learn.chatgpt.com/docs/hooks)                                                                                                                                                                                                                                                                                                                                                                                                                                           | Current Stable feature with command-hook trust review and documented event limits                                                                    | Current behavior                                                  | `.codex/hooks.json` and repo hook scripts                                                                                                                                    | High; upstream now documents `SessionEnd`, so the typed binding is behind the provider |
| Codex (`O4`)  | Config, MCP, telemetry                               | [Configuration](https://learn.chatgpt.com/docs/config-file/config-basic)                                                                                                                                                                                                                                                                                                                                                                                                                | Current reference; project-local layers require trust and some keys/features carry their own maturity labels                                         | Current behavior                                                  | No tracked `.codex/config.toml`; tracked Codex surfaces are `.codex/hooks.json`, agent TOMLs/skills, and Stage 00/provider notes                                             | High; installed/global MCP configuration and credentials remain unknown                |
| Codex (`O5`)  | Sandbox and approvals                                | [Agent approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security)                                                                                                                                                                                                                                                                                                                                                                                                 | Current documentation; permission profiles carry no beta label on the current page; the earlier beta qualifier is unverified                         | Current behavior                                                  | Stage 00 approval/environment rules                                                                                                                                          | High; actual global operator profile unknown                                           |
| Gemini (`G1`) | Configuration and context                            | [Generation settings](https://geminicli.com/docs/cli/generation-settings/), [memory](https://geminicli.com/docs/cli/tutorials/memory-management/)                                                                                                                                                                                                                                                                                                                                       | Current documentation                                                                                                                                | Current behavior                                                  | Root `GEMINI.md`; `.agents` is a separate workspace/Antigravity surface                                                                                                      | High                                                                                   |
| Gemini (`G2`) | Sandbox                                              | [Sandboxing](https://google-gemini.github.io/gemini-cli/docs/cli/sandbox.html)                                                                                                                                                                                                                                                                                                                                                                                                          | Optional; documented disabled-by-default behavior                                                                                                    | Current behavior                                                  | No tracked `.gemini` sandbox configuration                                                                                                                                   | High                                                                                   |
| Gemini (`G3`) | Tools and MCP                                        | [MCP servers](https://google-gemini.github.io/gemini-cli/docs/tools/mcp-server.html), [tools](https://google-gemini.github.io/gemini-cli/docs/tools/)                                                                                                                                                                                                                                                                                                                                   | Current documentation                                                                                                                                | Current behavior                                                  | Generated pointers do not configure MCP                                                                                                                                      | High                                                                                   |
| Gemini (`G4`) | Subagents/custom-agent schema                        | [Subagents](https://geminicli.com/docs/core/subagents/), [v0.38.1 announcement](https://github.com/google-gemini/gemini-cli/discussions/25562)                                                                                                                                                                                                                                                                                                                                          | Public support announced in v0.38.1 on 2026-04-16; current docs describe built-in/custom agents                                                      | Dated announcement precedes the 2026-07-10 evidence date          | Fourteen tracked `.gemini/agents/*.md` native adapters are generated separately from `.agents`; schema/drift validation passes, while live CLI acceptance remains unobserved | High for capability and tracked adoption; live provider behavior is not established    |
| Gemini (`G5`) | Hooks/events/commands                                | [Configuration](https://github.com/google-gemini/gemini-cli/blob/main/docs/reference/configuration.md), [writing hooks](https://github.com/google-gemini/gemini-cli/blob/main/docs/hooks/writing-hooks.md), [commands](https://github.com/google-gemini/gemini-cli/blob/main/docs/reference/commands.md), [v0.26.0 announcement](https://github.com/google-gemini/gemini-cli/discussions/17790), [v0.26.0 weekly update](https://github.com/google-gemini/gemini-cli/discussions/17812) | Hooks were announced with v0.26.0 on 2026-01-28 and announced as enabled by default; current docs describe first-class lifecycle events and `/hooks` | Dated announcements precede the 2026-07-10 evidence date          | Tracked `.gemini/settings.json`, `.gemini/hooks`, and fourteen native agent adapters are generated and schema/drift checked; live CLI interception remains unobserved        | High for capability and tracked adoption; live provider behavior is not established    |
| Gemini (`G6`) | CLI/headless, checkpointing, telemetry               | [Gemini CLI docs](https://google-gemini.github.io/gemini-cli/docs/), [checkpointing](https://google-gemini.github.io/gemini-cli/docs/cli/checkpointing.html), [telemetry](https://google-gemini.github.io/gemini-cli/docs/cli/telemetry.html)                                                                                                                                                                                                                                           | Headless operation current; checkpointing optional/default-off; telemetry opt-in                                                                     | Current behavior                                                  | Root shim/provider notes; no common provider checkpoint or telemetry backend                                                                                                 | High for documented surfaces; runtime enablement remains unknown                       |

## Workspace Implementation Status

| Category               | Current state                                                                                                                           | External primary               | Comparison                                                                                                                    | Status                | Gap                                                                                                                                                       | Recommendation                                                                                                                   | Canonical owner                                 | Evidence                                                                                | Confidence                   |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- | --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- | --------------------------------------------------------------------------------------- | ---------------------------- |
| Provider adapter model | Stage 00 owns roles/rules; Claude, Codex, Gemini, and shared compatibility surfaces are deterministic projections from typed contracts. | Official sources in the ledger | All three providers document native subagents and hooks, but schemas, events, sandbox, resume, and runtime acceptance differ. | Partially Implemented | Tracked schema/drift/event validation is current; live native acceptance, complete interception, entitlement, and global configuration remain unobserved. | Retain deterministic projection and validate live provider behavior only through a separately approved runtime-observation task. | `docs/00.agent-governance/subagent-protocol.md` | Tracked adapters, official ledger, provider sync, hook parity, and repository contracts | High for tracked definitions |

## Claude and Codex Harness and Loop Implementation Status

Harness engineering here means the tracked substrate that constrains an agent
before it acts: instruction loading, role definition, tool and permission
surface, and model/effort control. Loop engineering means the tracked mechanics
that observe and re-enter execution: lifecycle events, blocking gates, retry,
compaction, and subagent delegation. The rows below record what each provider
documents today and what this repository actually wires, as two separate facts.

### Harness surfaces

| Harness element      | Claude documented                                                                                                                                       | Codex documented                                                                                                                                                                                        | Tracked here                                                                                          |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Instruction file     | `CLAUDE.md`; Claude Code "reads `CLAUDE.md`, not `AGENTS.md`" (`C8`)                                                                                    | `AGENTS.md`, with `AGENTS.override.md` preferred in each directory (`O1`)                                                                                                                               | Separate root `CLAUDE.md` (205 B) and `AGENTS.md` (243 B) shims                                       |
| Instruction assembly | Discovered files "are concatenated into context rather than overriding each other", ordered filesystem root down to CWD (`C8`)                          | "Codex concatenates files from the root down, joining them with blank lines. Files closer to your current directory override earlier guidance because they appear later in the combined prompt." (`O1`) | One instruction file per provider at repository root; no nested instruction files                     |
| Transclusion         | `@path` imports expand at launch; "Imported files can recursively import other files, with a maximum depth of four hops" (`C8`)                         | No import or include directive documented on the AGENTS.md or subagent pages (`O1`, `O2`)                                                                                                               | `CLAUDE.md` imports four governance files; `AGENTS.md` names the same files as numbered prose steps   |
| Size boundary        | "CLAUDE.md files are loaded in full regardless of length"; guidance targets under 200 lines (`C8`)                                                      | "Codex skips empty files and stops adding files once the combined size reaches the limit defined by `project_doc_max_bytes` (32 KiB by default)." (`O1`)                                                | Claude auto-loads 24,597 B across the shim and its four imports; Codex auto-loads only the 243 B shim |
| Path-scoped rules    | `.claude/rules/*.md` with `paths:` frontmatter load only on matching file reads (`C8`)                                                                  | Nested `AGENTS.md` files scope by directory; no glob-scoped rule file documented (`O1`)                                                                                                                 | Neither `.claude/rules/` nor any nested `AGENTS.md` exists                                            |
| Role definition      | Markdown plus YAML frontmatter in `.claude/agents/` (`C2`)                                                                                              | TOML in `.codex/agents/`; `name`, `description`, and `developer_instructions` are required (`O2`)                                                                                                       | 14 roles on each surface, generated from one Stage 00 catalog                                         |
| Role body transport  | Markdown body is the system prompt (`C2`)                                                                                                               | Body is an escaped `developer_instructions` string (`O2`)                                                                                                                                               | Both carry the same canonical Stage 00 agent body                                                     |
| Model control        | `model` accepts alias, full ID, or `inherit`; omitted defaults to `inherit` (`C2`)                                                                      | `model` overrides parent selection (`O2`)                                                                                                                                                               | Exact IDs only; no alias and no `inherit` in any tracked adapter                                      |
| Effort control       | `effort` options are `low`, `medium`, `high`, `xhigh`, `max`; it "Overrides the session effort level" and "available levels depend on the model" (`C2`) | `model_reasoning_effort` options are `ultra`, `max`, `xhigh`, `high`, `medium`, `low` (`O2`)                                                                                                            | 13 of 14 Claude adapters set `effort`; 14 of 14 Codex adapters set `model_reasoning_effort`           |
| Skill attachment     | Subagent `skills` frontmatter field (`C2`)                                                                                                              | `[[skills.config]]` array with `path` and `enabled` (`O2`)                                                                                                                                              | 14 of 14 Claude adapters declare `skills`; 0 of 14 Codex adapters declare `skills.config`             |
| Sandbox              | Optional sandbox complements permissions (`C5`, `C6`)                                                                                                   | `sandbox_mode` per agent; "Subagents inherit your current sandbox policy" (`O2`, `O5`)                                                                                                                  | Codex adapters set `sandbox_mode`; Claude adapters set `permissionMode` instead                       |

### Loop surfaces

| Loop element              | Claude documented                                                                                          | Codex documented                                                                                              | Tracked here                                                                                               |
| ------------------------- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Event vocabulary          | 31 named events across five handler types (`C3`)                                                           | 11 named events (`O3`)                                                                                        | 7 canonical semantic events in `contracts/provider-models.yaml`                                            |
| Event bindings            | 7 of 7 semantic events bound                                                                               | 6 of 7 semantic events bound                                                                                  | Codex `session-end` is recorded `capability_status: unsupported` with `native_event: null`                 |
| Blocking gate             | `Stop` can block (`C3`)                                                                                    | `Stop` "Can block to continue processing" (`O3`)                                                              | Both route to the shared dispatcher; Claude mode is `blocking`, Codex mode is `retry`                      |
| Retry ceiling             | `stop_hook_active` signals an in-progress stop loop (`C3`)                                                 | Same field documented (`O3`)                                                                                  | The shared dispatcher inspects `stop_hook_active` and emits a `stopReason` when the retry limit is reached |
| Compaction                | `PreCompact` and `PostCompact` (`C3`)                                                                      | `PreCompact` and `PostCompact` (`O3`)                                                                         | Only the pre-compaction event is bound, advisory on both providers                                         |
| Subagent lifecycle        | `SubagentStart` and `SubagentStop`, and `SubagentStop` can block (`C3`)                                    | `SubagentStart` and `SubagentStop` documented (`O3`)                                                          | Neither provider binds a subagent event; there is no per-subagent gate                                     |
| Instruction observability | `InstructionsLoaded` fires "When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context" (`C3`)   | No equivalent event documented (`O3`)                                                                         | Unbound; instruction loading is unobserved on both providers                                               |
| Handler richness          | Command, HTTP, prompt, MCP-tool, and agent handlers; "Agent hooks are experimental and may change." (`C3`) | Command hooks only; "The async option is parsed, but asynchronous command hooks aren't supported yet." (`O3`) | Command handlers only on both providers                                                                    |

### What this means

Claude's harness is the deeper of the two here, because instruction
transclusion, path-scoped rules, per-agent skills, and instruction-load
observability have no tracked Codex equivalent. Codex's harness is the stricter
of the two, because `developer_instructions` is a required field that carries
the whole role body inline rather than by reference, so a Codex adapter cannot
silently lose its instructions to a broken path. The loop surfaces are closer to
parity than the harness surfaces: both providers bind the same six advisory
events plus a blocking stop, and both leave subagent and compaction depth
unused.

## Common Claude/Codex Environment: Method, Elements, and Current Status

A common environment across Claude and Codex is achievable, but only in layers.
Some elements can be one canonical source projected outward; others are
structurally provider-native and must be generated, not shared. The classification
below is derived from the official contracts cited above, not from preference.

### Required elements and their achievable sharing mode

| Element                                    | Sharing mode                              | Basis                                                                                                       | Status here                                                                                                           |
| ------------------------------------------ | ----------------------------------------- | ----------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Policy, roles, scopes, approval boundaries | Single canonical source                   | Neither provider constrains where policy prose lives                                                        | Implemented: `docs/00.agent-governance/` is the sole owner                                                            |
| Role catalog and role bodies               | Single source, projected                  | Both providers accept an externally generated role file                                                     | Implemented: 14 roles projected to `.claude/agents/`, `.codex/agents/`, `.gemini/agents/`, `.agents/agents/`          |
| Function/skill bodies                      | Single source, projected                  | Both providers accept a `SKILL.md` with `name` and `description`                                            | Partially implemented: 24 skills projected to `.claude/skills/` and `.agents/skills/`; no Codex agent references them |
| Model and effort selection                 | Single source, provider-native values     | Enums differ: Claude `low`/`medium`/`high`/`xhigh`/`max`, Codex `low`/`medium`/`high`/`xhigh`/`max`/`ultra` | Implemented: five work profiles in `contracts/provider-models.yaml` resolve to exact per-provider values              |
| Lifecycle behavior                         | Single dispatcher, provider-native events | Event names and payload schemas differ and cannot be aliased                                                | Implemented: both providers call `scripts/hooks/agent-event-hook.sh`                                                  |
| Instruction entry point                    | Provider-native file, shared body         | Claude "reads `CLAUDE.md`, not `AGENTS.md`"; Codex reads `AGENTS.md` and named fallbacks                    | Not implemented: the two shims are separate files with different loading semantics                                    |
| Instruction transclusion                   | Provider-native                           | Claude expands `@path` at launch; Codex documents no import directive                                       | Not shareable; the two shims must express the same chain differently                                                  |
| Permission and sandbox model               | Provider-native                           | Claude uses `permissionMode` plus settings allow/deny; Codex uses `sandbox_mode` plus approval policy       | Implemented per provider; not normalizable to one field                                                               |
| Settings file                              | Provider-native                           | `.claude/settings.json` and `.codex/config.toml` share no schema                                            | Partially implemented: `.claude/settings.json` exists; no tracked `.codex/config.toml`                                |

### The two documented methods for a shared instruction body

Both vendors document a supported way to converge on one instruction file, and
they converge from opposite directions.

1. **Claude reads the Codex file.** The Claude memory page states that if a
   repository "already uses `AGENTS.md` for other coding agents, create a
   `CLAUDE.md` that imports it", showing `@AGENTS.md` followed by
   Claude-specific content, and notes that a symlink also works when no
   Claude-specific content is needed (`C8`).
2. **Codex reads the Claude file.** The Codex AGENTS.md guide documents
   `project_doc_fallback_filenames`, which adds alternate instruction filenames
   to the ones Codex checks in each directory (`O1`). `CLAUDE.md` is not a
   default fallback, so this requires explicit configuration.

Method 1 costs nothing and is available immediately. Method 2 requires a tracked
`.codex/config.toml`, which does not exist here, and Codex project-scoped config
only loads for a trusted project (`O4`).

### Where parity structurally breaks

- **Transclusion asymmetry is the largest gap.** Claude expands its four
  governance imports automatically at session start. Codex has no import
  directive, so the same four files reach a Codex session only if the agent
  chooses to read them with tools. The repository currently states the
  requirement as numbered prose in `AGENTS.md`, which is guidance, not loading.
- **Size ceilings differ in kind.** Claude has no hard cap and only a soft
  200-line recommendation, so the 24,597 B chain loads in full. Codex enforces a
  32 KiB `project_doc_max_bytes` ceiling across the concatenated set and stops
  adding files at the cap. A shared body would therefore have to be sized to the
  Codex ceiling, not the Claude recommendation.
- **Event vocabularies are not aliasable.** Claude documents 31 events and Codex 11. Only the seven canonical semantic events are safely shared, and one of them
  is currently bound on Claude but not Codex.
- **Hook timeouts differ by an order of magnitude.** Tracked Claude bindings use
  10-30 second timeouts; tracked Codex bindings use 600 seconds. Codex documents
  a much tighter ceiling for `SessionEnd` specifically: a "1 second default and
  supports up to 3 seconds" (`O3`). Any future Codex `session-end` binding must
  therefore complete far faster than the existing Claude `SessionEnd` wrapper.
- **Skill attachment is one-directional today.** All 14 Claude adapters declare
  `skills`; no Codex adapter declares `skills.config`, so the 24 shared function
  bodies are projected to Codex's filesystem without being attached to any Codex
  role.
- **Project trust gates the entire Codex surface.** The Codex configuration
  reference states that "If you mark a project as untrusted, Codex skips
  project-scoped `.codex/` layers, including project-local config, hooks, and
  rules." The tracked `.codex/hooks.json` and 14 agent TOMLs therefore have no
  effect in an untrusted checkout, and this repository holds no evidence of the
  trust state.

## Required Normalizations

1. **Policy before adapters.** Stage 00 owns roles, authority, model policy, QA,
   and evidence; provider files implement only their native projection.
2. **Behavior before event names.** Pre-action guidance, post-change
   validation, stop gates, and subagent review may use different provider
   mechanics. Unsupported event names must not be fabricated.
3. **Metadata is not enforcement.** `scope`, `source_catalog`, model, and role
   fields do not prove filesystem/tool restrictions.
4. **Generation is not compatibility.** The sync script prevents projection
   drift but cannot prove that a provider currently accepts every generated
   field or event.
5. **Gemini CLI is not Antigravity.** Native `.gemini/agents/*.md`, settings,
   and hook wrappers are generated separately from `.agents` compatibility and
   shared skills. Tracked adoption does not prove live Gemini acceptance.
6. **Remote state stays unknown until observed.** Branch protection, global
   provider config, telemetry, credentials, and installed MCP servers require
   scoped runtime evidence.

## Stale-Claim Corrections

- Codex tracked agent TOMLs use the current strict schema but do not prove live
  tool/path enforcement.
- Codex `SessionEnd` is now documented upstream. The tracked six-mapping Codex
  binding is therefore a repository-side gap, not a provider limitation.
  `PreToolUse`/`PostToolUse` interception is still documented as partial.
- Provider adapter auto-scaffolding is present in
  `scripts/operations/sync-provider-surfaces.sh`.
- Gemini CLI custom agents and hooks are official, pre-evidence-date
  capabilities. The tracked workspace now has native `.gemini/agents`,
  settings, and hook wrappers, while live acceptance and behavioral parity
  remain unverified.
- Model freshness/cutoff claims belong to Task 2's provider landscape, not
  this implementation matrix.
- Current contract facts retain their exact
  `2026-07-26T20:08:18+09:00` retrieval timestamp; the provider documentation
  revalidation at `2026-08-07T12:45:40+09:00` is a separate observation and
  does not rewrite it.

### Tracked policy statements that disagree with their own adapters

Both statements below were independently re-derived from tracked files at commit
`82fc20dafc86b80393352ce53c86efb29748722a`. In each case the generated adapters
are correct and the prose describing them is wrong, so the corrected state is
recorded here rather than treated as an adapter defect.

- **Claude effort is not uniformly `high`.** `providers/claude.md:31-32` states
  that "Generated Sonnet and Opus adapters therefore emit the selected `high`
  effort." The tracked adapters emit three distinct values. Of the 14 Claude
  adapters, 13 declare `effort` and 11 of those declare `high`;
  `.claude/agents/doc-writer.md:12` declares `low` and
  `.claude/agents/workflow-supervisor.md:10` declares `xhigh`. Both exceptions
  are correct against `contracts/provider-models.yaml`, whose `evidence-research`
  profile assigns `claude-sonnet-5` with effort `low` and whose
  `long-horizon-supervision` profile assigns `claude-opus-5` with effort `xhigh`.
  `.claude/agents/drift-detector.md` correctly omits `effort` because its
  `routine-validation` profile records a null Claude effort. The corrected
  statement is that a generated Sonnet or Opus adapter emits the effort its
  assigned work profile selects, which is `low`, `high`, or `xhigh` today. The
  rest of the same paragraph survives revalidation: the Claude subagent
  reference documents `effort` options `low`, `medium`, `high`, `xhigh`, and
  `max`, states that the field "Overrides the session effort level", lists no
  per-subagent `thinking` field, and notes that "available levels depend on the
  model", which is the documented basis for the Haiku omission.
- **Gemini model identifiers named in prose exist nowhere else.**
  `providers/gemini.md:59-60` states that "Gemini model identifiers follow the
  typed work-profile policy: 3.5 Flash for supervision/complex work and 3.1
  Flash-Lite for read-heavy/repetitive work." Neither identifier appears in
  `contracts/provider-models.yaml`, which contains zero occurrences of a
  non-lite `gemini-3.5-flash` and zero occurrences of any `gemini-3.1` string,
  and neither appears in any of the 14 `.gemini/agents/*.md` adapters. The
  tracked values are `gemini-3.6-flash` in 12 adapters and
  `gemini-3.5-flash-lite` in 2, matching the contract's `adversarial-review`,
  `complex-implementation`, and `long-horizon-supervision` profiles on the one
  side and its `evidence-research` and `routine-validation` profiles on the
  other. `gemini-3.1-flash-lite` survives only as a retired record in
  `docs/90.references/data/governance/agent-governance-retirement-ledger.yaml`
  and in the superseded mapping tables of Spec 132, so the prose appears to
  describe a pre-migration state. The corrected statement is that Gemini
  supervision and complex work use `gemini-3.6-flash` and read-heavy or
  repetitive work uses `gemini-3.5-flash-lite`.

### Repository-side event gap confirmed

`contracts/provider-models.yaml` records the Codex binding for the `session-end`
semantic event as `native_event: null` with `capability_status: unsupported`,
and `.codex/hooks.json` wires six events where `.claude/settings.json` wires
seven. Current Codex documentation lists 11 hook events and documents
`SessionEnd` explicitly, so the contract's `unsupported` status is a stale
repository-side record rather than a provider limitation. Closing it requires
respecting the documented Codex `SessionEnd` timeout, a "1 second default" that
"supports up to 3 seconds", which is far tighter than the 600-second timeout
every other tracked Codex binding uses.

## Source Rules

- Use official vendor documentation or official repositories first.
- Record provider-specific maturity/defaults and explicit evidence gaps.
- Treat tracked adapters as implementation evidence only after direct file and
  generator/validator inspection.

## Sources

- Official provider URLs and maturity/evidence caveats are enumerated in the
  [Official Evidence Ledger](#official-evidence-ledger).
- Every Claude and Codex documentation page cited here was re-fetched at
  `2026-08-07T17:39:18+09:00`. None of them displays a publication or
  last-updated date, so each supports retrieval-time state only.
- [Claude Code memory](https://code.claude.com/docs/en/memory) - `CLAUDE.md`
  discovery, concatenation order, `@path` imports and their four-hop depth
  limit, the AGENTS.md import and symlink interop pattern, `.claude/rules/`
  path scoping, and managed-policy instruction files.
- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents) -
  frontmatter field table, the `effort` enum and its session override, the
  absence of a per-subagent `thinking` field, and the model resolution order.
- [Claude Code hooks](https://code.claude.com/docs/en/hooks) - the 31-event
  list, the five handler types, the experimental label on agent hooks, and the
  `InstructionsLoaded` event.
- [Codex AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md) -
  discovery order, `AGENTS.override.md` precedence, root-down concatenation,
  the 32 KiB `project_doc_max_bytes` default, and
  `project_doc_fallback_filenames`.
- [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) -
  the three required TOML fields, the six-value `model_reasoning_effort` enum,
  `[[skills.config]]`, and sandbox/permission inheritance.
- [Codex hooks](https://learn.chatgpt.com/docs/hooks) - the 11-event list,
  `SessionEnd` support and its 1-second default with a 3-second ceiling, and
  the unsupported async option.
- [Codex configuration basics](https://learn.chatgpt.com/docs/config-file/config-basic) -
  config layer precedence and the project-trust gate on `.codex/` layers.
- UNVERIFIED: no official Codex skills page could be retrieved during this
  revalidation. `https://learn.chatgpt.com/docs/skills` and
  `https://learn.chatgpt.com/docs/agent-configuration/skills` both returned
  HTTP 404. The `native_skill_pattern: .agents/skills/**/SKILL.md` value
  recorded for Codex in `contracts/provider-models.yaml` therefore has no
  confirming official source in this revalidation and is not treated as
  established. The per-agent `[[skills.config]]` field remains verified,
  because it appears on the Codex subagents page.
- UNVERIFIED: the count of Claude hook events that can block could not be
  re-derived deterministically. Repeated retrievals of the same page returned
  13, 14, and 15 for the same table column, so the previously recorded value of
  15 is retained unchanged rather than replaced by an unstable observation. The
  31-event total was stable across retrievals and is treated as established.
- [Subagent protocol](../../../00.agent-governance/subagent-protocol.md) -
  canonical workspace role/model/adapter boundary.
- [Claude provider notes](../../../00.agent-governance/providers/claude.md) -
  tracked Claude adapter boundary.
- [Codex provider notes](../../../00.agent-governance/providers/codex.md) -
  tracked Codex adapter boundary.
- [Gemini provider notes](../../../00.agent-governance/providers/gemini.md) -
  tracked Gemini/Antigravity boundary.

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Monthly during high provider release velocity, otherwise
  quarterly
- **Update Trigger**: Official schema/event/default changes or tracked adapter
  changes

## Related Documents

- [research pack index](./README.md)
- [workspace baseline](./workspace-baseline.md)
- [harness engineering](./harness-engineering.md)
- [loop engineering](./loop-engineering.md)
- [agent model selection](./agent-model-selection.md)
- [subagent protocol](../../../00.agent-governance/subagent-protocol.md)
