---
status: active
artifact_id: reference:agentic-research:provider-implementation-comparison
artifact_type: reference
parent_ids: [spec:123-agentic-engineering-audit-remediation]
reviewed_at: 2026-07-16
review_cycle: on-source-change
---

<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-implementation-comparison.md -->

# Reference: Claude, Codex, and Gemini Provider Implementation Comparison

## Overview

Claude Code, OpenAI Codex, and Gemini CLI expose overlapping agentic coding
features, but their schemas, defaults, lifecycle coverage, and maturity labels
are not interchangeable. This reference compares current official
documentation originally retrieved on 2026-07-10 and revalidated on 2026-07-11
with the tracked provider adapters at baseline
`1a80b6989304fa7b6a179861a9cad795dd875ca3`.

## Purpose

Keep Stage 00 provider-neutral while making provider-specific mechanics,
adapter drift, and evidence gaps visible.

## Repository Role

This reference informs provider notes and adapter maintenance. It does not
change `.claude/`, `.codex/`, `.agents/`, model policy, permissions, hooks, or
global provider configuration.

## Scope and Evidence Method

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
- **Current provider capability** means documented at external revalidation on
  2026-07-11. **Current workspace adoption** means tracked surfaces rechecked
  on 2026-07-16. Neither is a claim about the fixed 2026-07-10 10:00 KST model
  cutoff or live account entitlement.
- **Unknown** means the assigned official sources did not establish the
  capability.

## Provider Capability Matrix

Evidence IDs in provider cells resolve to the official evidence ledger below.
Provider cells are facts, the workspace column is tracked policy/implementation,
and the final column records normalization gaps or task-fit caveats.

