---
status: active
---

# Workspace Documentation Consistency 2026-05 Implementation Plan

## Overview (KR)

이 문서는 워크스페이스 문서 일관성·통일성 개선 작업의 실행 계획서다. `workspace-audit-2026-05` 감사에서 식별된 불일치를 5개 Phase로 단계적으로 수정하고, 각 Phase를 독립 커밋으로 분리하여 추적성과 롤백 가능성을 보장한다.

## Context

`workspace-audit-2026-05` 감사 결과, docs/01~05 계층 및 기술 인프라 전반에 다음과 같은 불일치가 발견되었다:

- docs/02.architecture: ADR 5개·ARD 5개 제목 형식 불일치
- docs/03.specs: 15개 파일에 Agent Role & IO Contract 섹션 누락
- docs/05.operations/policies: ~50개 파일에서 `## Applies To` vs `## Policy Scope` 헤딩 불일치
- docs/05.operations/{guides,policies,runbooks}: frontmatter `status:` 필드 60% 준수
- scripts/lib/hardening-lib.sh: 실행 권한 누락 (644)
- .github/workflows/: GitHub Actions SHA v3/v4 시대 해시로 고정

AI Agent가 작업할 때 참조하는 문서와 실제 파일 사이의 편차를 제거하는 것이 목적이다.

## Goals & In-Scope

- **Goals**:
  - 모든 ADR/ARD 제목이 거버넌스 규칙 형식을 준수
  - 모든 spec 파일이 Agent Role 섹션 보유
  - 모든 policy 파일이 `## Policy Scope` 헤딩 사용
  - operations docs frontmatter status 100% 준수
  - GitHub Actions SHA 최신화
  - 거버넌스 규칙 파일 현행화
- **In Scope**: docs/01~05, scripts/, .github/workflows/, docs/00.agent-governance/rules/

## Non-Goals & Out-of-Scope

- **Non-goals**: 문서 본문 내용 개정, 새로운 요구사항 반영
- **Out of Scope**: Docker Compose 변경, secret/env 변경, docs/99.templates 실질적 수정

## Work Breakdown

| Task ID | Description                     | Files / Docs Affected                                      | Target REQ  | Validation Criteria                      |
| ------- | ------------------------------- | ---------------------------------------------------------- | ----------- | ---------------------------------------- |
| PLN-000 | docs/99.templates 기준 확인     | 19개 template 파일 (read-only)                             | VAL-SPC-007 | Policy Scope·Agent Role 기준 확인        |
| PLN-001 | ADR 제목 형식 수정              | decisions/0003, 0009, 0010, 0011, 0026                     | VAL-SPC-001 | `grep -v "ADR-[0-9]\{4\}:"` 결과 빈 줄   |
| PLN-002 | ARD 제목 형식 수정              | requirements/0002, 0003, 0006, 0012, 0026                  | VAL-SPC-002 | `grep -v "(ARD)"` 결과 빈 줄             |
| PLN-003 | PRD 누락 섹션 보완              | docs/01.requirements/\*.md (선별)                          | VAL-SPC-007 | Overview(KR), AI Agent Requirements 100% |
| PLN-004 | Spec Agent Role N/A 추가        | docs/03.specs/\*/spec.md 15개                              | VAL-SPC-003 | Agent Role 섹션 누락 0건                 |
| PLN-005 | Task 파일 제목 접두사 수정      | tasks/2026-03-26-{07,08,09,10}-\*.md                       | VAL-SPC-007 | `# Task:` 접두사 100%                    |
| PLN-006 | Policy Scope 헤딩 통일          | policies/\*_/_.md ~50개                                    | VAL-SPC-004 | `## Applies To` 잔여 0건                 |
| PLN-007 | Guides frontmatter·섹션 보완    | guides/\*_/_.md (선별)                                     | VAL-SPC-005 | status frontmatter 누락 0건              |
| PLN-008 | Runbooks frontmatter 보완       | runbooks/\*_/_.md (선별)                                   | VAL-SPC-005 | status frontmatter 누락 0건              |
| PLN-009 | Incidents README 링크 보완      | incidents/README.md                                        | VAL-SPC-007 | 템플릿 링크 포함 확인                    |
| PLN-010 | hardening-lib.sh 권한 수정      | scripts/lib/hardening-lib.sh                               | VAL-SPC-006 | ls -la → -rwxr-xr-x                      |
| PLN-011 | use-qa-ci-tools.sh shebang 점검 | scripts/operations/use-qa-ci-tools.sh                      | VAL-SPC-007 | bash 전용 문법 시 bash shebang           |
| PLN-012 | GitHub Actions SHA 최신화       | .github/workflows/\*.yml 5개                               | VAL-SPC-007 | zizmor 검증 통과                         |
| PLN-013 | 깨진 링크 탐지·수정             | docs/ 전체 상대 경로 링크                                  | VAL-SPC-008 | check-doc-traceability.sh 통과           |
| PLN-014 | legacy/deprecated 항목 제거     | status: deprecated 파일 (선별)                             | VAL-SPC-007 | deprecated 파일 참조 없음                |
| PLN-015 | 거버넌스 파일 동기화            | rules/documentation-protocol.md, stage-authoring-matrix.md | VAL-SPC-007 | Policy Scope·ADR/ARD 규칙 명시           |

