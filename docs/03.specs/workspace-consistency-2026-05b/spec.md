---
status: completed
---

<!-- Target: docs/03.specs/workspace-consistency-2026-05b/spec.md -->

# Workspace Doc & Governance Consistency (2026-05b) Technical Specification

## Overview

이 문서는 PR #89(`workspace-doc-consistency-2026-05`) 후속 작업의 기술 명세다. 거버넌스 규칙 형식화(R4 Operations Profile Compliance, R5 Frontmatter Status), 유효성 검증 스크립트 확장, 템플릿 및 소규모 문서 수정을 통해 워크스페이스 일관성을 완성한다. 이 명세의 구현 결과로 `documentation-protocol.md`와 검증 스크립트가 실제 파일 기준과 완전히 일치하게 된다.

## Strategic Boundaries & Non-goals

**Scope:**

- `docs/00.agent-governance/rules/documentation-protocol.md`: R4(Operations Profile Compliance), R5(Frontmatter Status) 규칙 추가
- `docs/00.agent-governance/rules/github-governance.md`: CI/CD job taxonomy 섹션(Section 8) 추가
- `scripts/validation/check-repo-contracts.sh`: 가이드 프로파일 검사에 `## Common Checks`, `## Runbook Handoff` 섹션 요구 추가
- `docs/99.templates/README.md`: guide.template.md, runbook.template.md 목록 추가 및 링크 규약 설계 노트 추가
- `docs/99.templates/agent-design.template.md`: 예시 파일명을 디렉터리 링크로 교체
- `docs/05.operations/policies/01-gateway/nginx.md`: 중복 `## Policy Scope` 헤딩 제거

**Non-goals:**

- docs/01~04 구조적 변경 없음
- 새로운 기능 요구사항 반영 없음
- Docker Compose, 서비스 설정 변경 없음
- secret 값 또는 .env 변경 없음

## Related Inputs

- **PRD**: 해당 PRD 없음 — 반복적 워크스페이스 거버넌스 개선 세션
- **ARD**: 해당 ARD 없음
- **Related ADRs**: 해당 ADR 없음
- **Predecessor Spec**: [../../03.specs/workspace-doc-consistency-2026-05/spec.md](../../03.specs/workspace-doc-consistency-2026-05/spec.md)

## Contracts

- **Config Contract**: 모든 수정은 `docs/99.templates/*.template.md` 기준을 따른다.
- **Data / Interface Contract**:
  - R4: Operations guides는 `## Usage`, `## Common Checks`, `## Runbook Handoff` 섹션을 포함해야 한다.
  - R5: 모든 operations 문서(guides/policies/runbooks)에 `status:` frontmatter 필드가 필수다.
  - CI/CD taxonomy: workflow jobs를 lint, test, build, security, deploy, notify 계층으로 분류한다.
- **Governance Contract**: 모든 변경은 `task-checklists.md` 완료 기준을 충족해야 한다. 구조·형식 수정만 허용하며 본문 의미 변경은 금지한다.

## Core Design

- **Component Boundary**: `docs/00.agent-governance/rules/`, `scripts/validation/`, `docs/99.templates/`, `docs/05.operations/policies/`
- **Key Dependencies**: `docs/99.templates` (기준 문서), `scripts/validation/` (검증 스크립트)
- **Tech Stack**: bash, git (Conventional Commits)
- **Execution Strategy**: Documentation-first — 규칙 문서 추가 → 스크립트 강화 → 템플릿·문서 수정

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**: 파일 구조 변경 없음. 기존 파일의 섹션 헤딩, 내용 추가, 중복 제거만 수행.
- **Migration / Transition Plan**: 각 변경을 독립 커밋으로 분리하여 롤백 가능성 유지.

## Interfaces & Data Structures

### 적용 규칙 요약

| 문서 타입                | 변경 내용                                          | 목표 상태                                               |
| ------------------------ | -------------------------------------------------- | ------------------------------------------------------- |
| documentation-protocol   | R4, R5 규칙 추가                                   | Operations guides profile 및 frontmatter 요구사항 명시  |
| github-governance        | Section 8 CI/CD taxonomy 추가                      | CI/CD job 분류 체계 문서화                              |
| check-repo-contracts     | 가이드 프로파일 검사 강화                          | `## Common Checks`, `## Runbook Handoff` 섹션 검증 포함 |
| docs/99.templates/README | guide/runbook template 목록 및 링크 규약 노트 추가 | 전체 템플릿 목록 최신화                                 |
| agent-design.template    | 예시 파일명 → 디렉터리 링크 교체                   | 가상 파일명 없음                                        |
| nginx.md                 | 중복 `## Policy Scope` 헤딩 제거                   | 헤딩 1개만 존재                                         |

