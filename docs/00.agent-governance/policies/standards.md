---
title: AI Agent Standards
type: governance/policy
layer: agent-governance
owner: "@buenhyden"
---

# AI Agent Standards

Shared standards for instruction design, token efficiency, and execution quality.

## 1. Token Optimization and Lazy Loading

- Use only the canonical order in
  `policies/bootstrap.md#canonical-load-order`.
- Avoid duplicated instructions across root shims and rule files.

## 2. Language Standard

- Route artifact language by document role through
  `policies/documentation-protocol.md#authoring-rules`.
- Conversational responses follow the user's active language preference under
  `policies/output-style.md`.

## 3. Stage-Gate Compliance

- Treat `docs/01` to `docs/99` as project SSoT.
- Do not bypass `docs/01.requirements` and `docs/03.specs` for implementation work.
- Keep reciprocal traceability across Requirement Package, Architecture
  Description, ADR, Spec, Plan, Task, Guide, Policy, and Runbook artifacts.

## 4. Execution Discipline

- Use checklists from `policies/task-checklists.md` before, during, and after work.
- Use templates from `docs/99.templates/` when creating new stage docs.
- Prefer small, isolated changes with explicit verification evidence.
- Remove stale commands and dead links in editable scope immediately.

## 5. GitHub Repository and PR Standards

GitHub-specific repository, PR, and CI policy is governed by `policies/github-governance.md`.
This section is intentionally thin to avoid duplication. Refer to that document for:

- Branch protection and ruleset expectations.
- PR completion gate (required checks, required reviews, CODEOWNERS).
- GitHub Actions security baseline (least-privilege, OIDC, pinned actions, secret safety).
- Local instruction authority boundary (`docs/00.agent-governance/` + `.claude/` vs. GitHub-native instruction files).

## Related Documents

- `docs/00.agent-governance/policies/bootstrap.md`
- `docs/00.agent-governance/policies/agentic.md`
- `docs/00.agent-governance/policies/github-governance.md`
- `docs/00.agent-governance/policies/quality-standards.md`
