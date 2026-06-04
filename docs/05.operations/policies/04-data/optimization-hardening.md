---
status: active
---
<!-- Target: docs/05.operations/policies/04-data/optimization-hardening.md -->

# 04-Data Optimization Hardening Operations Policy

## Overview (KR)

이 문서는 `04-data` 계층의 최적화/하드닝 운영 정책을 정의한다. 즉시 적용 가능한 구성 정합성/healthcheck/검증 자동화를 Required 통제로 고정하고, 카탈로그 확장 항목은 승인 기반 전환 정책으로 관리한다.

## Policy Scope

- `infra/04-data/operational/supabase/docker-compose.yml`
- `infra/04-data/cache-and-kv/valkey-cluster/docker-compose.yml`
- `infra/04-data/lake-and-object/seaweedfs/docker-compose.yml`
- `infra/04-data/analytics/ksql/docker-compose.yml`
- `scripts/hardening/check-all-hardening.sh 04-data`

- **Systems**: 04-data 하위 전 서비스(analytics/cache-and-kv/lake-and-object/nosql/operational/relational/specialized)
- **Agents**: Infra/DevOps/Data-Ops agents
- **Environments**: Local, Dev, Stage, Production-like

## Controls

- **Required**:
  - 04-data 구성 변경은 `infrastructure-hardening` CI 게이트를 통과해야 한다.
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

- `bash scripts/hardening/check-all-hardening.sh 04-data`
- `bash scripts/validation/check-template-security-baseline.sh`
- `bash scripts/validation/check-doc-traceability.sh`
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
- **Eval / Guardrail Threshold**: `infrastructure-hardening` + 공통 기준선 통과 필수
- **Log / Trace Retention**: `06-observability` 정책 준수
- **Safety Incident Thresholds**: 데이터 손상 의심, 장기 healthcheck fail, 복구 불가 상태 발생 시 즉시 runbook 전환

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/04-data/optimization-hardening.md)
- [Recovery runbook](../../runbooks/04-data/optimization-hardening.md)
