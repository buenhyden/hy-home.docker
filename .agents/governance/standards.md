---
title: "AI Agent Standards"
version: "1.2.2"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-11-13"
---

# AI Agent Standards

## Purpose

### Objective

Shared standards for instruction design, token efficiency, and execution quality.

### Authority

This policy is the canonical owner of shared instruction, token, language, and execution standards under [bootstrap precedence](bootstrap.md#authority-and-precedence).

## Scope

### Applies To

Loading cost, language, stage gates, execution discipline, and GitHub delivery standards.

### Exclusions

None: this document states no exclusion.

## Rules

### Requirements

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

### Enforcement

None: this document states no separate check.

## Exceptions

### Exception Conditions

No exception is granted here; a separately authorized operation follows [Approval boundaries](approval-boundaries.md).

### Approval and Review

None: no exception exists to approve.

## Ownership

### Responsibilities

`@buenhyden` approves changes; `rules-engineer` reviews them ([approval boundaries](approval-boundaries.md#authorization-source-and-records)).

### Change and Adoption

Changes land in place with Task evidence; related documents:

- `.agents/governance/bootstrap.md`
- `.agents/governance/agentic.md`
- `.agents/governance/github-governance.md`
- `.agents/governance/quality-standards.md`
