---
layer: agentic
---

# GEMINI.md

Gemini-optimized operational patterns for `hy-home.docker`.

## 1. Shared Protocols (Core)
@file:docs/00.agent/gemini-provider.md
@file:docs/00.agent/README.md
@file:docs/00.agent/rules/bootstrap.md

## 2. Identity Hub
Always load **[Identity Hub](docs/00.agent/README.md)** at the start of every session to establish governance.

## 3. Cognitive Patterns
- **Token Hygiene**: Prioritize on-demand loading via `docs/00.agent/README.md`.
- **Reasoning Loop**: Document the "Why" behind command choices in the execution summary.
- **JIT Context**: Use `[LOAD:RULES:<CAT>]` markers for Just-In-Time knowledge retrieval.

## 4. Workflow Strategy
Always generate a detailed implementation plan in `docs/05.plans/` before execution. Follow the governance defined in `docs/00.agent/README.md`.
