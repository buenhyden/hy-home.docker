# 04-Data Optimization Hardening Specification

## Overview (KR)

이 문서는 `infra/04-data` 계층의 최적화/하드닝 구현 계약을 정의한다. 즉시 적용 가능한 compose 정합성, healthcheck, 시크릿 경로 계약, 검증 자동화를 우선 반영하고, 카탈로그 기반 확장 항목은 운영 정책/런북과 연결한다.

## Strategic Boundaries & Non-goals

- 본 Spec은 04-data 인프라 구성 하드닝과 검증 계약을 소유한다.
- 엔진별 대규모 토폴로지 확장(예: 멀티클러스터 전환)은 후속 단계로 이관한다.

## Related Inputs

- **PRD**: [../../01.prd/2026-03-28-04-data-optimization-hardening.md](../../01.prd/2026-03-28-04-data-optimization-hardening.md)
- **ARD**: [../../02.ard/0019-data-optimization-hardening-architecture.md](../../02.ard/0019-data-optimization-hardening-architecture.md)
- **Related ADRs**:
  - [../../03.adr/0004-postgresql-ha-patroni.md](../../03.adr/0004-postgresql-ha-patroni.md)
  - [../../03.adr/0019-04-data-hardening-and-ha-expansion-strategy.md](../../03.adr/0019-04-data-hardening-and-ha-expansion-strategy.md)

## Contracts

- **Config Contract**:
  - 04-data compose는 `infra/common-optimizations.yml` 템플릿 상속을 유지한다.
  - `supabase` 핵심 서비스는 healthcheck를 필수로 제공한다.
  - `ksql` tier 라벨은 `hy-home.tier: data`를 사용한다.
- **Data / Interface Contract**:
  - `valkey-cluster-exporter` 시크릿 파일 경로는 `/run/secrets/service_valkey_password`를 사용한다.
  - `seaweedfs` expose 정의는 유효한 포트 토큰만 허용한다.
- **Governance Contract**:
  - `scripts/check-data-hardening.sh`를 CI `data-hardening` job으로 강제한다.
  - `scripts/check-template-security-baseline.sh`, `scripts/check-doc-traceability.sh`와 함께 운영 게이트를 구성한다.

## Core Design

- **Component Boundary**:
  - 대상 범위: `infra/04-data/{analytics,cache-and-kv,lake-and-object,nosql,operational,relational,specialized}`
  - 즉시 하드닝 대상:
    - `operational/supabase`
    - `cache-and-kv/valkey-cluster`
    - `lake-and-object/seaweedfs`
    - `analytics/ksql`
- **Key Dependencies**:
  - `03-security` 시크릿 운영 정책
  - `01-gateway` 노출/라우팅 정책
  - `06-observability` 모니터링 정책
- **Tech Stack**:
  - Docker Compose
  - 공통 최적화 템플릿(`template-infra-*`, `template-stateful-*`)

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**:
  - `${DEFAULT_DATA_DIR}` 기반 서비스별 데이터 분리
- **Migration / Transition Plan**:
  - Phase 1: compose 정합성 및 healthcheck 계약 고정
  - Phase 2: 카탈로그 확장 항목(backup/retention/failover/reindex) 정책화
  - Phase 3: 승인 기반 서비스별 확장 실행

## Interfaces & Data Structures

### Core Interfaces

```typescript
interface DataHardeningContract {
  composePath: string;
  templateInherited: true;
  hasHealthcheck: boolean;
  secretsPathPolicy: 'service_valkey_password';
  malformedExposeForbidden: true;
}
```

## Catalog-aligned Expansion Targets

- Analytics: retention tiering, schema compatibility gate, ISM/rollover, batch window governance
- Cache & KV: failover drill, eviction policy split, exporter standardization
- Lake & Object: lifecycle/versioning/KMS policy, quorum/recovery automation
- NoSQL: compaction/repair, shard/replica balance, election/backup drill
- Operational: DB baseline + slow-query gate, supabase exposure/resource review
- Relational: failover SLA, vacuum tuning, PITR drill
- Specialized: graph/query guardrail, vector indexing/reindex policy

## Edge Cases & Error Handling

- `service_healthy` 의존인데 healthcheck 미구성 시 시작 순서 실패 위험
- 시크릿 파일 경로 불일치 시 exporter 인증 실패
- compose 토큰 오타(`]`)로 정적 검증 실패 또는 런타임 오류

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: `supabase` 스택의 의존 서비스 비정상 순환 재시작
- **Fallback**: healthcheck 계약 복원 후 `docker compose config` 및 runbook 절차로 재기동
- **Human Escalation**: Data Platform Operator + DevOps on-call 동시 호출

## Verification

```bash
docker compose -f infra/04-data/operational/supabase/docker-compose.yml config
docker compose -f infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml config
docker compose -f infra/04-data/lake-and-object/seaweedfs/docker-compose.yml config
docker compose -f infra/04-data/analytics/ksql/docker-compose.yml config
bash scripts/check-data-hardening.sh
bash scripts/check-template-security-baseline.sh
bash scripts/check-doc-traceability.sh
```

가능 환경에서 runtime 검증:

```bash
docker compose -f infra/04-data/operational/supabase/docker-compose.yml up -d
docker inspect --format '{{json .State.Health}}' supabase-analytics
docker inspect --format '{{json .State.Health}}' supabase-db
docker inspect --format '{{json .State.Health}}' supabase-pooler
```

## Success Criteria & Verification Plan

- **VAL-SPC-DATA-001**: `check-data-hardening` 실패 0건
- **VAL-SPC-DATA-002**: `supabase` 핵심 서비스 healthcheck 존재
- **VAL-SPC-DATA-003**: `valkey-cluster-exporter` 시크릿 경로 계약 정합화
- **VAL-SPC-DATA-004**: `seaweedfs` expose 토큰 오타 제거
- **VAL-SPC-DATA-005**: 04-data 문서 레이어 추적성 링크 동기화

## Related Documents

- **Plan**: [../../05.plans/2026-03-28-04-data-optimization-hardening-plan.md](../../05.plans/2026-03-28-04-data-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-04-data-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-04-data-optimization-hardening-tasks.md)
- **Guide**: [../../07.guides/04-data/optimization-hardening.md](../../07.guides/04-data/optimization-hardening.md)
- **Operations**: [../../08.operations/04-data/optimization-hardening.md](../../08.operations/04-data/optimization-hardening.md)
- **Runbook**: [../../09.runbooks/04-data/optimization-hardening.md](../../09.runbooks/04-data/optimization-hardening.md)
