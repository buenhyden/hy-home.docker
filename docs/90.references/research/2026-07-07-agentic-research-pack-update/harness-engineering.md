---
status: active
---

<!-- Target: docs/90.references/research/2026-07-07-agentic-research-pack-update/harness-engineering.md -->

# Reference: Harness Engineering and Framework Integration

## Overview

This reference analyzes the principles of Harness Engineering and documents the current harness implementations for the three major AI providers (Claude, Codex, Gemini) in this workspace.

## Purpose

Examine how the agent's runtime inputs, tool bindings, and outputs are structured and controlled via local validation frameworks.

## Repository Role

This document serves as a reference for harness architecture. It does not replace or modify active validation scripts (e.g., `check-repo-contracts.sh`, `validate-harness.sh`) or provider settings.

## Scope

### In Scope

- Definition and architecture of Harness Engineering
- Local runtime harness structures for Claude, Codex, and Gemini
- Assessment of harness implementation depth and identification of gaps

### Out of Scope

- Modifying active provider configurations
- Altering local sandbox or permission scopes
- Accessing or recording credentials or secrets

## Definitions / Facts

- **Harness Engineering**: The practice of designing and building a local execution testbed and safety sandbox that wraps an AI agent's operations, managing context ingestion, tool permissions, and automated code validation.
- **Claude Code Harness**: Uses the `.claude/` directory for runtime settings and loads agent files from `.claude/agents/*.md`. It integrates with local event hooks (`agent-event-hook.sh`) to normalise and validate code edits.
- **Codex Harness**: Managed via the `.codex/` directory. Uses `.codex/agents/*.toml` to set tool permissions and sandbox controls, and executes checkers based on events in `.codex/hooks.json`.
- **Gemini Harness**: Utilises `.agents/` as the runtime adapter surface and references `.agents/agents/` for agent definitions. Since native hooks are limited, it relies on shared wrapper scripts and manual prompt-driven checks.
- **Implementation Status & Gaps**:
  - *Status*: The workspace harness is validation-backed and mapped in `harness-implementation-map.md`, using scripts like `check-repo-contracts.sh` and `validate-harness.sh` to enforce structural rules.
  - *Gaps*: Isolation and sandbox capabilities vary across providers (Gemini lacks native tool approval gates), and updating the knowledge graph via `graphify` is currently a manual step rather than an automated hook-level action.

## Sources

- [Harness implementation map](../../../00.agent-governance/harness-implementation-map.md) - Local harness routing SSoT
- [Claude Code docs](https://code.claude.com/docs/en/overview) - Claude Code CLI specifications
- [Codex CLI docs](https://developers.openai.com/codex/cli) - Codex CLI configuration schema
- [Gemini CLI docs](https://developers.google.com/gemini-code-assist/docs/gemini-cli) - Gemini tool runtime specifications

## Maintenance

- **Owner**: Workspace Harness & Security Specialist
- **Review Cadence**: Review when new provider runtimes are introduced or when sandbox configurations change
- **Update Trigger**: Update when local validation scripts are modified or when new adapter boundaries are established

## Related Documents

- [README.md](./README.md)
- [workspace-baseline.md](./workspace-baseline.md)
- [loop-engineering.md](./loop-engineering.md)
