---
layer: agentic
---

# GEMINI.md

Gemini-specific operational triggers and guidance for `hy-home.docker`.

## 1. Core Contract

AI agents MUST follow the primary technical contract and "Day 1" commands defined in [AGENTS.md](AGENTS.md).

## 2. Gemini Optimized Workflow

As an agent with a large context window and advanced planning capabilities, prioritize the following:

- **Tiered Orchestration**: The infrastructure is split into 10 logical tiers under `infra/`. Use your ability to map cross-tier dependencies (e.g., how `02-auth` depends on `04-data/postgresql`).
- **Plan Verification**: When generating implementation plans in `docs/plans/`, ensure they account for the profile-driven nature of the stack (`COMPOSE_PROFILES`).
- **Interactive Discovery**: Proactively use the [Discovery Hub](docs/agentic/gateway.md) to find specialized rules for complex refactoring or infra tasks.

## 3. Rule Triggers

Identify your task and load the required rule module:

- **Refactoring**: `[LOAD:RULES:REFACTOR]` (Follows [March 2026 Standard](docs/adr/0003-2026-march-agentic-standard.md))
- **Documentation**: `[LOAD:RULES:DOCS]`
- **Infrastructure**: `[LOAD:RULES:INFRA]` (See [ARCHITECTURE.md](ARCHITECTURE.md))
- **Operations**: `[LOAD:RULES:OPS]` (See [OPERATIONS.md](OPERATIONS.md))
