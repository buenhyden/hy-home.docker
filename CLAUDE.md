---
layer: agentic
---

# CLAUDE.md

Claude-optimized operational patterns for `hy-home.docker`.

## 1. Shared Protocols (Core)
@docs/00.agent/claude-provider.md
@docs/00.agent/README.md
@docs/00.agent/rules/bootstrap.md

## 2. Identity Hub
Always load **[Identity Hub](docs/00.agent/README.md)** at the start of every session to establish governance.

## 3. Cognitive Patterns
- **Thinking First**: Describe intended logic in `<thinking>` tags before calling tools.
- **Task Boundaries**: Encapsulate independent work units within `<task>` boundaries.
- **JIT Context**: Use `[LOAD:RULES:<CAT>]` markers for Just-In-Time context loading.

## 4. Workflow Strategy
Always generate a detailed implementation plan in `docs/05.plans/` before execution. Follow the governance defined in `docs/00.agent/README.md`.
