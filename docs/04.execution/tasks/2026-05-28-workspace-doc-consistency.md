---
status: active
---

# Task: Workspace Documentation Consistency 2026-05

## Overview (KR)

이 문서는 워크스페이스 문서 일관성·통일성 개선 작업의 구현·검증 작업 목록이다. `workspace-doc-consistency-2026-05` Spec과 Plan에서 파생된 16개 태스크를 추적 가능하게 기록한다. 각 태스크는 독립 커밋으로 완료되며, Validation Evidence로 검증 명령 결과를 기록한다.

## Inputs

- **Parent Spec**: [workspace-doc-consistency-2026-05 spec](../../03.specs/workspace-doc-consistency-2026-05/spec.md)
- **Parent Plan**: [2026-05-28 workspace doc consistency plan](../plans/2026-05-28-workspace-doc-consistency.md)

## Working Rules

- 구조·형식 수정만 수행. 문서 본문 의미 변경 금지.
- sed 명령 실행 전 반드시 grep으로 현재 패턴 확인.
- 각 Phase 완료 후 검증 명령으로 잔여 불일치 0건 확인.
- 검증 통과 후 Conventional Commits 형식으로 커밋.
- Documentation-only 작업이지만 모든 태스크에 검증 Evidence 필수.

## Task Table

| Task ID | Description                      | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence                                    | Owner | Status |
| ------- | -------------------------------- | ---- | --------------------- | ------------------- | -------------------------------------------------------- | ----- | ------ |
| T-000   | docs/99.templates 기준 확인      | doc  | SPC / §Contracts      | Phase 0             | Policy Scope·Agent Role 섹션 존재 확인                   | agent | Done   |
| T-001   | ADR 제목 형식 수정 (5개)         | doc  | SPC / §Interfaces     | Phase 1             | `grep -v "ADR-[0-9]\{4\}:"` 결과 빈 줄                   | agent | Done   |
| T-002   | ARD 제목 형식 수정 (5개)         | doc  | SPC / §Interfaces     | Phase 1             | `grep -v "(ARD)"` 결과 빈 줄                             | agent | Todo   |
| T-003   | PRD 누락 섹션 보완               | doc  | SPC / §Contracts      | Phase 1             | Overview(KR)·AI Agent Requirements 누락 0건              | agent | Todo   |
| T-004   | Spec Agent Role N/A 추가 (15개)  | doc  | SPC / §Agent Role     | Phase 2             | `grep -rL "## Agent Role" docs/03.specs/*/spec.md` 빈 줄 | agent | Todo   |
| T-005   | Task 파일 제목 접두사 수정 (4개) | doc  | SPC / §Interfaces     | Phase 2             | `# Task:` 접두사 100%                                    | agent | Todo   |
| T-006   | Policy Scope 헤딩 통일 (~50개)   | doc  | SPC / §Interfaces     | Phase 2             | `grep -rl "^## Applies To" policies/` 빈 줄              | agent | Todo   |
| T-007   | Guides frontmatter·섹션 보완     | doc  | SPC / §Contracts      | Phase 2             | status frontmatter 누락 0건                              | agent | Todo   |
| T-008   | Runbooks frontmatter 보완        | doc  | SPC / §Contracts      | Phase 2             | status frontmatter 누락 0건                              | agent | Todo   |
| T-009   | Incidents README 링크 보완       | doc  | SPC / §Contracts      | Phase 2             | 템플릿 링크 포함 확인                                    | agent | Todo   |
| T-010   | hardening-lib.sh 권한 수정       | ops  | SPC / §Tools          | Phase 3             | `ls -la` → `-rwxr-xr-x`                                  | agent | Todo   |
| T-011   | use-qa-ci-tools.sh shebang 점검  | ops  | SPC / §Tools          | Phase 3             | bash 전용 문법 시 bash shebang 확인                      | agent | Todo   |
| T-012   | GitHub Actions SHA 최신화        | ops  | SPC / §Tools          | Phase 3             | zizmor 검증 통과                                         | agent | Todo   |
| T-013   | 깨진 링크 탐지·수정              | doc  | SPC / §Guardrails     | Phase 4             | check-doc-traceability.sh 통과                           | agent | Todo   |
| T-014   | legacy/deprecated 항목 제거      | doc  | SPC / §Guardrails     | Phase 4             | deprecated 파일 참조 없음                                | agent | Todo   |
| T-015   | 거버넌스 파일 동기화             | doc  | SPC / §Contracts      | Phase 4             | Policy Scope·ADR/ARD 규칙 명시 확인                      | agent | Todo   |

## Phase View

### Phase 0: Pre-flight (완료)

- [x] T-000 docs/99.templates 기준 확인 — `## Policy Scope`, `## Agent Role` 섹션 존재 확인, status frontmatter 전체 보유

### Phase 1: Foundation — 제목·형식 불일치 수정

- [x] T-001 ADR 제목 형식 수정 (5개) — commit `67d8a558`
- [ ] T-002 ARD 제목 형식 수정 (5개)
- [ ] T-003 PRD 누락 섹션 보완

### Phase 2: Core Operations — 대량 반복 수정

- [ ] T-004 Spec Agent Role N/A 추가 (15개)
- [ ] T-005 Task 파일 제목 접두사 수정 (4개)
- [ ] T-006 Policy Scope 헤딩 통일 (~50개)
- [ ] T-007 Guides frontmatter·섹션 보완
- [ ] T-008 Runbooks frontmatter 보완
- [ ] T-009 Incidents README 링크 보완

### Phase 3: Technical — Scripts & CI/CD

- [ ] T-010 hardening-lib.sh 권한 수정
- [ ] T-011 use-qa-ci-tools.sh shebang 점검
- [ ] T-012 GitHub Actions SHA 최신화

### Phase 4: Governance & Cleanup

- [ ] T-013 깨진 링크 탐지·수정
- [ ] T-014 legacy/deprecated 항목 제거
- [ ] T-015 거버넌스 파일 동기화

## Verification Summary

- **Test Commands**:

  ```bash
  # ADR
  grep "^# " docs/02.architecture/decisions/*.md | grep -v "ADR-[0-9]\{4\}:"
  # ARD
  grep "^# " docs/02.architecture/requirements/*.md | grep -v "(ARD)"
  # Spec Agent Role
  grep -rL "## Agent Role" docs/03.specs/*/spec.md
  # Policy Scope
  grep -rl "^## Applies To" docs/05.operations/policies/
  # Operations frontmatter
  find docs/05.operations -name "*.md" ! -name "README.md" | xargs grep -rL "^status:" | wc -l
  ```

- **Eval Commands**: N/A
- **Logs / Evidence Location**: git log `docs/workspace-doc-consistency-2026-05` 브랜치

## Related Documents

- **Parent Spec**: [workspace-doc-consistency-2026-05 spec](../../03.specs/workspace-doc-consistency-2026-05/spec.md)
- **Parent Plan**: [2026-05-28 workspace doc consistency plan](../plans/2026-05-28-workspace-doc-consistency.md)
- **Upstream Audit**: [workspace-audit-2026-05 spec](../../03.specs/workspace-audit-2026-05/spec.md)
- **Templates**: [docs/99.templates/](../../99.templates/)
