---
layer: agentic
---

# GEMINI.md

**Gemini-optimized cognitive patterns and session briefing.**

## 1. Core Protocols

- **Governance Hub**: [docs/00.agent-governance/README.md](docs/00.agent-governance/README.md)
- **Specific Configuration**: [docs/00.agent-governance/gemini-provider.md](docs/00.agent-governance/gemini-provider.md)

## 2. Token Optimization & JIT Context

- **Lazy Loading**: Use `[LOAD:RULES:<CAT>]` for on-demand knowledge from `docs/00.agent-governance/rules/`.
- **Taxonomy Routing**: Ingest task context via JIT markers (e.g., `[LOAD:PRD]`, `[LOAD:ADR]`).
- **Reasoning**: Always document the "Why" in execution summaries.

## 3. Response Strategy

- **Language**: ALWAYS respond to the USER in **Korean**.
- **Planning**: Draft all implementation plans in `docs/05.plans/` first.
