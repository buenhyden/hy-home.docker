---
status: completed
---

<!-- Target: docs/03.specs/workspace-doc-consistency-2026-05/spec.md -->

# Workspace Documentation Consistency 2026-05 Technical Specification

## Overview

이 문서는 2026년 5월 워크스페이스 문서 일관성·통일성 개선 작업의 기술 명세다. `workspace-audit-2026-05` 감사 결과에서 식별된 docs/01~05 계층, scripts/, .github/workflows/ 전반의 구조적 불일치를 체계적으로 수정하고, 거버넌스 파일을 현행화한다. 이 명세의 구현 결과로 AI Agent가 작업할 때 참조하는 모든 문서가 템플릿 기준과 일치하게 된다.

## Strategic Boundaries & Non-goals

**Scope:**

- docs/02.architecture: ADR/ARD 제목 형식 표준화
- docs/01.requirements: 누락 섹션(Overview KR, AI Agent Requirements) 보완
- docs/03.specs: 15개 spec 파일에 Agent Role & IO Contract 섹션 추가 (N/A 처리)
- docs/04.execution: task 파일 제목 접두사 통일, active plan 제목 접미사 보완
- docs/05.operations/policies: `## Applies To` → `## Policy Scope` 헤딩 통일 (~50개)
- docs/05.operations/guides, runbooks: frontmatter `status:` 필드 보완
- docs/05.operations/incidents: README 템플릿 링크 보완
- docs/99.templates: 기준 확인 (변경 없음)
- scripts/: 실행 권한, shebang 수정 (2개 파일)
- .github/workflows/: GitHub Actions SHA 최신화 (5개 파일)
- docs/00.agent-governance/rules/: Policy Scope 기준, ADR/ARD 제목 형식 규칙 명시

**Non-goals:**

- 문서 내용(본문) 개정 — 구조·형식 수정만 수행
- 새로운 요구사항 반영 — 기존 템플릿 기준 준수만
- Docker Compose, 서비스 설정 변경
- secret 값 또는 .env 변경
- docs/99.templates 실질적 내용 변경

## Related Inputs

- **PRD**: 해당 PRD 없음 — 반복적 워크스페이스 거버넌스 개선 세션
- **ARD**: 해당 ARD 없음
- **Related ADRs**: 해당 ADR 없음
- **Upstream Audit**: [../../03.specs/workspace-audit-2026-05/spec.md](../../03.specs/workspace-audit-2026-05/spec.md)

## Contracts

- **Config Contract**: 모든 수정은 `docs/99.templates/*.template.md` 기준을 따른다.
- **Data / Interface Contract**:
  - ADR 제목 형식: `# ADR-NNNN: English Title`
  - ARD 제목 형식: `# Domain Architecture Reference Document (ARD)`
  - Policy 헤딩: `## Policy Scope` (not `## Applies To`)
  - Agent Role 섹션: `## Agent Role & IO Contract (If Applicable)` — 해당 없는 경우 N/A
  - Task 제목 형식: `# Task: [Task Name]`
  - frontmatter: 모든 operations 문서(guides/policies/runbooks)에 `status:` 필드 필수
- **Governance Contract**: 모든 변경은 `task-checklists.md` 완료 기준을 충족해야 한다. 구조·형식 수정만 허용하며 본문 의미 변경은 금지한다.

## Core Design

- **Component Boundary**: docs/01~05, scripts/, .github/workflows/, docs/00.agent-governance/rules/
- **Key Dependencies**: docs/99.templates (기준 문서), scripts/validation/ (검증 스크립트)
- **Tech Stack**: bash, sed, git (Conventional Commits)
- **Execution Strategy**: Foundation-first — 템플릿 기준 확인 → 제목·구조 수정 → 대량 반복 수정 → 기술적 수정 → 거버넌스 동기화

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: 파일 구조 변경 없음. 기존 파일의 frontmatter 및 섹션 헤딩만 수정.
- **Migration / Transition Plan**: 각 Phase를 독립 커밋으로 분리하여 롤백 가능성 유지.

## Interfaces & Data Structures

### 적용 규칙 요약

| 문서 타입  | 필드/헤딩   | 기존 패턴                           | 목표 패턴                                          |
| ---------- | ----------- | ----------------------------------- | -------------------------------------------------- |
| ADR        | H1 제목     | `# ADR:`, `# ADR-YYYYMMDD:`, 한국어 | `# ADR-NNNN: English`                              |
| ARD        | H1 제목     | `# ARD:`, 접미사 없음               | `# Domain ARD (ARD)`                               |
| Spec       | 섹션        | Agent Role 누락                     | `## Agent Role & IO Contract (If Applicable)` 추가 |
| Policy     | 헤딩        | `## Applies To`                     | `## Policy Scope`                                  |
| Operations | frontmatter | status 누락                         | `status: active`                                   |
| Task       | H1 제목     | `# Task Tracking...` 등             | `# Task: ...`                                      |

## API Contract (If Applicable)

