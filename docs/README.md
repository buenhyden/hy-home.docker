# Documentation Hub (Human Domain)

This directory contains long-term, human-readable project documentation used across planning, design, and reference delivery.

## Purpose

- Retain durable project knowledge that must survive beyond a single feature implementation.
- **Isolate product/design knowledge** from executable logic (`specs/`), operational scripts (`runbooks/`), and AI Automation logic (`.agent/workflows/`).
- Serve as the primary reference point for **Human Developers** trying to understand the system.

## Sub-Directories & Content Mapping

- `adr/` — **Architecture Decision Records**. Must use `templates/architecture/adr-template.md`. Used for capturing "Why" a technical decision was made.
- `ard/` — **Architecture Reference Documents**. Must use `templates/architecture/ard-template.md`. Used for deep structural "How" designs.
- `prd/` — **Product Requirements Documents**. Must use `templates/product/prd-template.md`. Used for "What" features we are building and success metrics.
- `guides/` — Human-centric lifecycle procedures. Contains `pre-development-guide.md`, `during-development-guide.md`, `post-development-guide.md`.
- `api/` — API references, schemas, and contract documentation.
- `manuals/` — Non-technical human process manuals.

## Explicit Boundaries & Rules

1. **NO RUNBOOKS ALLOWED**: Do NOT create a `docs/runbook/` folder. All playbooks, incident response guides, and deployment workflows must go in the root `/runbooks/` directory.
2. **NO SPECS ALLOWED**: Do NOT place implementation specs here. All coding specs belong in `/specs/`.
3. **NO AI WORKFLOWS ALLOWED**: Do NOT place AI agent behavioral guidelines or prompts here. Those belong strictly in `.agent/workflows/`.
4. **TEMPLATE MANDATORY**: Any new ADR, ARD, or PRD created in this folder **MUST** be generated from its respective counterpart in the `templates/` directory.
5. **DOCUMENTATION PILLAR**: All content in this directory is subject to the Document Pillar (`.agent/rules/2100-documentation-pillar.md`) and must adhere to the Diátaxis framework where applicable.
6. **PROJECT-SPECIFIC OVERRIDES**: The `guides/` and `manuals/` folders serve as the official location for project-specific overrides to the generic `.agent/rules/`. AI Agents will prioritize instructions in these local guides during execution.
