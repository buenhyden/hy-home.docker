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

Use the following JIT loading markers to ingest task-specific context from the documentation taxonomy:

| Marker | Target README | Intent |
| :--- | :--- | :--- |
| `[LOAD:PRD]` | `docs/01.prd/README.md` | High-level requirements & vision |
| `[LOAD:ARD]` | `docs/02.ard/README.md` | Architectural reference & qualities |
| `[LOAD:ADR]` | `docs/03.adr/README.md` | Technical decisions & records |
| `[LOAD:SPECS]` | `docs/04.specs/README.md` | SSoT technical specifications |
| `[LOAD:PLANS]` | `docs/05.plans/README.md` | Implementation & validation plans |
| `[LOAD:RUNBOOKS]` | `docs/09.runbooks/README.md` | Operational execution procedures |

## Specialized Rule Dispatcher

| Strategy | Rule File | Dispatcher Marker |
| :--- | :--- | :--- |
| **Core Governance** | `rules/bootstrap.md` | `[LOAD:RULES:BOOTSTRAP]` |
| **Persona Matrix** | `rules/persona-matrix.md` | `[LOAD:RULES:PERSONA]` |
| **Documentation** | `scopes/docs.md` | `[LOAD:RULES:DOCS]` |

## Language Policy

- **Governance Documentation**: All files in this directory MUST be written in **English** for consistency and token efficiency.
- **User Communication**: AI Agents MUST translate all responses, summaries, and notifications into humanized **Korean**.
- **Rule Enforcement**: Follow the centralized policy in `rules/language-policy.md`.

## Compliance

All documentation in this project follows the **01-11 Stage-Gate Taxonomy**. AI Agents must ensure that internal technical docs are in English while human-facing manuals are in Korean.