- **API Spec**: N/A

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: AI Agent가 이 명세를 참조하여 일관성 수정 작업을 수행한다. bash/sed 명령, git 커밋 수행.
- **Inputs**: docs/99.templates/_.template.md (기준), docs/01~05/\*\*/_.md (수정 대상), scripts/ (수정 대상), .github/workflows/ (수정 대상)
- **Outputs**: 수정된 마크다운 파일들, git 커밋 이력
- **Success Definition**: 전체 검증 스크립트 통과, 타입별 헤딩 불일치 0건

## Tools & Tool Contract (If Applicable)

- **Tool List**: bash, grep, sed, find, chmod, git
- **Permission Boundary**: docs/01~05, scripts/, .github/workflows/, docs/00.agent-governance/rules/ 내 파일 수정만 허용. docs/99.templates 실질적 수정 금지.
- **Failure Handling**: sed 패턴 불일치 시 파일 변경 없음 — 수동 확인 후 재시도.

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**: N/A
- **Policy Constraints**: N/A
- **Versioning Rule**: N/A

## Memory & Context Strategy (If Applicable)

- **Short-term Context**: N/A
- **Long-term Memory**: N/A
- **Retrieval Boundary**: N/A

## Guardrails (If Applicable)

- **Input Guardrails**: sed 명령 실행 전 반드시 grep으로 현재 패턴 확인
- **Output Guardrails**: 각 Phase 완료 후 검증 명령으로 잔여 불일치 0건 확인
- **Blocked Conditions**: docs/99.templates 파일의 기준 패턴과 다른 패턴이 발견되면 즉시 중단하고 확인
- **Escalation Rule**: 검증 스크립트 실패 시 커밋 금지

## Evaluation (If Applicable)

- **Eval Types**: 구조적 검증 (grep/find 기반)
- **Metrics**: 타입별 불일치 건수 (0이어야 함)
- **Datasets / Fixtures**: docs/01~05/\*_/_.md 전체
- **How to Run**: 아래 Verification 섹션 참조

## Edge Cases & Error Handling

- **Error 1**: sed 패턴이 여러 라인에 걸친 경우 — 단일 라인 치환만 수행, 복잡한 경우 수동 편집
- **Error 2**: frontmatter가 없는 파일에 status 추가 — frontmatter 블록 생성 후 추가

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: sed가 예상치 못한 패턴 변경
- **Fallback**: `git diff` 검토 후 `git checkout -- <file>` 로 롤백
- **Human Escalation**: 10개 이상 파일에서 패턴 불일치 발생 시 사람에게 보고

## Verification

```bash
BASE=/home/hy/project-infra/hy-home.docker
cd "$BASE"

# ADR 제목 형식
grep "^# " docs/02.architecture/decisions/*.md | grep -v "ADR-[0-9]\{4\}:"

# ARD (ARD) 접미사
grep "^# " docs/02.architecture/requirements/*.md | grep -v "(ARD)"

# Spec Agent Role 섹션
grep -rL "## Agent Role" docs/03.specs/*/spec.md

# Policies Policy Scope 헤딩
grep -rl "^## Applies To" docs/05.operations/policies/

# Operations status frontmatter
find docs/05.operations -name "*.md" ! -name "README.md" | xargs grep -rL "^status:" | wc -l

# scripts 실행 권한
ls -la scripts/lib/hardening-lib.sh | grep "^-rwxr-xr-x"

# repo contracts
bash scripts/validation/check-repo-contracts.sh

# doc traceability
bash scripts/validation/check-doc-traceability.sh
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: `grep "^# " docs/02.architecture/decisions/*.md | grep -v "ADR-[0-9]\{4\}:"` 결과 빈 줄 (README 제외) — ADR 제목 형식 100% 준수
- **VAL-SPC-002**: `grep "^# " docs/02.architecture/requirements/*.md | grep -v "(ARD)"` 결과 빈 줄 (README 제외) — ARD 제목 형식 100% 준수
- **VAL-SPC-003**: `grep -rL "## Agent Role" docs/03.specs/*/spec.md` 결과 빈 줄 — 전체 spec Agent Role 섹션 100% 보유
- **VAL-SPC-004**: `grep -rl "^## Applies To" docs/05.operations/policies/` 결과 빈 줄 — Policy Scope 헤딩 100% 통일
- **VAL-SPC-005**: operations docs status frontmatter 누락 0건
- **VAL-SPC-006**: `scripts/lib/hardening-lib.sh` 실행 권한 755
- **VAL-SPC-007**: `bash scripts/validation/check-repo-contracts.sh` 통과
- **VAL-SPC-008**: `bash scripts/validation/check-doc-traceability.sh` 통과

## Related Documents

- **Upstream Audit Spec**: [workspace-audit-2026-05 spec](../../03.specs/workspace-audit-2026-05/spec.md)
- **Plan**: [2026-05-28 workspace doc consistency plan](../../04.execution/plans/2026-05-28-workspace-doc-consistency.md)
- **Tasks**: [2026-05-28 workspace doc consistency tasks](../../04.execution/tasks/2026-05-28-workspace-doc-consistency.md)
- **Templates**: [docs/99.templates/](../../99.templates/)
- **Governance Rules**: [docs/00.agent-governance/rules/](../../00.agent-governance/rules/)
