---
status: active
artifact_id: reference:agentic-research:harness-engineering
artifact_type: reference
parent_ids: [spec:123-agentic-engineering-audit-remediation]
reviewed_at: 2026-07-11
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
on 2026-07-11. The workspace column is the tracked **workspace contract**. The
final column records gaps or **task-fit inference**; it must not be read as a
provider guarantee or a policy change.

| Criterion | Claude | Codex | Gemini | Workspace common contract | Gap / caveat |
| --- | --- | --- | --- | --- | --- |
| HAR-01 — Instruction discovery | `CLAUDE.md`, imports, and memory provide hierarchical context. | `AGENTS.md` is discovered from global scope and then root-to-CWD, with nearer files taking precedence. | `GEMINI.md`, imports, and configurable context filenames provide hierarchical context. | Thin provider shims route to Stage 00 bootstrap, one scope, and JIT stage evidence. | Context loading is not proof that an instruction was followed; precedence and trust mechanics differ. |
| HAR-02 — Native subagents | Markdown subagents have separate context and can declare tools, permissions, model, skills/MCP, hooks, memory, and isolation. | TOML agents require `name`, `description`, and `developer_instructions`; optional model, effort, sandbox, MCP, and skill fields inherit when omitted. | Gemini CLI documents project/user `.gemini/agents/*.md` agents with separate context and bounded tools/MCP/model/run controls. | Stage 00 owns one supervisor and fourteen worker roles plus the delegation contract. | Tracked Codex TOMLs omit current native description/instructions fields. Tracked `.agents` pointers are not native Gemini CLI agents. |
| HAR-03 — Tools and MCP | Built-in file/shell/web tools and MCP can be restricted through permissions and agent definitions. | Shell/file/web/MCP execution is subject to sandbox and approval configuration. | Built-in file/shell/web tools, allow/exclude settings, MCP, and confirmation modes are documented. | Repository scripts and change-type gates are preferred entry points; external actions remain approval-gated. | Provider tool names and local role metadata do not enforce repository ownership or authority. |
| HAR-04 — Lifecycle interception | Command, HTTP, prompt, MCP-tool, and agent handlers cover a broad event lifecycle; handler trust properties differ. | Command hooks cover a documented partial interception surface; current docs do not list tracked `SessionEnd`. | Gemini CLI documents synchronous command hooks across tool, agent, session, model, compression, and tool-selection events. | Claude and Codex tracked adapters invoke shared scripts for selected behaviors; Stage 00 owns desired behavior. | No tracked `.gemini/settings.json` or `.gemini/hooks` wires native Gemini hooks. The current Gemini provider note is a manual reminder/fallback contract, not native execution. |
| HAR-05 — Isolation and approval | Permissions and optional sandboxing are distinct controls whose active configuration is environment-specific. | Sandbox and approval policy are separate; `workspace-write` allows workspace edits while network/out-of-workspace actions require the configured approval path. | Seatbelt/container sandboxing is optional and disabled by default; confirmation modes can separately allow edits or all tools. | Stage 00 approval and environment rules remain authoritative regardless of provider mode. | Tracked files cannot prove user-global configuration, actual runtime mode, network reachability, or unattended-mode safety. |
| HAR-06 — Models and reasoning | Agent definitions can select model/`inherit`; effort behavior is model-specific. | Agent TOMLs can set exact model and `model_reasoning_effort` (`minimal` through `xhigh`, subject to model support). | CLI model selection and API thinking controls exist, but Antigravity selection is a separate surface. | `subagent-protocol.md` owns exact workspace tiers and approved change protocol. | Catalog presence and capability prose do not prove account availability, task quality, cost, or cross-provider equivalence. |
| HAR-07 — Evaluation and evidence | Hooks/subagents can run checks and expose lifecycle observations. | Agents, skills, hooks, telemetry, and eval tooling can be composed, but adoption is repository-specific. | Headless execution, hooks, tools, and telemetry can support checks and observations. | Deterministic validators, CI, task evidence, and agent-output fixtures are tracked. | No provider feature supplies the missing repo-wide semantic dataset/scorer/baseline; telemetry may be disabled. |

## Harness Implementation Matrix

