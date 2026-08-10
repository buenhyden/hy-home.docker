---
status: active
artifact_id: reference:agentic-research:harness-engineering
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-07
review_cycle: on-source-change
---

<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/harness-engineering.md -->

# Reference: Harness Engineering for Agentic Workspaces

## Overview

Harness engineering is the design of the controlled environment in which an
agent receives context, selects tools, acts, verifies results, and leaves
reviewable evidence. It includes testing and evaluation, but also isolation,
approval, routing, infrastructure, observability, rollback, and escalation.

This reference describes the current tracked workspace at commit baseline
`1a80b6989304fa7b6a179861a9cad795dd875ca3`. It is advisory: Stage 00,
Compose, scripts, CI, and active lifecycle documents remain authoritative.

## Purpose

Map external harness patterns to exact workspace implementations without
mistaking provider features or research analogies for adopted policy.

## Repository Role

This reference supports the HAFE specification and policy, QA scope, provider
notes, scripts, and execution evidence. It defines no new control.

## Scope

### In Scope

- Context, tools, isolation, approvals, hooks, validation, and evaluation
- Compose/infrastructure and security harness boundaries
- Evidence, rollback, and human escalation
- Current Claude, Codex, and Gemini implementation comparisons

### Out of Scope

- Provider configuration changes or external actions
- New validators, hooks, datasets, scorers, or runtime adapters
- Treating Graphify output as architecture authority

## Definitions / Facts

- A **test harness** supplies repeatable drivers, fixtures, test data, and
  observation around a system under test.
- An **evaluation harness** supplies tasks or datasets, execution, scorers,
  baselines, and regression evidence for system behavior.
- An **agent runtime harness** adds instructions, tool routing, isolation,
  approval, model/role routing, lifecycle interception, and evidence capture.
- An **infrastructure harness** renders and validates Compose projects,
  profiles, networks, secrets references, health checks, and hardening rules.
- A **governance harness** binds those mechanisms to owners, lifecycle
  artifacts, review gates, and human authority.
- Status uses only `Implemented`, `Partially Implemented`, `Missing`, or
  `Not Applicable`. Confidence is based on source directness and coverage.
- The Graphify report was generated from a stale commit and reports a large
  isolated-node set and ambiguous inferred edges. It was used for navigation
  only; every implementation claim below was corroborated against tracked
  sources.

## Provider Harness Criteria

Provider cells in this matrix are retrieval-time **provider facts** revalidated
at `2026-08-07T12:45:40+09:00`. The workspace column is the tracked
**workspace contract** retrieved on 2026-07-26. The final column records gaps
or **task-fit inference**; it must not be read as a provider guarantee or a
policy change.

