---
status: completed
---

# Infra / Secrets / Docs Refresh Plan

## Overview (KR)

이 문서는 `infra`, `secrets`, `docs/05.operations/guides`, `docs/05.operations/policies`, `docs/05.operations/runbooks`, `docs/90.references`의 분석 결과를 바탕으로 README와 stage 문서를 템플릿에 맞춰 최신화하는 실행 계획서다.

## Context

현재 저장소는 계층형 Docker Compose 인프라와 stage-based docs taxonomy를 갖추고 있으며 repository contract 검증은 통과한다. README와 stage heading audit도 현재 gap 0이다. 이번 작업은 heading 통과를 품질 완료로 오해하지 않도록 root-active Compose 범위, secret 분류, semantic QA 결과를 문서에 보강하는 문서 중심 갱신이다.

## Goals & In-Scope

- **Goals**:
  - 대상 경로의 구현 요소, compose/config/related file, 문서 gap을 공식 stage 문서에 기록한다.
  - README를 `readme.template.md` base structure에 맞춘다.
  - `docs/05.operations/guides`, `docs/05.operations/policies`, `docs/05.operations/runbooks`, `docs/90.references` 문서가 대응 템플릿 필수 섹션을 포함하도록 보강한다.
  - root-active, optional, standalone, variant Compose 상태를 구분한다.
  - secret 값 열람 없이 root Compose 선언, bind-mounted cert, registry/local-only 파일을 분류한다.
  - heading audit과 semantic QA를 분리해 검증한다.
  - root `README.md`와 `docs/README.md`를 최신 분석 범위와 연결한다.
- **In Scope**:
  - 문서와 README 갱신
  - parent README 링크 갱신
  - 검증 명령 실행 및 task evidence 기록

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Docker Compose 서비스 동작 변경
  - secret 값 파일 열람 또는 재생성
  - agent runtime catalog 변경
- **Out of Scope**:
  - 신규 PRD, ARD, ADR, incident 생성
  - 외부 네트워크 조회
  - 배포, 마이그레이션, 인증서 재발급

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | 분석 spec/plan/task 생성 | `docs/03.specs`, `docs/04.execution/plans`, `docs/04.execution/tasks` | REQ-DOC-001 | 템플릿 필수 섹션 존재 |
| PLN-002 | root/docs/secrets README 최신화 | `README.md`, `docs/README.md`, `secrets/README.md` | REQ-RDM-001 | README base heading audit 통과 |
| PLN-003 | infra 및 docs stage README 보강 | `infra/**/README.md`, `docs/05.operations/{guides,policies,runbooks}/**/README.md`, `docs/90.references/**/README.md` | REQ-RDM-002 | 누락 heading 0, 비링크 참조 정리 |
| PLN-004 | guide/operation/runbook/reference 문서 보강 | `docs/05.operations/guides`, `docs/05.operations/policies`, `docs/05.operations/runbooks`, `docs/90.references` | REQ-STG-001 | stage heading audit 통과, semantic QA 통과 |
| PLN-005 | 검증 및 evidence 갱신 | `docs/04.execution/tasks/2026-05-09-infra-secrets-docs-refresh.md` | REQ-VAL-001 | 검증 명령 결과 기록 |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Structural | repository contract 확인 | `bash scripts/validation/check-repo-contracts.sh` | failures=0 |
| VAL-PLN-002 | Structural | docs traceability 확인 | `bash scripts/validation/check-doc-traceability.sh` | failures=0 |
| VAL-PLN-003 | Runtime config | Compose config 확인 | `bash scripts/validation/validate-docker-compose.sh` | service count > 0 |
| VAL-PLN-004 | Security baseline | template/security baseline 확인 | `bash scripts/validation/check-template-security-baseline.sh` | pass |
| VAL-PLN-005 | Hardening | baseline hardening 확인 | `bash scripts/validation/check-quickwin-baseline.sh` and `bash scripts/hardening/check-all-hardening.sh` | pass |
| VAL-PLN-006 | Docs template | README/stage heading audit | local `python3` audit | missing=0 |
| VAL-PLN-007 | Diff hygiene | Markdown whitespace 확인 | `git diff --check` | no errors |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| 오래된 문서를 템플릿에 맞추며 의미가 바뀜 | Medium | 기존 본문은 삭제하지 않고 누락 섹션만 보강 |
| secret 값이 문서에 노출됨 | High | `secrets/**/*.txt`는 열람하지 않고 경로와 example만 사용 |
| 문서 보강 범위가 너무 넓어짐 | Medium | 런타임/compose/governance 변경은 제외하고 template alignment에 집중 |
| `ksql`/`ksqldb` 명칭 차이를 누락으로 오판 | Low | README에 alias로 설명하고 파일 rename은 하지 않음 |
| 보유 Compose와 root-active Compose를 혼동함 | Medium | `root-active`, `root-commented-optional`, `standalone-only`, `dev/cluster variant` 상태를 문서화 |
| 검증 결과가 전체 profile 통과처럼 읽힘 | Medium | `validate-docker-compose.sh`의 기본 `core` profile 범위와 임시 파일 생성 가능성을 evidence에 기록 |
| heading audit 통과를 문서 품질 완료로 오해함 | Medium | semantic QA 항목을 task evidence와 README에 별도로 기록 |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: README/stage heading audit가 missing=0이어야 한다.
- **Sandbox / Canary Rollout**: 적용하지 않는다. 문서 전용 변경이다.
- **Human Approval Gate**: runtime, secret value, compose 변경이 필요하면 별도 승인으로 분리한다.
- **Rollback Trigger**: validation failure 또는 secret value exposure 발견 시 해당 문서 변경을 되돌리고 원인을 기록한다.
- **Prompt / Model Promotion Criteria**: 적용하지 않는다.

## Completion Criteria

- [x] Scoped work completed
- [x] Verification passed
- [x] Required docs updated

## Related Documents

- **PRD**: 명시적 PRD 없음
- **ARD**: 명시적 ARD 없음
- **Spec**: [../03.specs/infra-secrets-docs-refresh/spec.md](../../03.specs/infra-secrets-docs-refresh/spec.md)
- **ADR**: 명시적 ADR 없음
- **Task**: [../04.execution/tasks/2026-05-09-infra-secrets-docs-refresh.md](../tasks/2026-05-09-infra-secrets-docs-refresh.md)
- **Operation**: [../05.operations/README.md](../../05.operations/README.md)
- **Runbook**: [../05.operations/README.md](../../05.operations/README.md)
