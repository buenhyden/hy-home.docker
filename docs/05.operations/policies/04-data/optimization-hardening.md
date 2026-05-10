# 04-Data Optimization Hardening Operations Policy

## Overview (KR)

이 문서는 `04-data` 계층의 최적화/하드닝 운영 정책을 정의한다. 즉시 적용 가능한 구성 정합성/healthcheck/검증 자동화를 Required 통제로 고정하고, 카탈로그 확장 항목은 승인 기반 전환 정책으로 관리한다.

## Policy Scope

- `infra/04-data/operational/supabase/docker-compose.yml`
- `infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml`
- `infra/04-data/lake-and-object/seaweedfs/docker-compose.yml`
- `infra/04-data/analytics/ksql/docker-compose.yml`
- `scripts/check-data-hardening.sh`

## Applies To

- **Systems**: 04-data 하위 전 서비스(analytics/cache-and-kv/lake-and-object/nosql/operational/relational/specialized)
- **Agents**: Infra/DevOps/Data-Ops agents
- **Environments**: Local, Dev, Stage, Production-like

## Controls

- **Required**:
  - 04-data 구성 변경은 `data-hardening` CI 게이트를 통과해야 한다.
  - `supabase` 핵심 서비스 healthcheck 계약을 유지해야 한다.
  - `valkey-cluster-exporter` 시크릿 경로는 `/run/secrets/service_valkey_password`를 사용해야 한다.
  - `seaweedfs` expose 정의는 유효한 포트 토큰만 허용한다.
  - `ksql` tier 라벨은 `hy-home.tier: data`를 유지해야 한다.
- **Allowed**:
  - 카탈로그 기반 확장 항목을 서비스별 단계 계획으로 추진
  - liveness 기반 healthcheck에서 readiness 기반 healthcheck로 점진적 고도화
- **Disallowed**:
  - 시크릿 경로 임의 변경 및 하드코딩
  - 무검증 compose 변경 배포
  - 카탈로그/운영정책 미연계 확장 실행

## Exceptions

- 실험 환경에서 일시적 점검을 위해 일부 서비스 healthcheck 완화는 허용 가능
- 단, 운영 승격 전 표준 healthcheck 계약으로 반드시 복구해야 한다.

## Verification

- `bash scripts/check-data-hardening.sh`
- `bash scripts/check-template-security-baseline.sh`
- `bash scripts/check-doc-traceability.sh`
- `docker compose -f infra/04-data/operational/supabase/docker-compose.yml config`

## Review Cadence

- 월 1회 정기 검토
- 데이터 서비스 신규 추가/버전 대규모 변경 시 수시 검토

## Catalog Expansion Approval Gates

- **Analytics 확장 승인 조건**:
  - retention/lifecycle 정책 문서화
  - schema compatibility 및 복구 시간 목표(RTO) 검증
- **Stateful DB 확장 승인 조건**:
  - failover/PITR/backup drill 증적 확보
  - SLA/SLO와 경보 기준 합의
- **Storage 확장 승인 조건**:
  - lifecycle/versioning/encryption 정책 명시
  - 용량 계획과 복구 절차 검증

## AI Agent Policy Section (If Applicable)

- **Model / Prompt Change Process**: N/A
- **Eval / Guardrail Threshold**: `data-hardening` + 공통 기준선 통과 필수
- **Log / Trace Retention**: `06-observability` 정책 준수
- **Safety Incident Thresholds**: 데이터 손상 의심, 장기 healthcheck fail, 복구 불가 상태 발생 시 즉시 runbook 전환

## Related Documents

- **PRD**: [../../01.requirements/2026-03-28-04-data-optimization-hardening.md](../../../01.requirements/2026-03-28-04-data-optimization-hardening.md)
- **ARD**: [../../02.architecture/requirements/0019-data-optimization-hardening-architecture.md](../../../02.architecture/requirements/0019-data-optimization-hardening-architecture.md)
- **ADR**: [../../02.architecture/decisions/0019-04-data-hardening-and-ha-expansion-strategy.md](../../../02.architecture/decisions/0019-04-data-hardening-and-ha-expansion-strategy.md)
- **Spec**: [../../03.specs/04-data/spec.md](../../../03.specs/04-data/spec.md)
- **Plan**: [../../04.execution/plans/2026-03-28-04-data-optimization-hardening-plan.md](../../../04.execution/plans/2026-03-28-04-data-optimization-hardening-plan.md)
- **Tasks**: [../../04.execution/tasks/2026-03-28-04-data-optimization-hardening-tasks.md](../../../04.execution/tasks/2026-03-28-04-data-optimization-hardening-tasks.md)
- **Usage**: [../../05.operations/04-data/optimization-hardening.md](./optimization-hardening.md)
- **Procedure**: [../../05.operations/04-data/optimization-hardening.md](./optimization-hardening.md)
- **Catalog**: [../12-infra-service-optimization-catalog.md](../12-infra-service-optimization-catalog.md)