| Criterion                        | Claude                                                                                                                                                                                                                                                                                                | Codex                                                                                                                                                                                                                                                                                                                                                                                                                        | Gemini                                                                                                                                                                                                                                                                                                             | Workspace common contract                                                                                                                                            | Gap / caveat                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| HAR-01 — Instruction discovery   | `CLAUDE.md`, imports, and memory provide hierarchical context.                                                                                                                                                                                                                                        | `AGENTS.md` is discovered from global scope and then root-to-CWD, with nearer files taking precedence.                                                                                                                                                                                                                                                                                                                       | `GEMINI.md`, imports, and configurable context filenames provide hierarchical context.                                                                                                                                                                                                                             | Thin provider shims route to Stage 00 bootstrap, one scope, and JIT stage evidence.                                                                                  | Context loading is not proof that an instruction was followed; precedence and trust mechanics differ.                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| HAR-02 — Native subagents        | Markdown subagents have separate context and can declare tools, permissions, model, skills/MCP, hooks, memory, and isolation.                                                                                                                                                                         | TOML agents require `name`, `description`, and `developer_instructions`; optional model, effort, sandbox, MCP, and skill fields inherit when omitted.                                                                                                                                                                                                                                                                        | Gemini CLI documents project/user `.gemini/agents/*.md` agents with separate context and bounded tools/MCP/model/run controls.                                                                                                                                                                                     | Stage 00 owns one supervisor and thirteen workers; the renderer emits 14 strict native adapters for Claude, Codex, and Gemini plus 14 shared compatibility adapters. | Schema and drift checks do not prove live provider acceptance. `.agents` is not Gemini native configuration.                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| HAR-03 — Tools and MCP           | Built-in file/shell/web tools and MCP can be restricted through permissions and agent definitions.                                                                                                                                                                                                    | Shell/file/web/MCP execution is subject to sandbox and approval configuration.                                                                                                                                                                                                                                                                                                                                               | Built-in file/shell/web tools, allow/exclude settings, MCP, and confirmation modes are documented.                                                                                                                                                                                                                 | Repository scripts and change-type gates are preferred entry points; external actions remain approval-gated.                                                         | Provider tool names and local role metadata do not enforce repository ownership or authority.                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| HAR-04 — Lifecycle interception  | Command, HTTP, prompt, MCP-tool, and agent handlers span 31 documented event names, 15 of which can block; only the agent handler is marked experimental. Re-enumerated 2026-08-07.                                                                                                                   | Command hooks document 11 events, including `SessionEnd` and `SubagentStart`. Exactly four can stop work: `PreToolUse` (`permissionDecision: "deny"`), `PermissionRequest` (`behavior: "deny"`), `PostToolUse` (`decision: "block"`), and `UserPromptSubmit` (`decision: "block"`). Interception covers Bash, `apply_patch` edits, MCP calls, and other local function tools, and excludes hosted tools such as `WebSearch`. | Gemini CLI documents 11 synchronous command-hook events across tool, agent, session, model, compression, tool-selection, and notification events. Only `BeforeTool` and `AfterAgent` support blocking.                                                                                                             | A typed seven-event contract renders seven Claude, six Codex, and seven Gemini native mappings.                                                                      | The Codex mapping gap is repository-side, not provider-side: `SessionEnd` is documented upstream, but `.codex/hooks.json` still wires only six events and `provider-models.yaml` still records the Codex `session-end` binding as `native_event: null` / `capability_status: unsupported`. Twenty of the 21 tracked bindings carry `runtime_depth: configured-not-executed`; the twenty-first is that same Codex `session-end` binding, which carries `runtime_depth: unsupported`. No tracked file proves live interception for any of them. |
| HAR-05 — Isolation and approval  | Permissions and optional sandboxing are distinct controls whose active configuration is environment-specific.                                                                                                                                                                                         | Sandbox and approval policy are separate; `workspace-write` allows workspace edits while network/out-of-workspace actions require the configured approval path.                                                                                                                                                                                                                                                              | Seatbelt/container sandboxing is optional and disabled by default; confirmation modes can separately allow edits or all tools.                                                                                                                                                                                     | Stage 00 approval and environment rules remain authoritative regardless of provider mode.                                                                            | Tracked files cannot prove user-global configuration, actual runtime mode, network reachability, or unattended-mode safety.                                                                                                                                                                                                                                                                                                                                                                                                                   |
| HAR-06 — Models and reasoning    | Agent definitions select `model` (`sonnet`, `opus`, `haiku`, `fable`, a full ID, or `inherit`; default `inherit`) and set `effort` (`low`, `medium`, `high`, `xhigh`, `max`), which overrides the session value. Available levels depend on the model, and there is no per-subagent thinking setting. | Agent TOMLs set the exact model and `model_reasoning_effort`, which accepts `low`, `medium`, `high`, `xhigh`, `max`, and `ultra`. The two OpenAI surfaces diverge: the Codex product ladder is Low (named Light in the desktop app, web, and IDE), Medium, High, Extra High, Max, and Ultra with no `none`, while the API exposes `none`, `low`, `medium`, `high`, `xhigh`, and `max` with no `ultra`.                       | CLI model selection and settings-level or API thinking controls exist, but the subagent file schema is limited to `name`, `description`, `kind`, `tools`, `mcpServers`, `model`, `temperature`, `max_turns`, and `timeout_mins`, with no reasoning or thinking field. Antigravity selection is a separate surface. | `subagent-protocol.md` owns five exact profiles across the 11-model registry; there is no active fallback graph or implicit substitution.                            | Catalog presence and capability prose do not prove account availability, task quality, cost, or cross-provider equivalence. Codex effort values are surface-specific and must not be copied between the product and the API. A Claude organization `availableModels` allowlist can also substitute a configured subagent model at runtime, which no tracked repository file can observe.                                                                                                                                                      |
| HAR-07 — Evaluation and evidence | Hooks/subagents can run checks and expose lifecycle observations.                                                                                                                                                                                                                                     | Agents, skills, hooks, telemetry, and eval tooling can be composed, but adoption is repository-specific.                                                                                                                                                                                                                                                                                                                     | Headless execution, hooks, tools, and telemetry can support checks and observations.                                                                                                                                                                                                                               | Deterministic validators, CI/local routing, task evidence, 11 exact fixtures, 16 synthetic regressions, calibrated thresholds, and value-free scoring are tracked.   | The repository-semantic gate is synthetic; no provider feature or tracked result proves live comparative model quality.                                                                                                                                                                                                                                                                                                                                                                                                                       |

