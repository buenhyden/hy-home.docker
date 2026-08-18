---
status: draft
artifact_id: reference:agentic-engineering-research:harness-engineering
artifact_type: reference
parent_ids: []
reviewed_at: 2026-08-14
review_cycle: on-source-change
---

# Reference: Harness Engineering

## Overview

Harness engineering designs the controlled environment around an agent: what
context it receives, which role and model it uses, which tools it can invoke,
where mutation is allowed, how lifecycle events route to checks, and what
evidence is required before handoff. A harness is therefore broader than a
test runner. It joins governance, provider adapters, permissions, validation,
evaluation, and operations without making any one of those surfaces the policy
source for the others.

This reference satisfies REQ-01 and REQ-03 at tracked baseline
`9a6e09ca06d99ae8234199443974c978640f3ae6`. It uses the
[workspace baseline](./workspace-baseline.md) for the corpus inventory and the
[scope matrix](./scope-application-matrix.md) for the normative fourteen-scope
axis.

## Purpose

Define the elements and patterns of an agent harness, measure their current
workspace implementation, and state the environment and rules needed to adopt
or change them without confusing definition, configuration, execution,
enforcement, runtime acceptance, or remote proof.

## Repository Role

This Stage 90 reference is advisory analysis. Stage 00 contracts, provider
adapters, scripts, tests, lifecycle documents, and approved runtime evidence
remain authoritative. Recommendations here do not authorize provider,
security, infrastructure, secret, runtime, or remote mutations.

## Scope

### In scope

- Provider-neutral contracts and Claude/Codex projections.
- Instruction loading, roles, functions, model controls, tools, permissions,
  hooks, validation, evaluation, evidence, and escalation.
- Tracked implementation and validator depth at the Task 3 baseline.
- Adoption environment, ownership, failure boundaries, and all fourteen
  persona-scope implications.

### Out of scope

- Inspecting user-global provider configuration, credentials, private state,
  ignored volumes, transcripts, raw logs, or shell history.
- Starting services or proving live provider, model, hook, CI, or remote state.
- Editing Stage 00 contracts, provider adapters, hooks, scripts, or tests.

## Definitions / Facts

### Evidence depth

| Depth                  | What it establishes                                                                       | What it does not establish                                  |
| ---------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| Definition             | A typed or prose contract names an element and owner.                                     | That an adapter contains it or a runtime loads it.          |
| Configuration          | A tracked provider file contains a native setting or binding.                             | Trust, entitlement, event firing, or successful execution.  |
| Local execution        | A named local command ran and returned an observed result.                                | CI, provider service, or remote enforcement.                |
| Repository enforcement | A deterministic validator rejects contract drift or a repository gate returns a decision. | Provider acceptance unless the native runtime was observed. |
| Runtime proof          | A scoped provider or service run demonstrates behavior.                                   | Other accounts, machines, branches, or future versions.     |
| Remote proof           | A remote control-plane observation demonstrates enforcement.                              | Permanent policy or unobserved environments.                |

The tracked harness intentionally stops at different depths by element. The
four typed loops are marked `repository-enforced`; semantic event bindings are
configuration records, and provider/model `runtime_acceptance` remains
`needs_revalidation`.

### Harness element model