| Criterion | Claude | Codex | Gemini | Workspace common contract | Gap / caveat |
| --- | --- | --- | --- | --- | --- |
| PIC-01 — Project instructions | Hierarchical `CLAUDE.md` and memory/import surfaces (`C1`) | `AGENTS.md` discovery from global then root-to-CWD, with nearer files winning (`O1`) | Hierarchical `GEMINI.md`, `@` imports, and configurable context filenames (`G1`) | Thin root shims route to Stage 00. | Preserve provider discovery syntax; loaded context is not enforcement. |
| PIC-02 — Custom agents/subagents | Separate context, prompt, tools, permissions, skills/MCP, memory, hooks, foreground/background, and optional worktree isolation (`C2`) | Built-in/custom agents with parallel app/CLI/IDE operation and inherited sandbox/approval propagation (`O2`) | Built-in/custom subagents with independent context loops, specialized tools, named/automatic delegation, and parallel execution (`G4`) | `agents/README.md` plus `subagent-protocol.md` own 14 roles and handoffs; native adapters exist on all three provider surfaces. | Generation and schema checks do not prove live provider acceptance. `.agents` remains compatibility/shared skills rather than Gemini native configuration. |
| PIC-03 — Custom-agent schema | Markdown frontmatter/body can declare name, description, tools, model, permissions, skills, hooks, memory, MCP, and isolation (`C2`) | TOML requires `name`, `description`, and `developer_instructions`; model/effort/sandbox/MCP/skills fields are optional (`O2`) | `.gemini/agents/*.md` requires name/description and can declare kind, tools, MCP, model, temperature, turns, and timeouts (`G4`) | Stage 00 owns canonical role/scope/model metadata; the renderer emits strict provider-native fields and validators reject drift. | Native schema conformance is tracked; metadata still does not prove runtime permission enforcement or provider acceptance. |
| PIC-04 — Lifecycle hooks | Command, HTTP, prompt, MCP-tool, and agent handlers span a broad lifecycle; agent handlers have distinct trust/maturity caveats (`C3`) | Command hooks span documented events and interception paths (`O3`) | Synchronous command hooks are configured under `.gemini` and cover tool, agent, session, compression, model, and tool-selection events (`G5`) | Stage 00 owns seven semantic events; generated Claude and Gemini mappings cover seven, Codex covers six and marks `SessionEnd` unsupported. | Normalize behavior, not event names; configured mappings do not prove live interception. |
| PIC-05 — Hook coverage | Matchers, inputs, outputs, and blocking semantics vary by handler/event (`C3`) | Interception covers documented simple shell, patch, and MCP paths, not every execution/web path; current docs do not list `SessionEnd` (`O3`) | `BeforeTool`, `AfterTool`, `BeforeAgent`, `AfterAgent`, `SessionStart`, `SessionEnd`, `PreCompress`, `BeforeModel`, `AfterModel`, and `BeforeToolSelection` are documented (`G5`) | Typed mappings preserve provider-specific outputs, blocking modes, and time units; parity freshness is validator-backed. | Tracked completeness is not complete runtime enforcement; Codex `SessionEnd` remains explicitly unsupported. |
| PIC-06 — Configuration layers | User, project, local, managed settings, and permissions (`C4`) | User/project config with trusted-project loading and layered `config.toml` (`O4`) | System, user, workspace, and other settings layers with `.gemini/settings.json` (`G1`) | Repository adapters coexist with user-owned global configuration. | Never infer or overwrite global operator configuration from tracked files. |
| PIC-07 — Permissions/confirmation | Allow/ask/deny rules and permission modes restrict tools and Bash patterns (`C5`) | Approval policy is separate from sandbox; permission profiles add path/network controls (`O4`, `O5`) | Tool allow/exclude settings and default/auto-edit/YOLO confirmation modes (`G1`, `G3`) | `approval-boundaries.md` remains authoritative. | Native settings cannot grant repository authority; unattended modes can remove prompts. |
| PIC-08 — Filesystem sandbox | Optional sandbox complements permissions and can isolate filesystem/network access (`C5`, `C6`) | `workspace-write`, read-only, and full-access modes are configurable independently from approval (`O5`) | Optional Seatbelt or container sandbox; disabled by default (`G2`) | `environment-constraints.md` plus the actual executing provider mode. | Record actual runtime mode; documentation of an optional control is not local implementation evidence. |
| PIC-09 — Network boundary | Permissions/sandbox and managed settings can constrain access (`C5`, `C6`) | Sandbox network access and approvals are independently configurable (`O5`) | Sandbox profiles, confirmation, and MCP settings govern network/tool paths (`G1`–`G3`) | Approval rules plus actual provider/Compose runtime state. | Root Compose includes ordinary and external networks; provider docs do not prove live egress. |
| PIC-10 — MCP | Project/user MCP servers and subagent MCP configuration (`C7`) | MCP servers can be configured globally/project-locally and selected by agent TOMLs (`O2`, `O4`) | `mcpServers` supports server/tool inclusion/exclusion; subagents can declare inline MCP (`G3`, `G4`) | Stage 00/provider notes plus tracked adapters; no shared tracked project MCP baseline. | `.gemini/settings.json` exists for generated hooks, but neither it nor tracked role schemas prove installed global servers, credentials, or enablement. Project Codex MCP config is still absent. |
| PIC-11 — Shell/file/web tools | Built-in reads, edits, shell, web, and MCP extensibility (`C1`, `C7`) | Local shell/file changes, web/MCP, and sandboxed execution (`O4`, `O5`) | Built-in file/shell/web tools and MCP (`G3`, `G4`) | Canonical scripts and change-type QA gates. | Provider tool names do not define ownership, authority, or completion evidence. |
| PIC-12 — Noninteractive automation | CLI/headless use, hooks, CI patterns, and scheduled workflows (`C1`, `C3`) | Noninteractive execution and parallel/batch workflows; CSV batch mode is experimental (`O2`, `O4`) | Headless mode, hooks, and parallel subagents (`G4`–`G6`) | Tracked scripts and GitHub workflows. | Automation authority is limited to the initiating trigger; remote writes remain approval-gated. |
| PIC-13 — Checkpoint/resume | Foreground/background subagents and optional worktree isolation (`C2`) | Subagent threads inherit sandbox and propagate approvals (`O2`) | Shadow-Git checkpointing is optional and disabled by default (`G6`) | Git history, Stage 04 evidence, and Stage 05 runbooks. | Provider state is not repository rollback; resume must refresh current diff and authority. |
| PIC-14 — Telemetry/observability | Hooks, transcripts, and provider logs expose selected lifecycle observations (`C3`) | OpenTelemetry is opt-in and configurable (`O4`) | Local/GCP OTLP telemetry and tool/API metrics are opt-in (`G6`) | Command output, diffs, CI logs, SARIF, and task evidence. | No unified trace backend is tracked; telemetry may be disabled and must respect redaction rules. |
| PIC-15 — Provider adapter generation | Fourteen generated native Markdown agents plus 22 Claude skills/settings are present. | Fourteen generated strict TOML agents plus hooks and 22 shared skills are present. | Fourteen generated native agents/settings/hooks are distinct from `.agents` compatibility and shared skills. | The Stage 00-only renderer reports three providers and zero drift across roles, functions, settings, hooks, and indexes. | Generation plus strict schema checks still do not prove provider runtime acceptance. |
| PIC-16 — Model selection/reasoning | Agents select a model or inherit; effort behavior is model-specific (`C2`) | Agent TOMLs select exact model and reasoning effort (`O2`, `O4`) | CLI configuration selects a model; API thinking and Antigravity selection are distinct surfaces (`G1`) | `subagent-protocol.md` owns exact active values; the cutoff landscape owns evidence. | Model labels and provider prose do not prove account availability, quality, cost, or cross-provider equivalence. |
| PIC-17 — Evaluation integration | Hooks/subagents can invoke tests but do not create a repository semantic eval contract (`C2`, `C3`) | Skills/agents/hooks can invoke eval tooling (`O2`–`O4`) | Headless/tools/hooks/subagents can invoke checks (`G3`–`G5`) | QA scope, deterministic validators, eight exact fixtures, ten synthetic regressions, calibrated thresholds, and independent review form a repository-semantic gate. | The gate is synthetic and makes no live cross-provider model-quality claim. |

