---
layer: agentic
---

# Agentic Rules Index

This directory contains granular, machine-readable rules for AI agents. These files are designed for **Lazy Loading** via the discovery markers defined in `gateway.md`.

## Active Rules

- [Documentation Standards](documentation-rule.md): Metadata and taxonomy enforcement.
- [Infrastructure Workflows](infrastructure-rule.md): Validation and security protocols for Compose.
- [Persona Matrix](persona-rule.md): Selection guidelines for agent personas.
- [Infrastructure Lifecycle](lifecycle-rule.md): Step-by-step delivery process.
- [Change Governance](governance-rule.md): Verification checklist for architectural changes.

## Usage

Agents should never load this entire directory. Instead, use the `[LOAD:RULES:<CATEGORY>]` markers found in `gateway.md`.
