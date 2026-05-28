---
status: completed
---

<!-- Target: docs/03.specs/workspace-audit-2026-05/spec.md -->

# Workspace Audit 2026-05 Technical Specification

## Overview (KR)

이 문서는 2026년 5월 워크스페이스 전체 감사 및 개선 세션의 기술 명세다. 거버넌스 규칙, 문서 라이프사이클, 스크립트, Docker Compose 인프라, env/secrets 계약, QA/CI/CD, 훅, 스킬셋을 대상으로 저위험 변경을 구현하고 중/고위험 변경을 deferred 항목으로 기록한다.

## Strategic Boundaries & Non-goals

**Scope:** 거버넌스 규칙 감사, 문서 라이프사이클 stage README 보강, 루트/infra README 현황 확인, env/secrets 키 비교 보고서 생성, 7개 워크스페이스 전용 AI Agent 스킬 스텁 생성, session Spec/Plan/Task 생성, progress.md 업데이트.

**Non-goals:** Docker Compose healthcheck/restart policy 실제 구현 (deferred), CI 워크플로우 수정 (deferred), OPA/Conftest 정책 코드 구현 (deferred), secret 값 변경, 실제 .env 값 변경.

## Related Inputs

- **PRD**: 해당 PRD 없음 — 반복적 워크스페이스 거버넌스 감사 세션
- **ARD**: [../../02.architecture/requirements/README.md](../../02.architecture/requirements/README.md)
- **Related ADRs**: 해당 ADR 없음

## Contracts

- **Config Contract**: `.env.example`과 `.env`는 동일 키셋 유지. 키 비교 보고서를 `docs/05.operations/guides/`에 생성.
- **Data / Interface Contract**: 스킬 스텁은 `name`, `description`, `version`, `purpose`, `trigger`, `inputs`, `outputs`, `constraints`, `related-skills` 필드를 포함한다.
- **Governance Contract**: 모든 변경은 `task-checklists.md` 완료 기준을 충족해야 한다. 저위험 변경만 구현하고 중/고위험은 deferred로 기록한다.

## Core Design

- **Component Boundary**: 이 스펙은 워크스페이스 거버넌스 레이어에만 적용된다. 인프라 runtime, CI/CD 배포 동작, secret 값은 변경하지 않는다.
- **Key Dependencies**: `docs/99.templates/spec.template.md`, `docs/99.templates/plan.template.md`, `docs/99.templates/task.template.md`, `docs/00.agent-governance/rules/stage-authoring-matrix.md`
- **Tech Stack**: Markdown 문서, Bash 검증 스크립트, Claude skill.md 형식

## Gap Registry Summary

| ID     | Area                | Summary                                     | Risk   | Status       |
| ------ | ------------------- | ------------------------------------------- | ------ | ------------ |
| GAP-01 | Infra               | 46/47 compose 파일 healthcheck/restart 누락 | Medium | Deferred     |
| GAP-02 | Docs Lifecycle      | Stage README 라이프사이클 섹션 미비         | Low    | Implemented  |
| GAP-03 | Docs Operations     | docs/05.operations/ 교차 링크 정규화        | Low    | Implemented  |
| GAP-04 | Root README         | 현황 반영 여부 확인                         | Low    | Verified OK  |
| GAP-05 | Skills              | 워크스페이스 전용 AI Agent 스킬셋 7개 누락  | Low    | Implemented  |
| GAP-06 | Env Contract        | .env.example vs .env 키 비교 보고서 없음    | Low    | Implemented  |
| GAP-07 | Secrets Contract    | SENSITIVE_ENV_VARS 키 비교 보고서 없음      | Low    | Implemented  |
| GAP-08 | CI/CD               | CI 워크플로우 확장 (validate-compose 등)    | Medium | Deferred     |
| GAP-09 | infra/README        | 정규화 여부 확인                            | Low    | Verified OK  |
| GAP-10 | Spec/Plan/Task      | 세션 Spec/Plan/Task 생성                    | Low    | Implemented  |
| GAP-11 | Policy Verification | OPA/Conftest 정책-코드 미구현               | Medium | Deferred     |
| GAP-12 | Coverage Ledger     | progress.md 감사 세션 항목 없음             | Low    | Implemented  |
| GAP-13 | Stage 04 lifecycle  | stage-authoring-matrix 정합성 확인          | Low    | Verified OK  |
| GAP-14 | Hookify naming      | .local.md 네이밍 설명 여부                  | Low    | Pre-existing |

## Verification

```bash
bash scripts/validation/check-repo-contracts.sh
bash scripts/validation/check-doc-traceability.sh
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: `check-repo-contracts.sh` 통과 — docs taxonomy, README, template inventory 계약 준수
- **VAL-SPC-002**: `check-doc-traceability.sh` 통과 — execution/operations 교차 링크 무결성
- **VAL-SPC-003**: 7개 스킬 스텁이 `.claude/skills/` 아래에 생성됨
- **VAL-SPC-004**: env/secrets 키 비교 보고서에 secret 값 미포함
- **VAL-SPC-005**: session Plan과 Task가 template 필수 섹션을 포함

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: N/A
- **Inputs**: N/A
- **Outputs**: N/A
- **Success Definition**: N/A

## Related Documents

- **Plan**: [../../04.execution/plans/2026-05-26-workspace-audit.md](../../04.execution/plans/2026-05-26-workspace-audit.md)
- **Task**: [../../04.execution/tasks/2026-05-26-workspace-audit.md](../../04.execution/tasks/2026-05-26-workspace-audit.md)
- **Env Key Comparison**: [../../05.operations/guides/env-key-comparison.md](../../05.operations/guides/env-key-comparison.md)
- **Secrets Key Comparison**: [../../05.operations/guides/sensitive-env-vars-comparison.md](../../05.operations/guides/sensitive-env-vars-comparison.md)
- **Stage Authoring Matrix**: [../../00.agent-governance/rules/stage-authoring-matrix.md](../../00.agent-governance/rules/stage-authoring-matrix.md)
- **Progress Log**: [../../00.agent-governance/memory/progress.md](../../00.agent-governance/memory/progress.md)
