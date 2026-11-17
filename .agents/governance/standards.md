---
title: "AI Agent Standards"
version: "1.3.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-17"
---

# AI Agent Standards

## Purpose and Scope

### Objective

Shared standards for instruction design, token efficiency, and execution quality.

#### Authority

This policy is the canonical owner of shared instruction, token, language, and execution standards under [bootstrap precedence](bootstrap.md#authority-and-precedence).

### Applies To

Loading cost, language, stage gates, execution discipline, and GitHub delivery standards.

#### Exclusions

None: this document states no exclusion.

## Rules

### Requirements

| Rule ID | Condition | Requirement | Enforcement | Evidence |
| --- | --- | --- | --- | --- |
| STANDARDS-R1 | Always | Required: use only the canonical load order in `.agents/governance/bootstrap.md#canonical-load-order` | none | none |
| STANDARDS-R2 | Always | Required: avoid duplicated instructions across root shims and rule files | none | none |
| STANDARDS-R3 | Always | Required: follow document language from `.agents/governance/documentation-protocol.md#document-language` | none | none |
| STANDARDS-R4 | Always | Required: conversational responses follow the user's active language preference under `.agents/governance/output-style.md` | none | none |
| STANDARDS-R5 | Before, during, and after work | Required: use checklists from `.agents/governance/task-checklists.md` | none | none |
| STANDARDS-R6 | Creating new stage docs | Required: use templates from `docs/99.templates/` | none | none |
| STANDARDS-R7 | Always | Required: prefer small isolated changes with explicit verification evidence | none | Explicit verification evidence |
| STANDARDS-R8 | Editable scope | Required: remove stale commands and dead links immediately | none | none |
| STANDARDS-R9 | GitHub repository/PR/CI matters | Required: follow `.agents/governance/github-governance.md` | none | none |
| STANDARDS-R10 | Implementation work | Required: treat `docs/01` to `docs/99` as project SSoT | none | none |
| STANDARDS-R11 | Implementation work | Forbidden: bypassing `docs/01.requirements` and `docs/03.specs` | none | none |
| STANDARDS-R12 | Stage artifacts | Required: keep reciprocal traceability across Requirement Package/Architecture Description/ADR/Spec/Plan/Task/Guide/Policy/Runbook artifacts | none | none |

#### 1. Token Optimization and Lazy Loading

- Use only the canonical order in
  `.agents/governance/bootstrap.md#canonical-load-order`.
- Avoid duplicated instructions across root shims and rule files.

#### 2. Language Standard

- Document language is owned by
  `.agents/governance/documentation-protocol.md#document-language`.
- Conversational responses follow the user's active language preference under
  `.agents/governance/output-style.md`.

#### 3. Execution Discipline

- Use checklists from `.agents/governance/task-checklists.md` before, during, and after work.
- Use templates from `docs/99.templates/` when creating new stage docs.
- Prefer small, isolated changes with explicit verification evidence.
- Remove stale commands and dead links in editable scope immediately.

#### 4. GitHub Repository and PR Standards

GitHub-specific repository, PR, and CI policy is governed by `.agents/governance/github-governance.md`.
This section is intentionally thin to avoid duplication. Refer to that document for:

- Branch protection and ruleset expectations.
- PR completion gate (required checks, required reviews, CODEOWNERS).
- GitHub Actions security baseline (least-privilege, OIDC, pinned actions, secret safety).
- Local instruction authority boundary (`.agents/`, `.claude/` and `.codex/` vs. GitHub-native instruction files).

#### Stage-Gate Compliance

- Treat `docs/01` to `docs/99` as project SSoT.
- Do not bypass `docs/01.requirements` and `docs/03.specs` for implementation work.
- Keep reciprocal traceability across Requirement Package, Architecture
  Description, ADR, Spec, Plan, Task, Guide, Policy, and Runbook artifacts.

### Exceptions

#### Exception Conditions

No exception is granted here; a separately authorized operation follows [Approval boundaries](approval-boundaries.md).

#### Approval and Review

None: no exception exists to approve.

## Enforcement

### Mechanisms

None: this document states no separate check.

### Limits

The policy states no separate check (`Mechanisms` is `None`), so every rule rests on review and on the policies it points to:

- Load order, duplication, language, checklist use, templates, small changes, and stale-link removal (R1-R8): no validator is named.
- GitHub, CI, and PR standards (R9) are delegated to `github-governance.md`; their enforcement is not shown here.
- Stage-gate compliance and reciprocal traceability (R10-R12): no check is named.

## Ownership

### Owner

`@buenhyden` approves changes; `rules-engineer` reviews them ([approval boundaries](approval-boundaries.md#authorization-source-and-records)).

### Review Triggers

Changes land in place with Task evidence; related documents:

- `.agents/governance/bootstrap.md`
- `.agents/governance/agentic.md`
- `.agents/governance/github-governance.md`
- `.agents/governance/quality-standards.md`
