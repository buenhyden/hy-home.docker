---
status: completed
---

<!-- Target: docs/04.execution/plans/2026-05-29-workspace-consistency-2026-05b.md -->

# Workspace Doc & Governance Consistency (2026-05b) Implementation Plan

## Overview

이 문서는 워크스페이스 거버넌스 일관성 후속 작업(2026-05b)의 실행 계획서다. PR #89 이후 식별된 거버넌스 규칙 형식화, 검증 스크립트 확장, 템플릿 정규화, 소규모 문서 수정을 단계별로 수행하고 완료 기준을 정의한다.

## Context

PR #89(`workspace-doc-consistency-2026-05`)에서 대규모 구조적 일관성 작업을 완료했다. 이 작업은 그 후속으로, 다음 항목을 대상으로 한다:

- `documentation-protocol.md`에 실제 적용 중인 R4(Operations Profile Compliance), R5(Frontmatter Status) 규칙이 명문화되지 않은 상태
- `github-governance.md`에 CI/CD job taxonomy 섹션 부재
- `check-repo-contracts.sh` 가이드 프로파일 검사가 `## Usage`만 확인하고 `## Common Checks`, `## Runbook Handoff`는 미검증
- `docs/99.templates/README.md` 템플릿 목록에 guide.template.md, runbook.template.md 누락
- `agent-design.template.md` 예시에 가상 파일명 사용
- `docs/05.operations/policies/01-gateway/nginx.md`에 중복 `## Policy Scope` 헤딩 존재

## Goals & In-Scope

- **Goals**:
  - `documentation-protocol.md`에 R4, R5 규칙 추가
  - `github-governance.md`에 CI/CD job taxonomy 섹션(Section 8) 추가
  - `check-repo-contracts.sh` 가이드 프로파일 검사 강화
  - `docs/99.templates/README.md` 템플릿 목록 최신화
  - `agent-design.template.md` 예시 파일명 교체
  - `nginx.md` 중복 헤딩 제거
- **In Scope**: `docs/00.agent-governance/rules/`, `scripts/validation/`, `docs/99.templates/`, `docs/05.operations/policies/01-gateway/`

## Non-Goals & Out-of-Scope

- **Non-goals**: 문서 본문 내용 개정, 새로운 요구사항 반영
- **Out of Scope**: docs/01~04 구조 변경, Docker Compose 변경, secret/env 변경

## Work Breakdown

| Task ID | Description                                          | Files / Docs Affected                                      | Target REQ  | Validation Criteria                                |
| ------- | ---------------------------------------------------- | ---------------------------------------------------------- | ----------- | -------------------------------------------------- |
| PLN-001 | documentation-protocol.md에 R4+R5 규칙 추가          | `docs/00.agent-governance/rules/documentation-protocol.md` | VAL-SPC-001 | R4, R5 섹션 존재 확인                              |
| PLN-002 | github-governance.md에 Section 8 CI/CD taxonomy 추가 | `docs/00.agent-governance/rules/github-governance.md`      | VAL-SPC-002 | Section 8 존재 확인                                |
| PLN-003 | check-repo-contracts.sh 가이드 프로파일 검사 강화    | `scripts/validation/check-repo-contracts.sh`               | VAL-SPC-003 | `## Common Checks`, `## Runbook Handoff` 검사 포함 |
| PLN-004 | docs/99.templates/README.md 템플릿 목록 추가         | `docs/99.templates/README.md`                              | VAL-SPC-004 | guide.template.md, runbook.template.md 목록 포함   |
| PLN-005 | agent-design.template.md 예시 파일명 교체            | `docs/99.templates/agent-design.template.md`               | VAL-SPC-004 | 가상 파일명 없음, 디렉터리 링크 사용               |
| PLN-006 | nginx.md 중복 Policy Scope 헤딩 제거                 | `docs/05.operations/policies/01-gateway/nginx.md`          | VAL-SPC-005 | 중복 헤딩 0건                                      |

## Verification Plan

| ID          | Level       | Description               | Command / How to Run                                                        | Pass Criteria      |
| ----------- | ----------- | ------------------------- | --------------------------------------------------------------------------- | ------------------ |
| VAL-PLN-001 | Structural  | R4/R5 규칙 존재           | `grep -c "R4\|R5" docs/00.agent-governance/rules/documentation-protocol.md` | ≥2                 |
| VAL-PLN-002 | Structural  | CI/CD taxonomy 섹션 존재  | `grep "CI/CD" docs/00.agent-governance/rules/github-governance.md`          | 결과 있음          |
| VAL-PLN-003 | Structural  | 가이드 프로파일 검사 강화 | `grep "Common Checks" scripts/validation/check-repo-contracts.sh`           | 결과 있음          |
| VAL-PLN-004 | Integration | repo contracts 검증       | `bash scripts/validation/check-repo-contracts.sh`                           | exit 0, failures=0 |
| VAL-PLN-005 | Integration | doc traceability 검증     | `bash scripts/validation/check-doc-traceability.sh`                         | exit 0, failures=0 |

## Risks & Mitigations

| Risk                           | Impact | Mitigation                                              |
| ------------------------------ | ------ | ------------------------------------------------------- |
| 스크립트 강화로 기존 파일 실패 | Medium | 강화 전 영향 파일 사전 점검, 필요시 해당 파일 함께 수정 |
| 규칙 추가 후 번호 충돌         | Low    | 기존 규칙 번호 체계 확인 후 연번 배정                   |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: N/A
- **Sandbox / Canary Rollout**: N/A
- **Human Approval Gate**: 각 Phase 커밋 후 git diff 검토
- **Rollback Trigger**: `git revert <commit>` 또는 `git reset --hard HEAD~N`
- **Prompt / Model Promotion Criteria**: N/A

## Completion Criteria

- [x] PLN-001 ~ PLN-006 모든 태스크 완료
- [x] VAL-PLN-001 ~ VAL-PLN-005 전체 통과
- [x] `bash scripts/validation/check-repo-contracts.sh` exit 0
- [x] `bash scripts/validation/check-doc-traceability.sh` exit 0
- [x] Conventional Commits 형식으로 각 변경 커밋 완료

## Related Documents

- **Spec**: [workspace-consistency-2026-05b spec](../../03.specs/workspace-consistency-2026-05b/spec.md)
- **Task**: [2026-05-29 workspace consistency 2026-05b tasks](../tasks/2026-05-29-workspace-consistency-2026-05b.md)
- **Predecessor Plan**: [2026-05-28 workspace doc consistency plan](./2026-05-28-workspace-doc-consistency.md)
- **Templates**: [docs/99.templates/](../../99.templates/)
- **Governance Rules**: [docs/00.agent-governance/rules/](../../00.agent-governance/rules/)
- **Operations**: [Operations index](../../05.operations/README.md)
