---
status: completed
---
<!-- Target: docs/04.execution/tasks/2026-05-28-workspace-doc-consistency.md -->

# Task: Workspace Documentation Consistency 2026-05

## Overview

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
| T-002   | ARD 제목 형식 수정 (5개)         | doc  | SPC / §Interfaces     | Phase 1             | `grep -v "(ARD)"` 결과 빈 줄                             | agent | Done   |
| T-003   | PRD 누락 섹션 보완               | doc  | SPC / §Contracts      | Phase 1             | Overview(KR)·AI Agent Requirements 누락 0건              | agent | Done   |
| T-004   | Spec Agent Role N/A 추가 (15개)  | doc  | SPC / §Agent Role     | Phase 2             | `grep -rL "## Agent Role" docs/03.specs/*/spec.md` 빈 줄 | agent | Done   |
| T-005   | Task 파일 제목 접두사 수정 (4개) | doc  | SPC / §Interfaces     | Phase 2             | `# Task:` 접두사 100%                                    | agent | Done   |
| T-006   | Policy Scope 헤딩 통일 (~50개)   | doc  | SPC / §Interfaces     | Phase 2             | `grep -rl "^## Applies To" policies/` 빈 줄              | agent | Done   |
| T-007   | Guides frontmatter·섹션 보완     | doc  | SPC / §Contracts      | Phase 2             | status frontmatter 누락 0건 (이미 완비)                  | agent | Done   |
| T-008   | Runbooks frontmatter 보완        | doc  | SPC / §Contracts      | Phase 2             | status frontmatter 누락 0건 (이미 완비)                  | agent | Done   |
| T-009   | Incidents README 링크 보완       | doc  | SPC / §Contracts      | Phase 2             | 템플릿 링크 포함 확인 (이미 완비)                        | agent | Done   |
| T-010   | hardening-lib.sh 권한 수정       | ops  | SPC / §Tools          | Phase 3             | `ls -la` → `-rwxr-xr-x`                                  | agent | Done   |
| T-011   | use-qa-ci-tools.sh shebang 점검  | ops  | SPC / §Tools          | Phase 3             | POSIX sh 문법만 사용 — 변경 불필요                       | agent | Done   |
| T-012   | GitHub Actions SHA 최신화        | ops  | SPC / §Tools          | Phase 3             | zizmor 검증 통과                                         | agent | Done   |
| T-013   | 깨진 링크 탐지·수정              | doc  | SPC / §Guardrails     | Phase 4             | check-doc-traceability.sh 통과 — scope 내 0건            | agent | Done   |
| T-014   | legacy/deprecated 항목 제거      | doc  | SPC / §Guardrails     | Phase 4             | deprecated 파일 참조 없음 (0건)                          | agent | Done   |
| T-015   | 거버넌스 파일 동기화             | doc  | SPC / §Contracts      | Phase 4             | Policy Scope·ADR/ARD 규칙 명시 확인                      | agent | Done   |

## Phase View

### Phase 0: Pre-flight (완료)

- [x] T-000 docs/99.templates 기준 확인 — `## Policy Scope`, `## Agent Role` 섹션 존재 확인, status frontmatter 전체 보유

### Phase 1: Foundation — 제목·형식 불일치 수정 (완료)

- [x] T-001 ADR 제목 형식 수정 (5개) — commit `67d8a558`
- [x] T-002 ARD 제목 형식 수정 (5개) — commit `db344d2e`
- [x] T-003 PRD 누락 섹션 보완 — commit `499ef652`

### Phase 2: Core Operations — 대량 반복 수정 (완료)

- [x] T-004 Spec Agent Role N/A 추가 (15개) — commit `920300b1`
- [x] T-005 Task 파일 제목 접두사 수정 (4개) — commit `3c7eb8eb`
- [x] T-006 Policy Scope 헤딩 통일 (50개) — commit `92fad3b7`
- [x] T-007 Guides frontmatter·섹션 보완 — 이미 완비 (변경 없음)
- [x] T-008 Runbooks frontmatter 보완 — 이미 완비 (변경 없음)
- [x] T-009 Incidents README 링크 보완 — 이미 완비 (변경 없음)

### Phase 3: Technical — Scripts & CI/CD (완료)

- [x] T-010 hardening-lib.sh 권한 수정 — commit `c6bd6157`
- [x] T-011 use-qa-ci-tools.sh shebang 점검 — POSIX sh 정상 (변경 없음)
- [x] T-012 GitHub Actions SHA 최신화 — commit `e41704ab`

### Phase 4: Governance & Cleanup (완료)

- [x] T-013 깨진 링크 탐지·수정 — scope 내 0건 (변경 없음)
- [x] T-014 legacy/deprecated 항목 제거 — 0건 (변경 없음)
- [x] T-015 거버넌스 파일 동기화 — commit `d566ea97`

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

## Final Verification Evidence (2026-05-29)

| Check                             | Result            |
| --------------------------------- | ----------------- |
| ADR 제목 형식                     | PASS              |
| ARD (ARD) 접미사                  | PASS              |
| Spec Agent Role 섹션              | PASS              |
| Policy Scope 헤딩                 | PASS              |
| Operations status frontmatter     | PASS (0건 누락)   |
| scripts/lib/hardening-lib.sh 권한 | PASS (-rwxr-xr-x) |
| `check-repo-contracts.sh`         | PASS (failures=0) |
| `check-doc-traceability.sh`       | PASS (failures=0) |

## Related Documents

- **Parent Spec**: [workspace-doc-consistency-2026-05 spec](../../03.specs/workspace-doc-consistency-2026-05/spec.md)
- **Parent Plan**: [2026-05-28 workspace doc consistency plan](../plans/2026-05-28-workspace-doc-consistency.md)
- **Upstream Audit**: [workspace-audit-2026-05 spec](../../03.specs/workspace-audit-2026-05/spec.md)
- **Templates**: [docs/99.templates/](../../99.templates/)
