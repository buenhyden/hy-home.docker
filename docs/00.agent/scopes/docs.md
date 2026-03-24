---
layer: agentic
---

# Documentation Operational Scope

**Boundaries and permissions for agents interacting with project documentation.**

## 1. Domain Boundaries

- **Agentic Hub**: `docs/00.agent/` (Primary Authority for Agents).
- **Project Docs**: `docs/01.prd/` to `docs/99.templates/`.
- **Root Instructions**: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`.

## 2. Operational Permissions

- **READ**: Proactive discovery of project context via `docs/README.md` and related indexes.
- **WRITE**:
  - **docs/00.agent/**: Allowed for maintenance, translations, and rule updates.
  - **docs/[01~99]**: **READ-ONLY** by default. Changes require explicit User review and approval.
  - **Root Instructions**: Minimal shims only; details must be offloaded to the Agentic Hub.

## 3. Maintenance Standards

- **English Only**: All agent-facing documentation MUST be in English.
- **Link Integrity**: No broken links, absolute paths, or `file://` URIs.
- **Taxonomy Compliance**: Maintain the `NN.topic.md` numbering system.

