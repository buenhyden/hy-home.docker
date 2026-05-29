---
status: completed
---

<!-- Target: docs/04.execution/tasks/2026-05-29-workspace-consistency-2026-05b.md -->

# Task: Workspace Doc & Governance Consistency (2026-05b)

## Overview (KR)

이 문서는 워크스페이스 거버넌스 일관성 후속 작업(2026-05b)의 구현·검증 작업 목록이다. `workspace-consistency-2026-05b` Spec과 Plan에서 파생된 6개 태스크를 추적 가능하게 기록한다. 각 태스크는 독립 커밋으로 완료되며, Validation Evidence로 검증 명령 결과를 기록한다.

## Inputs

- **Parent Spec**: [workspace-consistency-2026-05b spec](../../03.specs/workspace-consistency-2026-05b/spec.md)
- **Parent Plan**: [2026-05-29 workspace consistency 2026-05b plan](../plans/2026-05-29-workspace-consistency-2026-05b.md)

## Working Rules

- 구조·형식 수정만 수행. 문서 본문 의미 변경 금지.
- 변경 전 대상 파일 현재 상태 확인.
- 각 변경 완료 후 검증 명령으로 잔여 불일치 0건 확인.
- 검증 통과 후 Conventional Commits 형식으로 커밋.
- Documentation-only 작업이지만 모든 태스크에 검증 Evidence 필수.

## Task Table

| Task ID | Description                                          | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence                                   | Owner | Status |
| ------- | ---------------------------------------------------- | ---- | --------------------- | ------------------- | ------------------------------------------------------- | ----- | ------ |
| T-001   | documentation-protocol.md에 R4+R5 규칙 추가          | doc  | SPC / §Contracts      | PLN-001             | R4, R5 섹션 존재 확인                                   | agent | Done   |
| T-002   | github-governance.md에 Section 8 CI/CD taxonomy 추가 | doc  | SPC / §Contracts      | PLN-002             | Section 8 CI/CD taxonomy 존재 확인                      | agent | Done   |
| T-003   | check-repo-contracts.sh 가이드 프로파일 검사 강화    | ops  | SPC / §Contracts      | PLN-003             | `## Common Checks`, `## Runbook Handoff` 검사 포함 확인 | agent | Done   |
| T-004   | docs/99.templates/README.md 템플릿 목록 추가         | doc  | SPC / §Interfaces     | PLN-004             | guide.template.md, runbook.template.md 항목 존재 확인   | agent | Done   |
| T-005   | agent-design.template.md 예시 파일명 교체            | doc  | SPC / §Interfaces     | PLN-005             | 가상 파일명 없음, 디렉터리 링크 사용 확인               | agent | Done   |
| T-006   | nginx.md 중복 Policy Scope 헤딩 제거                 | doc  | SPC / §Interfaces     | PLN-006             | 중복 헤딩 0건 확인                                      | agent | Done   |

## Phase View

### Phase 1: Governance Rule Additions (완료)

- [x] T-001 documentation-protocol.md에 R4+R5 규칙 추가
- [x] T-002 github-governance.md에 Section 8 CI/CD taxonomy 추가

### Phase 2: Script Extension (완료)

- [x] T-003 check-repo-contracts.sh 가이드 프로파일 검사 강화

### Phase 3: Template & Doc Fixes (완료)

- [x] T-004 docs/99.templates/README.md 템플릿 목록 추가
- [x] T-005 agent-design.template.md 예시 파일명 교체
- [x] T-006 nginx.md 중복 Policy Scope 헤딩 제거

## Verification Summary

- **Test Commands**:

  ```bash
  # R4/R5 규칙 존재
  grep -c "R4\|R5" docs/00.agent-governance/rules/documentation-protocol.md

  # CI/CD taxonomy 섹션 존재
  grep "CI/CD" docs/00.agent-governance/rules/github-governance.md

  # 가이드 프로파일 검사 강화
  grep "Common Checks" scripts/validation/check-repo-contracts.sh

  # repo contracts
  bash scripts/validation/check-repo-contracts.sh

  # doc traceability
  bash scripts/validation/check-doc-traceability.sh
  ```

- **Eval Commands**: N/A
- **Logs / Evidence Location**: git log `docs/workspace-consistency-2026-05b` 브랜치

## Final Verification Evidence

| Check                                               | Result            |
| --------------------------------------------------- | ----------------- |
| R4/R5 규칙 존재 (documentation-protocol.md)         | PASS              |
| CI/CD taxonomy 섹션 존재 (github-governance.md)     | PASS              |
| 가이드 프로파일 검사 강화 (check-repo-contracts.sh) | PASS              |
| nginx.md 중복 헤딩 제거                             | PASS              |
| `check-repo-contracts.sh`                           | PASS (failures=0) |
| `check-doc-traceability.sh`                         | PASS (failures=0) |

## Related Documents

- **Parent Spec**: [workspace-consistency-2026-05b spec](../../03.specs/workspace-consistency-2026-05b/spec.md)
- **Parent Plan**: [2026-05-29 workspace consistency 2026-05b plan](../plans/2026-05-29-workspace-consistency-2026-05b.md)
- **Predecessor Task**: [2026-05-28 workspace doc consistency tasks](./2026-05-28-workspace-doc-consistency.md)
- **Templates**: [docs/99.templates/](../../99.templates/)
