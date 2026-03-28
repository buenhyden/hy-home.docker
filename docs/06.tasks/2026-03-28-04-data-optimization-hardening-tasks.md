# Task: 04-Data Optimization Hardening

## Overview (KR)

이 문서는 `04-data` 최적화/하드닝 구현 태스크를 추적한다. compose 정합성 보강, 하드닝 검증 자동화, 문서 추적성 동기화를 작업 단위로 관리한다.

## Inputs

- **Parent Spec**: [../04.specs/04-data/spec.md](../04.specs/04-data/spec.md)
- **Parent Plan**: [../05.plans/2026-03-28-04-data-optimization-hardening-plan.md](../05.plans/2026-03-28-04-data-optimization-hardening-plan.md)

## Working Rules

- 04-data 하드닝은 카탈로그 우선순위에 맞춰 즉시 적용 항목부터 수행한다.
- 모든 compose 변경은 정적 검증(`docker compose config`)과 스크립트 증빙을 남긴다.
- 문서 변경은 PRD~Runbook 상호 링크를 유지한다.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-DATA-001 | `supabase` 핵심 서비스 healthcheck 추가 | impl | 04-data/spec.md / Contracts | PLN-DATA-001 | `docker compose ...supabase... config` | DevOps | Done |
| T-DATA-002 | Valkey exporter 시크릿 경로 정합화 | impl | 04-data/spec.md / Contracts | PLN-DATA-002 | `rg mng_valkey_password` 미검출 | DevOps | Done |
| T-DATA-003 | SeaweedFS expose 오타 제거 | impl | 04-data/spec.md / Contracts | PLN-DATA-003 | `rg ':-19333}]|:-18085}]|:-18888}]'` 미검출 | DevOps | Done |
| T-DATA-004 | ksql tier 라벨 정규화 | impl | 04-data/spec.md / Contracts | PLN-DATA-004 | `hy-home.tier: data` 확인 | DevOps | Done |
| T-DATA-005 | `check-data-hardening.sh` 신규 작성 | ops | 04-data/spec.md / Governance | PLN-DATA-005 | `bash scripts/check-data-hardening.sh` | DevOps | Done |
| T-DATA-006 | CI `data-hardening` job 추가 | ops | 04-data/spec.md / Governance | PLN-DATA-006 | workflow 변경 확인 | DevOps | Done |
| T-DATA-007 | scripts README 인덱스/예시 갱신 | doc | 04-data/spec.md / Related Docs | PLN-DATA-007 | README 항목 확인 | Docs | Done |
| T-DATA-008 | PRD/ARD/ADR/Plan/Task/Guide/Ops/Runbook 문서 반영 | doc | 04-data/spec.md / Related Docs | PLN-DATA-008 | 문서 링크/인덱스 확인 | Docs | Done |
| T-DATA-009 | 정적 검증 실행 및 결과 기록 | test | 04-data/spec.md / Verification | PLN-DATA-001~008 | compose + hardening + traceability 점검 | DevOps | Done |
| T-DATA-010 | runtime 검증(가능 환경) 증적 수집 | test | 04-data/spec.md / Verification | PLN-DATA-001~008 | health 상태 점검 증적 | DevOps | Planned |

## Suggested Types

- `impl`
- `test`
- `doc`
- `ops`

## Phase View (Optional)

### Phase 1

- [x] T-DATA-001
- [x] T-DATA-002
- [x] T-DATA-003
- [x] T-DATA-004
- [x] T-DATA-005
- [x] T-DATA-006

### Phase 2

- [x] T-DATA-007
- [x] T-DATA-008
- [x] T-DATA-009
- [ ] T-DATA-010

## Verification Summary

- **Test Commands**:
  - `docker compose -f infra/04-data/operational/supabase/docker-compose.yml config`
  - `docker compose -f infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml config`
  - `docker compose -f infra/04-data/lake-and-object/seaweedfs/docker-compose.yml config`
  - `docker compose -f infra/04-data/analytics/ksql/docker-compose.yml config`
  - `bash scripts/check-data-hardening.sh`
  - `bash scripts/check-template-security-baseline.sh`
  - `bash scripts/check-doc-traceability.sh`
- **Eval Commands**: N/A
- **Logs / Evidence Location**: 로컬 검증 로그 + CI `data-hardening` job

## Related Documents

- **PRD**: [../01.prd/2026-03-28-04-data-optimization-hardening.md](../01.prd/2026-03-28-04-data-optimization-hardening.md)
- **ARD**: [../02.ard/0019-data-optimization-hardening-architecture.md](../02.ard/0019-data-optimization-hardening-architecture.md)
- **ADR**: [../03.adr/0019-04-data-hardening-and-ha-expansion-strategy.md](../03.adr/0019-04-data-hardening-and-ha-expansion-strategy.md)
- **Plan**: [../05.plans/2026-03-28-04-data-optimization-hardening-plan.md](../05.plans/2026-03-28-04-data-optimization-hardening-plan.md)
- **Guide**: [../07.guides/04-data/optimization-hardening.md](../07.guides/04-data/optimization-hardening.md)
- **Operation**: [../08.operations/04-data/optimization-hardening.md](../08.operations/04-data/optimization-hardening.md)
- **Runbook**: [../09.runbooks/04-data/optimization-hardening.md](../09.runbooks/04-data/optimization-hardening.md)
