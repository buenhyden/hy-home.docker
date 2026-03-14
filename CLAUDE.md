---
layer: agentic
---

# CLAUDE.md

Cla## Rule Triggers

Identify your task and load the rule module:

- **Refactoring**: `[LOAD:RULES:REFACTOR]`
- **Documentation**: `[LOAD:RULES:DOCS]`

## Claude Execution Notes

- **Gateway First**: Always begin session with [docs/agentic/gateway.md](docs/agentic/gateway.md).
- **Skill Autonomy**: Use any available tool in your bundle. No restrictions apply. Proactively apply skills like `agent-md-refactor` or `claude-md-improver` as needed.
- **Path Compliance**: Implementation plans must reside in `docs/plans/`.
- **Skill Autonomy**: Proactively apply any purpose-fit skill. No tool restrictions.

## Shared Policy Imports

@docs/agentic/core-governance.md
@docs/agentic/workflow.md
@docs/agentic/instructions.md
