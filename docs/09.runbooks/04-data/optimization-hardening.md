# 04-Data Optimization Hardening Runbook

: 04-data Configuration Recovery & Baseline Restoration

## Overview (KR)

이 런북은 04-data 하드닝 항목에서 발생 가능한 회귀를 즉시 복구하기 위한 실행 절차를 제공한다. `supabase` healthcheck 이상, `valkey` exporter 인증 실패, `seaweedfs` compose 파싱 오류, `ksql` 라벨 회귀를 중심으로 점검/복구 절차를 정의한다.

## Purpose

- 04-data 하드닝 회귀를 신속하게 감지하고 복구한다.
- 배포 전후 정적 검증/증적 수집 절차를 표준화한다.

## Canonical References

- [Spec](../../04.specs/04-data/spec.md)
- [Operations Policy](../../08.operations/04-data/optimization-hardening.md)
- [Plan](../../05.plans/2026-03-28-04-data-optimization-hardening-plan.md)
- [Tasks](../../06.tasks/2026-03-28-04-data-optimization-hardening-tasks.md)

## When to Use

- `data-hardening` CI가 실패할 때
- `supabase` 서비스들이 `service_healthy` 대기 상태에서 시작되지 않을 때
- `valkey-cluster-exporter`가 인증 실패로 기동되지 않을 때
- `seaweedfs` compose 파싱/기동 오류가 발생할 때

## Procedure or Checklist

### Checklist

- [ ] 실패한 검증 항목과 대상 파일 식별
- [ ] 최근 변경 커밋/파일 범위 확인
- [ ] 영향 범위(analytics/cache/storage/operational) 식별

### Procedure

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

## Verification Steps

- [ ] 4개 compose `config` 검증 통과
- [ ] `data-hardening` 실패 0건
- [ ] 관련 문서 링크/인덱스가 최신 상태

## Observability and Evidence Sources

- **Signals**: CI `data-hardening` job 상태, compose config 결과, 컨테이너 health 상태
- **Evidence to Capture**:
  - 실패/복구 전후 `check-data-hardening.sh` 출력
  - `docker inspect --format '{{json .State.Health}}'` 결과
  - 수정 파일 diff

## Safe Rollback or Recovery Procedure

- [ ] 롤백 대상 파일
  - `infra/04-data/operational/supabase/docker-compose.yml`
  - `infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml`
  - `infra/04-data/lake-and-object/seaweedfs/docker-compose.yml`
  - `infra/04-data/analytics/ksql/docker-compose.yml`
  - `scripts/check-data-hardening.sh`
  - `.github/workflows/ci-quality.yml`
- [ ] 롤백 후 정적 검증 재실행
- [ ] 운영 정책/가이드/태스크 문서 동기화 재확인

## Agent Operations (If Applicable)

- **Prompt Rollback**: N/A
- **Model Fallback**: N/A
- **Tool Disable / Revoke**: `data-hardening` 게이트 임시 비활성은 승인 후만 수행
- **Eval Re-run**: `check-data-hardening`, `check-template-security-baseline`, `check-doc-traceability`
- **Trace Capture**: CI logs + compose config output

## Related Operational Documents

- **Guide**: [../../07.guides/04-data/optimization-hardening.md](../../07.guides/04-data/optimization-hardening.md)
- **Operation**: [../../08.operations/04-data/optimization-hardening.md](../../08.operations/04-data/optimization-hardening.md)
- **Catalog**: [../../08.operations/12-infra-service-optimization-catalog.md](../../08.operations/12-infra-service-optimization-catalog.md)
