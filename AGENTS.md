---
layer: agentic
---

# AGENTS.md

Canonical working contract for all AI agents in `hy-home.docker`.

## Rule Triggers

Identify your task and load the required rule module:

- **Refactoring**: `[LOAD:RULES:REFACTOR]`
- **Documentation**: `[LOAD:RULES:DOCS]`
- **Infrastructure**: `[LOAD:RULES:INFRA]`
- **Operations**: `[LOAD:RULES:OPS]`

## Execution Baseline

1. **Load Gateway**: Always start with [docs/agentic/gateway.md](docs/agentic/gateway.md).
2. **Skill Autonomy**: Use any tool in your bundle (Ref: [March 2026 Agentic Standard](docs/adr/0003-2026-march-agentic-standard.md)).
3. **Draft Plans**: Use pluralized paths for implementation plans ([docs/plans/](docs/plans/)).
4. **Validation**: Always run `docker compose config` before updating infrastructure (Ref: [ARCHITECTURE.md](ARCHITECTURE.md)).
5. **Safety & Ethics**: Adhere to [Code of Conduct](CODE_OF_CONDUCT.md) standards for interaction.
