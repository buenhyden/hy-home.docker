---
layer: agentic
---

# AI Agent Standards

Shared standards for instruction design, token efficiency, and execution quality.

## 1. Token Optimization and Lazy Loading

- Keep `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` as thin entry shims.
- Keep detailed governance only in `docs/00.agent-governance/`.
- Load in this order:
  1. `rules/bootstrap.md`
  2. `rules/persona.md`
  3. `rules/task-checklists.md`
  4. one primary `scopes/<layer>.md`
  5. `rules/stage-authoring-matrix.md` (docs authoring only)
  6. `rules/github-governance.md` (PR / merge / review tasks only)
  7. stage docs JIT (`docs/01` to `docs/11`, then `docs/90` or `docs/99`)
- Avoid duplicated instructions across root shims and rule files.

## 2. Language Standard

- Governance and provider policy files in `docs/00.agent-governance/` must be English.
- Human-facing repository guides and narratives should be Korean.
- User-facing agent responses should be Korean unless explicitly requested otherwise.

## 3. Stage-Gate Compliance

- Treat `docs/01` to `docs/99` as project SSoT.
- Do not bypass `docs/01.prd` and `docs/04.specs` for implementation work.
- Keep reciprocal traceability across PRD, ARD, ADR, Spec, Plan, Task, Guide, Operations, and Runbook artifacts.

## 4. Execution Discipline

- Use checklists from `rules/task-checklists.md` before, during, and after work.
- Use templates from `docs/99.templates/` when creating new stage docs.
- Prefer small, isolated changes with explicit verification evidence.
- Remove stale commands and dead links in editable scope immediately.

## 5. GitHub Repository and PR Standards

GitHub-specific repository, PR, and CI policy is governed by `rules/github-governance.md`.
This section is intentionally thin to avoid duplication. Refer to that document for:

- Branch protection and ruleset expectations.
- PR completion gate (required checks, required reviews, CODEOWNERS).
- GitHub Actions security baseline (least-privilege, OIDC, pinned actions, secret safety).
- AI instruction precedence (Copilot instructions vs. repo-local governance).
