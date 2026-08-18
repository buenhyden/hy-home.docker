---
layer: agentic
---

# AI Agent Standards

Shared standards for instruction design, token efficiency, and execution quality.

## 1. Token Optimization and Lazy Loading

- Keep `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` as thin entry shims.
- Keep detailed governance only in `docs/00.agent-governance/`.
- Use only the canonical order in
  `rules/bootstrap.md#3-canonical-load-order`.
- Avoid duplicated instructions across root shims and rule files.

## 2. Language Standard

- Route artifact language by document role through
  `rules/documentation-protocol.md#31-language-boundary-by-document-role`.
- Conversational responses follow the user's active language preference under
  `rules/output-style.md`.

## 3. Stage-Gate Compliance

- Treat `docs/01` to `docs/99` as project SSoT.
- Do not bypass `docs/01.requirements` and `docs/03.specs` for implementation work.
- Keep reciprocal traceability across PRD, SRS, Interface Requirement,
  Architecture Description, ADR, Spec, Plan, Task, Guide, Policy, and Runbook artifacts.

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
- Local instruction authority boundary (`docs/00.agent-governance/` + `.claude/` vs. GitHub-native instruction files).

## Related Documents

- `docs/00.agent-governance/rules/bootstrap.md`
- `docs/00.agent-governance/rules/agentic.md`
- `docs/00.agent-governance/rules/github-governance.md`
- `docs/00.agent-governance/rules/quality-standards.md`
