---
layer: docs
---

# Documentation Operational Scope

Boundaries and permissions for agents interacting with repository documentation.

## 1. Context and Objective

- Agentic hub: `docs/00.agent-governance/` (primary authority for agents).
- Project docs: `docs/01.prd/` to `docs/11.postmortems/`, plus `docs/90.references/` and `docs/99.templates/`.
- Root instructions: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`.

## 2. Operational Permissions

- Read: proactive discovery through stage README files and indexes.
- Write:
  - `docs/00.agent-governance/**`: allowed.
  - `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `README.md`: allowed.
  - `docs/01` to `docs/99`: read-only by default; explicit user approval required.

## 3. Maintenance Standards

- Language policy:
  - AI-focused docs (rules/scopes/providers/root shims): English.
  - Human-facing docs (README, guides, runbooks, reports): Korean by default.
- Link integrity: no broken links, no absolute filesystem links, no `file://` URIs.
- Taxonomy compliance: follow stage mapping in `rules/stage-authoring-matrix.md`.

## 4. Out-of-Scope Handling

If breakages are found in read-only stages (`docs/01` to `docs/99`):

1. Do not patch those files.
2. Record findings in `docs/00.agent-governance/memory/` with recommended fixes and priorities.
3. Reference the report in completion notes.
