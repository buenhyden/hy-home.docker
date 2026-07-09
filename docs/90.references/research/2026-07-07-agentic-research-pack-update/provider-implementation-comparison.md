---
status: active
---

<!-- Target: docs/90.references/research/2026-07-07-agentic-research-pack-update/provider-implementation-comparison.md -->

# Reference: Multi-Provider Implementation Comparison

This document analyzes the harness and loop engineering capabilities of Claude Code, OpenAI Codex, and Gemini Code Assist, and details the unified rules, compiler projection layers, and tool wrappers designed to flatten provider parity gaps.

---

## Overview

AI agent runtimes are shaped by distinct vendor paradigms, resulting in divergent configurations, folder layouts, and eventhook integration mechanisms in local environments:

- **Claude Code (`.claude/`)**: Highly suited for Markdown-based system directives and hooks. The CLI directly integrates human approval workflows for file edits and shell commands, and its post-tool event dispatching allows real-time linting and formatting.
- **OpenAI Codex (`.codex/`)**: Relies on structured TOML configurations to whitelist tools and parameters. Its sandboxing models are highly granular, blocking unapproved binaries at the system layer.
- **Gemini Code Assist (`.agents/`)**: Enjoys deep integration in the IDE and cloud runtimes. However, it lacks terminal-level eventhooks and sandboxes, relying heavily on self-correction prompts and client-side workspace policies.

## Purpose

This reference details the technical boundaries and configuration parity gaps across the three LLM providers. It informs adapter implementation designs without mutating active workspace templates.

## Repository Role

This document acts as an advisory reference for provider adapters. It does not replace Stage 00 agent protocols, active plans, or runner configurations.

## Scope

### In Scope

- Physical layout and configuration specification comparison of Claude, Codex, and Gemini.
- Detailed capabilities comparison matrix (harness isolation, hooks, self-correction, etc.).
- Architecture of the Stage 00 Spec Compiler and Shared Tool Wrapper.
- Gaps in provider alignment (adapter template tooling, context budget sizing).

### Out of Scope

- Creation of provider configuration files or execution of sync scripts.
- Execution of pipeline runs.
- Secret credentials or private environment properties.

## Definitions / Facts

### 1. Provider Capabilities Parity Matrix

A detailed comparison of vendor runtimes against harness and loop engineering attributes:

| Attribute | Claude Code | OpenAI Codex | Gemini Code Assist |
| :--- | :--- | :--- | :--- |
| **Physical Layout** | `.claude/settings.json`<br>`.claude/agents/*.md` | `.codex/settings.toml`<br>`.codex/agents/*.toml` | `.agents/settings.json`<br>`.agents/agents/*.md` |
| **Specification Format** | Markdown + JSON | TOML + JSON Schema | Markdown + JSON |
| **Sandbox Level** | High (Interactive CLI prompts) | Critical (Whitelist restrictions) | Medium (IDE client execution context) |
| **Native Eventhooks** | Critical (Pre-run, Post-tool hooks) | High (Event dispatcher registry) | Low (Self-evaluation and manual audits) |
| **Outer Feedback Loop** | Critical (Direct stdin/stdout streams) | High (JSON error mapping) | Medium (Chat UI prompt forwarding) |
| **DORA Risk Lead Time** | High (Immediate hook correction) | Medium-High (Fast spec audits) | Medium (Post-commit CI workflow failures) |
| **Self-Correction** | High (ReAct loop syntax adjustments) | Medium-High (Error-state blocking) | Medium (Dependent on prompting detail) |

### 2. Stage 00 Spec Compiler

To counteract provider specification fragmentation, the workspace uses `check-repo-contracts.sh` to project Markdown rules from [docs/00.agent-governance/agents/](../../../00.agent-governance/agents/) onto each provider adapter:

- **Claude Projection**: Copies Markdown headers directly to `.claude/agents/*.md`.
- **Codex Projection**: Parses allowed tools and scopes, converting them into TOML whitelists in `.codex/agents/*.toml`.
- **Gemini Projection**: Compiles index maps of the specifications to `.agents/agents/*.md`.

### 3. Shared Tool Wrapper

A unified wrapper is defined to ensure all providers run the same validation routines:

- Agents invoke tools via a shared script runner which automatically intercepts files, runs `prettier --check` and `git diff --check`, corrects code surfaces, and returns clean exits. This compensates for Gemini's hook limitations.

### 4. Identified Gaps

- **Lack of Auto-Scaffolding**: The contract checker only checks provider parity; it does not automatically generate missing adapter files from Stage 00 Markdown.
- **Context Budgets**: Prompts designed for Claude overflow Gemini's context limits, requiring context-aware compression filters.

## Sources

- [Provider Capability Matrix](../../../00.agent-governance/rules/provider-capability-matrix.md) - SSOT for vendor features and boundaries
- [Subagent Protocol Model Policy](../../../00.agent-governance/subagent-protocol.md) - Delegation rules and model mappings
- [Claude CLI Specification](https://code.claude.com/docs/en/overview) - Claude CLI architecture docs
- [Codex Hook Event Schema](https://developers.openai.com/codex/hooks) - Codex execution gate schemas

## Maintenance

- **Owner**: Workspace Lead Architect and Governance Board
- **Review Cadence**: Annually, or when new adapter specifications are released.
- **Update Trigger**: Triggered by changes to the lint rules in `check-repo-contracts.sh` or shifts in model tier allocations.

## Related Documents

- [Research Index README](./README.md)
- [References Category README](../README.md)
- [workspace-baseline.md](./workspace-baseline.md)
- [harness-engineering.md](./harness-engineering.md)
- [loop-engineering.md](./loop-engineering.md)
