---
layer: agentic
---

# AI Agent Instruction Hub (`docs/agentic/`)

This directory is the **authoritative home for all AI agent-specific logic, governance, and Discovery protocols**. Root files reference this hub to ensure consistent behavior across agent providers.

## Core Instruction Set

- [Agent Gateway](gateway.md) — Session start orientation.
- [Agent Core Governance](core-governance.md) — Persona management and taxonomy.
- [Agent System Spec](2026-03-15-agent-system-spec.md) — Technical definitions.
- [Agent Instructions](2026-03-15-agent-instructions.md) — Behavior and prompting rules.
- [Agent Workflow](2026-03-15-agent-workflow.md) — Interaction logic.

## Maintenance Policy

- **Concise Roots**: `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` are lightweight shims that point here.
- **No Duplication**: Common operational rules belong here, not scattered across root files.
- **Relative Linking**: All internal links must remain relative to ensure portability.
