---
status: active
---
<!-- Target: docs/90.references/research/2026-07-05-agentic-research-pack-refresh/provider-implementation-comparison.md -->

# Reference: Claude, Codex, and Gemini Provider Implementation Comparison

## Overview

This reference compares the current Claude, Codex, and Gemini implementation surfaces for harness engineering and loop engineering using official sources and the repo-local provider adapter model.

## Purpose

Avoid assuming that the three providers have identical capabilities. Identify which elements should be provider-neutral policy and which elements should remain provider-specific adapters.

## Repository Role

This reference provides background for `providers/claude.md`, `providers/codex.md`, `providers/gemini.md`, `subagent-protocol.md`, `.claude/`, `.codex/`, and `.agents/`. It does not change provider settings or model policy.

## Scope

### In Scope

- Claude Code official feature surface
- OpenAI Codex official feature surface
- Gemini CLI official feature surface
- Comparison of subagents, hooks, config, sandbox/approval, MCP, automation, and eval-related features
- Common provider-neutral system elements

### Out of Scope

- Provider adapter TOML/Markdown changes
- Model policy changes
- Global provider configuration changes
- External posting, pushing, or remote job dispatch

## Definitions / Facts

- **Claude Code**: Anthropic describes Claude Code as an agentic coding tool that reads codebases, edits files, runs commands, and integrates with development tools.
- **Claude subagents**: Claude Code subagents run in separate context windows with custom system prompts, tool access, and permissions.
- **Claude hooks**: Claude Code hooks are user-defined shell commands, HTTP endpoints, or LLM prompts that run on lifecycle events.
- **Codex CLI**: OpenAI describes Codex CLI as a local terminal coding agent with sandboxing, approvals, config, subagents, hooks, MCP, and noninteractive automation.
- **Codex subagents**: Codex supports built-in and custom subagents, `.codex/agents/*.toml`, inherited sandbox policy, and approval propagation across interactive agent threads.
- **Codex AGENTS.md**: OpenAI docs describe `AGENTS.md` as a project instruction discovery mechanism.
- **Gemini CLI**: Google describes Gemini CLI as an open-source terminal AI agent using a ReAct loop with built-in tools and MCP servers.
- **Gemini context files**: Gemini CLI supports `GEMINI.md` and configurable context file names for persistent context.
- **Gemini subagent gap**: As of the 2026-07-05 research pass, official Gemini CLI and Gemini Code Assist sources reviewed here did not show first-class subagents comparable to Claude and Codex. Gemini is interpreted through config, context, MCP, action, approval, and IDE integration surfaces.

## Provider Comparison Matrix

| Capability | Claude Code | OpenAI Codex | Gemini CLI | Repo-local Normalization |
| --- | --- | --- | --- | --- |
| Shared entry context | `CLAUDE.md`, memory docs | `AGENTS.md`, `.codex/config.toml`, project config | `GEMINI.md`, configurable context file names | root shims delegate to Stage 00 |
| Agent/subagent model | first-class custom subagents and parallel agents | first-class subagents and `.codex/agents/*.toml` | no confirmed first-class equivalent in official docs | `subagent-protocol.md` defines provider-equivalent roles, but Gemini is reference-index oriented |
| Hooks/lifecycle | rich lifecycle hooks | hooks with events such as PreToolUse/PostToolUse/Stop/Subagent events | no same hook parity in repo notes; manual behavioral contract | shared behavioral hooks contract, provider-specific mechanics |
| Sandbox/approval | permissions and sandbox docs | explicit sandbox/approval docs and permission profiles | sandbox/trust/config docs in official repo | approval boundaries and environment constraints |
| MCP | supported | supported | supported via `mcpServers` | project-local MCP baseline stays config-governed |
| Automation/CI | provider hooks and workflows | noninteractive mode, GitHub Action, hooks | official `run-gemini-cli` GitHub Action | external actions remain approval-gated |
| Docker/infra awareness | tool-driven through shell and project docs | sandboxed local shell plus project docs | tool-driven ReAct/MCP workflow | Stage 00 infra scope and scripts are provider-neutral |
| Security/approval model | permissions, hooks, human approval | sandbox/approval modes, hooks, config | trust/config/tool confirmation surfaces | approval boundaries and protected surface evidence |
| Common rule substrate | root shim and provider docs | `AGENTS.md`, `.codex/`, provider docs | `GEMINI.md`, `.agents/`, provider docs | Stage 00 remains the SSoT |
| Skills/functions | Claude skills standard extensions | Codex skill adapters in repo-local surface | `.agents/skills` reference indexes in this repo | Stage 00 function catalog is canonical |
| Model policy | Claude aliases and provider model names | Codex GPT model and reasoning effort | Gemini model selection | `subagent-protocol.md` mapping |

## Analysis

