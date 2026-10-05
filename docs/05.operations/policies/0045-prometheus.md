---
title: "Prometheus Operations Policy"
version: "1.4.0"
type: "operation/policy"
status: "active"
owner: "@buenhyden"
updated: "2026-10-01"
layer: "operations"
artifact_id: "POL-0045"
parent_ids:
- "AD-0006"
created: "2026-05-17"
---

# Prometheus Operations Policy

## Overview

### Overview

이 정책은 scrape target registration, alerting rule management, TSDB
persistence, lifecycle reload, secret file reference, protected access에
대한 Prometheus control을 정의한다. 순서가 있는 recovery나 reload
procedure는 해당 runbook에 있다.

## Scope

### Policy Scope

이 정책은 현재 `infra/06-observability/prometheus` compose, config,
alert-rule surface에 적용된다.

- **Systems**: compose service `prometheus`, container `infra-prometheus`, image [Compose image declaration](../../../infra/06-observability/docker-compose.yml), config `infra/06-observability/prometheus/config/prometheus.yml`, rules directory `infra/06-observability/prometheus/config/alert_rules`, volume `prometheus-data`
- **Environments**: 로컬·개발·홈랩 운영

### Traceability

- Declared parent: [Observability Architecture Description](../../02.architecture/descriptions/0006-observability-architecture.md) (`AD-0006`)
- Subject peers: [Guide](../guides/0045-prometheus.md) (`GDE-0045`), [Runbook](../runbooks/0045-prometheus.md) (`RUN-0045`)

## Rules

### Controls

- **Required**:
  - Prometheus service는 `template-stateful-high`, image
    [Compose image declaration](../../../infra/06-observability/docker-compose.yml), tmpfs `/tmp`와 `/etc/prometheus:size=10M`,
    read-only config/rules mount, persistent `prometheus-data` volume을
    유지한다.
  - Runtime command는 `--config.file=/etc/prometheus/prometheus.yml`,
    `--storage.tsdb.path=/prometheus`, `--web.enable-lifecycle`,
    `--web.enable-remote-write-receiver`를 유지한다.
  - Global cadence는 `scrape_interval: 30s`와 `evaluation_interval: 30s`를
    기준으로 한다. Prometheus의 `15s`, cAdvisor의 `1m`과 같은
    service-specific interval은 의도하고 검토한 값으로 유지해야 한다.
  - Scrape job은
    `infra/06-observability/prometheus/config/prometheus.yml`과
    `prometheus.dev.yml`에서 같은 내용으로 관리한다. 소스 하나를 두 job이
    수집하지 않으며, 모든 target은 `cluster="hy-home"`,
    `namespace="hy-home"` 라벨을 가진다(SPEC-0193).
  - Alert와 recording rule은
    `/etc/prometheus/alert_rules/alert_rules.local.*.yml`,
    `/etc/prometheus/alert_rules/alert_rules.keycloak.yml`,
    `/etc/prometheus/alert_rules/alert_rules.openbao.yml`,
    `/etc/prometheus/alert_rules/recording_rules*.yml`에서 로드된다.
  - Alert rule은 `expr`, 해당되는 경우 `for`, `labels.severity`, 실행
    가능한 `annotations`, 해당 서비스 runbook 파일을 가리키는
    `annotations.runbook_url`을 포함해야 한다. `expr`은 소스가 실행 중일
    때 방출하는 metric만 쓰며, on-demand job은 `up == 0`으로 알리지 않는다.
  - `opensearch_exporter_password`, `openbao_token`,
    `qdrant_read_only_api_key`(AI-009, Qdrant read-only key; Prometheus는
    full `qdrant_api_key`를 절대 보유하지 않는다)는 Docker Secret file
    reference일 뿐이다; 그 값이 문서, 로그, task evidence에 나타나서는
    안 된다.
    Active Compose는 위 세 scrape secret을 선언하고 mount한다. 선언은
    실제 credential 발급/target readiness를 증명하지 않는다. 별도 승인된
    migration closeout, revocation, file disposition 전까지 기존 private value를
    그대로 유지하며 문서 정리를 이유로 삭제하거나 폐기하지 않는다.
  - `SEC-002` / `openbao_token`은 수동 least-privilege OpenBao
    `prometheus`-policy credential contract다. Source declaration은
    token이 발급되었거나, 실행 중인 container가 로드했거나, UP scrape
    target을 만들었음을 증명하지 않는다.
  - Prometheus route는
    `gateway-standard-chain@file,sso-errors@file,sso-auth@file`을
    유지해야 한다.
  - `prometheus-api` route는 Prometheus host에서 Basic `Authorization`
    header를 가진 `/api/v1/` 요청만 `prometheus-api-auth@file`(Basic
    Auth from `INFRA-007`, `OBS-012`/`OBS-013`에서 파생) 뒤에서 허용한다.
    이 route는 hy-home.k8s cluster의 remote write와 Kiali query처럼
    SSO를 통과할 수 없는 machine client를 위한 것이다. UI와 그 외 모든
    경로(UI 자체의 `/api/v1/` 호출 포함)는 SSO 뒤에 유지되며
    admin API는 비활성 상태를 유지한다.
    `OBS-013`, `INFRA-007`, OpenBao `secret/platform/prometheus-api`는
    함께 회전한다; OpenBao entry가 stale하면 cluster의 remote write가
    `401`을 받는다.
  - TSDB retention 변경은 [retention policy](0048-telemetry-retention.md), volume impact review,
    plan/task evidence와 함께 진행해야 한다. 현재 compose command는
    명시적인 `--storage.tsdb.retention.*` flag를 선언하지 않는다.
