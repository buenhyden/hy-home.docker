---
status: active
---

<!-- Target: docs/90.references/research/2026-07-07-agentic-research-pack-update/provider-implementation-comparison.md -->

# Reference: Multi-Provider Implementation Comparison

## Overview

This reference compares the harness and loop engineering capabilities of Claude Code, Codex, and Gemini within the `hy-home.docker` workspace, identifying commonalities and provider-specific configurations.

## Purpose

Provide a comparative matrix of provider integration depths to guide the design of provider-neutral safety sandboxes and universal validation wrappers.

## Repository Role

This document is a comparative reference. It does not replace or modify active provider adapter files or SSoT rules under `docs/00.agent-governance/`.

## Scope

### In Scope

- Comparing harness structures, isolation levels, and hook mechanisms across Claude, Codex, and Gemini
- Analyzing the common rules and environment contracts in the workspace
- Proposing improvements for provider-neutral harness enforcement

### Out of Scope

- Rewriting provider-native execution binaries or adapters
- Editing live credential configurations or secrets
- Mutating active workflow files in the workspace

## Definitions / Facts

- **Provider Runtime Parity**:
  - Claude uses `.claude/` settings, supports markdown instructions, and hooks tightly into post-tool event dispatch.
  - Codex uses `.codex/` TOML files and maps execution gates via `.codex/hooks.json`.
  - Gemini references `.agents/` profiles and follows instructions behaviourally, but lacks native CLI hooks.
- **Common Workspace Rules**:
  - All providers share the same role definitions and instruction SSoT under `docs/00.agent-governance/agents/`.
  - `check-repo-contracts.sh` acts as a compiler that syncs SSoT markdown agents with the respective provider runtime structures.
- **Identified Gaps**:
  - The hook enforcement is uneven; Claude and Codex validate edits automatically, while Gemini relies on prompt-driven execution.
  - Reasoning and tool-use variations can lead to performance differences, requiring a universal CLI execution wrapper.

## Sources

- [Provider capability matrix](../../../00.agent-governance/rules/provider-capability-matrix.md) - Provider capability comparison SSoT
- [Subagent protocol](../../../00.agent-governance/subagent-protocol.md) - Model tier allocation protocol
- [Vendor CLI guides] - Official documentation for Claude CLI, Codex, and Gemini Assist CLI

## Maintenance

- **Owner**: Platform Governance Maintainer
- **Review Cadence**: Review when new AI models are added or when vendor CLI tools are updated
- **Update Trigger**: Update when model protocols are revised or when provider capability matrices are updated

## Related Documents

- [README.md](./README.md)
- [workspace-baseline.md](./workspace-baseline.md)
- [harness-engineering.md](./harness-engineering.md)
- [loop-engineering.md](./loop-engineering.md)
- [ai-agent-catalogs.md](./ai-agent-catalogs.md)