Claude and Codex have converged on explicit subagent and hook concepts, but their configuration and enforcement models differ. Claude expresses much of its runtime through Markdown/context/hook surfaces. Codex exposes TOML agents, config layers, sandbox/approval policies, and hook JSON/config. Gemini CLI has strong context, tool, MCP, ReAct loop, and automation support, but the official docs reviewed here do not show subagent parity comparable to Claude/Codex.

The safe common architecture is therefore not "all providers support the same features." The safer architecture is:

1. Stage 00 defines provider-neutral policy, agent roles, model tiers, approval boundaries, QA evidence, and template contracts.
2. Provider surfaces adapt those policies to native mechanics.
3. Validators check name/model/scope/protocol parity where machine-checkable.
4. Capability gaps are documented as provider-specific constraints rather than hidden behind identical labels.

This matches the repo-local Provider Adapter Model. `.claude/` can be a richer runtime mirror, `.codex/` can be a TOML/hook/context surface, and `.agents/` can be the Gemini shared/reference-index surface without making any provider the hidden source of truth.

## Common Environment and Rule Elements

- Thin root entrypoints that delegate to Stage 00.
- One canonical agent/function catalog with provider adapter projections.
- Explicit model policy per provider, with validation support before changes.
- Common approval boundaries for secrets, remote actions, provider config, model policy, and protected surfaces.
- Hook or behavioral equivalents for pre-edit guidance, post-edit validation, stop/completion gates, and progress evidence.
- Script-backed QA gates that do not depend on provider-specific agent memory.
- Reference docs that record provider feature drift without rewriting policy.

## Potential Follow-up / Gap

- Gemini first-class subagent parity should not be claimed without a newer official source.
- Provider releases move quickly; a periodic provider capability matrix review may be useful.
- Codex permission profiles are beta in official docs and should not be treated as stable policy until repo validators and provider notes explicitly adopt them.
- Claude sandbox/runtime details include beta/research-preview caveats in official docs; repo policy should keep sandbox claims precise.

## Source Rules

- Provider facts use official vendor docs or official GitHub repositories first.
- Release numbers are not frozen in this reference unless needed; verify again before operational adoption.
- Provider comparison records implementation status, not endorsement of new repo behavior.

## Sources

- [Claude Code overview](https://code.claude.com/docs/en/overview) - Claude Code product scope
- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents) - subagent capabilities and context isolation
- [Claude Code hooks](https://code.claude.com/docs/en/hooks) - lifecycle hook model
- [Claude Code settings](https://code.claude.com/docs/en/settings) - configuration surface
- [Claude Code security](https://code.claude.com/docs/en/security) - permissions and approval framing
- [Codex CLI](https://developers.openai.com/codex/cli) - Codex CLI overview
- [Codex subagents](https://developers.openai.com/codex/subagents) - Codex subagent model
- [Codex hooks](https://developers.openai.com/codex/hooks) - Codex hook model
- [Codex config reference](https://developers.openai.com/codex/config-reference) - `.codex` and config keys
- [Codex AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md) - project instruction discovery
- [Codex sandboxing](https://developers.openai.com/codex/concepts/sandboxing) - sandbox boundary
- [Gemini CLI overview](https://developers.google.com/gemini-code-assist/docs/gemini-cli) - Gemini CLI ReAct/tool/MCP summary
- [Gemini CLI configuration](https://google-gemini.github.io/gemini-cli/docs/get-started/configuration.html) - settings and configuration methods
- [Gemini CLI GEMINI.md docs](https://google-gemini.github.io/gemini-cli/docs/cli/gemini-md.html) - persistent context files
- [Gemini CLI commands](https://google-gemini.github.io/gemini-cli/docs/cli/commands.html) - CLI command surface
- [Gemini CLI MCP servers](https://google-gemini.github.io/gemini-cli/docs/tools/mcp-server.html) - MCP configuration
- [Gemini CLI GitHub repository](https://github.com/google-gemini/gemini-cli) - official repo
- [run-gemini-cli GitHub Action](https://github.com/google-github-actions/run-gemini-cli) - official automation action
- [Subagent protocol](../../../00.agent-governance/subagent-protocol.md) - repo-local model and provider adapter mapping
- [Claude provider notes](../../../00.agent-governance/providers/claude.md) - repo-local Claude boundary
- [Codex provider notes](../../../00.agent-governance/providers/codex.md) - repo-local Codex boundary
- [Gemini provider notes](../../../00.agent-governance/providers/gemini.md) - repo-local Gemini boundary

## Maintenance

- **Owner**: Documentation maintainers
- **Review Cadence**: Review monthly when provider release velocity is high, otherwise quarterly
- **Update Trigger**: Update when Claude, Codex, Gemini official docs or repo-local provider adapters change

## Related Documents

- [research pack index](./README.md)
- [workspace baseline](./workspace-baseline.md)
- [harness engineering](./harness-engineering.md)
- [loop engineering](./loop-engineering.md)
- [subagent protocol](../../../00.agent-governance/subagent-protocol.md)
