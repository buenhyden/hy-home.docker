# Task: 05-Messaging Optimization Hardening

## Overview (KR)

이 문서는 `05-messaging` 최적화/하드닝 구현 태스크를 추적한다. compose 하드닝, CI 기준선 자동화, 문서 추적성 동기화를 작업 단위로 관리한다.

## Inputs

- **Parent Spec**: [../04.specs/05-messaging/spec.md](../04.specs/05-messaging/spec.md)
- **Parent Plan**: [../05.plans/2026-03-28-05-messaging-optimization-hardening-plan.md](../05.plans/2026-03-28-05-messaging-optimization-hardening-plan.md)

## Working Rules

- 메시징 compose 변경은 정적 검증과 하드닝 스크립트 증빙을 남긴다.
- 라우팅 정책 변경은 게이트웨이/SSO 영향 범위를 명시한다.
- 문서 변경은 PRD~Runbook 상호 링크 및 README 인덱스를 함께 갱신한다.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-MSG-001 | Kafka UI 이미지 태그 고정 | impl | 05-messaging/spec.md / Contracts | PLN-MSG-001 | `rg 'kafka-ui:main' infra/05-messaging/kafka` 미검출 | DevOps | Done |
| T-MSG-002 | Kafka 관리 라우터 gateway chain 적용 | impl | 05-messaging/spec.md / Core Design | PLN-MSG-001 | 라벨 문자열 확인 | DevOps | Done |
| T-MSG-003 | Kafka dev compose 볼륨 경로 정합성 보강 | impl | 05-messaging/spec.md / Contracts | PLN-MSG-002 | dev compose config 통과 | DevOps | Done |
| T-MSG-004 | Kafka dev 라우터 chain+SSO 적용 | impl | 05-messaging/spec.md / Core Design | PLN-MSG-002 | 라벨 문자열 확인 | DevOps | Done |
| T-MSG-005 | RabbitMQ 관리 라우터 chain+SSO 적용 | impl | 05-messaging/spec.md / Contracts | PLN-MSG-003 | 라벨 문자열 확인 | DevOps | Done |
| T-MSG-006 | 메시징 하드닝 검증 스크립트 추가 | ops | 05-messaging/spec.md / Governance | PLN-MSG-004 | `bash scripts/check-messaging-hardening.sh` | DevOps | Done |
| T-MSG-007 | CI `messaging-hardening` job 추가 | ops | 05-messaging/spec.md / Governance | PLN-MSG-005 | workflow 정의 확인 | DevOps | Done |
| T-MSG-008 | scripts README 인덱스 갱신 | doc | 05-messaging/spec.md / Related Docs | PLN-MSG-006 | README 항목/예시 확인 | Docs | Done |
| T-MSG-009 | PRD/ARD/ADR/Plan/Task/Guide/Ops/Runbook 문서 반영 | doc | 05-messaging/spec.md / Related Docs | PLN-MSG-007 | 문서 링크/README 동기화 확인 | Docs | Done |
| T-MSG-010 | 정적 검증 실행 및 결과 기록 | test | 05-messaging/spec.md / Verification | PLN-MSG-001~007 | compose + hardening + traceability 점검 | DevOps | Done |
| T-MSG-011 | runtime/장애복구 리허설 증적 수집 | test | 05-messaging/spec.md / Verification | PLN-MSG-001~007 | 헬스/복구 절차 로그 | DevOps | Planned |

## Suggested Types

- `impl`
- `test`
- `doc`
- `ops`

## Phase View (Optional)

### Phase 1

- [x] T-MSG-001
- [x] T-MSG-002
- [x] T-MSG-003
- [x] T-MSG-004
- [x] T-MSG-005
- [x] T-MSG-006
- [x] T-MSG-007

### Phase 2

- [x] T-MSG-008
- [x] T-MSG-009
- [x] T-MSG-010
- [ ] T-MSG-011

## Verification Summary

- **Test Commands**:
  - `docker compose -f infra/05-messaging/kafka/docker-compose.yml config`
  - `docker compose -f infra/05-messaging/kafka/docker-compose.dev.yml config`
  - `docker compose -f infra/05-messaging/rabbitmq/docker-compose.yml config`
  - `bash scripts/check-messaging-hardening.sh`
  - `bash scripts/check-template-security-baseline.sh`
  - `bash scripts/check-doc-traceability.sh`
- **Eval Commands**: N/A
- **Logs / Evidence Location**: 로컬 검증 로그 + CI `messaging-hardening` job

## Related Documents

- **PRD**: [../01.prd/2026-03-28-05-messaging-optimization-hardening.md](../01.prd/2026-03-28-05-messaging-optimization-hardening.md)
- **ARD**: [../02.ard/0020-messaging-optimization-hardening-architecture.md](../02.ard/0020-messaging-optimization-hardening-architecture.md)
- **ADR**: [../03.adr/0020-messaging-hardening-and-ha-expansion-strategy.md](../03.adr/0020-messaging-hardening-and-ha-expansion-strategy.md)
- **Plan**: [../05.plans/2026-03-28-05-messaging-optimization-hardening-plan.md](../05.plans/2026-03-28-05-messaging-optimization-hardening-plan.md)
- **Guide**: [../07.guides/05-messaging/optimization-hardening.md](../07.guides/05-messaging/optimization-hardening.md)
- **Operation**: [../08.operations/05-messaging/optimization-hardening.md](../08.operations/05-messaging/optimization-hardening.md)
- **Runbook**: [../09.runbooks/05-messaging/optimization-hardening.md](../09.runbooks/05-messaging/optimization-hardening.md)
