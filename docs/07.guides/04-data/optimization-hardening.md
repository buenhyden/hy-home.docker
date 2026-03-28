# 04-Data Optimization Hardening Guide

## Overview (KR)

이 문서는 `04-data` 계층의 즉시 하드닝 항목을 운영자/개발자가 재현 가능하게 적용하기 위한 가이드다. `supabase` healthcheck 보강, `valkey` 시크릿 경로 정합화, `seaweedfs` compose 정합화, `ksql` 라벨 정규화 절차를 제공한다.

## Guide Type

`system-guide | how-to`

## Target Audience

- Data Platform Operator
- DevOps Engineer
- Service Developer

## Purpose

- 04-data 구성 회귀를 예방하기 위한 기본 하드닝 절차를 표준화한다.
- 카탈로그 확장 전에 필요한 최소 안정성 계약을 확보한다.

## Prerequisites

- Docker / Docker Compose 실행 환경
- `infra/04-data` 디렉터리 쓰기 권한
- `scripts/` 검증 스크립트 실행 권한

## Step-by-step Instructions

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

## Common Pitfalls

- `service_healthy` 의존 서비스를 정의하면서 healthcheck를 누락하는 실수
- exporter 시크릿 파일 경로를 서비스 계약과 다르게 유지하는 실수
- compose 오타(토큰/브래킷)로 정적 검증 실패를 유발하는 실수

## Related Documents

- **PRD**: [../../01.prd/2026-03-28-04-data-optimization-hardening.md](../../01.prd/2026-03-28-04-data-optimization-hardening.md)
- **Spec**: [../../04.specs/04-data/spec.md](../../04.specs/04-data/spec.md)
- **Plan**: [../../05.plans/2026-03-28-04-data-optimization-hardening-plan.md](../../05.plans/2026-03-28-04-data-optimization-hardening-plan.md)
- **Tasks**: [../../06.tasks/2026-03-28-04-data-optimization-hardening-tasks.md](../../06.tasks/2026-03-28-04-data-optimization-hardening-tasks.md)
- **Operation**: [../../08.operations/04-data/optimization-hardening.md](../../08.operations/04-data/optimization-hardening.md)
- **Runbook**: [../../09.runbooks/04-data/optimization-hardening.md](../../09.runbooks/04-data/optimization-hardening.md)
- **Catalog**: [../../08.operations/12-infra-service-optimization-catalog.md](../../08.operations/12-infra-service-optimization-catalog.md)