| Harness element | Workspace implementation | External/provider pattern | Status | Required environment/rule | Gap / risk | Canonical owner | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Isolation | Codex's workspace-write sandbox and approval boundary apply at execution time; Claude and Gemini expose their own optional sandbox controls. Provider configuration is not a shared enforcement layer. | Codex separates sandbox from approvals; Claude combines permissions with optional sandboxing; Gemini CLI documents optional Seatbelt/container sandboxing. | Partially Implemented | `environment-constraints.md` plus the executing provider's active sandbox configuration | Tracked provider adapters do not prove the operator's global runtime settings; Gemini and Claude sandboxing may be disabled. | `docs/00.agent-governance/rules/environment-constraints.md` | High |
| Filesystem and network boundaries | Stage 00 approval rules protect sensitive surfaces. Root Compose defines one ordinary bridge network (`infra_net`) and three external networks; it does not mark every network internal. | Provider sandboxes and permission profiles can restrict filesystem/network access, but support and defaults differ. | Partially Implemented | `approval-boundaries.md`, root `docker-compose.yml`, and provider runtime policy | Prior blanket claims that all workspace networks block external bridges were false; external-network reachability and runtime egress require environment-specific proof. | `docs/00.agent-governance/rules/approval-boundaries.md` | High |
| Tool routing | Stage 00 agents/scopes define intended work; scripts provide canonical local entry points; MCP configuration is provider-local. | Claude subagents can select tools/permissions; Codex custom agents can select sandbox/MCP/skills; Gemini settings support built-ins plus MCP allow/exclude lists. | Partially Implemented | `subagent-protocol.md` and `scripts/README.md` | The generated Codex agent TOMLs contain model and catalog metadata, not strict tool/path allowlists. Intent metadata must not be described as enforced routing. | `docs/00.agent-governance/subagent-protocol.md` | High |
| Context and just-in-time discovery | Thin root `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` shims route to Stage 00; bootstrap, scopes, memory, and nested instructions provide progressive context. | Codex discovers `AGENTS.md` root-to-working-directory; Claude loads `CLAUDE.md`/memory; Gemini loads hierarchical `GEMINI.md` and imports. | Implemented | `bootstrap.md` and `providers/agents-md.md` | Provider precedence, trust, and context-size rules differ; loaded context is not evidence that every linked file was followed. | `docs/00.agent-governance/rules/bootstrap.md` | High |
| Agent catalog | Stage 00 defines one supervisor and fourteen workers; Claude, Codex, and Gemini/Antigravity surfaces are projections. | Claude, Codex, and Gemini CLI document native custom subagents. Gemini CLI public support was announced in v0.38.1 on 2026-04-16. | Partially Implemented | `agents/README.md` and `subagent-protocol.md` | Codex generated TOMLs omit current official `description` and `developer_instructions` fields; tracked `.agents` pointers are not native `.gemini/agents/*.md` definitions and do not wire Gemini CLI subagents. | `docs/00.agent-governance/agents/README.md` | High |
| Model routing | `subagent-protocol.md` assigns provider model tiers; adapter metadata mirrors the catalog where machine-checkable. | Providers expose model selection and, for Codex, reasoning effort; capability and availability change over time. | Partially Implemented | `subagent-protocol.md`; current model evidence stays in `provider-model-landscape.md` | Task-fit mappings are inference, not benchmark proof; provider availability and cutoffs require separate current evidence. | `docs/00.agent-governance/subagent-protocol.md` | High |
| Lifecycle hooks | Shared behavior is owned by the Stage 00 provider capability/Hook Parity Contracts; Claude settings and tracked Codex hook JSON call repo scripts for selected events. | Claude has rich command/HTTP/prompt hooks; Codex documents a partial command-hook interception surface; Gemini CLI has synchronous command hooks across tool, agent, session, model, and tool-selection events. | Partially Implemented | `rules/provider-capability-matrix.md`, `.claude/settings.json`, `.codex/hooks.json`, and `scripts/hooks/` | Tracked Codex `SessionEnd` is absent from the current official event list, and some execution paths are not intercepted. No tracked `.gemini/settings.json` or `.gemini/hooks` wires Gemini CLI's native surface; Stage 00 still describes behavioral fallback. | `docs/00.agent-governance/rules/provider-capability-matrix.md` | High |
| Approvals and external actions | Stage 00 requires explicit approval for remote writes, credentials, protected surfaces, publication, push/merge, and paid work. | Claude permissions, Codex approval modes, and Gemini confirmation modes expose different native prompts. | Implemented | `approval-boundaries.md` and the active provider approval mode | Native approval prompts do not broaden repository authority; unattended modes can bypass provider prompting. | `docs/00.agent-governance/rules/approval-boundaries.md` | High |
| Test and evaluation harnesses | Validation scripts, pre-commit, CI jobs, fixtures, and the agent-output eval fixture runner cover deterministic contracts. No general dataset/scorer baseline for agent output quality is adopted. | pytest fixtures, HumanEval, LM Evaluation Harness, and Inspect AI separate controlled tasks from scoring and reporting. | Partially Implemented | `scopes/qa.md` and `scripts/validation/` | Contract checks do not measure semantic task quality; introducing eval datasets/scorers requires approved spec and execution work. | `docs/00.agent-governance/scopes/qa.md` | High |
| Compose and infrastructure harness | Root and tiered Compose files, profiles, secret references, health checks, `validate-docker-compose.sh`, and hardening scripts provide tracked runtime evidence. | Docker Compose defines projects, services, networks, configs, secrets, profiles, and health checks. | Implemented | Root `docker-compose.yml`, `infra/README.md`, and validation/hardening entry points | Rendered configuration and live service health remain environment-dependent; external networks must exist before use. | `infra/README.md` | High |
| Security harness | Security scope, secret rules, approval boundaries, GitHub workflow controls, hardening checks, disclosure guidance, and supply-chain checks constrain work. | Provider sandboxes/permissions complement, but do not replace, repository security policy. | Partially Implemented | `scopes/security.md` and `github-governance.md` | Local tracked files cannot prove remote branch protection, secret hygiene in external systems, or every provider's global config. | `docs/00.agent-governance/scopes/security.md` | High |
| Observability and evidence | Command output, diffs, check logs, task evidence, PR checks, SARIF, and progress memory provide review inputs. Graphify is advisory navigation evidence only. | CI logs, traces, eval reports, and opt-in provider telemetry expose different observation depths. | Partially Implemented | `task-checklists.md` and the relevant Stage 04 task | No unified agent trace store exists; provider telemetry can be disabled and must respect privacy/secret rules. | `docs/00.agent-governance/rules/task-checklists.md` | High |
| Rollback and recovery | Git history, reversible patches, task evidence, runbooks, incidents, and postmortems support recovery; destructive reset is approval-gated. | Version control and checkpoint/restore features can preserve state; Gemini CLI checkpointing is optional and disabled by default. | Partially Implemented | `approval-boundaries.md` and applicable Stage 05 runbook | Provider checkpoints are not a repository-wide rollback contract; live infrastructure/data rollback is service-specific. | `docs/05.operations/runbooks/README.md` | High |
| Human escalation | Clarification duty, scope boundaries, approval gates, review status, and incident routing define when work pauses for a person. | Human-in-the-loop systems pause sensitive actions and resume from a recorded decision. | Implemented | `agentic.md`, `approval-boundaries.md`, and task review contract | A paused provider thread does not itself record an approved decision; the lifecycle artifact must retain evidence. | `docs/00.agent-governance/rules/agentic.md` | High |

