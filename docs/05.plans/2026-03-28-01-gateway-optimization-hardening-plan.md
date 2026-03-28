# 01-Gateway Optimization Hardening Implementation Plan

## Overview (KR)

이 문서는 `infra/01-gateway`의 Traefik/Nginx를 `Traefik Primary, Balanced Hardening` 기준으로 최적화하는 실행 계획서다. 설정 변경, 검증 자동화, CI 게이트, 문서 추적성(`05.plans ↔ 08.operations ↔ 09.runbooks`) 동기화를 포함한다.

## Context

- 기준 카탈로그: [12-infra-service-optimization-catalog.md](../08.operations/12-infra-service-optimization-catalog.md)
- 기준 계획: [2026-03-27-infra-service-optimization-priority-plan.md](./2026-03-27-infra-service-optimization-priority-plan.md)
- 범위 결정:
  - Scope: `Config+Docs`
  - Runtime model: `Traefik Primary`
  - Hardening level: `Balanced`
  - Validation gate: `Strict CI Gate`
  - Traefik scope: `Gateway-owned routers only`

## Goals & In-Scope

- **Goals**:
  - Traefik 미들웨어 표준 체인(`rate-limit/retry/circuit-breaker`)을 01-gateway 소유 라우터에 적용한다.
  - Nginx를 readonly 운영 모델과 명시적 failover/timeout 정책으로 하드닝한다.
  - 01-gateway 변경을 CI 자동 검증으로 강제한다.
  - 계획/운영정책/런북/가이드 문서를 상호 링크와 인덱스로 동기화한다.
- **In Scope**:
  - `infra/01-gateway/traefik/**`, `infra/01-gateway/nginx/**`
  - `scripts/check-gateway-hardening.sh`, `.github/workflows/ci-quality.yml`
  - `docs/05.plans`, `docs/06.tasks`, `docs/08.operations/01-gateway`, `docs/09.runbooks/01-gateway`, `docs/07.guides/01-gateway`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - 02~11 티어 전역 라우터 라벨 일괄 변경
  - 인증/비즈니스 로직 변경
- **Out of Scope**:
  - 신규 외부 포트/서비스 추가
  - API/타입/스키마 변경

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-GW-001 | Traefik middleware 표준 체인 정의 | `infra/01-gateway/traefik/dynamic/middleware.yml` | REQ-GW-TRAEFIK-CHAIN | `req-rate-limit/retry/circuit-breaker/gateway-standard-chain` 존재 |
| PLN-GW-002 | Dashboard router 체인 적용 | `infra/01-gateway/traefik/docker-compose.yml` | REQ-GW-TRAEFIK-ROUTER | `dashboard-auth@file,gateway-standard-chain@file` 적용 |
| PLN-GW-003 | Nginx readonly 템플릿+tmpfs 전환 | `infra/01-gateway/nginx/docker-compose.yml` | REQ-GW-NGINX-READONLY | readonly 템플릿 + 필수 tmpfs + `/ping` healthcheck |
| PLN-GW-004 | Nginx timeout/failover/cache 하드닝 | `infra/01-gateway/nginx/config/nginx.conf` | REQ-GW-NGINX-HARDEN | `server_tokens`, timeout, upstream fail params, `proxy_next_upstream`, static cache 정책 적용 |
| PLN-GW-005 | Gateway hardening 검증 스크립트 추가 | `scripts/check-gateway-hardening.sh`, `scripts/README.md` | REQ-GW-VERIFY-AUTO | 스크립트 non-zero fail/zero pass 동작 |
| PLN-GW-006 | CI Strict Gate 연결 | `.github/workflows/ci-quality.yml` | REQ-GW-CI-GATE | `gateway-hardening` job 필수 실행 |
| PLN-GW-007 | 문서 추적성 동기화 | `docs/05.plans/**`, `docs/06.tasks/**`, `docs/08.operations/01-gateway/**`, `docs/09.runbooks/01-gateway/**`, `docs/07.guides/01-gateway/**` | REQ-GW-DOC-TRACE | 상호 링크/README 인덱스 반영 |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-GW-001 | Structural | Gateway 하드닝 정책 정적 검증 | `bash scripts/check-gateway-hardening.sh` | 실패 0건 |
| VAL-GW-002 | Compliance | 템플릿/보안 기준선 검증 | `bash scripts/check-template-security-baseline.sh` | 실패 0건 |
| VAL-GW-003 | Traceability | 05/08/09 문서 추적성 검증 | `bash scripts/check-doc-traceability.sh` | 실패 0건 |
| VAL-GW-004 | Compose | Compose 해석 검증 | `docker compose config` | 오류 없이 출력 |
| VAL-GW-005 | Runtime lint | Nginx 설정 구문 검증 | `docker compose -f infra/01-gateway/nginx/docker-compose.yml exec nginx nginx -t` | `syntax is ok` |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| 대시보드 요청 429 증가 | Medium | `req-rate-limit` 현행값(100/50) 유지, 관측 후 조정 |
| retry/circuit-breaker로 비정상 응답 패턴 변화 | Medium | 적용 범위를 gateway-owned router로 한정 |
| readonly 전환 후 쓰기 경로 오류 | High | `/var/cache/nginx`, `/var/log/nginx`, `/var/run` tmpfs 명시 |
| nginx.conf 실수로 리로드 실패 | High | `nginx -t` 선검증 + 런북 롤백 절차 제공 |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: 정적 체크 3종(`gateway-hardening`, `template-security`, `doc-traceability`) 통과
- **Sandbox / Canary Rollout**: Traefik 반영 후 Nginx 반영 순서 고정
- **Human Approval Gate**: Infra/Ops reviewer 승인 후 병합
- **Rollback Trigger**: 인증 루프, 대량 429, `/ping` 실패 발생 시 직전 커밋 복구
- **Prompt / Model Promotion Criteria**: N/A

## Completion Criteria

- [x] Traefik/Nginx 설정 변경 반영
- [x] Gateway hardening 스크립트 및 CI 게이트 추가
- [x] Plan/Task/Operation/Runbook/Guide 문서 동기화 완료
- [x] 관련 README 인덱스 갱신 완료
- [x] 검증 명령(VAL-GW-001~004) 통과

## Related Documents

- **Operations Catalog**: [12-infra-service-optimization-catalog.md](../08.operations/12-infra-service-optimization-catalog.md)
- **Parent Priority Plan**: [2026-03-27-infra-service-optimization-priority-plan.md](./2026-03-27-infra-service-optimization-priority-plan.md)
- **Task**: [2026-03-28-01-gateway-optimization-hardening-tasks.md](../06.tasks/2026-03-28-01-gateway-optimization-hardening-tasks.md)
- **Gateway Operations**: [01-gateway/README.md](../08.operations/01-gateway/README.md)
- **Gateway Runbooks**: [01-gateway/README.md](../09.runbooks/01-gateway/README.md)
