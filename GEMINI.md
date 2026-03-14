---
layer: agentic
---

# Gemini Project Context

Gemini-specific root only. Shared repository policy lives in [AGENTS.md](AGENTS.md) and the linked `docs/agentic/*.md` guides.

## Rule Triggers

Identify your task category and load the rule module immediately.

- **Docs Migration**: `[LOAD:RULES:REFACTOR]`
- **Management Docs**: `[LOAD:RULES:DOCS]`
- **Infra/Compose**: `[LOAD:RULES:INFRA]`
- **SRE/Ops**: `[LOAD:RULES:OPS]`

## Gemini Execution Notes

- Always load [docs/agentic/gateway.md](docs/agentic/gateway.md) at session start.
- For complex tasks (spec/plan creation), activate **Reasoner** persona before specialist personas.
- **Skill Autonomy**: Use any available tool in your bundle. No restrictions apply.
- Validate all infrastructure changes with `docker compose config` before proposing `up`.
