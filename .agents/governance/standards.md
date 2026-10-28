---
title: "AI Agent Standards"
version: "1.1.0"
type: "governance/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-29"
---

# AI Agent Standards

## Overview

Shared standards for instruction design, token efficiency, and execution quality.

## Scope

Loading cost, language, stage gates, execution discipline, and GitHub delivery standards.

## Rules

### 1. Token Optimization and Lazy Loading

- Use only the canonical order in
  `.agents/governance/bootstrap.md#canonical-load-order`.
- Avoid duplicated instructions across root shims and rule files.

### 2. Language Standard

- Stage 01·02·03의 non-README 본문은 영어로, 모든 `README.md`와
  `docs/05.operations/` 본문은 한국어로 작성합니다. native key, 필수 heading,
  명령·코드·인용은 원래 형식을 유지합니다. profile별 판정은
  `.agents/governance/documentation-protocol.md#document-language`가 소유합니다.
- Conversational responses follow the user's active language preference under
  `.agents/governance/output-style.md`.

### 4. Execution Discipline

- Use checklists from `.agents/governance/task-checklists.md` before, during, and after work.
- Use templates from `docs/99.templates/` when creating new stage docs.
- Prefer small, isolated changes with explicit verification evidence.
- Remove stale commands and dead links in editable scope immediately.

### 5. GitHub Repository and PR Standards

GitHub-specific repository, PR, and CI policy is governed by `.agents/governance/github-governance.md`.
This section is intentionally thin to avoid duplication. Refer to that document for:

- Branch protection and ruleset expectations.
- PR completion gate (required checks, required reviews, CODEOWNERS).
- GitHub Actions security baseline (least-privilege, OIDC, pinned actions, secret safety).
- Local instruction authority boundary (`.agents/` + `.claude/` vs. GitHub-native instruction files).

## Exceptions

No exception is granted here; a separately authorized operation follows [Approval boundaries](approval-boundaries.md).

## Verification

### 3. Stage-Gate Compliance

- Treat `docs/01` to `docs/99` as project SSoT.
- Do not bypass `docs/01.requirements` and `docs/03.specs` for implementation work.
- Keep reciprocal traceability across Requirement Package, Architecture
  Description, ADR, Spec, Plan, Task, Guide, Policy, and Runbook artifacts.

## Related Documents

- `.agents/governance/bootstrap.md`
- `.agents/governance/agentic.md`
- `.agents/governance/github-governance.md`
- `.agents/governance/quality-standards.md`