## Usage

> Migrated from `docs/05.operations/04-data/optimization-hardening.md` during the 2026-05-10 operations taxonomy consolidation.

### 04-Data Optimization Hardening Usage

#### Overview (KR)

이 문서는 `04-data` 계층의 즉시 하드닝 항목을 운영자/개발자가 재현 가능하게 적용하기 위한 가이드다. `supabase` healthcheck 보강, `valkey` 시크릿 경로 정합화, `seaweedfs` compose 정합화, `ksql` 라벨 정규화 절차를 제공한다.

#### Usage Type

`system-guide | how-to`

#### Target Audience

- Data Platform Operator
- DevOps Engineer
- Service Developer

#### Purpose

- 04-data 구성 회귀를 예방하기 위한 기본 하드닝 절차를 표준화한다.
- 카탈로그 확장 전에 필요한 최소 안정성 계약을 확보한다.

#### Prerequisites

- Docker / Docker Compose 실행 환경
- `infra/04-data` 디렉터리 쓰기 권한
- `scripts/` 검증 스크립트 실행 권한

#### Step-by-step Instructions

1. 변경 전 구성 점검
   - `docker compose -f infra/04-data/operational/supabase/docker-compose.yml config`
   - `docker compose -f infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml config`
   - `docker compose -f infra/04-data/lake-and-object/seaweedfs/docker-compose.yml config`
   - `docker compose -f infra/04-data/analytics/ksql/docker-compose.yml config`
2. Supabase healthcheck 계약 적용
   - 핵심 서비스(`studio`, `kong`, `auth`, `rest`, `realtime`, `storage`, `analytics`, `db`, `vector`, `supavisor`)에 healthcheck가 있는지 확인한다.
3. Valkey exporter 시크릿 경로 확인
   - `/run/secrets/service_valkey_password` 사용 여부 점검
4. SeaweedFS expose 정합성 확인
   - `]`가 포함된 malformed 포트 토큰이 없는지 점검
5. ksql tier 라벨 확인
   - `hy-home.tier: data` 적용 여부 확인
6. 하드닝/추적성 검증 실행
   - `bash scripts/check-data-hardening.sh`
   - `bash scripts/check-template-security-baseline.sh`
   - `bash scripts/check-doc-traceability.sh`

#### Common Pitfalls

- `service_healthy` 의존 서비스를 정의하면서 healthcheck를 누락하는 실수
- exporter 시크릿 파일 경로를 서비스 계약과 다르게 유지하는 실수
- compose 오타(토큰/브래킷)로 정적 검증 실패를 유발하는 실수

#### Related Documents

- **PRD**: [../../01.requirements/2026-03-28-04-data-optimization-hardening.md](../../../01.requirements/2026-03-28-04-data-optimization-hardening.md)
- **Spec**: [../../03.specs/04-data/spec.md](../../../03.specs/04-data/spec.md)
- **Plan**: [../../04.execution/plans/2026-03-28-04-data-optimization-hardening-plan.md](../../../04.execution/plans/2026-03-28-04-data-optimization-hardening-plan.md)
- **Tasks**: [../../04.execution/tasks/2026-03-28-04-data-optimization-hardening-tasks.md](../../../04.execution/tasks/2026-03-28-04-data-optimization-hardening-tasks.md)
- **Operation**: [../../05.operations/04-data/optimization-hardening.md](./optimization-hardening.md)
- **Procedure**: [../../05.operations/04-data/optimization-hardening.md](./optimization-hardening.md)
- **Catalog**: [../../05.operations/12-infra-service-optimization-catalog.md](../12-infra-service-optimization-catalog.md)

## Procedure

> Migrated from `docs/05.operations/04-data/optimization-hardening.md` during the 2026-05-10 operations taxonomy consolidation.

### 04-Data Optimization Hardening Procedure