| Element                   | Required contract                                                                          | Current tracked implementation                                                                         | Evidence depth                                     | Gap or adoption condition                                                                                                 |
| ------------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ | -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Canonical authority       | One provider-neutral owner for roles, functions, models, events, permissions, and evidence | Stage 00 catalogs and rules                                                                            | Definition + repository validation                 | Change the canonical owner before regenerating adapters; never patch policy into one adapter.                             |
| Context and instructions  | Deterministic entry, precedence, scope, and freshness                                      | `AGENTS.md`, `CLAUDE.md`, provider overlays, bootstrap, one primary scope, JIT stage docs              | Definition + tracked configuration                 | Loading remains behavioral context, not hard enforcement.                                                                 |
| Role/function routing     | Registered role, scope, permissions, inputs, outputs, and functions                        | 14 agents, 24 functions, one supervisor and 13 workers                                                 | Definition + generated projection validation       | Six normative scopes remain outside the typed scope enum; `architecture` is enum-only.                                    |
| Provider/model routing    | Work profile, provider-native model/control, fallback and status axes                      | Five work profiles over an 11-model registry; native Claude/Codex/Gemini fields                        | Definition + configuration                         | Entitlement, runtime acceptance, quality, latency, and cost are unverified.                                               |
| Tools and skills          | Least-privilege tool set and canonical reusable function body                              | Claude role tools and skills; Codex sandbox and full developer instructions; 24 projected skill bodies | Configuration + parity validation                  | Tool names and skill presence do not prove invocation or filesystem enforcement.                                          |
| Permission and isolation  | Explicit authority distinct from technical sandboxing                                      | Read-only/workspace-write profiles, approval rules, Claude permission settings, Codex sandbox fields   | Definition + configuration                         | Active session overrides and user-global modes are private/runtime facts.                                                 |
| Lifecycle interception    | Semantic event mapped honestly to a native event and shared behavior                       | Seven semantic events; Claude wires seven, Codex wires six; shared dispatcher                          | Configuration + repository Stop decision logic     | Codex `SessionEnd` is upstream-supported but stale/unsupported in the local contract and absent from `.codex/hooks.json`. |
| Validation and evaluation | Deterministic change-type checks, fixtures, scorers, thresholds, and independent review    | Harness wrapper, repository contracts, 11 synthetic fixtures, 16 regressions                           | Local executable + repository enforcement when run | Synthetic semantics do not prove comparative provider quality.                                                            |
| Evidence and handoff      | Sanitized fields, exact commands/results, rollback, skips, reviewer independence           | Stage 04 Task, four permitted evidence fields, prohibited-sensitive-evidence set                       | Definition + reviewed task evidence                | Raw logs, credentials, tokens, auth files, secret values, and shell history stay excluded.                                |
| Runtime/remote operations | Explicit target, approval, pre-check, rollback, post-check, and durable outcome            | Rules and runbooks describe the boundary                                                               | Definition only for this Task                      | No live provider, Compose, CI, branch-protection, or deployment proof was collected.                                      |

### Measured local construction

The following counts were re-derived from complete tracked owners, not from
Graphify or predecessor prose.

| Surface                        |                                   Count or state | Tracked owner and derivation                                                                                  |
| ------------------------------ | -----------------------------------------------: | ------------------------------------------------------------------------------------------------------------- |
| Canonical agents               |                                               14 | `contracts/agent-catalog.yaml` `agents`                                                                       |
| Canonical functions            |                                               24 | `contracts/agent-catalog.yaml` function records                                                               |
| Catalog projection memberships |                                              104 | 14 agents × four targets plus 24 functions × two targets                                                      |
| Native role adapters           | 14 Claude, 14 Codex, 14 Gemini, 14 compatibility | Complete provider directories and renderer tests                                                              |
| Skill projections              |         24 Claude-native and 24 shared `.agents` | Complete `SKILL.md` directories and renderer tests                                                            |
| Harness layers                 |                                                8 | `contracts/provider-models.yaml` `harness_layers`                                                             |
| Workflow states                |                                                8 | `discover` through `handoff`                                                                                  |
| Typed harness loops            |                                                4 | `harness_loops`, each `repository-enforced`                                                                   |
| Semantic events                |                                                7 | `semantic_events`                                                                                             |
| Semantic binding cells         |                                               21 | Seven events × three providers: 20 `configured-not-executed`, one `unsupported`                               |
| Evaluation corpus              |                      11 fixtures, 16 regressions | `agent-catalog.yaml` `evaluation.fixture_count`/`regression_count` typed fields, corroborated by tests        |
| Tracked hook configuration     |                      7 Claude, 6 Codex, 7 Gemini | `.claude/settings.json`, `.codex/hooks.json`, `.gemini/settings.json`                                         |
| Hookify rule catalog           |                      19 rules (7 block, 12 warn) | `docs/00.agent-governance/rules/hooks/hookify.*.md`; **definition only**, no tracked local runtime projection |

Graphify was built from `f8a72211` and is stale. Its navigation was
corroborated against the listed tracked owners; it supplied no count or
implementation conclusion.

### Control-plane surface: `.claude/settings.json`

Re-read directly at this baseline. The tracked project file configures a
narrower slice of upstream capability than Claude Code exposes:

