---
layer: agentic
---

# AI Agent Governance Hub

This directory is the canonical governance system for coding agents in this repository.

## 1. Context & Objective

- **Purpose**: Define deterministic rules for planning, implementation, and documentation workflows.
- **Entry Point**: Agents start from [AGENTS.md](../../AGENTS.md), then load this hub JIT.
- **Compliance Boundary**: Work must align with the Stage-Gate taxonomy in `docs/01` to `docs/11`, plus `docs/90` and `docs/99`.

## 2. Requirements & Constraints

- **Language**: Every file in `docs/00.agent-governance/` must be English-only.
- **Structure**:
  - `rules/`: Shared governance policies and execution standards.
  - `scopes/`: Layer-specific constraints.
  - `providers/`: Agent-runtime-specific overlays.
  - `memory/`: Templates and operating protocol for reusable governance memory.
- **No Duplicate Authority**: Root files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) are thin shims. Detailed policies live here.

## 3. Implementation Flow

### Stage-Gate JIT Markers

| Marker | Target | Purpose |
| :--- | :--- | :--- |
| `[LOAD:PRD]` | `docs/01.prd/README.md` | Product intent and requirements |
| `[LOAD:ARD]` | `docs/02.ard/README.md` | Architecture reference |
| `[LOAD:ADR]` | `docs/03.adr/README.md` | Decision history |
| `[LOAD:SPECS]` | `docs/04.specs/README.md` | Technical source of truth |
| `[LOAD:PLANS]` | `docs/05.plans/README.md` | Implementation planning |
| `[LOAD:TASKS]` | `docs/06.tasks/README.md` | Execution evidence and tracking |
| `[LOAD:GUIDES]` | `docs/07.guides/README.md` | Human-facing guidance |
| `[LOAD:OPS]` | `docs/08.operations/README.md` | Operational policy |
| `[LOAD:RUNBOOKS]` | `docs/09.runbooks/README.md` | Operational procedures |
| `[LOAD:INCIDENTS]` | `docs/10.incidents/README.md` | Incident records |
| `[LOAD:POSTMORTEMS]` | `docs/11.postmortems/README.md` | Lessons learned |
| `[LOAD:REFERENCES]` | `docs/90.references/README.md` | Stable references |
| `[LOAD:TEMPLATES]` | `docs/99.templates/README.md` | Document templates |

### Rule Dispatch Markers

| Marker | Rule |
| :--- | :--- |
| `[LOAD:RULES:BOOTSTRAP]` | `rules/bootstrap.md` |
| `[LOAD:RULES:PERSONA]` | `rules/persona.md` |
| `[LOAD:RULES:STANDARDS]` | `rules/standards.md` |
| `[LOAD:RULES:GIT]` | `rules/git-workflow.md` |
| `[LOAD:RULES:DOCS]` | `rules/documentation-protocol.md` |
| `[LOAD:RULES:QUALITY]` | `rules/quality-standards.md` |
| `[LOAD:RULES:AGENTIC]` | `rules/agentic.md` |

## 4. Operational Procedures

1. Resolve target layer and stage before any mutation.
2. Activate persona through `rules/persona.md`.
3. Load one primary scope from `scopes/` and only adjacent scopes when required.
4. Validate completion using relevant checks and document evidence in stage docs.

## 5. Maintenance & Safety

- Keep policy files concise, explicit, and conflict-free.
- Remove stale commands and dead links immediately.
- Any major governance change should be traceable to an ADR or an explicit user directive.
