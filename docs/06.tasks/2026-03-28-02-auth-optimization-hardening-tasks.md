# Task: 02-Auth Optimization Hardening

## Overview (KR)

이 문서는 `02-auth` 최적화/하드닝 구현 태스크를 추적한다. Keycloak/OAuth2 Proxy 설정 변경, CI 게이트, 문서 추적성 정비를 작업 단위로 관리한다.

## Inputs

- **Parent Spec**: [../04.specs/02-auth/spec.md](../04.specs/02-auth/spec.md)
- **Parent Plan**: [../05.plans/2026-03-28-02-auth-optimization-hardening-plan.md](../05.plans/2026-03-28-02-auth-optimization-hardening-plan.md)

## Working Rules

- 시크릿은 파일 기반(`/run/secrets`) 계약을 유지한다.
- fail-open 변경은 금지하며, degraded-mode는 문서화된 절차로만 수행한다.
- 문서 수정 시 폴더 README 인덱스를 같은 변경 세트에서 갱신한다.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-AUTH-001 | OAuth2 Proxy compose 인라인 셸 제거, 엔트리포인트 기반 실행으로 전환 | impl | 02-auth/spec.md / Contracts | PLN-AUTH-001 | `bash scripts/check-auth-hardening.sh` | Infra | Done |
| T-AUTH-002 | OAuth2 Proxy 엔트리포인트에서 cookie/client/redis secret 파일 주입 처리 | impl | 02-auth/spec.md / Core Design | PLN-AUTH-001 | `bash scripts/check-auth-hardening.sh` | Infra | Done |
| T-AUTH-003 | OAuth2 Proxy Dockerfile non-root 사용자 생성 및 USER 적용 | impl | 02-auth/spec.md / Security | PLN-AUTH-002 | `bash scripts/check-auth-hardening.sh` | DevOps | Done |
| T-AUTH-004 | Keycloak compose에서 시크릿 길이 출력 제거 | impl | 02-auth/spec.md / Security | PLN-AUTH-003 | 코드 리뷰 + `docker compose config` | Infra | Done |
| T-AUTH-005 | `scripts/check-auth-hardening.sh` 추가 | ops | 02-auth/spec.md / Verification | PLN-AUTH-004 | 스크립트 pass/fail 동작 확인 | DevOps | Done |
| T-AUTH-006 | CI workflow에 `auth-hardening` job 추가 | ops | 02-auth/spec.md / CI | PLN-AUTH-005 | PR CI logs | DevOps | Done |
| T-AUTH-007 | PRD/ARD/ADR/Plan/Task 문서 생성 및 링크 연결 | doc | 02-auth/spec.md / Traceability | PLN-AUTH-006 | 상대경로 양방향 링크 확인 | Docs | Done |
| T-AUTH-008 | 02-auth Guide/Operation/Runbook 재정비 및 README 인덱스 갱신 | doc | 02-auth/spec.md / Traceability | PLN-AUTH-006, PLN-AUTH-007 | `bash scripts/check-doc-traceability.sh` | Docs | Done |
| T-AUTH-009 | 02-auth 관련 검증 명령 실행 및 결과 기록 | test | 02-auth/spec.md / Verification | PLN-AUTH-004~005 | 실행 결과 수집 | Infra | Done |

## Suggested Types

- `impl`
- `test`
- `doc`
- `ops`

## Phase View (Optional)

### Phase 1

- [x] T-AUTH-001
- [x] T-AUTH-002
- [x] T-AUTH-003
- [x] T-AUTH-004

### Phase 2

- [x] T-AUTH-005
- [x] T-AUTH-006
- [x] T-AUTH-007
- [x] T-AUTH-008
- [x] T-AUTH-009

## Verification Summary

- **Test Commands**:
  - `bash scripts/check-auth-hardening.sh`
  - `bash scripts/check-template-security-baseline.sh`
  - `bash scripts/check-doc-traceability.sh`
  - `docker compose config`
  - `docker compose -f infra/02-auth/keycloak/docker-compose.yml config`
  - `docker compose -f infra/02-auth/oauth2-proxy/docker-compose.yml config`
- **Eval Commands**: N/A
- **Logs / Evidence Location**: PR CI logs + local command output (`auth-hardening/template-security/doc-traceability/config`)
