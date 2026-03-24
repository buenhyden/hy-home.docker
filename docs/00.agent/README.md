---
layer: agentic
---

# AI Agent Instruction Hub (`docs/00.agent/`)

This directory is the **authoritative home for all AI agent-specific logic, governance, and Discovery protocols**. Root files reference this hub to ensure consistent behavior across agent providers.

## Core Instruction Set

- [00.index.md](README.md) — This documentation.
- [01.gateway.md](01.gateway.md) — Session start orientation and Dispatcher.
- [02.governance.md](02.governance.md) — Persona management and taxonomy.
- [03.behavior.md](03.behavior.md) — Behavioral and prompting rules.
- [04.workflow.md](04.workflow.md) — Interaction logic and execution loop.
- [05.system-spec.md](05.system-spec.md) — Technical boundaries and system definitions.

## Maintenance Policy

- **Concise Roots**: `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` are lightweight shims that point here.
- **No Duplication**: Common operational rules belong here, not scattered across root files.
- **Relative Linking**: All internal links must remain relative to ensure portability.
- **Numeric Taxonomy**: All files in this directory must use the `00~99` numeric prefix.