: 04-data Configuration Recovery & Baseline Restoration

#### Overview (KR)

이 런북은 04-data 하드닝 항목에서 발생 가능한 회귀를 즉시 복구하기 위한 실행 절차를 제공한다. `supabase` healthcheck 이상, `valkey` exporter 인증 실패, `seaweedfs` compose 파싱 오류, `ksql` 라벨 회귀를 중심으로 점검/복구 절차를 정의한다.

#### Purpose

- 04-data 하드닝 회귀를 신속하게 감지하고 복구한다.
- 배포 전후 정적 검증/증적 수집 절차를 표준화한다.

#### Canonical References

- [Spec](../../../03.specs/04-data/spec.md)
- [Operations Policy](./optimization-hardening.md)
- [Plan](../../../04.execution/plans/2026-03-28-04-data-optimization-hardening-plan.md)
- [Tasks](../../../04.execution/tasks/2026-03-28-04-data-optimization-hardening-tasks.md)

#### When to Use

- `data-hardening` CI가 실패할 때
- `supabase` 서비스들이 `service_healthy` 대기 상태에서 시작되지 않을 때
- `valkey-cluster-exporter`가 인증 실패로 기동되지 않을 때
- `seaweedfs` compose 파싱/기동 오류가 발생할 때

#### Procedure or Checklist

##### Checklist

- [ ] 실패한 검증 항목과 대상 파일 식별
- [ ] 최근 변경 커밋/파일 범위 확인
- [ ] 영향 범위(analytics/cache/storage/operational) 식별

##### Procedure

1. 정적 구성 점검
   - `docker compose -f infra/04-data/operational/supabase/docker-compose.yml config`
   - `docker compose -f infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml config`
   - `docker compose -f infra/04-data/lake-and-object/seaweedfs/docker-compose.yml config`
   - `docker compose -f infra/04-data/analytics/ksql/docker-compose.yml config`
2. 하드닝 기준 점검
   - `bash scripts/check-data-hardening.sh`
3. 증상별 복구
   - Supabase healthcheck 누락/오류:
     - 대상 서비스 블록에 healthcheck 복원
     - `db`는 `pg_isready` 계약 유지
   - Valkey exporter 인증 실패:
     - `/run/secrets/service_valkey_password` 경로로 복원
   - SeaweedFS compose 파싱 오류:
     - expose 포트 토큰에서 오타(`]`) 제거
   - ksql 라벨 회귀:
     - `hy-home.tier: data`로 복원
4. 재검증
   - `bash scripts/check-data-hardening.sh`
   - `bash scripts/check-template-security-baseline.sh`
   - `bash scripts/check-doc-traceability.sh`

#### Verification Steps

- [ ] 4개 compose `config` 검증 통과
- [ ] `data-hardening` 실패 0건
- [ ] 관련 문서 링크/인덱스가 최신 상태

#### Observability and Evidence Sources

- **Signals**: CI `data-hardening` job 상태, compose config 결과, 컨테이너 health 상태
- **Evidence to Capture**:
  - 실패/복구 전후 `check-data-hardening.sh` 출력
  - `docker inspect --format '{{json .State.Health}}'` 결과
  - 수정 파일 diff

#### Safe Rollback or Recovery Procedure

- [ ] 롤백 대상 파일
  - `infra/04-data/operational/supabase/docker-compose.yml`
  - `infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml`
  - `infra/04-data/lake-and-object/seaweedfs/docker-compose.yml`
  - `infra/04-data/analytics/ksql/docker-compose.yml`
  - `scripts/check-data-hardening.sh`
  - `.github/workflows/ci-quality.yml`
- [ ] 롤백 후 정적 검증 재실행
- [ ] 운영 정책/가이드/태스크 문서 동기화 재확인

#### Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: `data-hardening` 게이트 임시 비활성은 승인 후만 수행
- **Eval Re-run**: `check-data-hardening`, `check-template-security-baseline`, `check-doc-traceability`
- **Trace Capture**: CI logs + compose config output

#### Related Operational Documents

- **Usage**: [../../05.operations/04-data/optimization-hardening.md](./optimization-hardening.md)
- **Operation**: [../../05.operations/04-data/optimization-hardening.md](./optimization-hardening.md)
- **Catalog**: [../../05.operations/12-infra-service-optimization-catalog.md](../12-infra-service-optimization-catalog.md)