## Harness Implementation Matrix

| Harness element                    | Workspace implementation                                                                                                                                                                                          | External/provider pattern                                                                                                                                                                              | Status                                         | Required environment/rule                                                                                            | Gap / risk                                                                                                                                                                                                                                             | Canonical owner                                             | Confidence                     |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------- | ------------------------------ |
| Isolation                          | Codex's workspace-write sandbox and approval boundary apply at execution time; Claude and Gemini expose their own optional sandbox controls. Provider configuration is not a shared enforcement layer.            | Codex separates sandbox from approvals; Claude combines permissions with optional sandboxing; Gemini CLI documents optional Seatbelt/container sandboxing.                                             | Partially Implemented                          | `environment-constraints.md` plus the executing provider's active sandbox configuration                              | Tracked provider adapters do not prove the operator's global runtime settings; Gemini and Claude sandboxing may be disabled.                                                                                                                           | `docs/00.agent-governance/rules/environment-constraints.md` | High                           |
| Filesystem and network boundaries  | Stage 00 approval rules protect sensitive surfaces. Root Compose defines one ordinary bridge network (`infra_net`) and three external networks; it does not mark every network internal.                          | Provider sandboxes and permission profiles can restrict filesystem/network access, but support and defaults differ.                                                                                    | Partially Implemented                          | `approval-boundaries.md`, root `docker-compose.yml`, and provider runtime policy                                     | Prior blanket claims that all workspace networks block external bridges were false; external-network reachability and runtime egress require environment-specific proof.                                                                               | `docs/00.agent-governance/rules/approval-boundaries.md`     | High                           |
| Tool routing                       | Stage 00 agents/scopes define intended work; scripts provide canonical local entry points; MCP configuration is provider-local.                                                                                   | Claude subagents can select tools/permissions; Codex custom agents can select sandbox/MCP/skills; Gemini settings support built-ins plus MCP allow/exclude lists.                                      | Partially Implemented                          | `subagent-protocol.md` and `scripts/README.md`                                                                       | Generated Codex TOMLs use strict native fields, including supported model, effort, sandbox, MCP, and skill controls where configured, but they do not enforce a repository path allowlist. Intent metadata must not be described as enforced routing.  | `docs/00.agent-governance/subagent-protocol.md`             | High                           |
| Context and just-in-time discovery | Thin root `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` shims route to Stage 00; bootstrap, scopes, memory, and nested instructions provide progressive context.                                                      | Codex discovers `AGENTS.md` root-to-working-directory; Claude loads `CLAUDE.md`/memory; Gemini loads hierarchical `GEMINI.md` and imports.                                                             | Implemented                                    | `bootstrap.md` and `providers/agents-md.md`                                                                          | Provider precedence, trust, and context-size rules differ; loaded context is not evidence that every linked file was followed.                                                                                                                         | `docs/00.agent-governance/rules/bootstrap.md`               | High                           |
| Agent catalog                      | Stage 00 defines one supervisor and thirteen workers, 24 canonical functions, and generated Claude/Codex/Gemini/shared projections.                                                                               | Claude, Codex, and Gemini CLI document native custom subagents. Gemini CLI public support was announced in v0.38.1 on 2026-04-16.                                                                      | Implemented for tracked definitions            | `agents/README.md` and `subagent-protocol.md`                                                                        | Four role surfaces each contain 14 adapters; 24 functions project only to Claude and shared skills by design. Live provider acceptance remains separate.                                                                                               | `docs/00.agent-governance/agents/README.md`                 | High for tracked definitions   |
| Model routing                      | `subagent-protocol.md` assigns five exact profiles; the typed contract, renderer, adapters, and validators preserve provider-native controls with no active fallback graph or implicit substitution.              | Providers expose model selection and distinct effort/thinking mechanisms; capability and availability change over time.                                                                                | Implemented for tracked policy                 | `subagent-protocol.md`; current model evidence stays in `provider-model-landscape.md`                                | Task-fit mappings are inference, not benchmark proof; provider availability, entitlement, and historical cutoff evidence remain separate.                                                                                                              | `docs/00.agent-governance/subagent-protocol.md`             | High for tracked policy        |
| Lifecycle hooks                    | Shared behavior is owned by the Stage 00 provider-model event contract; Claude, Codex, and Gemini settings call generated/shared hook adapters.                                                                   | Claude documents 31 hook events across command/HTTP/prompt/MCP/agent handlers; Codex documents 11 command-hook events including `SessionEnd`; Gemini CLI documents 11 synchronous command-hook events. | Partially Implemented                          | Provider-model contract, `.claude/settings.json`, `.codex/hooks.json`, `.gemini/settings.json`, and `scripts/hooks/` | Seven Claude and Gemini mappings and six Codex mappings are tracked. Codex now documents `SessionEnd` upstream, so the six-mapping Codex binding is a repository-side gap rather than a provider limitation, and live interception remains unobserved. | `docs/00.agent-governance/contracts/provider-models.yaml`   | High for tracked configuration |
| Approvals and external actions     | Stage 00 requires explicit approval for remote writes, credentials, protected surfaces, publication, push/merge, and paid work.                                                                                   | Claude permissions, Codex approval modes, and Gemini confirmation modes expose different native prompts.                                                                                               | Implemented                                    | `approval-boundaries.md` and the active provider approval mode                                                       | Native approval prompts do not broaden repository authority; unattended modes can bypass provider prompting.                                                                                                                                           | `docs/00.agent-governance/rules/approval-boundaries.md`     | High                           |
| Test and evaluation harnesses      | Validation scripts, controlled pre-commit wrapper, CI/local routing, 11 versioned fixtures, 16 synthetic regressions, deterministic scorers, exact thresholds, and independent review cover repository semantics. | pytest fixtures, HumanEval, LM Evaluation Harness, and Inspect AI separate controlled tasks from scoring and reporting.                                                                                | Implemented for synthetic repository semantics | `scopes/qa.md` and `scripts/validation/`                                                                             | No live provider comparison, latency/cost baseline, or entitlement evidence is claimed.                                                                                                                                                                | `docs/00.agent-governance/scopes/qa.md`                     | High                           |
| Compose and infrastructure harness | Root and tiered Compose files, profiles, secret references, health checks, `validate-docker-compose.sh`, and hardening scripts provide tracked configuration evidence.                                            | Docker Compose defines projects, services, networks, configs, secrets, profiles, and health checks.                                                                                                    | Implemented                                    | Root `docker-compose.yml`, `infra/README.md`, and validation/hardening entry points                                  | Rendered configuration and live service health remain environment-dependent; external networks must exist before use.                                                                                                                                  | `infra/README.md`                                           | High                           |
| Security harness                   | Security scope, secret rules, approval boundaries, GitHub workflow controls, hardening checks, disclosure guidance, and supply-chain checks constrain work.                                                       | Provider sandboxes/permissions complement, but do not replace, repository security policy.                                                                                                             | Partially Implemented                          | `scopes/security.md` and `github-governance.md`                                                                      | Local tracked files cannot prove remote branch protection, secret hygiene in external systems, or every provider's global config.                                                                                                                      | `docs/00.agent-governance/scopes/security.md`               | High                           |
| Observability and evidence         | Command output, diffs, check logs, task evidence, PR checks, SARIF, and progress memory provide review inputs. Graphify is advisory navigation evidence only.                                                     | CI logs, traces, eval reports, and opt-in provider telemetry expose different observation depths.                                                                                                      | Partially Implemented                          | `task-checklists.md` and the relevant Stage 04 task                                                                  | No unified agent trace store exists; provider telemetry can be disabled and must respect privacy/secret rules.                                                                                                                                         | `docs/00.agent-governance/rules/task-checklists.md`         | High                           |
| Rollback and recovery              | Git history, reversible patches, task evidence, runbooks, incidents, and postmortems support recovery; destructive reset is approval-gated.                                                                       | Version control and checkpoint/restore features can preserve state; Gemini CLI checkpointing is optional and disabled by default.                                                                      | Partially Implemented                          | `approval-boundaries.md` and applicable Stage 05 runbook                                                             | Provider checkpoints are not a repository-wide rollback contract; live infrastructure/data rollback is service-specific.                                                                                                                               | `docs/05.operations/runbooks/README.md`                     | High                           |
| Human escalation                   | Clarification duty, scope boundaries, approval gates, review status, and incident routing define when work pauses for a person.                                                                                   | Human-in-the-loop systems pause sensitive actions and resume from a recorded decision.                                                                                                                 | Implemented                                    | `agentic.md`, `approval-boundaries.md`, and task review contract                                                     | A paused provider thread does not itself record an approved decision; the lifecycle artifact must retain evidence.                                                                                                                                     | `docs/00.agent-governance/rules/agentic.md`                 | High                           |

