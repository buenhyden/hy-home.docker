# Task: 01-Gateway Optimization Hardening

## Overview (KR)

이 문서는 `01-gateway` 최적화/하드닝 실행 태스크를 추적한다. 상위 Plan을 기준으로 설정 변경, 검증 자동화, CI 게이트, 문서 동기화를 작업 단위로 관리한다.

## Inputs

- **Parent Spec**: [../04.specs/01-gateway/spec.md](../04.specs/01-gateway/spec.md)
- **Parent Plan**: [../05.plans/2026-03-28-01-gateway-optimization-hardening-plan.md](../05.plans/2026-03-28-01-gateway-optimization-hardening-plan.md)

## Working Rules

- 핵심 동작 변경은 정적 검증 커맨드로 증적을 남긴다.
- 모든 태스크는 변경 파일과 검증 명령을 연결한다.
- 문서 변경 시 해당 폴더 README 인덱스를 같은 변경에 포함한다.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-GW-001 | Traefik middleware에 `req-retry`, `req-circuit-breaker`, `gateway-standard-chain` 추가 | impl | 01-gateway/spec.md / Gateway | PLN-GW-001 | `bash scripts/check-gateway-hardening.sh` | Infra | Done |
| T-GW-002 | Traefik dashboard router에 `gateway-standard-chain@file` 적용 | impl | 01-gateway/spec.md / Gateway | PLN-GW-002 | `bash scripts/check-gateway-hardening.sh` | Infra | Done |
| T-GW-003 | Nginx compose를 `template-infra-readonly-low` + 필수 tmpfs + `/ping` healthcheck로 전환 | impl | 01-gateway/spec.md / Gateway | PLN-GW-003 | `bash scripts/check-gateway-hardening.sh` | Infra | Done |
| T-GW-004 | Nginx config에 timeout/failover/cache/server_tokens 하드닝 반영 | impl | 01-gateway/spec.md / Gateway | PLN-GW-004 | `bash scripts/check-gateway-hardening.sh` | Infra | Done |
| T-GW-005 | `scripts/check-gateway-hardening.sh` 추가 및 문서화 | ops | 01-gateway/spec.md / Verification | PLN-GW-005 | `bash scripts/check-gateway-hardening.sh` | DevOps | Done |
| T-GW-006 | CI workflow에 `gateway-hardening` job 추가 | ops | 01-gateway/spec.md / CI | PLN-GW-006 | PR CI run | DevOps | Done |
| T-GW-007 | Plan/Task/Operation/Runbook/Guide 문서 및 README 인덱스 동기화 | doc | 01-gateway/spec.md / Docs | PLN-GW-007 | `bash scripts/check-doc-traceability.sh` | Docs | Done |
| T-GW-008 | Compose/기본 검증 커맨드 실행 결과 기록 | test | 01-gateway/spec.md / Validation | PLN-GW-001~007 | `docker compose config`, baseline checks | Infra | Done |

## Suggested Types

- `impl`
- `test`
- `doc`
- `ops`

## Phase View (Optional)

### Phase 1

- [x] T-GW-001
- [x] T-GW-002
- [x] T-GW-003
- [x] T-GW-004

### Phase 2

- [x] T-GW-005
- [x] T-GW-006
- [x] T-GW-007
- [x] T-GW-008

## Verification Summary

- **Test Commands**:
  - `bash scripts/check-gateway-hardening.sh`
  - `bash scripts/check-template-security-baseline.sh`
  - `bash scripts/check-doc-traceability.sh`
  - `docker compose config`
  - `docker compose -f infra/01-gateway/traefik/docker-compose.yml config`
  - `docker compose -f infra/01-gateway/nginx/docker-compose.yml config`
- **Eval Commands**: N/A
- **Logs / Evidence Location**: PR CI logs + local command outputs (`gateway-hardening/template-security/doc-traceability/config` pass, `nginx -t`는 `service \"nginx\" is not running`로 미수행)
