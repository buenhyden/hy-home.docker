# 09-Tooling Optimization Hardening Implementation Plan

## Overview (KR)

이 문서는 `infra/09-tooling` 최적화/하드닝 실행 계획서다. gateway+SSO 경계 정렬, 네트워크 격리 명시, 테스트 도구 런타임 안정화, CI 정책 게이트 도입, 카탈로그 확장 로드맵을 단계적으로 수행한다.

## Context

- 기준 카탈로그: [../08.operations/12-infra-service-optimization-catalog.md](../08.operations/12-infra-service-optimization-catalog.md)
- 상위 우선순위 계획: [2026-03-27-infra-service-optimization-priority-plan.md](./2026-03-27-infra-service-optimization-priority-plan.md)
- 대상 구성: `infra/09-tooling/**/*`, `scripts/`, `.github/workflows/`, `docs/01~09`

## Goals & In-Scope

- **Goals**:
  - SonarQube/Terrakube/Syncthing 공개 경로를 gateway 표준+SSO 정책으로 정렬한다.
  - tooling compose의 `infra_net` external 경계 선언을 표준화한다.
  - locust-worker healthcheck와 k6 volume 계약을 정렬한다.
  - tooling 전용 하드닝 검증 스크립트 및 CI 게이트를 도입한다.
  - 카탈로그 확장 항목을 문서/태스크 기반으로 실행 가능하게 만든다.
- **In Scope**:
  - `infra/09-tooling/*/docker-compose.yml`
  - `scripts/check-tooling-hardening.sh`
  - `scripts/README.md`
  - `.github/workflows/ci-quality.yml`
  - `docs/01~09` tooling optimization-hardening 문서/README

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - 즉시 카탈로그 확장 항목의 전면 런타임 적용
  - tooling 서비스 major upgrade
- **Out of Scope**:
  - 신규 도구 도입
  - data tier 아키텍처 변경

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-TLG-001 | SonarQube/Terrakube/Syncthing middleware를 gateway+SSO 체인으로 정렬 | `infra/09-tooling/{sonarqube,terrakube,syncthing}/docker-compose.yml` | REQ-PRD-TLG-FUN-01 | compose label 확인 |
| PLN-TLG-002 | tooling compose `infra_net` external 선언 표준화 | `infra/09-tooling/*/docker-compose.yml` | REQ-PRD-TLG-FUN-02 | network contract 확인 |
| PLN-TLG-003 | locust worker healthcheck + k6 volume 참조 정렬 | `infra/09-tooling/{locust,k6}/docker-compose.yml` | REQ-PRD-TLG-FUN-03 | health/volume 계약 확인 |
| PLN-TLG-004 | tooling hardening script + CI 게이트 추가 | `scripts/check-tooling-hardening.sh`, `.github/workflows/ci-quality.yml`, `scripts/README.md` | REQ-PRD-TLG-FUN-04 | script/CI job 확인 |
| PLN-TLG-005 | PRD~Runbook 문서 체계 생성 및 상호 링크 | `docs/01~09/**` | REQ-PRD-TLG-FUN-05 | 링크 정합성 확인 |
| PLN-TLG-006 | 카탈로그 확장 항목 작업 분해(도구별) | Plan/Task/Ops/Guide docs | REQ-PRD-TLG-FUN-06 | 태스크/정책 반영 확인 |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-TLG-001 | Structural | tooling compose 정적 검증 | `for f in infra/09-tooling/*/docker-compose.yml; do docker compose -f "$f" config >/dev/null; done` | 오류 없음 |
| VAL-TLG-002 | Compliance | tooling 하드닝 기준선 검증 | `bash scripts/check-tooling-hardening.sh` | 실패 0건 |
| VAL-TLG-003 | Baseline | 템플릿/보안 기준선 | `bash scripts/check-template-security-baseline.sh` | 실패 0건 |
| VAL-TLG-004 | Traceability | 문서 추적성 검증 | `bash scripts/check-doc-traceability.sh` | 실패 0건 |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| SSO 강화로 기존 테스트 접근 경로 영향 | Medium | runbook에 예외/복구 절차 반영 |
| locust/k6 런타임 계약 변경으로 테스트 스크립트 영향 | Medium | 단계적 검증 및 기본 시나리오 점검 |
| 카탈로그 확장 항목 미완료로 정책 공백 | Medium | tasks에 단계/우선순위/승인 게이트 명시 |

## Completion Criteria

- [x] tooling compose/script/ci 하드닝 반영
- [x] tooling optimization-hardening 문서 세트 생성
- [x] docs `01~09` README 인덱스 반영
- [ ] runtime 리허설/성능 증적 확보 (환경 허용 시)

## Related Documents

- **PRD**: [../01.prd/2026-03-28-09-tooling-optimization-hardening.md](../01.prd/2026-03-28-09-tooling-optimization-hardening.md)
- **ARD**: [../02.ard/0024-tooling-optimization-hardening-architecture.md](../02.ard/0024-tooling-optimization-hardening-architecture.md)
- **ADR**: [../03.adr/0024-tooling-hardening-and-ha-expansion-strategy.md](../03.adr/0024-tooling-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../04.specs/09-tooling/spec.md](../04.specs/09-tooling/spec.md)
- **Tasks**: [../06.tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md](../06.tasks/2026-03-28-09-tooling-optimization-hardening-tasks.md)
- **Guide**: [../07.guides/09-tooling/optimization-hardening.md](../07.guides/09-tooling/optimization-hardening.md)
- **Operations**: [../08.operations/09-tooling/optimization-hardening.md](../08.operations/09-tooling/optimization-hardening.md)
- **Runbooks**: [../09.runbooks/09-tooling/optimization-hardening.md](../09.runbooks/09-tooling/optimization-hardening.md)