## Claude and Codex Implementation Status

Every element above is provider-neutral by design. This section states what is
actually wired for the two providers whose CLI versions the contract records as
`observed`, so that a reader can tell configured surface from executed
behavior without re-deriving it.

Counts were re-derived from the tracked tree on 2026-08-07. The four provider
surfaces hold 48 tracked files under `.claude/`, 16 under `.codex/`, 17 under
`.gemini/`, and 41 under `.agents/`. `.claude/` shows 49 files on disk because
`.gitignore:102` excludes `.claude/settings.local.json`; that difference is the
personal-override boundary, not drift.

| Criterion | Harness element   | Claude wiring                                                                                                                                                                               | Codex wiring                                                                                                                                                                                                                                                                 | Status                                          | Evidence                                                                            |
| --------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- | ----------------------------------------------------------------------------------- |
| HCS-01    | Event surface     | Seven events in `.claude/settings.json`: `SessionStart`, `PreToolUse`, `PostToolUse`, `SessionEnd`, `Stop`, `PreCompact`, `UserPromptSubmit`.                                               | Six events in `.codex/hooks.json`. `SessionEnd` is absent although Codex documents it.                                                                                                                                                                                       | Claude Implemented; Codex Partially Implemented | `.claude/settings.json`; `.codex/hooks.json`                                        |
| HCS-02    | Wrapper layer     | Seven executable wrappers under `.claude/hooks/`, each dispatching to `scripts/hooks/agent-event-hook.sh`.                                                                                  | No wrapper directory; `.codex/hooks.json` invokes the shared dispatcher directly.                                                                                                                                                                                            | Implemented both, by different mechanisms       | `.claude/hooks/`; `.codex/hooks.json`                                               |
| HCS-03    | Name translation  | None required. The seven semantic event IDs render to Claude-native names one-to-one, and the dispatcher's `case` arms at `scripts/hooks/agent-event-hook.sh:648-673` use those same names. | None required. The six wired Codex names match the same set.                                                                                                                                                                                                                 | Not Applicable                                  | `scripts/hooks/agent-event-hook.sh:648`                                             |
| HCS-04    | Stop semantics    | `repository_hook_mode: blocking`. The dispatcher emits `decision: block` with `reason` and `systemMessage`.                                                                                 | `repository_hook_mode: retry`. The dispatcher branches on `HY_HOME_HOOK_PROVIDER == "codex"`, reads `stop_hook_active` from the payload, and emits `continue: false` with `Stop retry limit reached` once the retry has already fired; otherwise it emits `decision: block`. | Implemented                                     | `scripts/hooks/agent-event-hook.sh:394-412`; `provider-models.yaml` `stop` bindings |
| HCS-05    | Timeouts          | Rendered per event and matched to the contract: 15 s `SessionStart`, 30 s `PostToolUse` and `Stop`, 10 s for the rest.                                                                      | One uniform 600 s value on every binding.                                                                                                                                                                                                                                    | Implemented                                     | `.claude/settings.json`; `provider-models.yaml` `timeout_value`                     |
| HCS-06    | Tool matchers     | `PreToolUse` matches ten tool names including `apply_patch` and `ApplyPatch`; `PostToolUse` matches the five write-class names.                                                             | Provider-side interception covers Bash, `apply_patch`, MCP, and local function tools; hosted tools are excluded upstream.                                                                                                                                                    | Implemented                                     | `.claude/settings.json` matchers                                                    |
| HCS-07    | Role adapters     | 14 strict `.claude/agents/*.md`.                                                                                                                                                            | 14 strict `.codex/agents/*.toml`.                                                                                                                                                                                                                                            | Implemented                                     | `git ls-files .claude/agents .codex/agents`                                         |
| HCS-08    | Function adapters | 24 `.claude/skills/**/SKILL.md`.                                                                                                                                                            | None native; Codex consumes the 24 shared `.agents/skills/**/SKILL.md`.                                                                                                                                                                                                      | Implemented by design                           | `provider-models.yaml` `native_skill_pattern`                                       |
| HCS-09    | Execution proof   | None. All seven bindings carry `runtime_depth: configured-not-executed` and `local_runtime_acceptance: needs_revalidation`.                                                                 | Same.                                                                                                                                                                                                                                                                        | Missing for both                                | `provider-models.yaml`                                                              |