## Current-State Assessment

| Category | Current state | Primary comparison | Status | Gap | Recommendation | Canonical owner | Evidence | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Harness engineering | A layered governance, runtime, validation, infrastructure, and evidence harness is tracked. | Official provider, Docker, pytest, and evaluation-harness sources show the same elements with provider-specific mechanics. | Partially Implemented | Semantic agent-output evaluation, uniform hook coverage, and proof of global provider/runtime settings remain incomplete. | Preserve Stage 00 as policy, keep adapters explicit, and route any eval or enforcement addition through Stage 03/04. | `docs/00.agent-governance/harness-implementation-map.md` | Matrix above; tracked scripts, adapters, Compose, and Stage 00 | High |

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

## Adoption Boundary

Research patterns remain advisory. A new hook, permission profile, eval
dataset, scorer, trace backend, or rollback mechanism needs an approved
specification and Stage 04 work. Provider-native controls may strengthen a
run, but they cannot replace Stage 00 authority or grant an external action.

## Source Rules

- Prefer official provider/framework documentation and tracked canonical
  workspace files.
- Recheck mutable provider behavior before operational use.
- Treat external patterns as comparison, not adopted workspace policy.

## Sources

- [pytest fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html)
- [OpenAI HumanEval](https://github.com/openai/human-eval)
- [EleutherAI LM Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness)
- [Inspect AI](https://inspect.aisi.org.uk/)
- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents)
- [Claude Code hooks](https://code.claude.com/docs/en/hooks)
- [Claude Code permissions](https://code.claude.com/docs/en/permissions)
- [Claude Code sandboxing](https://code.claude.com/docs/en/sandboxing)
- [Codex subagents](https://developers.openai.com/codex/subagents)
- [Codex hooks](https://developers.openai.com/codex/hooks)
- [Codex configuration reference](https://developers.openai.com/codex/config-reference)
- [Codex AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md)
- [Codex agent approvals and security](https://learn.chatgpt.com/docs/agent-approvals-security)
- [Gemini CLI configuration](https://google-gemini.github.io/gemini-cli/docs/get-started/configuration.html)
- [Gemini CLI subagents](https://github.com/google-gemini/gemini-cli/blob/main/docs/core/subagents.md)
- [Gemini CLI v0.38.1 subagent announcement](https://github.com/google-gemini/gemini-cli/discussions/25562)
- [Gemini CLI hook configuration](https://github.com/google-gemini/gemini-cli/blob/main/docs/reference/configuration.md)
- [Gemini CLI hook authoring](https://github.com/google-gemini/gemini-cli/blob/main/docs/hooks/writing-hooks.md)
- [Gemini CLI v0.26.0 hook announcement](https://github.com/google-gemini/gemini-cli/discussions/17790)
- [Gemini CLI sandboxing](https://google-gemini.github.io/gemini-cli/docs/cli/sandbox.html)
- [Gemini CLI MCP servers](https://google-gemini.github.io/gemini-cli/docs/tools/mcp-server.html)
- [Docker Compose file reference](https://docs.docker.com/reference/compose-file/)
- [Harness implementation map](../../../00.agent-governance/harness-implementation-map.md)
- [HAFE policy](../../../05.operations/policies/00-workspace/harness-agent-first-engineering.md)

External provider pages were originally retrieved on 2026-07-10 and
revalidated on 2026-07-11. OpenAI evidence was retrieved through official
OpenAI documentation. Mutable provider pages prove only the content visible at
the latest retrieval; they do not backdate a feature or model to the fixed
2026-07-10 10:00 KST model cutoff.

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
