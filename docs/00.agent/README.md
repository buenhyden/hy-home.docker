---
layer: agentic
---

# AI Agent Governance Hub

Welcome to the central governance directory for AI Agents. This folder defines the rules, scopes, and protocols for all automated and assisted development tasks.

## Identity Protocol

AI Agents must establish identity via [AGENTS.md](../../AGENTS.md) and load this hub at session start.

## Directory Structure

- `rules/`: Universal core governance, persona mapping, and repository-wide standards.
- `scopes/`: Layer-specific technical instructions and constraints (Architecture, Backend, Infra, etc.).
- `claude-provider.md`: Provider-specific configuration for Claude Code.
- `gemini-provider.md`: Provider-specific configuration for Gemini CLI.

## Gateway Dispatcher

Use the following markers to load task-specific context via external `README.md` files:

| Marker | Target README | Intent |
| :--- | :--- | :--- |
| `[LOAD:PRD]` | `docs/01.prd/README.md` | Understanding high-level requirements |
| `[LOAD:ARD]` | `docs/02.ard/README.md` | Reviewing architectural qualities |
| `[LOAD:ADR]` | `docs/03.adr/README.md` | Reviewing technical decisions |
| `[LOAD:SPECS]` | `docs/04.specs/README.md` | Implementing or verifying specifications |
| `[LOAD:PLANS]` | `docs/05.plans/README.md` | Executing architectural plans |
| `[LOAD:RUNBOOKS]` | `docs/09.runbooks/README.md` | Operational manual tasks |

## Specialized Rule Dispatcher

| Strategy | Rule File | Dispatcher Marker |
| :--- | :--- | :--- |
| **Core Governance** | `rules/bootstrap.md` | `[LOAD:RULES:BOOTSTRAP]` |
| **Persona Matrix** | `rules/persona-matrix.md` | `[LOAD:RULES:PERSONA]` |


## Compliance

All documentation in this project follows the **01-11 Stage-Gate Taxonomy**.
