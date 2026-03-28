# Task: 11-Laboratory Optimization Hardening

## Overview (KR)

이 문서는 `11-laboratory` 최적화/하드닝 실행 태스크를 추적한다. ingress 경계 강화, direct 노출 제거, 최소권한 개선, CI 정책 게이트, 카탈로그 확장 로드맵을 작업 단위로 관리한다.

## Inputs

- **Parent Spec**: [../04.specs/11-laboratory/spec.md](../04.specs/11-laboratory/spec.md)
- **Parent Plan**: [../05.plans/2026-03-28-11-laboratory-optimization-hardening-plan.md](../05.plans/2026-03-28-11-laboratory-optimization-hardening-plan.md)

## Working Rules

- Laboratory compose 변경은 정적 검증 + hardening check 결과를 남긴다.
- 인증/allowlist 완화 변경은 승인자 검토를 필수로 한다.
- 문서 변경은 PRD~Runbook 링크와 README 인덱스를 동시 갱신한다.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-LAB-001 | 모든 Laboratory 라우터 middleware를 gateway+allowlist+SSO 체인으로 정렬 | impl | Contracts / Config | PLN-LAB-001 | compose label 확인 | DevOps | Done |
| T-LAB-002 | compose `infra_net` external 선언 정렬 | impl | Network Boundary | PLN-LAB-002 | network contract 확인 | DevOps | Done |
| T-LAB-003 | dashboard direct host `ports` 제거 및 `expose` 전환 | impl | Least Privilege | PLN-LAB-003 | ports 제거 확인 | DevOps | Done |
| T-LAB-004 | dozzle docker socket read-only 적용 | impl | Least Privilege | PLN-LAB-004 | `docker.sock:ro` 확인 | DevOps | Done |
| T-LAB-005 | service mount 기반 healthcheck 추가 | impl | Runtime Stability | PLN-LAB-001~004 | healthcheck block 확인 | DevOps | Done |
| T-LAB-006 | laboratory hardening script 추가 | ops | Governance Contract | PLN-LAB-005 | `bash scripts/check-laboratory-hardening.sh` | DevOps | Done |
| T-LAB-007 | CI `laboratory-hardening` job 추가 | ops | Governance Contract | PLN-LAB-005 | workflow job 확인 | DevOps | Done |
| T-LAB-008 | scripts inventory/usage README 갱신 | doc | Related Docs | PLN-LAB-005 | README 항목 반영 | Docs | Done |
| T-LAB-009 | PRD/ARD/ADR/Plan/Task/Guide/Ops/Runbook 문서 생성 | doc | Related Docs | PLN-LAB-006 | 링크/인덱스 동기화 | Docs | Done |
| T-LAB-010 | dashboard 만료 정책 로드맵 정의 | doc | Catalog Expansion Targets | PLN-LAB-007 | operations/tasks 반영 | Platform Owner | Done |
| T-LAB-011 | dozzle 로그 접근 제한 로드맵 정의 | doc | Catalog Expansion Targets | PLN-LAB-007 | operations/tasks 반영 | Platform Owner | Done |
| T-LAB-012 | portainer 세션/승인 정책 로드맵 정의 | doc | Catalog Expansion Targets | PLN-LAB-007 | operations/tasks 반영 | Security/DevOps | Done |
| T-LAB-013 | redisinsight 최소권한/감사 정책 로드맵 정의 | doc | Catalog Expansion Targets | PLN-LAB-007 | operations/tasks 반영 | Security/DevOps | Done |
| T-LAB-014 | 정적 검증 실행 및 결과 기록 | test | Verification | PLN-LAB-001~007 | compose/script/baseline/traceability 체크 | DevOps | Done |
| T-LAB-015 | runtime 리허설 및 운영 증적 수집 | test | Verification | PLN-LAB-001~007 | health/access evidence | DevOps | Planned |

## Suggested Types

- `impl`
- `test`
- `doc`
- `ops`

## Phase View (Optional)

### Phase 1

- [x] T-LAB-001
- [x] T-LAB-002
- [x] T-LAB-003
- [x] T-LAB-004
- [x] T-LAB-005
- [x] T-LAB-006
- [x] T-LAB-007
- [x] T-LAB-008

### Phase 2

- [x] T-LAB-009
- [x] T-LAB-010
- [x] T-LAB-011
- [x] T-LAB-012
- [x] T-LAB-013
- [x] T-LAB-014
- [ ] T-LAB-015

## Verification Summary

- **Test Commands**:
  - `for f in infra/11-laboratory/*/docker-compose.yml; do docker compose -f "$f" config >/dev/null; done`
  - `bash scripts/check-laboratory-hardening.sh`
  - `bash scripts/check-template-security-baseline.sh`
  - `bash scripts/check-doc-traceability.sh`
- **Eval Commands**: N/A
- **Logs / Evidence Location**: 로컬 검증 로그 + CI `laboratory-hardening` job

## Related Documents

- **PRD**: [../01.prd/2026-03-28-11-laboratory-optimization-hardening.md](../01.prd/2026-03-28-11-laboratory-optimization-hardening.md)
- **ARD**: [../02.ard/0025-laboratory-optimization-hardening-architecture.md](../02.ard/0025-laboratory-optimization-hardening-architecture.md)
- **ADR**: [../03.adr/0025-laboratory-hardening-and-ha-expansion-strategy.md](../03.adr/0025-laboratory-hardening-and-ha-expansion-strategy.md)
- **Plan**: [../05.plans/2026-03-28-11-laboratory-optimization-hardening-plan.md](../05.plans/2026-03-28-11-laboratory-optimization-hardening-plan.md)
- **Guide**: [../07.guides/11-laboratory/optimization-hardening.md](../07.guides/11-laboratory/optimization-hardening.md)
- **Operation**: [../08.operations/11-laboratory/optimization-hardening.md](../08.operations/11-laboratory/optimization-hardening.md)
- **Runbook**: [../09.runbooks/11-laboratory/optimization-hardening.md](../09.runbooks/11-laboratory/optimization-hardening.md)
