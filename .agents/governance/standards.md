---
title: "AI Agent Standards"
version: "1.0.1"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-09-06"
---

# AI Agent Standards

Shared standards for instruction design, token efficiency, and execution quality.

## 1. Token Optimization and Lazy Loading

- Use only the canonical order in
  `.agents/governance/bootstrap.md#canonical-load-order`.
- Avoid duplicated instructions across root shims and rule files.

## 2. Language Standard

- Route artifact language by document role through
  `.agents/governance/documentation-protocol.md#authoring-rules`.
- Conversational responses follow the user's active language preference under
  `.agents/governance/output-style.md`.

## 3. Stage-Gate Compliance

- Treat `docs/01` to `docs/99` as project SSoT.
- Do not bypass `docs/01.requirements` and `docs/03.specs` for implementation work.
- Keep reciprocal traceability across Requirement Package, Architecture
  Description, ADR, Spec, Plan, Task, Guide, Policy, and Runbook artifacts.

## 4. Execution Discipline

- Use checklists from `.agents/governance/task-checklists.md` before, during, and after work.
- Use templates from `docs/99.templates/` when creating new stage docs.
- Prefer small, isolated changes with explicit verification evidence.
- Remove stale commands and dead links in editable scope immediately.

## 5. GitHub Repository and PR Standards

GitHub-specific repository, PR, and CI policy is governed by `.agents/governance/github-governance.md`.
This section is intentionally thin to avoid duplication. Refer to that document for:

- Branch protection and ruleset expectations.
- PR completion gate (required checks, required reviews, CODEOWNERS).
- GitHub Actions security baseline (least-privilege, OIDC, pinned actions, secret safety).
- Local instruction authority boundary (`.agents/` + `.claude/` vs. GitHub-native instruction files).

## Related Documents

- `.agents/governance/bootstrap.md`
- `.agents/governance/agentic.md`
- `.agents/governance/github-governance.md`
- `.agents/governance/quality-standards.md`
