---
status: draft
---
<!-- Target: docs/05.plans/2026-04-10-infra-team-agent-cross-validation.md -->

# Infra Team Agent Cross-Validation Plan

## Overview (KR)

이 문서는 infra 변경 직후 실행되는 team-agent cross-validation 설계를 canonical stage 경로로 정착시키기 위한 실행 계획서다. 기존 `docs/superpowers` 문서의 내용을 `docs/04.specs/07-workflow/agent-design.md` 및 본 계획 문서로 이관하고, 비표준 경로 재발을 막는 로컬 거버넌스 규칙까지 함께 정비한다.

## Context

기존 cross-validation 관련 문서는 `docs/superpowers/specs`와 `docs/superpowers/plans`에 위치해 있어 stage taxonomy와 template contract를 우회하고 있었다. 이 상태는 spec/plan 검색 경로를 분산시키고, 향후 스킬이 비표준 위치에 활성 문서를 생성하는 문제를 반복시킬 수 있다.

## Goals & In-Scope

- **Goals**:
  - `DOC-AGT-001`: 활성 agent design 문서를 `docs/04.specs/<feature-id>/agent-design.md`에만 둔다.
  - `DOC-AGT-002`: 활성 implementation plan 문서를 `docs/05.plans/YYYY-MM-DD-<slug>.md`에만 둔다.
  - `DOC-AGT-003`: repo-local governance가 비표준 `docs/*` 경로의 활성 spec/plan 생성을 금지하도록 만든다.
  - `DOC-AGT-004`: README와 traceability가 새 canonical 경로를 기준으로 정렬되도록 만든다.
- **In Scope**:
  - canonical `agent-design.md` 작성
  - canonical `plan.md` 작성
  - governance rule hardening
  - README sync
  - `docs/superpowers` 제거

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - infra-team-agent 전용 PRD/ARD/ADR 신규 생성
  - 글로벌 스킬 저장소 수정
  - `.claude/agents/` 및 `.claude/skills/`의 런타임 동작 변경
- **Out of Scope**:
  - workflow tier의 다른 spec/plan 재구조화
  - provider overlay (`CLAUDE.md`, `GEMINI.md`) 대규모 재작성

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | `docs/superpowers` spec 내용을 template-based canonical agent design으로 재작성 | `docs/04.specs/07-workflow/agent-design.md`, `docs/04.specs/07-workflow/spec.md` | `DOC-AGT-001` | 새 agent design이 필수 섹션과 `## Related Documents`를 포함한다. |
| PLN-002 | `docs/superpowers` plan 내용을 canonical plan 문서로 정규화 | `docs/05.plans/2026-04-10-infra-team-agent-cross-validation.md` | `DOC-AGT-002` | 새 plan이 Work Breakdown, Verification Plan, Risks 섹션을 포함한다. |
| PLN-003 | non-stage active path 금지 규칙을 로컬 governance에 추가 | `AGENTS.md`, `docs/00.agent-governance/rules/documentation-protocol.md`, `docs/00.agent-governance/scopes/docs.md` | `DOC-AGT-003` | 규칙 문서가 canonical path와 금지 경로를 명시한다. |
| PLN-004 | stage README를 actual structure 기준으로 동기화 | `docs/README.md`, `docs/04.specs/README.md`, `docs/05.plans/README.md` | `DOC-AGT-004` | README 구조 설명이 실제 파일 상태와 일치한다. |
| PLN-005 | legacy `docs/superpowers` 문서와 디렉터리를 제거하고 잔여 참조를 청소 | `docs/superpowers/**` | `DOC-AGT-001`, `DOC-AGT-002` | 저장소에 활성 `docs/superpowers` 참조가 남지 않는다. |
| PLN-006 | 문서 추적성 및 경로 정합성 검증 | changed docs set, validation scripts | `DOC-AGT-001`, `DOC-AGT-002`, `DOC-AGT-003`, `DOC-AGT-004` | `check-doc-traceability.sh` 통과 및 `docs/superpowers` 경로 제거 확인 |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | canonical agent design exists in the stage path | `test -f docs/04.specs/07-workflow/agent-design.md` | exit code 0 |
| VAL-PLN-002 | Structural | canonical plan exists in the stage path | `test -f docs/05.plans/2026-04-10-infra-team-agent-cross-validation.md` | exit code 0 |
| VAL-PLN-003 | Content | changed docs include required related-doc sections | `rg -n "^## Related Documents" AGENTS.md docs/00.agent-governance/scopes/docs.md docs/00.agent-governance/rules/documentation-protocol.md docs/04.specs/07-workflow/agent-design.md docs/05.plans/2026-04-10-infra-team-agent-cross-validation.md` | every changed doc matched |
| VAL-PLN-004 | Hygiene | no active `docs/superpowers` references remain | `rg -n "docs/superpowers" docs AGENTS.md CLAUDE.md .claude \|\| true` | no matches |
| VAL-PLN-005 | Traceability | repository doc traceability check passes | `bash scripts/check-doc-traceability.sh` | script exits successfully |
| VAL-PLN-006 | Filesystem | legacy directory removed | `test ! -d docs/superpowers` | exit code 0 |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Legacy references survive in README or plan text | Medium | Use repo-wide `rg` against `docs/superpowers` before completion |
| Canonical doc is too governance-heavy for `07-workflow` | Medium | Keep runtime behavior in `.claude/` and keep the new agent design focused on orchestration contract only |
| README structure drifts from actual files again | Medium | Update folder structure blocks in the same change set and verify with `find` output |
| Missing upstream PRD/ARD/ADR causes ambiguity | Low | Explicitly document that no dedicated upstream stage docs are created for this capability |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: canonical `agent-design.md` must define deterministic `PASS|WARN|BLOCK` terminal states
- **Sandbox / Canary Rollout**: not applicable for docs-only migration
- **Human Approval Gate**: user-approved removal of `docs/superpowers`
- **Rollback Trigger**: any traceability script failure or unresolved legacy reference
- **Prompt / Model Promotion Criteria**: not applicable

## Completion Criteria

- [ ] Canonical `agent-design.md` created under `docs/04.specs/07-workflow/`
- [ ] Canonical plan created under `docs/05.plans/`
- [ ] Governance rules updated to forbid non-stage active docs
- [ ] README files synced to actual structure
- [ ] `docs/superpowers` removed
- [ ] Verification passed

## Related Documents

- **Spec**: [../04.specs/07-workflow/agent-design.md](../04.specs/07-workflow/agent-design.md)
- **Workflow Parent Spec**: [../04.specs/07-workflow/spec.md](../04.specs/07-workflow/spec.md)
- **PRD Context**: [../01.prd/2026-03-28-07-workflow-optimization-hardening.md](../01.prd/2026-03-28-07-workflow-optimization-hardening.md)
- **ARD Context**: [../02.ard/0022-workflow-optimization-hardening-architecture.md](../02.ard/0022-workflow-optimization-hardening-architecture.md)
- **Documentation Protocol**: [../00.agent-governance/rules/documentation-protocol.md](../00.agent-governance/rules/documentation-protocol.md)
