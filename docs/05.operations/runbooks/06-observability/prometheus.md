---
status: active
---
<!-- Target: docs/05.operations/runbooks/06-observability/prometheus.md -->

# Prometheus Readiness and Recovery Runbook

## Prometheus Readiness and Recovery Procedure

> Scope: readiness checks, config/rule validation, lifecycle reload, scrape target triage, restart, and TSDB symptom escalation.

### Overview

이 런북은 Prometheus service disruption, scrape target failure, alert rule evaluation failure, lifecycle reload, and TSDB corruption symptom을 다룬다. Policy와 guide의 설명을 반복하지 않고, 실행 가능한 확인 절차와 evidence 기준만 제공한다.

### Purpose

운영자가 `infra-prometheus` 상태를 안전하게 확인하고, config/rule 변경을 검증한 뒤 reload or restart를 수행하며, 데이터 손실 가능성이 있는 TSDB 조치는 별도 승인으로 격리하도록 돕는다.

### Canonical References

- **Policy**: [Prometheus operations policy](../../policies/06-observability/prometheus.md)
- **Guide**: [Prometheus usage guide](../../guides/06-observability/prometheus.md)
- **Infrastructure**: [Prometheus infra README](../../../../infra/06-observability/prometheus/README.md)

## When to Use

- Prometheus UI or `/-/healthy` endpoint가 실패할 때.
- Grafana dashboards에서 metrics가 비어 있거나 stale하게 보일 때.
- 특정 scrape target이 `DOWN`이거나 `PrometheusAllTargetsMissing` 계열 alert가 발생할 때.
- `PrometheusRuleEvaluationFailures` or rule loading error가 발생할 때.
- `prometheus.yml` or `alert_rules/` 변경 후 reload가 필요할 때.
- TSDB corruption, compaction failure, WAL 관련 로그가 보일 때.

## Procedure

### Checklist

- [ ] 변경 전 `prometheus.yml`, alert rule files, compose service boundary를 확인한다.
- [ ] Secret values를 열람하지 않는다. Secret ID and file reference만 evidence에 기록한다.
- [ ] 문제 유형을 readiness, config/rule, scrape target, route, storage/TSDB 중 하나로 분류한다.
- [ ] 데이터 삭제, WAL 제거, volume mutation이 필요해 보이면 즉시 중단하고 owning operator approval을 받는다.

### Steps

1. 현재 service 상태와 최근 로그를 캡처한다.

   ```bash
   docker compose -f infra/06-observability/docker-compose.yml --profile obs ps prometheus
   docker logs --tail=200 infra-prometheus
   docker exec infra-prometheus wget -qO- http://localhost:9090/-/healthy
   ```

2. Config와 rule syntax를 검증한다.

   ```bash
   docker exec infra-prometheus promtool check config /etc/prometheus/prometheus.yml
   docker exec infra-prometheus promtool check rules /etc/prometheus/alert_rules/*.yml
   ```

3. Scrape target 장애는 Prometheus `Targets` page에서 failing job을 확인하고, Prometheus container에서 target endpoint를 직접 확인한다.

   ```bash
   docker exec infra-prometheus wget -qO- http://<target-service-name>:<metrics-port>/metrics
   ```

   Target이 `/metrics`가 아닌 custom path를 사용하면 `prometheus.yml`의 `metrics_path`를 기준으로 endpoint를 바꾼다.

4. Config or rule 변경이 검증을 통과했고 service가 healthy하면 lifecycle reload를 수행한다.

   ```bash
   docker exec infra-prometheus wget -qO- --post-data='' http://localhost:9090/-/reload
   ```

5. Reload 후에도 service가 unhealthy하거나 runtime state가 회복되지 않으면 profile 포함 compose 명령으로 restart한다.

   ```bash
   docker compose -f infra/06-observability/docker-compose.yml --profile obs restart prometheus
   ```

6. TSDB corruption, compaction failure, WAL 관련 로그가 보이면 삭제 조치를 하지 말고 evidence를 수집한다.

   ```bash
   docker logs --tail=500 infra-prometheus | grep -Ei 'tsdb|wal|compact|corrupt|block'
   docker compose -f infra/06-observability/docker-compose.yml config | grep -n 'prometheus-data'
   ```

   이 런북은 WAL 삭제나 TSDB file mutation을 검증된 복구 절차로 제공하지 않는다. 데이터 손실 가능성이 있는 조치는 별도 incident/task approval과 backup evidence가 필요하다.

### Verification Steps

- [ ] `docker exec infra-prometheus wget -qO- http://localhost:9090/-/healthy`가 healthy response를 반환한다.
- [ ] Prometheus `Targets` page에서 affected critical target이 `UP`이다.
- [ ] `promtool check config` and `promtool check rules`가 성공한다.
- [ ] Grafana dashboard에서 새 metrics timestamp가 갱신된다.
- [ ] 문서 또는 config만 바꾼 경우 관련 repository validation을 실행하고 evidence에 기록한다.

### Observability and Evidence Sources

- **Logs**: `docker logs --tail=200 infra-prometheus`
- **Health**: `/-/healthy`, Prometheus UI `Targets`, Grafana dashboards
- **Validation**: `promtool check config`, `promtool check rules`
- **Metrics**: `prometheus_rule_evaluation_failures_total`, `prometheus_tsdb_compactions_failed_total`, target `up`
- **Evidence to Capture**: failing job name, affected target, command output summary, reload/restart timestamp, final recovery or escalation state

### Safe Rollback or Recovery Procedure

- Git-managed `prometheus.yml` or alert rule 변경이 원인이면 직전 Git diff 단위로 되돌리고 `promtool` 검증 후 lifecycle reload를 다시 수행한다.
- Runtime restart는 `obs` profile compose 명령만 사용한다.
- TSDB/WAL 삭제, volume file mutation, retention flag change는 이 런북의 안전 롤백 범위를 벗어난다. 별도 approval, backup evidence, incident/task 기록 없이 수행하지 않는다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

## Evidence

- 실행한 명령, timestamp, operator or agent action을 기록한다.
- Secret values는 기록하지 않는다.
- Target 장애는 job name, endpoint, observed error, final `UP/DOWN` state를 기록한다.
- TSDB symptom은 로그 발췌, volume boundary, approval state를 기록한다.

## Rollback or Recovery

이 런북에 명시된 validation, reload, restart, and Git-managed config rollback만 사용한다. 데이터 손실 가능성이 있는 TSDB/WAL 조치는 검증된 안전 복구 절차가 아니므로 `## Escalation`으로 이동한다.

## Escalation

verification이 실패하거나, secret exposure risk가 보이거나, destructive data change가 필요하거나, TSDB/WAL 조치가 필요하거나, 관찰된 상태가 예상 절차와 다르면 owning operator에게 escalation한다. 캡처한 evidence, 시도한 step, 현재 rollback/recovery 상태를 함께 제공한다.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/06-observability/prometheus.md)
- [Operations policy](../../policies/06-observability/prometheus.md)
