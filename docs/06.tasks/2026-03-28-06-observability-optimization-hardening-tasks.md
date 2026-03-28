# Task: 06-Observability Optimization Hardening

## Overview (KR)

이 문서는 `06-observability` 최적화/하드닝 구현 태스크를 추적한다. gateway 경계 강화, health 기반 의존성 보강, 컨테이너 하드닝, CI 기준선 자동화, 문서 추적성 동기화를 작업 단위로 관리한다.

## Inputs

- **Parent Spec**: [../04.specs/06-observability/spec.md](../04.specs/06-observability/spec.md)
- **Parent Plan**: [../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md](../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md)

## Working Rules

- 관측성 compose 변경은 정적 검증 + 하드닝 스크립트 증빙을 남긴다.
- 라우팅/인증 정책 변경은 gateway/auth 영향 범위를 기록한다.
- 문서 변경은 PRD~Runbook 상호 링크와 README 인덱스를 동시 갱신한다.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-OBS-001 | 공개 라우터 middleware 계약 정렬 | impl | 06-observability/spec.md / Contracts | PLN-OBS-001 | 라벨 문자열 확인 | DevOps | Done |
| T-OBS-002 | Loki/Tempo/Pyroscope Traefik 라우팅 추가 | impl | 06-observability/spec.md / Core Design | PLN-OBS-002 | 라우터 라벨 확인 | DevOps | Done |
| T-OBS-003 | Alloy/Grafana depends_on health 계약 강화 | impl | 06-observability/spec.md / Core Design | PLN-OBS-003 | compose config 통과 | DevOps | Done |
| T-OBS-004 | cAdvisor healthcheck 추가 | impl | 06-observability/spec.md / Verification | PLN-OBS-003 | healthcheck 정의 확인 | DevOps | Done |
| T-OBS-005 | Loki/Tempo 커스텀 이미지 비루트/secret guard 보강 | impl | 06-observability/spec.md / Contracts | PLN-OBS-004 | Dockerfile/entrypoint 확인 | DevOps | Done |
| T-OBS-006 | observability 하드닝 검증 스크립트 추가 | ops | 06-observability/spec.md / Governance | PLN-OBS-005 | `bash scripts/check-observability-hardening.sh` | DevOps | Done |
| T-OBS-007 | CI `observability-hardening` job 추가 | ops | 06-observability/spec.md / Governance | PLN-OBS-006 | workflow 정의 확인 | DevOps | Done |
| T-OBS-008 | scripts README 인덱스 갱신 | doc | 06-observability/spec.md / Related Docs | PLN-OBS-006 | README 항목/예시 반영 | Docs | Done |
| T-OBS-009 | PRD/ARD/ADR/Plan/Task/Guide/Ops/Runbook 문서 반영 | doc | 06-observability/spec.md / Related Docs | PLN-OBS-007 | 문서 링크/README 동기화 확인 | Docs | Done |
| T-OBS-010 | 정적 검증 실행 및 결과 기록 | test | 06-observability/spec.md / Verification | PLN-OBS-001~007 | compose + hardening + traceability 점검 | DevOps | Done |
| T-OBS-011 | runtime/복구 리허설 증적 수집 | test | 06-observability/spec.md / Verification | PLN-OBS-001~007 | 헬스/복구 절차 로그 | DevOps | Planned |

## Suggested Types

- `impl`
- `test`
- `doc`
- `ops`

## Phase View (Optional)

### Phase 1

- [x] T-OBS-001
- [x] T-OBS-002
- [x] T-OBS-003
- [x] T-OBS-004
- [x] T-OBS-005
- [x] T-OBS-006
- [x] T-OBS-007

### Phase 2

- [x] T-OBS-008
- [x] T-OBS-009
- [x] T-OBS-010
- [ ] T-OBS-011

## Verification Summary

- **Test Commands**:
  - `docker compose -f infra/06-observability/docker-compose.yml config`
  - `bash scripts/check-observability-hardening.sh`
  - `bash scripts/check-template-security-baseline.sh`
  - `bash scripts/check-doc-traceability.sh`
- **Eval Commands**: N/A
- **Logs / Evidence Location**: 로컬 검증 로그 + CI `observability-hardening` job

## Related Documents

- **PRD**: [../01.prd/2026-03-28-06-observability-optimization-hardening.md](../01.prd/2026-03-28-06-observability-optimization-hardening.md)
- **ARD**: [../02.ard/0021-observability-optimization-hardening-architecture.md](../02.ard/0021-observability-optimization-hardening-architecture.md)
- **ADR**: [../03.adr/0021-observability-hardening-and-ha-expansion-strategy.md](../03.adr/0021-observability-hardening-and-ha-expansion-strategy.md)
- **Plan**: [../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md](../05.plans/2026-03-28-06-observability-optimization-hardening-plan.md)
- **Guide**: [../07.guides/06-observability/optimization-hardening.md](../07.guides/06-observability/optimization-hardening.md)
- **Operation**: [../08.operations/06-observability/optimization-hardening.md](../08.operations/06-observability/optimization-hardening.md)
- **Runbook**: [../09.runbooks/06-observability/optimization-hardening.md](../09.runbooks/06-observability/optimization-hardening.md)
