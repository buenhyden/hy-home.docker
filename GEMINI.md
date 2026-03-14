---
layer: agentic
---

# Gemini Project Context

Gemini-specific root only. Shared repository policy lives in [AGENTS.md](AGENTS.md) and the linked `docs/agentic/*.md` guides.

## Shared References

- [AGENTS.md](AGENTS.md) — Canonical cross-agent entrypoint
- [docs/agentic/gateway.md](docs/agentic/gateway.md) — Centralized discovery gateway

## Gemini Execution Notes

- Always load [docs/agentic/gateway.md](docs/agentic/gateway.md) at session start.
- Use `[LOAD:*]` markers from instructions to identify which doc families to read.
- Validate all infrastructure changes with `docker compose config` before proposing `up`.
- For complex tasks, activate Reasoner persona before specialist personas.
