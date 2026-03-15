---
layer: agentic
---

# GEMINI.md

Gemini-specific operational triggers for `hy-home.docker`.

## Rule Triggers

Identify your task and load the required rule module:

- **Refactoring**: `[LOAD:RULES:REFACTOR]`
- **Documentation**: `[LOAD:RULES:DOCS]`
- **Infrastructure**: `[LOAD:RULES:INFRA]`
- **Operations**: `[LOAD:RULES:OPS]`

## Execution Baseline

1. **Load Gateway**: Always start with [docs/agentic/gateway.md](docs/agentic/gateway.md).
2. **Skill Autonomy**: Use any tool in your bundle. No restrictions.
3. **Draft Plans**: Use pluralized paths for implementation plans ([docs/plans/](docs/plans/)).
4. **Validation**: Always run `docker compose config` before updating infrastructure.