## API Contract (If Applicable)

- **API Spec**: N/A

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: AI Agent가 이 명세를 참조하여 거버넌스 규칙 추가, 스크립트 확장, 템플릿·문서 수정 작업을 수행한다.
- **Inputs**: `docs/99.templates/*.template.md` (기준), `docs/00.agent-governance/rules/` (수정 대상), `scripts/validation/` (수정 대상), `docs/05.operations/` (수정 대상)
- **Outputs**: 수정된 마크다운·쉘 파일들, git 커밋 이력
- **Success Definition**: `check-repo-contracts.sh` 및 `check-doc-traceability.sh` 통과, failures=0

## Tools & Tool Contract (If Applicable)

- **Tool List**: bash, git
- **Permission Boundary**: `docs/00.agent-governance/rules/`, `scripts/validation/`, `docs/99.templates/`, `docs/05.operations/policies/` 내 파일 수정만 허용.
- **Failure Handling**: 스크립트 실패 시 `git diff` 검토 후 롤백.

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**: N/A
- **Policy Constraints**: N/A
- **Versioning Rule**: N/A

## Memory & Context Strategy (If Applicable)

- **Short-term Context**: N/A
- **Long-term Memory**: N/A
- **Retrieval Boundary**: N/A

## Guardrails (If Applicable)

- **Input Guardrails**: 변경 전 대상 파일의 현재 상태를 grep으로 확인
- **Output Guardrails**: 각 변경 완료 후 검증 명령으로 잔여 불일치 0건 확인
- **Blocked Conditions**: 검증 스크립트 실패 시 커밋 금지
- **Escalation Rule**: 예상치 못한 패턴 변경 발견 시 즉시 중단하고 사람에게 보고

## Evaluation (If Applicable)

- **Eval Types**: 구조적 검증 (bash/grep 기반)
- **Metrics**: 검증 실패 건수 (0이어야 함)
- **Datasets / Fixtures**: 수정된 파일 전체
- **How to Run**: 아래 Verification 섹션 참조

## Edge Cases & Error Handling

- **Error 1**: 규칙 추가 위치 선택 — 기존 섹션 순서와 번호 체계를 유지
- **Error 2**: 스크립트 검사 강화로 기존 파일 실패 — 해당 파일을 스펙에 맞게 수정

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: 스크립트 변경이 false positive를 유발
- **Fallback**: `git diff` 검토 후 `git checkout -- <file>`로 롤백
- **Human Escalation**: 검증 스크립트가 예상치 못한 파일을 실패시킬 경우 사람에게 보고

## Verification

```bash
cd /home/hy/project-infra/hy-home.docker

# R4/R5 규칙 존재 확인
grep -c "R4\|R5" docs/00.agent-governance/rules/documentation-protocol.md

# CI/CD taxonomy 섹션 존재 확인
grep -c "CI/CD" docs/00.agent-governance/rules/github-governance.md

# 가이드 프로파일 검사 강화 확인
grep "Common Checks" scripts/validation/check-repo-contracts.sh

# repo contracts 검증
bash scripts/validation/check-repo-contracts.sh

# doc traceability 검증
bash scripts/validation/check-doc-traceability.sh
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: `documentation-protocol.md`에 R4, R5 규칙이 존재한다.
- **VAL-SPC-002**: `github-governance.md`에 CI/CD job taxonomy 섹션(Section 8)이 존재한다.
- **VAL-SPC-003**: `check-repo-contracts.sh`가 `## Common Checks`와 `## Runbook Handoff`를 검사한다.
- **VAL-SPC-004**: `docs/99.templates/README.md`에 guide.template.md와 runbook.template.md가 목록에 포함된다.
- **VAL-SPC-005**: `nginx.md`에 중복 `## Policy Scope` 헤딩이 없다.
- **VAL-SPC-006**: `bash scripts/validation/check-repo-contracts.sh` — failures=0 통과
- **VAL-SPC-007**: `bash scripts/validation/check-doc-traceability.sh` — failures=0 통과

## Related Documents

- **Predecessor Spec**: [workspace-doc-consistency-2026-05 spec](../../03.specs/workspace-doc-consistency-2026-05/spec.md)
- **Plan**: [2026-05-29 workspace consistency 2026-05b plan](../../04.execution/plans/2026-05-29-workspace-consistency-2026-05b.md)
- **Tasks**: [2026-05-29 workspace consistency 2026-05b tasks](../../04.execution/tasks/2026-05-29-workspace-consistency-2026-05b.md)
- **Templates**: [docs/99.templates/](../../99.templates/)
- **Governance Rules**: [docs/00.agent-governance/rules/](../../00.agent-governance/rules/)
