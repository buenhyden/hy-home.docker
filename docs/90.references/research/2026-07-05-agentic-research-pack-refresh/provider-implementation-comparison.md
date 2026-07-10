---
status: active
---

<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-implementation-comparison.md -->

# Reference: Claude, Codex, and Gemini Provider Implementation Comparison

## Overview

Claude Code, OpenAI Codex, and Gemini CLI expose overlapping agentic coding
features, but their schemas, defaults, lifecycle coverage, and maturity labels
are not interchangeable. This reference compares current official
documentation retrieved on 2026-07-10 with the tracked provider adapters at
baseline `1a80b6989304fa7b6a179861a9cad795dd875ca3`.

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
- OpenAI pages were retrieved through the official Docs MCP after the local
  Codex manual helper rejected a response missing `x-content-sha256`.
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
- **Current** means documented at retrieval on 2026-07-10; it is not a claim
  about a historical release cutoff.
- **Unknown** means the assigned official sources did not establish the
  capability.

## Provider Capability Matrix

Evidence IDs in provider cells resolve to the official evidence ledger below.

| Capability | Claude | Codex | Gemini | Common workspace substrate | Gap / normalization rule | Evidence date |
| --- | --- | --- | --- | --- | --- | --- |
| Project instructions | Hierarchical `CLAUDE.md` and memory/import surfaces (`C1`) | `AGENTS.md` discovery from global then root-to-CWD, with nearer files winning (`O1`) | Hierarchical `GEMINI.md`, `@` imports, and configurable context filenames (`G1`) | Thin root shims route to Stage 00 | Preserve provider discovery syntax but keep Stage 00 canonical; loaded context is not enforcement | 2026-07-10 |
| Custom agents/subagents | First-class subagents with separate context, prompt, tools, permissions, skills/MCP, memory, hooks, foreground/background, and optional worktree isolation (`C2`) | First-class built-in/custom agents, parallel app/CLI/IDE operation, inherited sandbox and approval propagation (`O2`) | Not established by the reviewed official Gemini CLI configuration, context, tool, and command entry points (`G1`–`G4`) | `agents/README.md` plus `subagent-protocol.md` | Use `Unknown` for Gemini CLI parity; do not infer native agents from workspace pointers or a third-party installer | 2026-07-10 |
| Custom-agent schema | Markdown frontmatter/body can declare name, description, tools, model, permissions, skills, hooks, memory, MCP, and isolation (`C2`) | Current TOML requires `name`, `description`, and `developer_instructions`; optional model/effort/sandbox/MCP/skills fields are documented (`O2`) | No equivalent official schema established in assigned sources (`G1`–`G4`) | Canonical Stage 00 role/scope/model metadata | Tracked Codex TOMLs contain local catalog fields but omit current required description/instructions; generated metadata is not a strict permission schema | 2026-07-10 |
| Lifecycle hooks | Command, HTTP, and prompt hooks across rich lifecycle events; agent hooks are explicitly experimental (`C3`) | Command hooks across documented lifecycle events (`O3`) | No equivalent first-class lifecycle-hook surface established in reviewed entry points (`G1`–`G4`) | Stage 00 hook behavior contract and repo scripts | Normalize desired behavior, not event-name parity; provider-specific events stay adapters | 2026-07-10 |
| Hook coverage and limitations | Hook matchers and permission behavior vary; deterministic command hooks and model-evaluated hooks have different trust properties (`C3`) | Pre/Post interception covers specified simple shell, patch, and MCP paths, not every unified execution/web path; prompt/agent hooks are parsed but skipped (`O3`) | Explicit gap in assigned sources | `rules/hooks.md` and `post-tool-validate.sh` | Hook presence cannot be described as universal enforcement | 2026-07-10 |
| Configuration layers | User, project, local, managed settings and permissions are documented (`C4`) | User/project config with trusted-project loading and layered `config.toml` (`O4`) | System, user, workspace, and other settings layers with `.gemini/settings.json` (`G1`) | Repository adapters plus user-owned global configuration | Never infer global operator config from tracked project files; preserve user config | 2026-07-10 |
| Tool permissions/confirmation | Allow/ask/deny rules and permission modes can restrict tools and Bash patterns (`C5`) | Approval policy is separate from sandbox; permission profiles support path/network rules as beta (`O4`, `O5`) | Tool allow/exclude settings, allowed command confirmation, and default/auto-edit/YOLO approval modes (`G1`, `G3`) | `approval-boundaries.md` | Native settings strengthen execution but never grant repository authority; local role metadata is not an allowlist | 2026-07-10 |
| Filesystem sandbox | Optional sandbox complements permissions and can isolate filesystem/network access (`C5`, `C6`) | Workspace-write sandbox is a documented default pattern with protected `.git`, `.agents`, and `.codex`; policy is configurable (`O5`) | Optional Seatbelt or Docker/Podman sandbox; disabled by default (`G2`) | `environment-constraints.md` | Record actual runtime mode per run; do not call optional/default-off controls implemented merely because docs describe them | 2026-07-10 |
| Network boundary | Permissions/sandbox and managed settings can constrain access (`C5`, `C6`) | Sandbox network and approval behavior are independently configurable (`O5`) | Sandbox/profile and MCP settings govern provider/tool paths; default-off sandbox limits guarantees (`G1`–`G3`) | Approval rules plus actual Compose/provider runtime | Root Compose includes ordinary and external networks; no provider doc proves live infrastructure egress | 2026-07-10 |
| MCP | Project/user MCP servers and subagent MCP configuration are documented (`C7`) | MCP servers can be configured and agent TOMLs can select MCP servers (`O2`, `O4`) | `mcpServers` with server/tool include/exclude controls (`G3`) | Project-local MCP baseline in Codex config; provider-specific adapters elsewhere | Keep credentials out of tracked docs and do not claim parity for transports/auth without direct config evidence | 2026-07-10 |
| Shell/file/web tools | Reads, edits, shell, web, and extensibility through tools/MCP are core product surfaces (`C1`, `C7`) | Local shell/file changes, web/MCP, and sandboxed execution are documented (`O4`, `O5`) | Built-in file/shell/web tools and MCP are documented (`G3`, `G4`) | Canonical scripts and change-type QA gates | Route through repository scripts where available; provider tool names do not define policy | 2026-07-10 |
| Noninteractive automation | Hooks, CLI use, CI patterns, and scheduled `/loop` workflows are current product surfaces (`C1`, `C3`) | Noninteractive execution and parallel/batch agent workflows are documented; CSV batch mode is experimental (`O2`, `O4`) | Headless mode and automation are documented (`G4`) | `scripts/` and tracked GitHub workflows | Automation authority is limited to the initiating trigger; remote writes remain explicit-approval actions | 2026-07-10 |
| Checkpoint/resume | Subagent foreground/background and worktree isolation are documented; no cross-provider checkpoint contract is inferred (`C2`) | Subagent threads inherit sandbox and propagate approvals, but provider state is not repository rollback (`O2`) | Checkpointing uses shadow Git and is disabled by default (`G5`) | Git history, Stage 04 evidence, Stage 05 runbooks | Normalize on repository evidence and revalidation after resume, not provider checkpoint format | 2026-07-10 |
| Telemetry/observability | Hooks and provider logs expose lifecycle observations (`C3`) | OpenTelemetry is opt-in and configurable (`O4`) | Telemetry is opt-in with local/GCP OTLP and documented tool/API metrics (`G6`) | Command output, diffs, CI logs, SARIF, task evidence | Telemetry may be disabled and must obey privacy/secret boundaries; no unified trace backend is tracked | 2026-07-10 |
| Provider adapter generation | Rich tracked Markdown agents/skills and settings are present | Minimal agent TOMLs and hook/config surfaces are tracked | `.agents` contains Antigravity-native rules/workflows plus generated agent/skill pointers, not `.gemini` CLI config | `sync-provider-surfaces.sh` generates Codex TOMLs and Gemini pointers from Stage 00/Claude sources | Auto-scaffolding is implemented; generated output still requires native-schema and behavioral validation | 2026-07-10 |
| Model selection | Agent definitions can select model/`inherit` (`C2`) | Agent TOMLs can select model and reasoning effort (`O2`) | CLI configuration supports model selection (`G1`) | `subagent-protocol.md` owns active mapping; Task 2 owns current landscape evidence | Do not infer task quality from a model label; keep cutoff and capability evidence in Task 2 artifacts | 2026-07-10 |
| Evaluation integration | Hooks/subagents can invoke tests, but provider docs do not make repository semantic evals automatic (`C2`, `C3`) | Skills/agents/hooks can invoke eval tooling, but no repo-wide scorer follows from provider support (`O2`–`O4`) | Headless/tools can invoke tests; no assigned source proves a native semantic eval harness (`G3`, `G4`) | QA scope, validation scripts, agent-output fixtures | Provider executability is not an adopted dataset/scorer/baseline contract | 2026-07-10 |

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
| Codex (`O4`) | Config, MCP, telemetry | [Configuration reference](https://developers.openai.com/codex/config-reference) | Current reference; some keys/features carry their own maturity labels | Current behavior | `.codex/config.toml` and agent TOMLs | High |
| Codex (`O5`) | Sandbox and approvals | [Agent approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security) | Current documentation; permission profiles documented as beta | Current behavior | Stage 00 approval/environment rules | High; actual global operator profile unknown |
| Gemini (`G1`) | Configuration and context | [Configuration](https://google-gemini.github.io/gemini-cli/docs/get-started/configuration.html), [GEMINI.md](https://google-gemini.github.io/gemini-cli/docs/cli/gemini-md.html) | Current documentation | Current behavior | Root `GEMINI.md`; `.agents` is a separate workspace/Antigravity surface | High |
| Gemini (`G2`) | Sandbox | [Sandboxing](https://google-gemini.github.io/gemini-cli/docs/cli/sandbox.html) | Optional; documented disabled-by-default behavior | Current behavior | No tracked `.gemini` sandbox configuration | High |
| Gemini (`G3`) | Tools and MCP | [MCP servers](https://google-gemini.github.io/gemini-cli/docs/tools/mcp-server.html), [tools](https://google-gemini.github.io/gemini-cli/docs/tools/) | Current documentation | Current behavior | Generated pointers do not configure MCP | High |
| Gemini (`G4`) | CLI/headless/commands | [Gemini CLI docs](https://google-gemini.github.io/gemini-cli/docs/), [commands](https://google-gemini.github.io/gemini-cli/docs/cli/commands.html) | Current documentation | Current behavior | Root shim and provider notes | Medium: assigned entry points did not establish hooks/subagents |
| Gemini (`G5`) | Checkpointing | [Checkpointing](https://google-gemini.github.io/gemini-cli/docs/cli/checkpointing.html) | Optional and disabled by default | Current behavior | No common provider checkpoint contract | High |
| Gemini (`G6`) | Telemetry | [Telemetry](https://google-gemini.github.io/gemini-cli/docs/cli/telemetry.html) | Opt-in current feature | Current behavior | No tracked shared provider telemetry backend | High |

## Workspace Implementation Status

| Category | Current state | External primary | Comparison | Status | Gap | Recommendation | Canonical owner | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Provider adapter model | Stage 00 owns roles/rules; Claude, Codex, and Gemini/Antigravity surfaces are distinct tracked projections generated or maintained through repo scripts. | Official sources in the ledger | All providers support project context and tools, but native subagent, hook, schema, sandbox, and resume surfaces differ. | Partially Implemented | Codex schema/event drift, incomplete hook interception, Gemini evidence gaps, and unknown global settings prevent parity claims. | Validate native compatibility separately from catalog parity; update Stage 00 first and regenerate projections. | `docs/00.agent-governance/subagent-protocol.md` | Tracked adapters, `sync-provider-surfaces.sh --check`, `check-repo-contracts.sh` | High |

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
5. **Gemini CLI is not Antigravity.** The workspace `.agents` directory
   contains native rules/workflows and generated reference pointers; it is not
   a tracked `.gemini/settings.json` or proof of Gemini CLI custom agents.
6. **Remote state stays unknown until observed.** Branch protection, global
   provider config, telemetry, credentials, and installed MCP servers require
   scoped runtime evidence.

## Stale-Claim Corrections

- Codex tracked agent TOMLs do not enforce strict tool or path allowlists.
- Codex's tracked `SessionEnd` event is not in the current official hook event
  list; `PreToolUse`/`PostToolUse` interception is documented as partial.
- Provider adapter auto-scaffolding is present in
  `scripts/operations/sync-provider-surfaces.sh`.
- Gemini custom-agent and hook parity remains an official-evidence gap, not a
  blanket claim about all Google agent products.
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
