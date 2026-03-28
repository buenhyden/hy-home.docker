# 11-Laboratory Optimization Hardening Implementation Plan

## Overview (KR)

이 문서는 `infra/11-laboratory` 최적화/하드닝 실행 계획서다. ingress 보안 경계 강화, direct 노출 제거, 최소권한 개선, CI 정책 게이트 도입, 카탈로그 확장 항목의 단계적 운영 적용을 수행한다.

## Context

- 기준 카탈로그: [../08.operations/12-infra-service-optimization-catalog.md](../08.operations/12-infra-service-optimization-catalog.md)
- 상위 우선순위 계획: [2026-03-27-infra-service-optimization-priority-plan.md](./2026-03-27-infra-service-optimization-priority-plan.md)
- 대상 구성: `infra/11-laboratory/**/*`, `scripts/`, `.github/workflows/`, `docs/01~09`

## Goals & In-Scope

- **Goals**:
  - Laboratory UI 라우터를 gateway+allowlist+SSO 경계로 정렬한다.
  - dashboard direct host 노출을 제거한다.
  - `infra_net` external 선언을 표준화한다.
  - dozzle socket 최소권한(read-only)을 적용한다.
  - laboratory hardening script + CI gate를 도입한다.
  - 카탈로그 확장 항목을 정책/작업 로드맵으로 반영한다.
- **In Scope**:
  - `infra/11-laboratory/*/docker-compose.yml`
  - `.env.example`
  - `scripts/check-laboratory-hardening.sh`
  - `.github/workflows/ci-quality.yml`
  - `docs/01~09` optimization-hardening 문서/README

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Laboratory 서비스군 신규 도입/대체
  - Keycloak/Traefik 코어 정책 재설계
- **Out of Scope**:
  - 비-Laboratory tier 런타임 변경
  - 도구 major version migration

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-LAB-001 | 라우터 middleware를 gateway+allowlist+SSO 체인으로 정렬 | `infra/11-laboratory/*/docker-compose.yml` | REQ-PRD-LAB-FUN-01/02 | compose label 확인 |
| PLN-LAB-002 | `infra_net` external 네트워크 선언 표준화 | `infra/11-laboratory/*/docker-compose.yml` | REQ-PRD-LAB-FUN-04 | network contract 확인 |
| PLN-LAB-003 | dashboard direct host 노출 제거 | `infra/11-laboratory/dashboard/docker-compose.yml` | REQ-PRD-LAB-FUN-03 | `ports:` 제거/`expose` 확인 |
| PLN-LAB-004 | dozzle socket 최소권한 적용 | `infra/11-laboratory/dozzle/docker-compose.yml` | REQ-PRD-LAB-FUN-05 | `docker.sock:ro` 확인 |
| PLN-LAB-005 | lab hardening script + CI gate 추가 | `scripts/check-laboratory-hardening.sh`, `.github/workflows/ci-quality.yml`, `scripts/README.md` | REQ-PRD-LAB-FUN-06 | script/CI job 확인 |
| PLN-LAB-006 | PRD~Runbook 문서 세트/README 인덱스 동기화 | `docs/01~09/**` | REQ-PRD-LAB-FUN-07 | 링크 정합성 확인 |
| PLN-LAB-007 | 카탈로그 확장 항목 roadmap 문서화 | Plan/Task/Ops/Guide docs | REQ-PRD-LAB-FUN-08 | 정책/태스크 반영 확인 |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-LAB-001 | Structural | laboratory compose 정적 검증 | `for f in infra/11-laboratory/*/docker-compose.yml; do docker compose -f "$f" config >/dev/null; done` | 오류 없음 |
| VAL-LAB-002 | Compliance | laboratory 하드닝 기준선 검증 | `bash scripts/check-laboratory-hardening.sh` | 실패 0건 |
| VAL-LAB-003 | Baseline | 템플릿/보안 기준선 | `bash scripts/check-template-security-baseline.sh` | 실패 0건 |
| VAL-LAB-004 | Traceability | 문서 추적성 검증 | `bash scripts/check-doc-traceability.sh` | 실패 0건 |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| allowlist 정책으로 운영자 접근 차단 | Medium | `LAB_ALLOWED_CIDRS` 환경값 표준 운영 절차 제공 |
| dashboard direct 경로 제거로 기존 접근 혼선 | Low | 가이드/런북에서 새 접근 경로 고지 |
| 실험성 서비스 정책 확장 미완료 | Medium | tasks에 단계/승인/증적 기준 명시 |

## Completion Criteria

- [x] compose/script/ci hardening 반영
- [x] optimization-hardening 문서 세트 생성
- [x] docs `01~09` README 인덱스 반영
- [ ] runtime 리허설/운영 증적 확보 (환경 허용 시)

## Related Documents

- **PRD**: [../01.prd/2026-03-28-11-laboratory-optimization-hardening.md](../01.prd/2026-03-28-11-laboratory-optimization-hardening.md)
- **ARD**: [../02.ard/0025-laboratory-optimization-hardening-architecture.md](../02.ard/0025-laboratory-optimization-hardening-architecture.md)
- **ADR**: [../03.adr/0025-laboratory-hardening-and-ha-expansion-strategy.md](../03.adr/0025-laboratory-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../04.specs/11-laboratory/spec.md](../04.specs/11-laboratory/spec.md)
- **Tasks**: [../06.tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md](../06.tasks/2026-03-28-11-laboratory-optimization-hardening-tasks.md)
- **Guide**: [../07.guides/11-laboratory/optimization-hardening.md](../07.guides/11-laboratory/optimization-hardening.md)
- **Operations**: [../08.operations/11-laboratory/optimization-hardening.md](../08.operations/11-laboratory/optimization-hardening.md)
- **Runbooks**: [../09.runbooks/11-laboratory/optimization-hardening.md](../09.runbooks/11-laboratory/optimization-hardening.md)
