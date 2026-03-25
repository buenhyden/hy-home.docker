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

## Gateway Dispatcher (JIT Context)

Use the following JIT loading markers to ingest task-specific context from the documentation taxonomy:

| Marker | Target README | Intent |
| :--- | :--- | :--- |
| `[LOAD:PRD]` | `docs/01.prd/README.md` | High-level requirements & vision |
| `[LOAD:ARD]` | `docs/02.ard/README.md` | Architectural reference & qualities |
| `[LOAD:ADR]` | `docs/03.adr/README.md` | Technical decisions & records |
| `[LOAD:SPECS]` | `docs/04.specs/README.md` | SSoT technical specifications |
| `[LOAD:PLANS]` | `docs/05.plans/README.md` | Implementation & validation plans |
| `[LOAD:TASKS]` | `docs/06.tasks/README.md` | Granular task & progress tracking |
| `[LOAD:RUNBOOKS]` | `docs/09.runbooks/README.md` | Operational execution procedures |

## Specialized Rule Dispatcher

| Strategy | Rule File | Dispatcher Marker |
| :--- | :--- | :--- |
| **Core Governance** | `rules/bootstrap.md` | `[LOAD:RULES:BOOTSTRAP]` |
| **Persona Matrix** | `rules/persona-matrix.md` | `[LOAD:RULES:PERSONA]` |
| **Language Policy** | `rules/language-policy.md` | `[LOAD:RULES:LANG]` |
| **Git Workflow** | `rules/git-workflow.md` | `[LOAD:RULES:GIT]` |
| **Operations** | `scopes/ops.md` | `[LOAD:RULES:OPS]` |
| **Documentation** | `scopes/docs.md` | `[LOAD:RULES:DOCS]` |

## Language Policy

- **Governance Documentation**: All files in this directory MUST be written in **English** (token optimized).
- **User Communication**: AI Agents MUST translate all responses and notifications into manual **Korean**.
- **Rule Enforcement**: Follow the centralized policy in [language-policy.md](rules/language-policy.md).

## Compliance

All work must follow the **01-11 Stage-Gate Taxonomy**. Decisions must be anchored in ADRs, and implementations must be grounded in approved Specs.