| Upstream capability (2026-08-14) | This workspace's configuration | Gap |
| --- | --- | --- |
| `permissions.allow`/`deny`/`ask`, merged across scopes (any-scope deny wins; allow accumulates) | `allow`: 18 entries — `$defaults` plus 17 `Bash(...)` prefixes (four general tools `git`/`python3`/`grep`/`rg`; six read-only docker/compose probes; seven named repository scripts, of which five are under `scripts/validation/`, one under `scripts/hardening/`, and one under `scripts/knowledge/`). Corrected 2026-08-18: this cell previously read "8 `Bash(...)` prefixes" while its own parenthetical enumerated thirteen and the tracked file holds seventeen. The undercount came from counting only `docker compose ...` among the docker probes and only `scripts/validation/` among the named scripts, without stating either narrowing; `deny`: 4 destructive prefixes (`docker system prune`, `rm -rf`, `docker compose down`, `docker volume rm`) | No `ask` entries; every command runs unprompted or is denied. `.claude/settings.local.json` (git-ignored, not part of the tracked corpus) adds a small personal `allow` list. |
| `autoMode.allow`/`soft_deny`/`hard_deny`/`classifyAllShell` | Only `autoMode.allow: ["$defaults"]` | `soft_deny`/`hard_deny`/`classifyAllShell` unset; relies on the built-in classifier plus `permissions`. |
| `deniedMcpServers` | `MCP_DOCKER`, `notebooklm` | Matches upstream schema; no other MCP allow/ask list configured. |
| Managed > CLI args > local > project > user precedence (exact order, 2026-08-14) | Only project (tracked) and local (git-ignored) layers observed | Managed policy, CLI overrides, and user-scope `~/.claude/settings.json` are private/session facts outside this Task's reach. |
| `outputStyle` | `"hy-home"`, bound to `.claude/output-styles/hy-home.md` | Matches a Claude-only capability; Codex/Gemini follow it as a behavioral contract per the capability matrix. |

### Enforcement boundary: dispatcher and validator mechanics

Two tracked executables carry out the constructed behavior behind the seven
configured hook events; both were read directly rather than inferred from
their names.

`scripts/hooks/agent-event-hook.sh` dispatches on the event name (`SessionStart`,
`PreToolUse`, `PostToolUse`, `SessionEnd`, `Stop`, `PreCompact`,
`UserPromptSubmit`) and is invoked identically by the Claude thin wrappers
(`.claude/hooks/*.sh`, each a two-line `exec` into this script) and by
`.codex/hooks.json` (same script, `HY_HOME_HOOK_PROVIDER=codex` set). Per
event:

- `SessionStart` prints branch, changed-file count, last commit, and the
  `infra/` directory listing as a `systemMessage` — advisory context only.
- `PreToolUse` emits **advisory** `systemMessage`/`additionalContext` for up to
  five independent triggers matched by changed-path pattern: a stale Graphify
  graph present, a Docker Compose path, a `.agents/` compatibility-surface
  path, a `docs/00.agent-governance/memory/` path, a target-stage doc path
  (`docs/01`–`docs/05`, `docs/90`), and a `README.md` path (with a separate
  infra-service-readiness message when a Compose/Dockerfile marker sits beside
  it). None of these five triggers can block the tool call; they only prepend
  guidance text.
- `PostToolUse` delegates entirely to `scripts/hooks/post-tool-validate.sh`.
- `SessionEnd` and `PreCompact` each print a state-snapshot reminder
  (branch/last-commit/uncommitted-count plus a fixed checklist); both are
  advisory.
- `Stop` is the **only** locally blocking gate. It runs two Python-coded
  checks in sequence — `template_stop_gate` (blocks when a changed
  target-stage doc fails `check-repo-contracts.sh`) and
  `logical_commit_stop_gate` (blocks when task-owned changes remain
  uncommitted, bypassed only by `AGENT_ALLOW_UNCOMMITTED_STOP=1`) — and only
  calls `session_end` if both pass.
- `UserPromptSubmit` keyword-matches the incoming prompt against seven named
  Stage 00 functions (`compose-stack-agent`, `requirements-to-design-agent`,
  `execution-plan-agent`, `task-breakdown-agent`, `ops-runbook-agent`,
  `knowledge-map-agent`, `policy-gate-agent`) and, on a hit, injects their
  catalog paths as `additionalContext`. This is routing advice, not tool
  selection or execution.