Two observations follow from this table and belong in any adoption argument.
First, Claude and Codex both avoid a translation shim because the repository
chose Claude-native event names as its semantic IDs; only Gemini needs the
generated native-to-semantic adapter and response normalizer in
`.gemini/hooks/agent-event-hook.sh`. That is a deliberate cost shifted onto one
provider, not accidental parity. Second, the contract's own
`runtime_depth` field already distinguishes the four `repository-enforced`
harness loops from the 21 event bindings, 20 of which are
`configured-not-executed` and one `unsupported`, so the
gap between wiring and execution is typed rather than merely narrated.

## Repository Investigation Checklist

Adopting any further harness pattern in this workspace requires resolving these
specific questions first. They are recorded here so the work is scoped rather
than rediscovered.

1. **Codex `SessionEnd`.** Extending the binding touches
   `provider-models.yaml`, the renderer, `.codex/hooks.json`, and the
   dispatcher's `case` list together. Decide whether the semantic
   `session-end` event should stay `required: false` once all three providers
   support it.
2. **Execution evidence.** Nothing in the tree distinguishes a hook that ran
   from a hook that was merely configured. A minimal, secret-free run-marker
   would move nine of these rows off `configured-not-executed`, and needs a
   Stage 03 decision about where such markers live.
3. **Blocking budget.** Only `stop` is blocking; the other six events are
   advisory even where `provider_can_block: true`. Confirm this is intended
   before adding a hook that assumes `pre-tool` can deny.