- **Allowed**:
  - target이 Prometheus network에서 도달 가능한 안정적인 metrics
    endpoint를 노출하고 일치하는 alerting이나 문서화된 no-alert
    rationale이 있다면 새 scrape target을 추가할 수 있다.
  - dashboard와 rule impact review 후 expensive PromQL을 recording
    rule로 옮길 수 있다.
  - config/rule validation 후 lifecycle reload를 사용할 수 있다;
    operational reload 단계는 runbook에 있다.
- **Disallowed**:
  - architectural 승인과 capacity evidence 없이 `10s` 미만의 scrape
    interval
  - cardinality review 없는 high-cardinality label 추가
  - git-managed `prometheus.yml`이나 `alert_rules`를 우회하는 UI/API
    전용 변경
  - 문서나 evidence에 secret 값, bearer token, rendered secret
    content를 기록하는 행위
  - `prometheus-api` rule을 Basic-authenticated `/api/v1/` 요청 이상으로
    확장하거나, 이 route가 존재하는 동안
    `--web.enable-admin-api`를 활성화하거나, 인증되지 않은 Prometheus
    host port를 게시하는 행위
  - compose/config와 retention policy가 뒷받침하지 않는 retention
    동작을 선언하는 행위

### Lifecycle and data controls

- Prometheus는 `HOME`으로 유지한다; gateway auth, least-privilege scrape secret, 검증된 rule, 선언된 local TSDB boundary를 유지한다.
- `prometheus-data`는 현재 source 아래에서 승인된 consistent stopped copy/snapshot으로만 백업한다. 별도 검토를 거쳐 `--web.enable-admin-api`를 활성화하지 않는 한 `/api/v1/admin/tsdb/snapshot`을 호출하지 않는다.
- isolated TSDB storage에서 rehearse하며 production remote-write/alert는 사용하지 않는다. WAL replay, historical/current query, target label, rule evaluation, Alertmanager delivery, remote-write receiver client를 검증한다.
- Resource/retention 변경에는 측정된 disk 증가, query/scrape pressure, rollback threshold가 필요하다. Removal에는 scraper/client migration과 명시적인 TSDB-retention/deletion 승인이 필요하다.

### Host and GPU exporter boundary

`node-exporter`는 `obs`/`obs-host`/`dev`로 선택하는 HOME host 관측기다. Host PID와 읽기 전용 root/proc/sys/textfile은 민감한 host 정보를 노출하므로 읽기 전용 권한, timex 비활성화와 제한된 collector를 유지한다. Backup textfile 경로는 `create_host_path: false`여서 소유자가 미리 준비해야 한다. HTTP probe와 Prometheus target은 별도로 확인한다. `dcgm-exporter`는 POL-0078에 따라 HOME에 포함되는 `obs-gpu` 전용 서비스이고 선언 GPU를 예약하나 Compose healthcheck는 없다. GPU, DCGM metric과 scrape 상태를 구분하며 SYS_ADMIN을 추가하거나 image/HTTP 응답만으로 driver 호환성을 추정하지 않는다. 둘 다 애플리케이션 상태나 Docker Secret이 없으며 복구 자산은 image/config와 metric 기준이다. GPU 유지보수는 [RUN-0055](../runbooks/0055-gpu-recovery.md)가 맡는다.

`PROMETHEUS_CONFIG_FILE`이 마운트 파일을 선택하며 Compose 기본값은 `prometheus.dev.yml`이다. 두 tracked config의 job은 현재 동일하다. Retention flag가 없어 선언 버전의 15d 기본값이 적용되며 무기한 보존을 약속하지 않는다. Admin snapshot API는 비활성 상태다. 일관된 정지 TSDB 백업은 [RUN-0045](../runbooks/0045-prometheus.md)와 백업 소유자 절차를 따른다.

### Verification

- Compose service boundary:
  `rg -n 'service: template-stateful-high|image: prom/prometheus:|--web.enable-lifecycle|--web.enable-remote-write-receiver|prometheus-data|opensearch_exporter_password|openbao_token|prometheus.middlewares' infra/06-observability/docker-compose.yml`
- Prometheus config:
  `rg -n 'scrape_interval: 30s|evaluation_interval: 30s|rule_files:|alert_rules.local|recording_rules|password_file: "/run/secrets/opensearch_exporter_password"|bearer_token_file: /run/secrets/openbao_token' infra/06-observability/prometheus/config/prometheus.yml`
- Repository contracts:
  `python3 scripts/validation/run-ci-gate.py --profile changed`

책임 소유자는 **@buenhyden**이다. 예외·통제 변경에는 기존 범위별 승인 기록이 필요하며 문서 수정은 승인 근거가 아니다. 통제 실패나 복구 증거 누락은 수용을 중단하고 정제된 증거로 에스컬레이션한다.

### Review Cadence

- Prometheus image, runtime flags, scrape jobs, alert rules, recording rules,
  secret references, route, retention, mounted paths가 변경될 때 검토한다.
- 정기 검토는 quarterly cadence로 수행한다.

## Exceptions

### Exceptions

- Scrape interval, retention, secret reference, route, rule-loading
  예외는 사용자 승인과 관련 plan/task evidence가 있을 때만 허용한다.
- 긴급 reload나 target suppression은 rollback evidence와 함께 Prometheus
  runbook을 통해 기록해야 한다.

## Related Documents

- [Runtime image declarations](../../../infra/06-observability/docker-compose.yml)
- [Operations index](../README.md)
- [Usage guide](../guides/0045-prometheus.md)
- [Recovery runbook](../runbooks/0045-prometheus.md)
- [Retention policy](0048-telemetry-retention.md)
