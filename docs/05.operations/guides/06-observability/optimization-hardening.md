---
status: active
---
<!-- Target: docs/05.operations/guides/06-observability/optimization-hardening.md -->

# 06-Observability Optimization Hardening Usage Guide

## Usage

### Overview (KR)

이 문서는 `06-observability` 계층의 최적화/하드닝 항목을 운영자/개발자가 재현 가능하게 적용하기 위한 가이드다. gateway 체인+SSO 정렬, health 기반 의존성, 커스텀 이미지 하드닝, CI 검증 절차를 제공한다.

### Usage Type

`system-guide | how-to`

### Target Audience

- SRE / Platform Operator
- DevOps Engineer
- Observability Maintainer

### Purpose

- 관측성 관리 경로를 게이트웨이 표준 정책에 정렬한다.
- 초기 기동 안정성과 회귀 차단 능력을 강화한다.
- 카탈로그 기반 확장(샘플링/retention/pipeline module) 준비 상태를 확보한다.

### Prerequisites

- Docker / Docker Compose 실행 환경
- `infra/06-observability` 및 `scripts/` 수정 권한
- Traefik `gateway-standard-chain` 및 `sso-*` middleware 준비

### Step-by-step Instructions

1. 변경 전 정적 상태 점검
   - `docker compose -f infra/06-observability/docker-compose.yml config`
2. Gateway/SSO 경계 정렬
   - 공개 라우터(`prometheus`, `alloy`, `grafana`, `alertmanager`, `pushgateway`, `loki`, `tempo`, `pyroscope`)에 `gateway-standard-chain@file,sso-errors@file,sso-auth@file`를 적용한다.
3. 의존성/헬스 보강
   - Alloy/Grafana의 Loki/Tempo 의존성을 `service_healthy`로 설정한다.
   - cAdvisor healthcheck(`/healthz`)를 추가한다.
4. 커스텀 이미지 하드닝
   - Loki/Tempo Dockerfile에 non-root user(`10001`)를 강제한다.
   - entrypoint에서 MinIO secret 존재를 선검증한다.
5. 자동 검증 및 CI 반영
   - `bash scripts/hardening/check-all-hardening.sh 06-observability`
   - CI workflow에 `infrastructure-hardening` job 반영 여부 확인
6. 문서 추적성 동기화
   - PRD~Procedure optimization-hardening 문서 링크를 점검한다.

### Common Pitfalls

- 일부 라우터만 SSO 체인을 적용해 관리 경로 노출이 발생하는 실수
- `service_started` 의존성으로 부팅 race condition을 남기는 실수
- custom 이미지에 root 실행 경로를 재도입하는 실수
- 하드닝 스크립트/README 인덱스를 함께 갱신하지 않는 실수

## Common Checks

- `docker compose -f infra/06-observability/docker-compose.yml config`
- `bash scripts/hardening/check-all-hardening.sh 06-observability`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/06-observability/optimization-hardening.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/06-observability/optimization-hardening.md)
- [Recovery runbook](../../runbooks/06-observability/optimization-hardening.md)
