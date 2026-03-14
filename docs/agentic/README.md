---
layer: agentic
---

# AI Agent Instruction Hub (`docs/agentic/`)

This directory is the **authoritative home for all AI agent-specific logic, governance, and Discovery protocols**. Root files reference this hub to ensure consistent behavior across agent providers.

## Core Instruction Set

1. [**Discovery Gateway**](gateway.md) — The session-start entrypoint. Load this first to map out documentation families.
2. [**Core Governance**](core-governance.md) — Shared persona matrix, rule-loading policies, and template contracts.
3. [**Shared Workflow**](workflow.md) — The standard execution loop, validation commands, and anti-patterns.

## Maintenance Policy

- **Concise Roots**: `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` are lightweight shims that point here.
- **No Duplication**: Common operational rules belong here, not scattered across root files.
- **Relative Linking**: All internal links must remain relative to ensure portability.