4. **Provider timeout asymmetry.** Codex's uniform 600 s and Gemini's uniform
   60000 ms are placeholders next to Claude's per-event values. Deriving real
   values requires measuring the dispatcher, which nothing currently does.

## Current-State Assessment

| Category            | Current state                                                                                                                                                                    | Primary comparison                                                                                                         | Status                | Gap                                                                                                                     | Recommendation                                                                                                                          | Canonical owner                                          | Evidence                                                                  | Confidence |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | --------------------- | ----------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------- | ---------- |
| Harness engineering | A layered governance, runtime, validation, infrastructure, and evidence harness is tracked; typed loops and a calibrated synthetic evaluator close repository-semantic feedback. | Official provider, Docker, pytest, and evaluation-harness sources show the same elements with provider-specific mechanics. | Partially Implemented | Live hook interception, global provider/runtime settings, entitlement, and comparative model quality remain incomplete. | Preserve Stage 00 as policy, keep adapters explicit, and route live/runtime evaluation through a separately approved Stage 03/04 chain. | `docs/00.agent-governance/harness-implementation-map.md` | Matrix above; tracked contracts, scripts, adapters, Compose, and Stage 00 | High       |

## Corrections to Stale Claims

- `scripts/hooks/post-tool-validate.sh` does not run `prettier --check`. It
  normalizes whitespace/newlines and conditionally invokes `shfmt`,
  `shellcheck`, `yamllint`, `git diff --check`, and repository validators.
