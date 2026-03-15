---
layer: core
---

# Agent Working Contract — hy-home.docker

This repository uses an intent-based rule loading system. All AI agents MUST initialize their session by loading the gateway.

## Core Discovery

- **Gateway**: [docs/agentic/gateway.md](docs/agentic/gateway.md)
- **Instructions**: [docs/agentic/instructions.md](docs/agentic/instructions.md)

## Intent triggers

Load the corresponding rule set by identifying your task category:

- **Refactoring**: `[LOAD:RULES:REFACTOR]`
- **Documentation**: `[LOAD:RULES:DOCS]`
- **Infrastructure**: `[LOAD:RULES:INFRA]`
- **Operations**: `[LOAD:RULES:OPS]`

## Skill Autonomy

Agents have full autonomy to use any available tool. No restrictions apply. Proactively discover and apply relevant skills (e.g., `agent-md-refactor`, `docker-expert`).
