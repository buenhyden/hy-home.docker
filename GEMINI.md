---
layer: agentic
---

# GEMINI.md

Gemini-optimized operational patterns for `hy-home.docker`.

## 1. CORE DIRECTIVE
Follow the primary contract in **[AGENTS.md](AGENTS.md)**. Use your large context window to map cross-tier dependencies effectively across all 10 infrastructure blocks.

## 2. CONTEXT ANCHORING
When processing the codebase, anchor your reasoning based on:
1.  **[System Definition](docs/00.agent/05.system-spec.md)**: Technical boundaries.
2.  **[Behavioral Policy](docs/00.agent/03.behavior.md)**: Prompting and interaction standards.
3.  **[Gateway Dispatcher](docs/00.agent/01.gateway.md)**: Document discovery and lazy-loading.

## 3. LAZY-LOADING TRIGGERS
Execute specialized tasks by loading focused context markers:
- `[LOAD:RULES:REFACTOR]` — System-wide refactoring logic.
- `[LOAD:RULES:INFRA]` — Infrastructure lifecycle and validation.
- `[LOAD:RULES:DOCS]` — Documentation taxonomy (01~99) enforcement.
- `[LOAD:RULES:OPS]` — Operational procedures and incident handling.

## 4. WORKFLOW ANCHOR
ALWAYS generate a detailed implementation plan in `docs/05.plans/` before execution. Ensure plans account for `COMPOSE_PROFILES` dependencies.