## Verification Plan

| ID          | Level       | Description                   | Command / How to Run                                                                             | Pass Criteria         |
| ----------- | ----------- | ----------------------------- | ------------------------------------------------------------------------------------------------ | --------------------- |
| VAL-PLN-001 | Structural  | ADR 제목 형식 준수            | `grep "^# " docs/02.architecture/decisions/*.md \| grep -v "ADR-[0-9]\{4\}:"`                    | 빈 결과 (README 제외) |
| VAL-PLN-002 | Structural  | ARD (ARD) 접미사 준수         | `grep "^# " docs/02.architecture/requirements/*.md \| grep -v "(ARD)"`                           | 빈 결과 (README 제외) |
| VAL-PLN-003 | Structural  | Spec Agent Role 섹션          | `grep -rL "## Agent Role" docs/03.specs/*/spec.md`                                               | 빈 결과               |
| VAL-PLN-004 | Structural  | Policy Scope 헤딩             | `grep -rl "^## Applies To" docs/05.operations/policies/`                                         | 빈 결과               |
| VAL-PLN-005 | Structural  | Operations status frontmatter | `find docs/05.operations -name "*.md" ! -name "README.md" \| xargs grep -rL "^status:" \| wc -l` | 0                     |
| VAL-PLN-006 | Technical   | scripts 실행 권한             | `ls -la scripts/lib/hardening-lib.sh \| grep "^-rwxr-xr-x"`                                      | PASS                  |
| VAL-PLN-007 | Integration | repo contracts                | `bash scripts/validation/check-repo-contracts.sh`                                                | exit 0                |
| VAL-PLN-008 | Integration | doc traceability              | `bash scripts/validation/check-doc-traceability.sh`                                              | exit 0                |

## Risks & Mitigations

| Risk                                     | Impact | Mitigation                                             |
| ---------------------------------------- | ------ | ------------------------------------------------------ |
| sed 패턴이 예상치 못한 라인 변경         | High   | 실행 전 grep으로 패턴 확인, 실행 후 git diff 검토      |
| ~50개 Policy 파일 일괄 치환 오류         | Medium | 도메인 폴더별 분할 실행, 각 단계 검증                  |
| GitHub Actions SHA 업그레이드 후 CI 실패 | Medium | SHA 교체 후 zizmor 로컬 검증, PR에서 CI 확인           |
| frontmatter 삽입 위치 오류               | Low    | frontmatter 존재 여부 먼저 확인, 없는 파일은 별도 처리 |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: N/A
- **Sandbox / Canary Rollout**: N/A
- **Human Approval Gate**: 각 Phase 커밋 후 git diff 검토
- **Rollback Trigger**: `git revert <commit>` 또는 `git reset --hard HEAD~N`
- **Prompt / Model Promotion Criteria**: N/A

## Completion Criteria

- [ ] PLN-000 ~ PLN-015 모든 태스크 완료
- [ ] VAL-PLN-001 ~ VAL-PLN-008 전체 통과
- [ ] `bash scripts/validation/check-repo-contracts.sh` exit 0
- [ ] `bash scripts/validation/check-doc-traceability.sh` exit 0
- [ ] Conventional Commits 형식으로 각 Phase 커밋 완료

## Related Documents

- **Upstream Audit Spec**: [workspace-audit-2026-05 spec](../../03.specs/workspace-audit-2026-05/spec.md)
- **Spec**: [workspace-doc-consistency-2026-05 spec](../../03.specs/workspace-doc-consistency-2026-05/spec.md)
- **Task**: [2026-05-28 workspace doc consistency tasks](../tasks/2026-05-28-workspace-doc-consistency.md)
- **Templates**: [docs/99.templates/](../../99.templates/)
- **Governance Rules**: [docs/00.agent-governance/rules/](../../00.agent-governance/rules/)
- **Operations**: [Operations index](../../05.operations/README.md)
