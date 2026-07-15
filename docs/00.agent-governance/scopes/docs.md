---
layer: docs
---

# Documentation Operational Scope

Boundaries and permissions for agents interacting with repository documentation.

## 1. Context and Objective

- Agentic hub: `docs/00.agent-governance/` (primary authority for agents).
- Project docs: `docs/01.requirements/` to `docs/05.operations/incidents/`, plus `docs/90.references/`, `docs/98.archive/`, and `docs/99.templates/`.
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
  - Human-facing docs (README, operations, reports): Korean by default.
- Link integrity: no broken links, no absolute filesystem links, no `file://` URIs.
- Taxonomy compliance: follow stage mapping in `rules/stage-authoring-matrix.md`.
- Template-first compliance: before creating or modifying target-stage docs
  under `docs/01.requirements/`, `docs/02.architecture/`, `docs/03.specs/`,
  `docs/04.execution/`, `docs/05.operations/`, `docs/90.references/`,
  or `docs/98.archive/`,
  load the mapped template from `docs/99.templates/templates/` and keep its
  required contract.
- Active stage artifacts must live only in canonical stage paths; non-stage `docs/*` paths are not valid targets for active specs, plans, or tasks.

## 4. Out-of-Scope Handling

If breakages are found in read-only stages (`docs/01` to `docs/99`):

1. Do not patch those files.
2. Record findings in `docs/00.agent-governance/memory/` with recommended fixes and priorities.
3. Reference the report in completion notes.

If legacy active-stage content is found in a non-stage `docs/*` path:

1. Migrate the content into the canonical stage path.
2. Remove the legacy file after README and link synchronization.
3. Do not leave redirect-style active artifacts in non-stage locations.

If a whole active document conflicts with current implementation, move it to a
`docs/98.archive/<original-stage>/...` tombstone, remove active references, and
record the migration in the archive README.

## 5. File Ownership SSOT

| Path Pattern                          | Owner Agent  | Read-Only For                           |
| ------------------------------------- | ------------ | --------------------------------------- |
| `docs/00.agent-governance/`           | `doc-writer`   | governance rules — all agents read      |
| `docs/90.references/llm-wiki/`        | `doc-writer`   | `knowledge-map-agent` (generated-index procedure) |
| `docs/98.archive/`                    | `doc-writer`   | all other agents                         |
| `docs/99.templates/`                  | `doc-writer`   | all — template edits need user approval |
| `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` | `doc-writer`   | all other agents                        |
| `docs/05.operations/`                 | `doc-writer`   | all other agents                        |

## 6. Subagent Bridge

```text
# doc-writer agent preamble
@import docs/00.agent-governance/scopes/docs.md
# Docs pattern — template → draft → link
# DOCS 3 RULES enforced (R1 template · R2 README · R3 related-docs)
# Changed target-stage docs must pass check-repo-contracts template gate.
```

Spawn via the active runtime's delegated-agent facility. Do not embed documentation policy inline in agent files.

## Related Documents

- `docs/00.agent-governance/rules/documentation-protocol.md`
- `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- `docs/00.agent-governance/rules/task-checklists.md`
- `AGENTS.md`
