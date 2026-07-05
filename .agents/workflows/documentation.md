---
layer: agentic
---

# Documentation Workflow

Gemini/Antigravity workflow adapter for repository documentation work. The
canonical documentation rules live in Stage 00 and Stage 99; this file only
orders the runtime steps.

## 1. Objective

Apply the repository documentation workflow while deferring policy ownership to
`docs/00.agent-governance/` and template ownership to `docs/99.templates/`.

## 2. Pipeline Steps

1. **Load owner rules**: Read `AGENTS.md`,
   `docs/00.agent-governance/scopes/docs.md`,
   `docs/00.agent-governance/rules/documentation-protocol.md`, and the
   target stage row in `docs/00.agent-governance/rules/stage-authoring-matrix.md`.
2. **Select runtime tier**: Use the Gemini model tier from
   `docs/00.agent-governance/subagent-protocol.md`; do not redefine model
   values here.
3. **Load mapped template**: Use the template path defined by
   `docs/00.agent-governance/rules/documentation-protocol.md` and
   `docs/99.templates/support/template-selection.md`.
4. **Draft in the right place**: Use `_workspace/repo-support/` only for intermediate
   analysis. Active artifacts must be written to the canonical stage path.
5. **Validate before completion**: Run the repository gates required by the
   owner rules, including target-relative link and template-contract checks for
   changed stage documents.
