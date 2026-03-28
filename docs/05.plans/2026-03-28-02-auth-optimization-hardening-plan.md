# 02-Auth Optimization Hardening Implementation Plan

## Overview (KR)

이 문서는 `infra/02-auth`(Keycloak, OAuth2 Proxy)의 최적화/하드닝 실행 계획서다. 설정 개선, CI 검증 게이트, 그리고 `01.prd~09.runbooks` 문서 추적성 동기화를 포함한다.

## Context

- 기준 카탈로그: [12-infra-service-optimization-catalog.md](../08.operations/12-infra-service-optimization-catalog.md)
- 상위 우선순위 계획: [2026-03-27-infra-service-optimization-priority-plan.md](./2026-03-27-infra-service-optimization-priority-plan.md)
- 적용 원칙:
  - Scope: `Config+Docs`
  - Security posture: `Fail-closed`
  - Hardening level: `Balanced`
  - Validation gate: `Strict CI Gate`

## Goals & In-Scope

- **Goals**:
  - OAuth2 Proxy 시크릿 주입/런타임 권한을 표준 하드닝으로 정리한다.
  - Keycloak/OAuth2 Proxy의 인증 경로 운영 기준을 문서와 자동 검증으로 고정한다.
  - Plan/Task/Guide/Operation/Runbook 상호 링크를 일관화한다.
- **In Scope**:
  - `infra/02-auth/keycloak/docker-compose.yml`
  - `infra/02-auth/oauth2-proxy/{docker-compose.yml,Dockerfile,docker-entrypoint.sh,config/oauth2-proxy.cfg}`
  - `scripts/check-auth-hardening.sh`, `.github/workflows/ci-quality.yml`, `scripts/README.md`
  - `docs/01~09`의 02-auth 관련 문서/README

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - Keycloak realm/business RBAC 구조 재설계
  - 타 티어(01, 03~11) 설정 일괄 변경
- **Out of Scope**:
  - 신규 외부 노출 포트 추가
  - 신규 IdP/인증 프로토콜 도입

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-AUTH-001 | OAuth2 Proxy 시크릿 주입을 엔트리포인트 중심으로 정리 | `infra/02-auth/oauth2-proxy/docker-entrypoint.sh`, `docker-compose.yml` | REQ-PRD-FUN-01 | 시크릿 파일 기반 export 확인 |
| PLN-AUTH-002 | OAuth2 Proxy 이미지 non-root 하드닝 | `infra/02-auth/oauth2-proxy/Dockerfile` | REQ-PRD-FUN-02 | `USER oauth2proxy:oauth2proxy` 존재 |
| PLN-AUTH-003 | Keycloak 시크릿 로그 노출 최소화 | `infra/02-auth/keycloak/docker-compose.yml` | REQ-PRD-FUN-01 | 시크릿 길이 echo 제거 |
| PLN-AUTH-004 | 02-auth 하드닝 검증 스크립트 추가 | `scripts/check-auth-hardening.sh` | REQ-PRD-FUN-03 | 실패시 non-zero, 통과시 zero |
| PLN-AUTH-005 | CI에 `auth-hardening` 게이트 추가 | `.github/workflows/ci-quality.yml` | REQ-PRD-FUN-03 | PR/Push 시 job 실행 |
| PLN-AUTH-006 | PRD~Runbook 문서 세트 생성/정비 | `docs/01~09` 관련 파일 | REQ-PRD-FUN-04 | 양방향 링크 및 README 인덱스 반영 |
| PLN-AUTH-007 | degraded-mode 운영/복구 절차 명문화 | `docs/08.operations/02-auth/*.md`, `docs/09.runbooks/02-auth/*.md` | REQ-PRD-FUN-05 | 정책+절차 문서 일치 |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-AUTH-001 | Structural | 02-auth 하드닝 정적 검증 | `bash scripts/check-auth-hardening.sh` | 실패 0건 |
| VAL-AUTH-002 | Compliance | 템플릿/보안 기준선 검증 | `bash scripts/check-template-security-baseline.sh` | 실패 0건 |
| VAL-AUTH-003 | Traceability | 05/08/09 추적성 검증 | `bash scripts/check-doc-traceability.sh` | 실패 0건 |
| VAL-AUTH-004 | Compose | Compose 해석 검증 | `docker compose config` | 오류 없이 출력 |
| VAL-AUTH-005 | Service Compose | 서비스별 compose 검증 | `docker compose -f infra/02-auth/keycloak/docker-compose.yml config` and `docker compose -f infra/02-auth/oauth2-proxy/docker-compose.yml config` | 오류 없이 출력 |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| 도메인 환경 변수 불일치로 OIDC 리다이렉션 실패 | High | 운영 가이드에 도메인/Redirect 동기화 체크리스트 추가 |
| non-root 전환 후 런타임 권한 문제 | Medium | 엔트리포인트/바이너리 소유권을 명시적으로 설정 |
| 인증 장애 시 서비스 접근 영향 확대 | Medium | fail-closed 유지 + degraded-mode 절차를 제한적으로 문서화 |
| 문서 링크 회귀 | Medium | README 인덱스/상호 참조를 동일 커밋에서 동기화 |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: `check-auth-hardening`, `check-template-security-baseline`, `check-doc-traceability` 통과
- **Sandbox / Canary Rollout**: OAuth2 Proxy 반영 후 Keycloak 변경 반영
- **Human Approval Gate**: Infra/Ops reviewer 승인 후 병합
- **Rollback Trigger**: 인증 루프 지속, `/ping` 실패 지속, OIDC 콜백 장애 증가
- **Prompt / Model Promotion Criteria**: N/A

## Completion Criteria

- [x] 02-auth 설정 하드닝 반영
- [x] CI 게이트와 스크립트 추가
- [x] PRD~Runbook 문서 세트 동기화
- [x] README 인덱스 갱신
- [x] 검증 커맨드 통과

## Related Documents

- **PRD**: [../01.prd/2026-03-28-02-auth-optimization-hardening.md](../01.prd/2026-03-28-02-auth-optimization-hardening.md)
- **ARD**: [../02.ard/0014-auth-optimization-hardening-architecture.md](../02.ard/0014-auth-optimization-hardening-architecture.md)
- **ADR**: [../03.adr/0017-auth-hardening-runtime-and-fail-closed.md](../03.adr/0017-auth-hardening-runtime-and-fail-closed.md)
- **Spec**: [../04.specs/02-auth/spec.md](../04.specs/02-auth/spec.md)
- **Tasks**: [../06.tasks/2026-03-28-02-auth-optimization-hardening-tasks.md](../06.tasks/2026-03-28-02-auth-optimization-hardening-tasks.md)
- **Operations**: [../08.operations/02-auth/README.md](../08.operations/02-auth/README.md)
- **Runbooks**: [../09.runbooks/02-auth/README.md](../09.runbooks/02-auth/README.md)
