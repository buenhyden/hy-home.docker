---
layer: agentic
---

# CLAUDE.md

**Claude-optimized cognitive patterns and memory briefing.**

## 1. Core Protocols

- **Governance Hub**: [docs/00.agent-governance/README.md](docs/00.agent-governance/README.md)
- **Specific Configuration**: [docs/00.agent-governance/claude-provider.md](docs/00.agent-governance/claude-provider.md)

## 2. Interaction & Memory

- **Thinking Process**: Use `<thinking>` tags for planning and internal logic mapping.
- **Progressive Disclosure**: Offload layer-specific rules to `docs/00.agent-governance/scopes/`.
- **JIT Context**: Use `[LOAD:...]` markers to ingest taxonomy context from `docs/01-11`.

## 3. Response Strategy

- **Language**: ALWAYS respond to the USER in **Korean**.
- **Validation**: Verify all work via tests or scripts as defined in the plan.
