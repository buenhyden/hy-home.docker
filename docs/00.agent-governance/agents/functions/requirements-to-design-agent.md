---
layer: agentic
---

# requirements-to-design-agent

## Overview

Bridges Stage 01 (requirements) to Stage 02 (architecture) by tracing PRD items
to ARD/ADR outputs and identifying handoff traceability gaps.

## Purpose

Ensure every product requirement has a traceable architecture requirement or
decision. Surface gaps without creating duplicate documents.

## Scope

**Covers:**

- PRD to ARD/ADR traceability gap analysis
- New ARD or ADR stub creation in `docs/02.architecture/`

**Excludes:**

- Spec authoring (handled by stage 03 workflow)
- Implementation planning (handled by execution-plan-agent)

## Structure

- Reads `docs/01.requirements/README.md` PRD inventory
- Reads `docs/02.architecture/requirements/` and `decisions/` ARD/ADR inventory
- Reports gaps as a table; proposes stubs only with user approval

## Agents

- **doc-writer** — primary caller

## Skills

- `.claude/skills/requirements-to-design-agent/skill.md`

## Usage

- **Inputs:** PRD inventory, ARD/ADR inventory, stage-authoring-matrix
- **Outputs:** gap report table, optional ARD/ADR stubs, updated cross-links

## Related Documents

- `../../scopes/docs.md`
- `../../rules/stage-authoring-matrix.md`
- `../README.md`
