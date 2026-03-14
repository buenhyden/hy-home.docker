---
title: 'Meta-Documentation & Agentic Framework ARD'
status: 'Draft'
version: 'v1.1.0'
owner: 'Antigravity'
layer: 'architecture'
---

# Meta-Documentation & Agentic Framework ARD

## 1. Directory Taxonomy

The repository follows a flat category-based documentation structure:

- `docs/adr/`: Architectural Decisions.
- `docs/ard/`: Architectural Requirements.
- `docs/prd/`: Product Requirements.
- `docs/specs/`: Technical Specifications.
- `docs/plans/`: Tactical Plans.
- `docs/runbooks/`: Executable procedures.
- `docs/operations/`: Incidence history and postmortems.
- `docs/agentic/`: AI Agent instructions and rules.

## 2. Metadata Schema

Every file MUST contain:

```yaml
---
layer: [common | architecture | backend | frontend | infra | mobile | product | qa | security | entry | meta | ops | agentic]
---
```

## 3. Agent Instruction Architecture

- **Entry Point**: `AGENTS.md` directs all providers to `docs/agentic/gateway.md`.
- **Gateway**: Serves as a lookup table for markers like `[LOAD:TASK_NAME]`.
- **Rules**: Modular rules in `docs/agentic/rules/` contain granular instructions and "Lazy Loading" pointers to relevant `docs/`.
- **Skills**: Skill usage is governed by `docs/agentic/core-governance.md`.