- `scripts/operations/sync-provider-surfaces.sh` already auto-scaffolds Codex
  agent TOMLs and Gemini agent/skill pointers. Adapter generation is therefore
  implemented, although native compatibility and enforcement still need
  provider-specific review.
- Canonical execution artifacts are Stage 04 plans and tasks. Generic
  `implementation_plan.md` and `walkthrough.md` names are not workspace
  lifecycle sources of truth.
- Root Compose networks do not all block external bridges. `infra_net` is a
  normal bridge; `project_net`, `hyhome-external-net`, and `k3d-hyhome` are
  external.
- Codex agent `scope` and `source_catalog` fields are local projection
  metadata. They are not strict filesystem/tool allowlists.
- Added 2026-08-07. The Codex `session-end` gap is repository-side and remains
  open. Codex documents `SessionEnd`, and `.codex/hooks.json` still wires six
  events. Earlier text that framed six mappings as a provider limitation was
  wrong and stays corrected.
- Added 2026-08-07. `high` is not a strengthening of the Claude default.
  Official effort guidance states that setting `effort` to `"high"` produces
  exactly the same behavior as omitting the parameter, so the two Claude
  profiles configured at `high` match the API default rather than raising it.
- Added 2026-08-07. Claude effort is not universally available. The official
  supported-model list for the effort parameter names `claude-fable-5`,
  `claude-mythos-5`, `claude-mythos-preview`, `claude-opus-5`,
  `claude-opus-4-8`, `claude-opus-4-7`, `claude-opus-4-6`, `claude-sonnet-5`,
  `claude-sonnet-4-6`, and `claude-opus-4-5-20251101`, and does not name
  `claude-haiku-4-5-20251001`. The workspace's omission of the Haiku effort key
  is therefore correct against the source, not a rendering shortcut.
- Added 2026-08-07. The `.claude/` surface holds 48 tracked files, not 49. The
  forty-ninth file on disk is the gitignored `.claude/settings.local.json`.

## Adoption Boundary

Research patterns remain advisory. A new hook, permission profile, eval
dataset, scorer, trace backend, or rollback mechanism needs an approved
specification and Stage 04 work. Provider-native controls may strengthen a
run, but they cannot replace Stage 00 authority or grant an external action.

Three boundaries are specific to this workspace and are worth restating because
the matrices above could be misread as clearance.

- **The typed contract is the adoption unit, not the adapter.** A hook,
  effort value, or event mapping is adopted when it exists in
  `docs/00.agent-governance/contracts/provider-models.yaml` and is rendered.
  Hand-editing `.claude/settings.json`, `.codex/hooks.json`, or a generated
  adapter creates drift that the renderer will overwrite.
- **`configured-not-executed` is a real ceiling.** No row in this document may
  be promoted to `Implemented` on runtime grounds until an execution artifact
  exists. Provider documentation proves capability; it never proves that this
  repository's wiring fired.
- **Provider-native blocking is not repository authority.** `provider_can_block`
  records what a provider could do; `repository_hook_mode` records what this
  repository does. Only the Stop gates block here, and a hook that blocks does
  not thereby authorize the action it was protecting.

## Source Rules

- Prefer official provider/framework documentation and tracked canonical
  workspace files.
