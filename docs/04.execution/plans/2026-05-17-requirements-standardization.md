---
status: completed
---
<!-- Target: docs/04.execution/plans/2026-05-17-requirements-standardization.md -->

# docs/01.requirements Remediation Plan

## Overview (KR)

이 문서는 `docs/01.requirements` PRD 문서 세트를 `docs/99.templates/prd.template.md` 계약에 맞게 정리하는 실행 계획이다. 요구사항의 제품 의미는 변경하지 않고 문서 구조, 링크 추적성, canonical docs taxonomy, 검증 evidence를 복구한다.

## Context

`docs/01.requirements`는 전체 설계와 구현의 시작점이지만 일부 PRD가 템플릿 섹션명, H1 형식, Related Documents 링크 형식을 벗어나 있다. 또한 기존 `docs/superpowers/` 산출물이 tracked 상태로 남아 repo top-level docs taxonomy를 깨고 있으며, LLM Wiki index도 path 변경 전 상태로 stale 상태다.

## Goals & In-Scope

- **Goals**:
  - PRD 23개와 `docs/01.requirements/README.md`가 PRD stage 목적과 템플릿 규칙을 따르게 한다.
  - Related Documents 링크를 클릭 가능한 target-relative Markdown 링크로 통일한다.
  - `docs/superpowers/` tracked legacy artifacts를 제거해 canonical docs taxonomy를 복구한다.
  - LLM Wiki index와 governance progress log를 현재 문서 상태와 동기화한다.
- **In Scope**:
  - `docs/01.requirements/`
  - `docs/99.templates/prd.template.md`
  - `docs/02.architecture/requirements/0002-auth-architecture.md`의 adjacent auth traceability link
  - `docs/04.execution/plans/README.md`
  - `docs/00.agent-governance/memory/progress.md`
  - `docs/90.references/llm-wiki/index.md`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - PRD의 제품 요구사항, 우선순위, 성공 지표, 서비스 동작을 새로 정의하지 않는다.
  - 신규 PRD, ARD, ADR, Spec, Task, Operations 문서를 만들지 않는다.
  - gateway와 communication hardening PRD 부재를 새 TODO나 요구사항으로 발명하지 않는다.
- **Out of Scope**:
  - 런타임 구성, Docker Compose 동작, 서비스 설정, public API 변경
  - unrelated untracked `projects/storybook/mcp/`

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | `docs/superpowers/` tracked legacy artifacts 제거 | `docs/superpowers/**` | REQ-PRD-DOC-001 | `test ! -d docs/superpowers` |
| PLN-002 | PRD template Related Documents 예시를 클릭 가능한 Markdown 링크로 수정 | `docs/99.templates/prd.template.md` | REQ-PRD-DOC-002 | Template keeps target-relative guidance and has no backticked pseudo-links |
| PLN-003 | PRD H1과 필수 섹션을 템플릿 계약에 맞게 정규화 | `docs/01.requirements/*.md` | REQ-PRD-DOC-003 | PRD scan: exactly one H1, required sections present |
| PLN-004 | Related Documents 링크와 auth ADR placeholder 수정 | `docs/01.requirements/*.md`, `docs/02.architecture/requirements/0002-auth-architecture.md` | REQ-PRD-DOC-004 | No backticked pseudo-links, no `####-` placeholder paths, local links resolve |
| PLN-005 | Execution plan index와 governance progress 갱신 | `docs/04.execution/plans/README.md`, `docs/00.agent-governance/memory/progress.md` | REQ-PRD-DOC-005 | Parent README references this plan, progress log records evidence |
| PLN-006 | LLM Wiki index 재생성 | `docs/90.references/llm-wiki/index.md` | REQ-PRD-DOC-006 | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` passes |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Workspace | Confirm unrelated untracked Storybook MCP remains no-touch | `git status --short --untracked-files=all` | `projects/storybook/mcp/` may remain untracked; no unintended files appear |
| VAL-PLN-002 | PRD Structure | Count and validate PRD structural contract | Custom Python scan over `docs/01.requirements/2026-*.md` | 23 PRDs, `status: draft`, Target comments, one H1, required sections, no broken local links |
| VAL-PLN-003 | Link Format | Ensure pseudo-links are gone | Custom scan for backticked Related Documents pseudo-links | No matches |
| VAL-PLN-004 | Placeholder/H1 | Ensure placeholder paths and invalid H1s are gone | `rg -n '####-\|^# PRD\|^# Product Requirements Document\|Product Requirements Document$' docs/01.requirements/2026-*.md` | No matches |
| VAL-PLN-005 | Wiki Freshness | Verify generated LLM Wiki index is current | `bash scripts/knowledge/generate-llm-wiki-index.sh --check` | PASS |
| VAL-PLN-006 | Traceability | Verify plan/operations traceability remains synchronized | `bash scripts/validation/check-doc-traceability.sh` | PASS |
| VAL-PLN-007 | Repo Contract | Verify repository contracts pass | `bash scripts/validation/check-repo-contracts.sh` | PASS |
| VAL-PLN-008 | Diff Hygiene | Verify no whitespace errors | `git diff --check` | PASS |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Section additions accidentally invent product scope | High | Add only summaries derived from existing bullets in the same PRD or linked canonical docs |
| Canonical taxonomy remains broken after deletion | High | Remove tracked `docs/superpowers` files and verify with `check-repo-contracts.sh` |
| LLM Wiki index remains stale after path changes | Medium | Regenerate index and run `generate-llm-wiki-index.sh --check` |
| Unrelated untracked Storybook MCP gets staged | High | Do not stage or edit `projects/storybook/mcp/`; verify with `git status --short --untracked-files=all` |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Custom PRD structural/link scan must pass before final validators.
- **Sandbox / Canary Rollout**: Not applicable; documentation-only remediation.
- **Human Approval Gate**: This plan is based on the user-approved remediation scope.
- **Rollback Trigger**: Revert only this branch's scoped documentation changes if repo contract or PRD scans cannot be made to pass.
- **Prompt / Model Promotion Criteria**: Not applicable; no model or prompt runtime changes.

## Completion Criteria

- [x] Scoped PRD/template/taxonomy cleanup completed
- [x] LLM Wiki index regenerated
- [x] Required validation commands passed
- [x] `projects/storybook/mcp/` left untouched

## Related Documents

- **PRD README**: [../../01.requirements/README.md](../../01.requirements/README.md)
- **Execution Task**: [../tasks/2026-05-17-requirements-standardization.md](../tasks/2026-05-17-requirements-standardization.md)
- **PRD Template**: [../../99.templates/prd.template.md](../../99.templates/prd.template.md)
- **README Template**: [../../99.templates/readme.template.md](../../99.templates/readme.template.md)
- **Documentation Protocol**: [../../00.agent-governance/rules/documentation-protocol.md](../../00.agent-governance/rules/documentation-protocol.md)
