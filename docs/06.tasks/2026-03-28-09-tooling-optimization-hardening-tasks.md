# Task: 09-Tooling Optimization Hardening

## Overview (KR)

이 문서는 `09-tooling` 최적화/하드닝 실행 태스크를 추적한다. compose hardening, CI 정책 게이트, 문서 추적성, 카탈로그 확장 항목을 작업 단위로 관리한다.

## Inputs

- **Parent Spec**: [../04.specs/09-tooling/spec.md](../04.specs/09-tooling/spec.md)
- **Parent Plan**: [../05.plans/2026-03-28-09-tooling-optimization-hardening-plan.md](../05.plans/2026-03-28-09-tooling-optimization-hardening-plan.md)

## Working Rules

- tooling 구성 변경은 compose static validation + hardening script 결과를 남긴다.
- gateway/auth 영향 변경은 접근 경계 영향도를 기록한다.
- 문서 변경은 PRD~Runbook 링크와 README 인덱스를 동시 갱신한다.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-TLG-001 | SonarQube/Terrakube/Syncthing middleware를 gateway+SSO 체인으로 정렬 | impl | Contracts / Config | PLN-TLG-001 | compose label 확인 | DevOps | Done |
| T-TLG-002 | tooling compose `infra_net` external 선언 정렬 | impl | Contracts / Config | PLN-TLG-002 | network contract 확인 | DevOps | Done |
| T-TLG-003 | locust-worker healthcheck 추가 | impl | Runtime Stability | PLN-TLG-003 | compose healthcheck 확인 | DevOps | Done |
| T-TLG-004 | k6 volume 참조 drift 정렬 | impl | Runtime Stability | PLN-TLG-003 | `k6-data` mount 확인 | DevOps | Done |
| T-TLG-005 | tooling hardening script 추가 | ops | Governance Contract | PLN-TLG-004 | `bash scripts/check-tooling-hardening.sh` | DevOps | Done |
| T-TLG-006 | CI `tooling-hardening` job 추가 | ops | Governance Contract | PLN-TLG-004 | workflow job 확인 | DevOps | Done |
| T-TLG-007 | scripts inventory/usage README 갱신 | doc | Related Docs | PLN-TLG-004 | README 항목 반영 | Docs | Done |
| T-TLG-008 | PRD/ARD/ADR/Plan/Task/Guide/Ops/Runbook 문서 생성 | doc | Related Docs | PLN-TLG-005 | 링크/인덱스 동기화 | Docs | Done |
| T-TLG-009 | terraform 승인 게이트/state 백업/drift 자동 탐지 roadmap 정의 | doc | Catalog Expansion Targets | PLN-TLG-006 | operations/tasks 반영 | Platform Owner | Done |
| T-TLG-010 | terrakube workspace 분리/권한/감사로그 roadmap 정의 | doc | Catalog Expansion Targets | PLN-TLG-006 | operations/tasks 반영 | Platform Owner | Done |
| T-TLG-011 | registry 서명/검증/취약점 차단 roadmap 정의 | doc | Catalog Expansion Targets | PLN-TLG-006 | operations/tasks 반영 | Security/DevOps | Done |
| T-TLG-012 | sonarqube/k6/locust/syncthing 확장 정책 로드맵 정의 | doc | Catalog Expansion Targets | PLN-TLG-006 | operations/tasks 반영 | Platform Owner | Done |
| T-TLG-013 | 정적 검증 실행 및 결과 기록 | test | Verification | PLN-TLG-001~006 | compose/script/baseline/traceability 체크 | DevOps | Done |
| T-TLG-014 | runtime 리허설 및 운영 증적 수집 | test | Verification | PLN-TLG-001~006 | health/latency/log evidence | DevOps | Planned |

## Suggested Types

- `impl`
- `test`
- `doc`
- `ops`

## Phase View (Optional)

### Phase 1

- [x] T-TLG-001
- [x] T-TLG-002
- [x] T-TLG-003
- [x] T-TLG-004
- [x] T-TLG-005
- [x] T-TLG-006
- [x] T-TLG-007

### Phase 2

- [x] T-TLG-008
- [x] T-TLG-009
- [x] T-TLG-010
- [x] T-TLG-011
- [x] T-TLG-012
- [x] T-TLG-013
- [ ] T-TLG-014

## Verification Summary

- **Test Commands**:
  - `for f in infra/09-tooling/*/docker-compose.yml; do docker compose -f "$f" config >/dev/null; done`
  - `bash scripts/check-tooling-hardening.sh`
  - `bash scripts/check-template-security-baseline.sh`
  - `bash scripts/check-doc-traceability.sh`
- **Eval Commands**: N/A
- **Logs / Evidence Location**: 로컬 검증 로그 + CI `tooling-hardening` job

## Related Documents

- **PRD**: [../01.prd/2026-03-28-09-tooling-optimization-hardening.md](../01.prd/2026-03-28-09-tooling-optimization-hardening.md)
- **ARD**: [../02.ard/0024-tooling-optimization-hardening-architecture.md](../02.ard/0024-tooling-optimization-hardening-architecture.md)
- **ADR**: [../03.adr/0024-tooling-hardening-and-ha-expansion-strategy.md](../03.adr/0024-tooling-hardening-and-ha-expansion-strategy.md)
- **Plan**: [../05.plans/2026-03-28-09-tooling-optimization-hardening-plan.md](../05.plans/2026-03-28-09-tooling-optimization-hardening-plan.md)
- **Guide**: [../07.guides/09-tooling/optimization-hardening.md](../07.guides/09-tooling/optimization-hardening.md)
- **Operation**: [../08.operations/09-tooling/optimization-hardening.md](../08.operations/09-tooling/optimization-hardening.md)
- **Runbook**: [../09.runbooks/09-tooling/optimization-hardening.md](../09.runbooks/09-tooling/optimization-hardening.md)