- Recheck mutable provider behavior before operational use.
- Treat external patterns as comparison, not adopted workspace policy.

## Sources

- [pytest fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html) - NOT RE-VERIFIED on the 2026-08-07 pass: the host returned HTTP 429 to automated retrieval. The fixture concept, dependency-injection model, scope levels, and the stated improvements over xUnit setup and teardown are carried from the earlier verification against the `pytest-dev/pytest` documentation source and were not disproved
- [OpenAI HumanEval](https://github.com/openai/human-eval)
- [EleutherAI LM Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness)
- [Inspect AI](https://inspect.aisi.org.uk/)
- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents)
- [Claude Code hooks](https://code.claude.com/docs/en/hooks)
- [Claude Code permissions](https://code.claude.com/docs/en/permissions)
- [Claude Code sandboxing](https://code.claude.com/docs/en/sandboxing)
- [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Codex hooks](https://learn.chatgpt.com/docs/hooks)
- [Codex configuration](https://learn.chatgpt.com/docs/config-file/config-basic)
- [Codex AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Codex agent approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security)
- [Gemini CLI configuration](https://google-gemini.github.io/gemini-cli/docs/get-started/configuration.html)
- [Gemini CLI subagents](https://github.com/google-gemini/gemini-cli/blob/main/docs/core/subagents.md)
- [Gemini CLI v0.38.1 subagent announcement](https://github.com/google-gemini/gemini-cli/discussions/25562)
- [Gemini CLI hook configuration](https://github.com/google-gemini/gemini-cli/blob/main/docs/reference/configuration.md)
- [Gemini CLI hook authoring](https://github.com/google-gemini/gemini-cli/blob/main/docs/hooks/writing-hooks.md)
- [Gemini CLI v0.26.0 hook announcement](https://github.com/google-gemini/gemini-cli/discussions/17790)
- [Gemini CLI sandboxing](https://google-gemini.github.io/gemini-cli/docs/cli/sandbox.html)
- [Gemini CLI MCP servers](https://google-gemini.github.io/gemini-cli/docs/tools/mcp-server.html)
- [Claude effort parameter](https://platform.claude.com/docs/en/build-with-claude/effort) - supported-model list, the five effort levels, and the statement that `high` equals omitting the parameter
- [OpenAI model catalog](https://developers.openai.com/api/docs/models) - API reasoning-effort values `none` through `max`
- [Codex model and effort guidance](https://learn.chatgpt.com/docs/models) - the six-step product effort ladder including `Ultra`
- [Docker Compose file reference](https://docs.docker.com/reference/compose-file/)
- [Provider model contract](../../../00.agent-governance/contracts/provider-models.yaml)
- [Shared hook dispatcher](../../../../scripts/hooks/agent-event-hook.sh)
- [Post-tool validation script](../../../../scripts/hooks/post-tool-validate.sh)
- [Harness implementation map](../../../00.agent-governance/harness-implementation-map.md)
- [HAFE policy](../../../05.operations/policies/00-workspace/harness-agent-first-engineering.md)

External provider pages were originally retrieved on 2026-07-10 and
revalidated at `2026-08-07T12:45:40+09:00`. Current contract facts retain the
separate `2026-07-26T20:08:18+09:00` retrieval timestamp. Mutable provider
pages prove only the content visible at retrieval; they do not backdate a
feature or model to the fixed 2026-07-10 10:00 KST model cutoff.

One source was not reachable on this pass. The pytest fixtures page returned
HTTP 429 to automated retrieval and is marked accordingly in the list above.
Every workspace count, path, and line reference in this document was re-derived
from the tracked tree on 2026-08-07 rather than carried from earlier text.

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Quarterly, or when provider harness surfaces change
- **Update Trigger**: Provider hooks/agents/security changes, or tracked
  harness implementation changes

## Related Documents

- [research pack index](./README.md)
- [workspace baseline](./workspace-baseline.md)
- [loop engineering](./loop-engineering.md)
- [provider implementation comparison](./provider-implementation-comparison.md)
- [quality, CI, and formatting](./quality-ci-formatting.md)
