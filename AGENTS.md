---
layer: agentic
---

# AGENTS.md

Canonical working contract for all AI agents in `hy-home.docker`.

## 1. Governance Model

This repository follows a **Spec-Driven Infrastructure** lifecycle. Agents MUST NOT implement features without an approved PRD, Spec, and Plan.

## 2. Discovery Gateway

To avoid context bloat, agents use a lazy-loading protocol.

1. **Start**: Read [docs/agentic/gateway.md](docs/agentic/gateway.md).
2. **Behavior**: Read [docs/agentic/instructions.md](docs/agentic/instructions.md).
3. **Trigger**: Use `[LOAD:RULES:<CATEGORY>]` to pull specific logic from `docs/agentic/rules/`.

## 3. Tool Policy

- **Full Skill Autonomy**: Agents are encouraged to use any purpose-fit skill in their toolkit.
- **Verification**: All code changes must be validated via `docker compose config`.

## 4. Documentation Taxonomy

- **Authority**: `docs/adr/`, `docs/ard/`, `docs/prd/`.
- **Implementation**: `docs/plans/`, `docs/specs/`, `docs/runbooks/`.