## Official Evidence Ledger

| Provider | Surface | Official URL | Documented maturity | Cutoff relevance | Workspace adapter | Confidence / evidence gap |
| --- | --- | --- | --- | --- | --- | --- |
| Claude (`C1`) | Overview, instructions, memory, automation | [Claude Code overview](https://code.claude.com/docs/en/overview), [memory](https://code.claude.com/docs/en/memory) | Current documentation; individual preview labels apply where stated | Mutable pages support retrieval-time state only | Root `CLAUDE.md` and `.claude/` | High |
| Claude (`C2`) | Custom subagents | [Subagents](https://code.claude.com/docs/en/sub-agents) | Current first-class feature; page contains feature-specific version notes | Current behavior, not historical cutoff proof | `.claude/agents/*.md` | High |
| Claude (`C3`) | Hooks | [Hooks](https://code.claude.com/docs/en/hooks) | Command/HTTP/prompt hooks current; agent hooks explicitly experimental | Current behavior | `.claude/settings.json` and repo scripts | High |
| Claude (`C4`) | Configuration | [Configuration](https://code.claude.com/docs/en/configuration) | Current documentation | Current behavior | `.claude/settings.json` | High |
| Claude (`C5`) | Permissions | [Permissions](https://code.claude.com/docs/en/permissions) | Current documentation | Current behavior | Stage 00 approvals plus Claude settings | High |
| Claude (`C6`) | Security/sandbox | [Security](https://code.claude.com/docs/en/security), [sandboxing](https://code.claude.com/docs/en/sandboxing) | Current docs; sandbox configuration is optional | Current behavior | Environment/approval rules; actual global config unknown | Medium: local files cannot prove runtime enablement |
| Claude (`C7`) | MCP | [MCP](https://code.claude.com/docs/en/mcp) | Current documentation | Current behavior | Provider/user configuration | High |
| Codex (`O1`) | Project instructions | [AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md) | Current documentation | Current behavior | Root `AGENTS.md` and nested instruction chain | High |
| Codex (`O2`) | Subagents/custom-agent schema | [Subagents](https://developers.openai.com/codex/subagents) | Current first-class feature; CSV batch mode explicitly experimental | Current behavior | `.codex/agents/*.toml` | High; tracked schema compatibility gap is directly observable |
| Codex (`O3`) | Hooks/events/coverage | [Hooks](https://developers.openai.com/codex/hooks) | Current command hooks; prompt/agent forms parsed but skipped; documented interception limits | Current behavior | `.codex/hooks.json` and repo hook scripts | High; tracked `SessionEnd` lacks current official event support |
| Codex (`O4`) | Config, MCP, telemetry | [Configuration reference](https://developers.openai.com/codex/config-reference) | Current reference; some keys/features carry their own maturity labels | Current behavior | No tracked `.codex/config.toml`; tracked Codex surfaces are `.codex/hooks.json`, agent TOMLs/skills, and Stage 00/provider notes | High; installed/global MCP configuration and credentials remain unknown |
| Codex (`O5`) | Sandbox and approvals | [Agent approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security) | Current documentation; permission profiles documented as beta | Current behavior | Stage 00 approval/environment rules | High; actual global operator profile unknown |
| Gemini (`G1`) | Configuration and context | [Configuration](https://google-gemini.github.io/gemini-cli/docs/get-started/configuration.html), [GEMINI.md](https://google-gemini.github.io/gemini-cli/docs/cli/gemini-md.html) | Current documentation | Current behavior | Root `GEMINI.md`; `.agents` is a separate workspace/Antigravity surface | High |
| Gemini (`G2`) | Sandbox | [Sandboxing](https://google-gemini.github.io/gemini-cli/docs/cli/sandbox.html) | Optional; documented disabled-by-default behavior | Current behavior | No tracked `.gemini` sandbox configuration | High |
| Gemini (`G3`) | Tools and MCP | [MCP servers](https://google-gemini.github.io/gemini-cli/docs/tools/mcp-server.html), [tools](https://google-gemini.github.io/gemini-cli/docs/tools/) | Current documentation | Current behavior | Generated pointers do not configure MCP | High |
| Gemini (`G4`) | Subagents/custom-agent schema | [Subagents](https://github.com/google-gemini/gemini-cli/blob/main/docs/core/subagents.md), [v0.38.1 announcement](https://github.com/google-gemini/gemini-cli/discussions/25562) | Public support announced in v0.38.1 on 2026-04-16; current docs describe built-in/custom agents | Dated announcement precedes the 2026-07-10 evidence date | Fourteen tracked `.gemini/agents/*.md` native adapters are generated separately from `.agents`; schema/drift validation passes, while live CLI acceptance remains unobserved | High for capability and tracked adoption; live provider behavior is not established |
| Gemini (`G5`) | Hooks/events/commands | [Configuration](https://github.com/google-gemini/gemini-cli/blob/main/docs/reference/configuration.md), [writing hooks](https://github.com/google-gemini/gemini-cli/blob/main/docs/hooks/writing-hooks.md), [commands](https://github.com/google-gemini/gemini-cli/blob/main/docs/reference/commands.md), [v0.26.0 announcement](https://github.com/google-gemini/gemini-cli/discussions/17790), [v0.26.0 weekly update](https://github.com/google-gemini/gemini-cli/discussions/17812) | Hooks were announced with v0.26.0 on 2026-01-28 and announced as enabled by default; current docs describe first-class lifecycle events and `/hooks` | Dated announcements precede the 2026-07-10 evidence date | No tracked `.gemini/settings.json` or `.gemini/hooks`; Stage 00 provider notes still specify behavioral fallback | High; native provider capability is established, local enablement/parity is not |
| Gemini (`G6`) | CLI/headless, checkpointing, telemetry | [Gemini CLI docs](https://google-gemini.github.io/gemini-cli/docs/), [checkpointing](https://google-gemini.github.io/gemini-cli/docs/cli/checkpointing.html), [telemetry](https://google-gemini.github.io/gemini-cli/docs/cli/telemetry.html) | Headless operation current; checkpointing optional/default-off; telemetry opt-in | Current behavior | Root shim/provider notes; no common provider checkpoint or telemetry backend | High for documented surfaces; runtime enablement remains unknown |

## Workspace Implementation Status

| Category | Current state | External primary | Comparison | Status | Gap | Recommendation | Canonical owner | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Provider adapter model | Stage 00 owns roles/rules; Claude, Codex, Gemini, and shared compatibility surfaces are deterministic projections from typed contracts. | Official sources in the ledger | All three providers document native subagents and hooks, but schemas, events, sandbox, resume, and runtime acceptance differ. | Partially Implemented | Tracked schema/drift/event validation is current; live native acceptance, complete interception, entitlement, and global configuration remain unobserved. | Retain deterministic projection and validate live provider behavior only through a separately approved runtime-observation task. | `docs/00.agent-governance/subagent-protocol.md` | Tracked adapters, official ledger, provider sync, hook parity, and repository contracts | High for tracked definitions |

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
- Codex `SessionEnd` is explicitly unsupported; `PreToolUse`/`PostToolUse`
  interception is documented as partial.
- Provider adapter auto-scaffolding is present in
  `scripts/operations/sync-provider-surfaces.sh`.
- Gemini CLI custom agents and hooks are official, pre-evidence-date
  capabilities. The tracked workspace now has native `.gemini/agents`,
  settings, and hook wrappers, while live acceptance and behavioral parity
  remain unverified.
- Model freshness/cutoff claims belong to Task 2's provider landscape, not
  this implementation matrix.

## Source Rules

- Use official vendor documentation or official repositories first.
- Record provider-specific maturity/defaults and explicit evidence gaps.
- Treat tracked adapters as implementation evidence only after direct file and
  generator/validator inspection.

## Sources

- Official provider URLs and maturity/evidence caveats are enumerated in the
  [Official Evidence Ledger](#official-evidence-ledger).
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