`scripts/hooks/post-tool-validate.sh` (invoked by `PostToolUse` on both
providers) reads the hook's JSON payload for changed paths, then runs a fixed
set of **path-triggered, not always-on** checks: trailing-whitespace/newline
normalization for `.md/.sh/.yml/.yaml/.json` files (skipped entirely under
`--check`); `shfmt -w` and `shfmt -d`/`shellcheck` for changed shell files
**only if those binaries are present on `PATH`** — there is no hard failure
when they are absent, so shell-style enforcement is opportunistic, not
guaranteed; `yamllint` under the same present-or-skip rule; `git diff --check`
whitespace-conflict scanning; `python3 -m json.tool` validation of exactly
four tracked JSON/config files (`.claude/settings.json`, `.codex/hooks.json`,
`.gemini/settings.json`, `infra/tech-stack.versions.json`) when one of them
changed; `bash -n` syntax-checking of `.claude/hooks/*.sh`, `.gemini/hooks/*.sh`,
and `scripts/**/*.sh` when a hook/script shell file changed;
`validate-docker-compose.sh` when a Compose/`infra/`/`.env.example` path
changed; and `check-repo-contracts.sh` plus `check-doc-traceability.sh` when a
governance-relevant path changed (root shims, `docs/*`, `.github/*`,
`.claude/*`, `.codex/*`, `.gemini/*`, `.agents/*`, `scripts/*`, or the
tech-stack version file). This is the closest thing this workspace has to a
"local execution" evidence depth for style and contract drift, and it fires
only on the file patterns above — an edit outside those patterns produces no
local check at all beyond the whitespace pass.

### Hookify: a defined rule catalog without a tracked local projection

`docs/00.agent-governance/rules/hooks/` holds 19 canonical Hookify rule files
(re-counted directly: 7 `action: block`, 12 `action: warn`; by trigger, 6
`event: bash`, 11 `event: file`, 2 `event: stop`). `rules/provider-capability-matrix.md`
§1 records the Claude "Rules" row as "canonical Hookify rules + `settings.json`;
local projection not tracked" — verified directly in this worktree: no
`.claude/hookify/` directory, no Hookify-specific entry in
`.claude/settings.json`, and no code path in `scripts/hooks/agent-event-hook.sh`
that parses a Hookify file's `name`/`event`/`pattern`/`action` frontmatter at
runtime. Per the evidence-depth table above, the 19 rules sit at
**Definition** only, not **Configuration**: each rule names a blocking or
warning behavior (for example `block-direct-main-push`,
`require-logical-commits-before-stop`), but nothing in the tracked runtime
executes that declaration as a tool-level gate. The two `event: stop` rules
(`require-logical-commits-before-stop`, `warn-docker-infra-stop`) restate —
rather than extend — the `logical_commit_stop_gate` already hard-coded in
`scripts/hooks/agent-event-hook.sh`; the seven `action: block` rules (for
example blocking a direct `git push origin main`) are enforceable today only
through an agent's own compliance with written policy, since no tool-level
interception reads them. Closing this gap — generating an actual Hookify
runtime projection, or wiring these declarations into `PreToolUse`/`Stop`
matchers — is an explicit adoption decision this reference does not make.

### Native event surface size versus local wiring depth

Direct retrieval of the official hooks pages on 2026-08-14 (LLM-mediated
fetch, not raw HTML inspection — a retrieval-method limitation noted here)
gives a fuller blocking/advisory split than this pack previously recorded:

| Provider |                                                                                                         Upstream event total | Blocking-capable (examples)                                                                                                                                                   | Advisory-only (examples)                                                                                          |                                                                                           Locally wired | Locally blocking          |
| -------- | ---------------------------------------------------------------------------------------------------------------------------: | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------: | ------------------------- |
| Claude   |                                                                                                     31 (matches prior count) | ~14: `PreToolUse`, `UserPromptSubmit`, `Stop`, `SubagentStop`, `TaskCreated`/`TaskCompleted`, `ConfigChange`, `PostToolBatch`, `PreCompact`, `WorktreeCreate`, `Elicitation*` | ~17: `SessionStart`, `Setup`, `SessionEnd`, `PostToolUse`, `Notification`, `SubagentStart`, `PostCompact`, others |                                                                                                 7 of 31 | `Stop` only               |
| Codex    |                                                                                                     11 (matches prior count) | 7: `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `UserPromptSubmit`, `SubagentStop`, `Stop`                                                                 | 4: `SessionStart`, `SessionEnd`, `PostCompact`, `SubagentStart`                                                   |                                                                        6 of 11 (all but `SubagentStop`) | `Stop` (bounded retry)    |
| Gemini   | `UNVERIFIED` — fetched summary lists 11 rows but its own header claims "12 Total"; a direct raw-page re-read would settle it | includes `BeforeTool`, `AfterTool`, `BeforeAgent`, `AfterAgent`, `BeforeModel`, `AfterModel`                                                                                  | `SessionStart`, `SessionEnd`, `Notification`, `PreCompress`, `BeforeToolSelection`                                | 7 (`SessionStart`, `BeforeTool`, `AfterTool`, `SessionEnd`, `AfterAgent`, `PreCompress`, `BeforeAgent`) | `AfterAgent` (deny-retry) |

Five Claude handler types exist (`command`, `http`, `prompt`, `agent`,
`mcp_tool`); this workspace uses only `command`. Two coverage gaps follow
directly from the table: Claude's `SubagentStop`, `TaskCreated`,
`TaskCompleted`, `ConfigChange`, `PostToolBatch`, and `WorktreeCreate` are
upstream blocking-capable events with **no local binding at all** (not
configured, not advisory — absent from `.claude/settings.json`); Gemini's
`BeforeModel`, `AfterModel`, `BeforeToolSelection`, and `Notification` are the
mirror case, upstream capability with no local `.gemini/settings.json` entry.
Closing either requires a Stage 00 semantic-event addition, a renderer
change, and a validator update — out of scope for this reference.

### A third tracked provider surface: Gemini

This reference's in-scope statement names "Claude/Codex projections," but the
tracked contracts and native surface already extend the same construction to
a third provider. `contracts/provider-models.yaml`'s `providers` list (read
directly) carries `claude`, `codex`, and `gemini` entries side by side, each
with `native_agent_pattern`, `native_config_path`, a source/hook-source URL,
and a `local_cli_observation` field: Claude is `observed` at
`local_cli_version: 2.1.209`, Codex is `observed` at `0.140.0`, and Gemini is
`unavailable` with `local_cli_version: null`. `.gemini/` holds 14 native
agent adapters (`.gemini/agents/*.md`), one `.gemini/settings.json` binding 7
native events through a single thin adapter
(`.gemini/hooks/agent-event-hook.sh`, read directly) that translates event
names and output schemas before calling the same
`scripts/hooks/agent-event-hook.sh` used by Claude and Codex, and a
`modelConfigs.overrides` block assigning a Gemini `thinkingLevel` per role
(`HIGH` for ten roles, `MEDIUM` for `doc-writer`, `MINIMAL` for
`drift-detector`) that mirrors the Claude `effort` / Codex
`model_reasoning_effort` distribution by role exactly. Gemini's harness is
therefore as fully **configured** as Claude's and Codex's by every element in
the model above, while its local runtime presence is the least verified of
the three — a concrete instance of this reference's central distinction
between configuration and execution. Deep two-way Claude/Codex construction
comparison remains the dedicated subject of
[`provider-implementation-comparison.md`](./provider-implementation-comparison.md);
this leaf records the third-provider fact only so the harness element model
above does not silently understate what "canonical authority" currently
spans.

### Environment and rules for workspace application

1. Start from an approved requirement and specification, then resolve the
   canonical Stage 00 owner before touching an adapter.
2. Load the bootstrap, provider overlay, one primary scope, and only the stage
   documents needed for the task. Record instruction loading as context, not
   enforcement.
3. Select a registered role and its work profile. Translate model, effort,
   permission, sandbox, hook, and instruction fields into the provider's native
   schema through the renderer.
4. Bind every mutation to explicit path ownership and approval. A provider
   sandbox may narrow technical reach but cannot broaden repository authority.
5. Route provider events through semantic behavior. Unsupported or stale
   mappings remain gaps; do not fabricate parity by copying event names.
6. Run the smallest applicable deterministic checks, then the named aggregate
   gate. Record commands, results, rollback, and skipped checks only.
7. Require a reviewer distinct from the implementing loop owner. Completion
   needs current evidence, not a configured hook, generated adapter, or vendor
   capability statement.
8. Keep credentials, secret values, auth material, raw logs, shell history,
   ignored volumes, private provider state, and unapproved runtime/remote
   actions outside the evidence system.

## Scope Implications

Every row uses the disposition and evidence owners in the
[scope application matrix](./scope-application-matrix.md); this table states
the harness-specific implication so no scope is inherited silently.

| Scope          | Harness implication                                                                                           | Current disposition / route                                                                    |
| -------------- | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `agentic`      | Owns contracts, adapters, hooks, roles, skills, and provider translation.                                     | Implemented as tracked definitions; runtime unverified; route changes through Stage 00 owners. |
| `architecture` | Harness boundaries and provider trade-offs need ARD/ADR/Spec ownership.                                       | Partial; enum-only scope with no typed agent.                                                  |
| `backend`      | Apply tool, secret, test, and runtime isolation only after a backend surface exists.                          | Not Applicable now; future product/Spec decision required.                                     |
| `common`       | Shared review, diff hygiene, and controlled QA apply across harness changes.                                  | Partial; use `code-reviewer`, never direct all-files pre-commit.                               |
| `docs`         | Stage 90 research, templates, metadata, links, and Task evidence are harness inputs/outputs.                  | Implemented corpus; route switch remains pending.                                              |
| `entry`        | Gateway tooling needs infra ownership, targeted approval, and runtime evidence.                               | Partial; route through `infra-implementer`; edge state unverified.                             |
| `frontend`     | Frontend-specific harness gates apply only to the tracked Storybook/Next fixture or a future product surface. | Partial; current fixture remains QA/review-owned.                                              |
| `infra`        | Compose, filesystem, network, secret-reference, and rollback controls form the infrastructure harness.        | Definitions implemented; live state unverified.                                                |
| `meta`         | Typed metadata and generated indexes constrain harness evidence and navigation.                               | Partial; route through docs because the typed meta route is missing.                           |
| `mobile`       | Device, signing, store, and mobile test harnesses need a real surface and approved lifecycle chain.           | Not Applicable; no tracked mobile source.                                                      |
| `ops`          | Observability, incident, deployment, and recovery evidence close operational harness loops.                   | Partial; definitions exist, outcomes unverified.                                               |
| `product`      | Product intent decides whether harness cost, latency, autonomy, and risk are acceptable.                      | Partial; human approval and Stage 01 ownership remain required.                                |
| `qa`           | Owns deterministic validation, fixture/regression evidence, and independent evaluation.                       | Partial but extensive; remote gates and live model quality unverified.                         |
| `security`     | Least privilege, approval, redaction, supply-chain, and secret boundaries apply to every element.             | Partial; `security-auditor` reviews, secret/runtime/remote state excluded.                     |

## Sources

The 2026-08-08 pages below were reopened directly at
`2026-08-08T15:48:51+09:00` and returned HTTP 200 without redirect; none
displayed a stable revision identifier, so every vendor observation is
external mutable and valid only at retrieval time. A second retrieval pass on
2026-08-14 re-fetched the highest-value pages through an LLM-mediated fetch
tool (noted per-row) to extract event/schema breakdowns not previously
recorded; this is a retrieval-method limitation distinct from the source
itself and is flagged wherever it produced an unresolved discrepancy (see the
Gemini event-count note above).

| Source | Class | Verification |
| --- | --- | --- |
| [Claude hooks](https://code.claude.com/docs/en/hooks) | External mutable, primary | Re-verified 2026-08-14: 31 events, 5 handler types, blocking split, 6 config scopes. |
| [Claude subagents](https://code.claude.com/docs/en/sub-agents) | External mutable, primary | Verified 2026-08-08: agent schema, effort, permissions, hooks, memory, isolation. |
| [Claude settings](https://code.claude.com/docs/en/settings) | External mutable, primary | Re-verified 2026-08-14: 5-level precedence, permission-merge rule, `autoMode` schema. |
| [Claude memory](https://code.claude.com/docs/en/memory) | External mutable, primary | Re-verified 2026-08-14: CLAUDE.md load order, `@import` 4-hop limit, "context not enforcement." |
| [Codex hooks](https://learn.chatgpt.com/docs/hooks) | External mutable, primary | Re-verified 2026-08-14: 11-event split, `stop_hook_active`, main-thread `SessionEnd`. |
| [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | External mutable, primary | Re-verified 2026-08-14: TOML fields incl. `skills.config`, reasoning-effort set, sandbox inheritance. |
| [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | External mutable, primary | Re-verified 2026-08-14: discovery order, `AGENTS.override.md`, 32 KiB cap, "prepended not transcluded." |
| [Codex config basics](https://learn.chatgpt.com/docs/config-file/config-basic) | External mutable, primary | Verified 2026-08-08: config precedence, trusted-project boundary. |
| [Codex models](https://learn.chatgpt.com/docs/models) | External mutable, primary | Verified 2026-08-08: model/reasoning controls; no entitlement proof. |
| [Gemini CLI hooks reference](https://geminicli.com/docs/hooks/reference/) | External mutable, primary | New 2026-08-14: event list; header/table count mismatch (11 vs "12") marked `UNVERIFIED`. |
| [Gemini CLI subagents](https://geminicli.com/docs/core/subagents/) | External mutable, primary | New 2026-08-14: frontmatter schema, tool allowlist, no-recursive-subagent rule. |
| [Agent catalog](../../../00.agent-governance/contracts/agent-catalog.yaml) | Workspace tracked | Re-read 2026-08-14: 14 agents, 24 functions, typed eval fields, per-agent work profiles. |
| [Provider/model contract](../../../00.agent-governance/contracts/provider-models.yaml) | Workspace tracked | Re-read 2026-08-14: 3-provider list, `local_cli_observation`, all 21 event cells, 4 loops. |
| [Provider capability matrix](../../../00.agent-governance/rules/provider-capability-matrix.md) | Workspace tracked | Re-read 2026-08-14: 3-column matrix, Hookify "local projection not tracked" line. |
| [Harness implementation map](../../../00.agent-governance/harness-implementation-map.md) | Workspace tracked | Corroborated routing map; policy remains in linked owners. |
| [`.claude/settings.json`](../../../../.claude/settings.json) | Workspace tracked | Read 2026-08-14: `permissions`, `hooks`, `autoMode`, `deniedMcpServers`. |
| [`scripts/hooks/agent-event-hook.sh`](../../../../scripts/hooks/agent-event-hook.sh) | Workspace tracked | Read 2026-08-14: all 7 event handlers, both Stop-gate functions. |
| [`scripts/hooks/post-tool-validate.sh`](../../../../scripts/hooks/post-tool-validate.sh) | Workspace tracked | Read 2026-08-14: path-triggered check matrix, optional-tool behavior. |
| [`.gemini/settings.json`](../../../../.gemini/settings.json) + [adapter](../../../../.gemini/hooks/agent-event-hook.sh) | Workspace tracked | Read 2026-08-14: 7 native events, `modelConfigs.overrides`, translation logic. |
| Hookify catalog (`docs/00.agent-governance/rules/hooks/hookify.*.md`) | Workspace tracked | Counted 2026-08-14: 19 files, 7 block/12 warn; no runtime binding found. |
| [Graphify report](../../../../graphify-out/GRAPH_REPORT.md) | Workspace tracked, stale | Read first; built from `f8a72211`; no uncorroborated claim retained. |

## Maintenance

Re-measure this leaf when agent/function catalogs, provider models, adapters,
hooks, harness layers, loop/event contracts, eval fixtures, regressions, or
official provider pages change. Record a new baseline and retrieval timestamp,
preserve the evidence-depth distinctions, and route implementation changes to
their canonical Stage 00/03/04 owner.

## Related Documents

- [Loop engineering](./loop-engineering.md)
- [Provider implementation comparison](./provider-implementation-comparison.md)
- [Workspace baseline](./workspace-baseline.md)
- [Scope application matrix](./scope-application-matrix.md)
- [Spec 137](../../../03.specs/137-agentic-research-pack-rebuild/spec.md)
- [Execution Task](../../../04.execution/tasks/2026-08-08-agentic-research-pack-rebuild.md)
