---
title: "Pushgateway Operations Policy"
version: "1.0.1"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "POL-0046"
parent_ids:
- "AD-0006"
created: "2026-05-17"
---

# Pushgateway Operations Policy

## Overview

### Overview

이 문서는 `06-observability` 계층의 Pushgateway 운영 정책을 정의한다. Pushgateway는 Prometheus pull 모델이 직접 적용되기 어려운 단기 실행 작업과 배치 작업의 메트릭을 임시로 받는 버퍼이며, 장기 저장소나 일반 서비스 메트릭 프록시가 아니다.

## Scope

### Policy Scope

이 정책은 `infra/06-observability/docker-compose.yml`의 `pushgateway` 서비스, 해당 서비스에 메트릭을 push하는 작업, Pushgateway의 stale metric cleanup, 그리고 Prometheus scrape 연동 계약에 적용된다.

- **Systems**: `pushgateway` service/container, image [prom/pushgateway image declaration](../../../infra/06-observability/docker-compose.yml), port `9091`, `/-/ready` healthcheck, `pushgateway.${DEFAULT_URL}` protected Traefik route, Prometheus scrape integration contract
- **Environments**: 로컬·홈랩 관측 환경의 `obs` 또는 `batch-metrics` Docker Compose profile

### Traceability

- Declared parent: [Observability Architecture Description](../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Guide](../guides/0046-pushgateway.md) (`GDE-0046`), [Runbook](../runbooks/0046-pushgateway.md) (`RUN-0046`)

## Rules

### Controls

- **Required**:
  - Compose 서비스는 `profiles: [obs, batch-metrics]`, `template-infra-readonly-low`, image [prom/pushgateway image declaration](../../../infra/06-observability/docker-compose.yml), expose `${PUSHGATEWAY_PORT:-9091}`, `/-/ready` healthcheck, and protected Traefik middleware chain을 유지해야 한다.
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
  - cardinality가 높은 label, 상한 없는 tenant·user·request·build 식별자, secret을 포함한 label·지표 payload를 사용하는 행위.
  - 현재 Compose에 선언되지 않은 persistence option, route relaxation, image change, or scrape-job behavior를 문서에서 구현 완료로 표현하는 행위.

### Lifecycle and data controls

- Pushgateway는 OPTIONAL을 유지한다. Batch 동안 시작하거나 기존 실행 컨테이너를 발견해도 HOME으로 재분류하지 않는다.
- Metric은 휘발성이므로 grouping-key 소유권, stale-series 삭제, gateway 인증과 producer의 실제 관측을 요구한다. 영속 보존·정확한 복구를 주장하지 않는다.
- Upgrade/restart는 metric 손실을 승인하고 현재 관측의 제한된 재전송을 준비해야 한다. 자원 변경에는 series/cardinality 근거가 필요하다.
- 제거에는 producer 이전·중지, scrape 정리, stale group 삭제와 route 폐쇄가 필요하다. 삭제할 자체 데이터 볼륨은 없다.

### Verification

- **Compose Check**: `rg -n 'service: template-infra-readonly-low|image: prom/pushgateway:|PUSHGATEWAY_PORT|/-/ready|pushgateway.middlewares' infra/06-observability/docker-compose.yml`
- **Scrape Contract Check**: `rg -n 'job_name: "pushgateway"|pushgateway:9091|honor_labels' infra/06-observability/prometheus/config/prometheus.yml`. Match가 없으면 Prometheus integration을 gap으로 기록하고 runtime 설정 변경 task를 별도로 만든다.
- **Stale Metric Check**: scrape job이 존재하는 환경에서는 `push_time_seconds` 기준으로 1시간 이상 갱신되지 않은 `job` group을 식별한다.
- **API Audit**: Pushgateway API or UI에서 비정상적으로 큰 metric group, high-cardinality labels, cleanup되지 않은 debug groups를 확인한다.
- **Documentation Check**: guide and runbook은 사용법과 복구 절차만 설명하고, policy control은 이 문서에 유지한다.

책임 소유자는 **@buenhyden**이다. 예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다. 통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

### Review Cadence

분기마다, 그리고 image·profile·route middleware·healthcheck·영속성·scrape job·label 정책·cleanup 자동화가 바뀔 때 검토한다.

## Exceptions

### Exceptions

예외는 운영 owner가 승인해야 하며, 승인 사유, label cardinality boundary, cleanup 절차, rollback 기준, 관련 task or incident evidence를 남겨야 한다. Emergency cleanup은 runbook 절차로 수행하고 사후에 evidence를 보강한다.

## Related Documents

- 런타임 고정값은 Compose/Dockerfile 선언이 소유하며 [파생 이미지 목록](../../../infra/tech-stack.versions.json)은 드리프트 검증에 사용한다.

- [Operations index](../README.md)
- [Usage guide](../guides/0046-pushgateway.md)
- [Recovery runbook](../runbooks/0046-pushgateway.md)
