---
status: draft
---
<!-- Target: docs/04.execution/plans/2026-05-30-standardizing-agent-governance.md -->

# Standardizing Agent Governance Implementation Plan

**Goal:** Clean up, align, and integrate the AI Agent governance system across Gemini (Antigravity), Claude, and Codex under Antigravity 2.0 IDE standards with perfect verification in `check-repo-contracts.sh`.

---

## Overview (KR)

이 문서는 AI Agent 거버넌스 정비 작업의 실행 계획서다. Gemini/Antigravity 2.0, Claude, Codex용 런타임 설정 및 SSOT 거버넌스(docs/00.agent-governance) 간의 차이와 중복을 정비하고, 유효성 검증 체계를 완벽하게 동기화하기 위한 구체적인 작업 분해 및 완료 기준을 정의한다.

## Context

Current repository maintains a multi-provider setup where Claude acts as canonical runtime, Codex mirrors, and Gemini functions via reference pointers. To prevent rules duplication and version drift, we need to enforce the three-tier Provider Parity Model under Antigravity 2.0.

## Goals & In-Scope

- **Goals**:
  - Enforce perfect parity rules: name parity, content parity, and pointer parity.
  - Verify that the Gemini compatibility surface (`.agents/`) carries no divergent rule copies.
  - Define modern 2026 model assignment policies clearly.

- **In Scope**:
  - `docs/00.agent-governance/` core policies alignment.
  - `GEMINI.md`, `CLAUDE.md`, `AGENTS.md` root shims review.
  - `docs/04.execution/plans/` and `docs/04.execution/tasks/` execution documents creation.
  - Verification run via `check-repo-contracts.sh`.

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Creating new custom subagents or skills that do not exist.
  - Changing functional Docker infra structure or changing compose operations.

- **Out of Scope**:
  - Remote GitHub secrets configuration or live production deployments.

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Create Execution documents | `docs/04.execution/plans/2026-05-30-standardizing-agent-governance.md`, `docs/04.execution/tasks/2026-05-30-standardizing-agent-governance.md` | GOV-001 | Documents exist and match template schemas |
| PLN-002 | Review & Standardize core policies | `docs/00.agent-governance/README.md`, `docs/00.agent-governance/rules/workflows.md`, `docs/00.agent-governance/rules/provider-capability-matrix.md` | GOV-002 | Files aligned with Antigravity 2.0 IDE specifications |
| PLN-003 | Standardize Platform Overlays | `docs/00.agent-governance/providers/gemini.md`, `GEMINI.md`, `AGENTS.md` | GOV-003 | Pointers and model policy checks pass |
| PLN-004 | Execute and fix verification findings | `scripts/validation/check-repo-contracts.sh` | GOV-004 | Shell validation outputs PASS with failures=0 |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | Verify name, content and pointer parity | `bash scripts/validation/check-repo-contracts.sh` | Output says "PASS: repository Docker/docs contracts are synchronized" |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Divergent content in .codex or .agents | Medium | Always use Claude as Tier 2 Canonical source and regenerate/mirror properly |

## Completion Criteria

- [ ] Scoped work completed
- [ ] Verification passed
- [ ] Required docs updated

## Related Documents

- **Task**: [2026-05-30-standardizing-agent-governance task](../tasks/2026-05-30-standardizing-agent-governance.md)
- **Operations**: [Operations index](../../05.operations/README.md)
