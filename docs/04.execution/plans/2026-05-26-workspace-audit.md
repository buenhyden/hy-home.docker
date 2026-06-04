---
status: completed
---

<!-- Target: docs/04.execution/plans/2026-05-26-workspace-audit.md -->

# Workspace Audit 2026-05 Implementation Plan

## Overview (KR)

이 문서는 2026년 5월 워크스페이스 전체 감사 및 개선 세션의 실행 계획서다. 저위험 변경 항목의 실행 순서, 검증 기준, 완료 조건을 정의한다.

## Context

이 감사는 반복 워크스페이스 거버넌스 사이클의 일환으로 수행된다. 3개의 병렬 Explore 에이전트가 거버넌스, 인프라, CI/CD/훅/스킬 영역을 탐색하고 14개 Gap을 식별했다. 저위험 Gap은 즉시 구현하고 중/고위험 Gap은 deferred로 기록한다.

## Goals & In-Scope

- **Goals**: Gap Registry의 저위험 항목 구현, 중/고위험 항목 deferred 기록, session 추적 문서 생성
- **In Scope**: 세션 Spec/Plan/Task, 7개 스킬 스텁, env/secrets 키 비교 보고서, stage README 라이프사이클 보강, progress.md 업데이트, 검증 실행

## Non-Goals & Out-of-Scope

- **Non-goals**: Docker Compose runtime 변경, CI/CD 배포 동작 변경, secret 값 변경
- **Out of Scope**: GAP-01(healthcheck), GAP-08(CI 워크플로우), GAP-11(OPA)

## Work Breakdown

| Task    | Description                             | Files / Docs Affected                                                                                                         | Risk | Validation Criteria                              |
| ------- | --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ---- | ------------------------------------------------ |
| PLN-001 | Session Spec/Plan/Task 생성             | `docs/03.specs/workspace-audit-2026-05/spec.md`, `plans/2026-05-26-workspace-audit.md`, `tasks/2026-05-26-workspace-audit.md` | Low  | Template 필수 섹션 포함                          |
| PLN-002 | 7개 AI Agent 스킬 스텁 생성             | `.claude/skills/*/skill.md` (7개)                                                                                             | Low  | 각 스킬이 frontmatter와 핵심 섹션 포함           |
| PLN-003 | Env 키 비교 보고서 생성                 | `docs/05.operations/guides/00-workspace/env-key-comparison.md`                                                                             | Low  | secret 값 미포함, 키 이름만                      |
| PLN-004 | Secrets 키 비교 보고서 생성             | `docs/05.operations/guides/00-workspace/sensitive-env-vars-comparison.md`                                                                  | Low  | secret 값 미포함, ID/경로만                      |
| PLN-005 | Stage README 라이프사이클 보강          | `docs/03.specs/README.md`, `docs/04.execution/README.md`, `docs/05.operations/README.md`, `docs/90.references/README.md`      | Low  | frontmatter status 추가, Stage Handoff 섹션 추가 |
| PLN-006 | Execution/Specs 인덱스 README 링크 추가 | `docs/04.execution/README.md`, `docs/03.specs/README.md`                                                                      | Low  | 새 plan/task/spec 파일 링크 포함                 |
| PLN-007 | progress.md 업데이트                    | `docs/00.agent-governance/memory/progress.md`                                                                                 | Low  | 감사 세션 항목 기록                              |

## Verification Plan

| ID          | Level      | Description                     | Command / How to Run                                | Pass Criteria |
| ----------- | ---------- | ------------------------------- | --------------------------------------------------- | ------------- |
| VAL-PLN-001 | Structural | docs taxonomy 계약 검증         | `bash scripts/validation/check-repo-contracts.sh`   | exit 0        |
| VAL-PLN-002 | Structural | 문서 추적성 검증                | `bash scripts/validation/check-doc-traceability.sh` | exit 0        |
| VAL-PLN-003 | Manual     | 스킬 스텁 존재 여부             | `ls .claude/skills/*/skill.md`                      | 7개 파일 존재 |
| VAL-PLN-004 | Manual     | 키 비교 보고서 secret 값 미포함 | 파일 수동 검토                                      | 값 컬럼 없음  |

## Risks & Mitigations

| Risk                                      | Impact | Mitigation                      |
| ----------------------------------------- | ------ | ------------------------------- |
| Stage README 수정이 기존 링크 깨뜨림      | Medium | 기존 섹션 유지, 마지막에만 추가 |
| check-repo-contracts.sh 새 파일 탐지 실패 | Low    | 검증 후 수동 확인               |

## Completion Criteria

- [x] PLN-001 ~ PLN-007 완료
- [x] VAL-PLN-001, VAL-PLN-002 통과
- [x] 중/고위험 항목 deferred 기록 완료

## Related Documents

- **Spec**: [../../03.specs/workspace-audit-2026-05/spec.md](../../03.specs/workspace-audit-2026-05/spec.md)
- **Task**: [../tasks/2026-05-26-workspace-audit.md](../tasks/2026-05-26-workspace-audit.md)
- **Operations**: [../../05.operations/README.md](../../05.operations/README.md)
