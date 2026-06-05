---
status: active
---
<!-- Target: docs/05.operations/guides/04-data/optimization/optimization-hardening.md -->

# 04-Data Optimization Hardening Usage Guide

## Usage

### Overview

이 문서는 `04-data` 계층의 즉시 하드닝 항목을 운영자/개발자가 재현 가능하게 적용하기 위한 가이드다. `supabase` healthcheck 보강, `valkey` 시크릿 경로 정합화, `seaweedfs` compose 정합화, `ksql` 라벨 정규화 절차를 제공한다.

### Usage Type

`system-guide | how-to`

### Target Audience

- Data Platform Operator
- DevOps Engineer
- Service Developer

### Purpose

- 04-data 구성 회귀를 예방하기 위한 기본 하드닝 절차를 표준화한다.
- 카탈로그 확장 전에 필요한 최소 안정성 계약을 확보한다.

### Prerequisites

- Docker / Docker Compose 실행 환경
- `infra/04-data` 디렉터리 쓰기 권한
- `scripts/` 검증 스크립트 실행 권한

### Step-by-step Instructions

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
   - `bash scripts/hardening/check-all-hardening.sh 04-data`
   - `bash scripts/validation/check-template-security-baseline.sh`
   - `bash scripts/validation/check-doc-traceability.sh`

### Common Pitfalls

- `service_healthy` 의존 서비스를 정의하면서 healthcheck를 누락하는 실수
- exporter 시크릿 파일 경로를 서비스 계약과 다르게 유지하는 실수
- compose 오타(토큰/브래킷)로 정적 검증 실패를 유발하는 실수

## Common Checks

- `docker compose -f infra/04-data/operational/supabase/docker-compose.yml config`
- `docker compose -f infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml config`
- `docker compose -f infra/04-data/lake-and-object/seaweedfs/docker-compose.yml config`
- `docker compose -f infra/04-data/analytics/ksql/docker-compose.yml config`
- `bash scripts/hardening/check-all-hardening.sh 04-data`
- `bash scripts/validation/check-template-security-baseline.sh`
- `bash scripts/validation/check-doc-traceability.sh`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../../runbooks/04-data/optimization/optimization-hardening.md)을 따른다.

## Related Documents

- [Operations index](../../../README.md)
- [Operations policy](../../../policies/04-data/optimization/optimization-hardening.md)
- [Recovery runbook](../../../runbooks/04-data/optimization/optimization-hardening.md)
