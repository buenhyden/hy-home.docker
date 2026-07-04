---
status: active
---
<!-- Target: docs/05.operations/policies/06-observability/pushgateway.md -->

# Pushgateway Operations Policy

## Overview

이 문서는 `06-observability` 계층의 Pushgateway 운영 정책을 정의한다. Pushgateway는 Prometheus pull 모델이 직접 적용되기 어려운 단기 실행 작업과 배치 작업의 메트릭을 임시로 받는 버퍼이며, 장기 저장소나 일반 서비스 메트릭 프록시가 아니다.

## Policy Scope

이 정책은 `infra/06-observability/docker-compose.yml`의 `pushgateway` 서비스, 해당 서비스에 메트릭을 push하는 작업, Pushgateway의 stale metric cleanup, 그리고 Prometheus scrape 연동 계약에 적용된다.

- **Systems**: `pushgateway` service/container, image `prom/pushgateway:v1.11.3`, port `9091`, `/-/ready` healthcheck, `pushgateway.${DEFAULT_URL}` protected Traefik route, Prometheus scrape integration contract
- **Agents**: Operators, CI/CD jobs, batch scripts, AI agents changing observability documentation
- **Environments**: `obs` Docker Compose profile in the local/homelab observability tier

## Controls

- **Required**:
  - Compose 서비스는 `profiles: [obs]`, `template-infra-readonly-low`, image `prom/pushgateway:v1.11.3`, expose `${PUSHGATEWAY_PORT:-9091}`, `/-/ready` healthcheck, and protected Traefik middleware chain을 유지해야 한다.
  - Pushgateway는 Prometheus가 직접 scrape할 수 없는 단기 실행 작업, 배치 작업, CI/CD 작업에만 사용한다.
  - 모든 push path에는 안정적인 `job` label을 포함해야 한다.
  - `instance` label은 안정적인 worker, node, or bounded execution identity를 구분할 때만 사용한다. 고유 request ID, user ID, unbounded build ID는 cleanup evidence가 없는 한 label로 쓰지 않는다.
  - Push한 metric group은 작업 lifecycle 종료 후 삭제하거나 다음 실행에서 명확히 overwrite해야 한다. 1시간 이상 갱신되지 않은 `push_time_seconds` group은 stale candidate로 검토한다.
  - Prometheus dashboard, alert, or SLO가 Pushgateway metric에 의존하려면 `prometheus.yml`에 `job_name: "pushgateway"`와 `pushgateway:9091` target 및 `honor_labels: true` 또는 동등한 label 보존 정책이 있어야 한다. 이 문서 정리 시점의 repository scan에서는 해당 scrape block이 확인되지 않았으므로, 런타임 설정 변경 없이 이를 구현된 상태로 단정하지 않는다.
  - metric payload와 label에는 secret, token, credential, personal data를 포함하지 않는다.
- **Allowed**:
  - 직접 scrape가 어려운 network boundary 안쪽의 short-lived job metric push.
  - 수동 디버깅 목적의 임시 push. 단, 작업 종료 후 stale group cleanup evidence를 남긴다.
  - 별도 승인된 prototype에서 제한된 label set으로 짧게 검증하는 행위.
- **Disallowed**:
  - 장기 실행 서비스의 일반 metrics collection을 Pushgateway로 우회하는 행위.
  - high-cardinality label, unbounded tenant/user/request/build identifiers, secret-bearing label or metric payload.
  - 현재 Compose에 선언되지 않은 persistence option, route relaxation, image change, or scrape-job behavior를 문서에서 구현 완료로 표현하는 행위.

## Exceptions

예외는 운영 owner가 승인해야 하며, 승인 사유, label cardinality boundary, cleanup 절차, rollback 기준, 관련 task or incident evidence를 남겨야 한다. Emergency cleanup은 runbook 절차로 수행하고 사후에 evidence를 보강한다.

## Verification

- **Compose Check**: `rg -n 'service: template-infra-readonly-low|image: prom/pushgateway:v1.11.3|PUSHGATEWAY_PORT|/-/ready|pushgateway.middlewares' infra/06-observability/docker-compose.yml`
- **Scrape Contract Check**: `rg -n 'job_name: "pushgateway"|pushgateway:9091|honor_labels' infra/06-observability/prometheus/config/prometheus.yml`. Match가 없으면 Prometheus integration을 gap으로 기록하고 runtime 설정 변경 task를 별도로 만든다.
- **Stale Metric Check**: scrape job이 존재하는 환경에서는 `push_time_seconds` 기준으로 1시간 이상 갱신되지 않은 `job` group을 식별한다.
- **API Audit**: Pushgateway API or UI에서 비정상적으로 큰 metric group, high-cardinality labels, cleanup되지 않은 debug groups를 확인한다.
- **Documentation Check**: guide and runbook은 사용법과 복구 절차만 설명하고, policy control은 이 문서에 유지한다.

## Review Cadence

Quarterly, and on material change to image version, Docker profile, route middleware, healthcheck, persistence behavior, Prometheus scrape job, label policy, or cleanup automation.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/06-observability/pushgateway.md)
- [Recovery runbook](../../runbooks/06-observability/pushgateway.md)
