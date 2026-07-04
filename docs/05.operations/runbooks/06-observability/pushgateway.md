---
status: active
---
<!-- Target: docs/05.operations/runbooks/06-observability/pushgateway.md -->

# Pushgateway Metrics Buffer Recovery Runbook

## Pushgateway Metrics Buffer Recovery Procedure

> Scope: stale metric cleanup, Pushgateway readiness checks, and in-memory buffer reset.

### Overview

이 런북은 Pushgateway 운영 중 발생할 수 있는 stale metric, metric group contamination, memory pressure, and push failure를 복구하기 위한 실행 절차를 정의한다.

### Purpose

Pushgateway의 안정적인 메트릭 버퍼 상태를 유지하고, 비정상적인 메트릭 데이터를 정제하여 가시성 품질을 확보한다.

### Canonical References

- ARD: [Observability architecture ARD](../../../02.architecture/requirements/0006-observability-architecture.md)
- Infrastructure: [Pushgateway infra README](../../../../infra/06-observability/pushgateway/README.md)
- Operation: [Pushgateway operations policy](../../policies/06-observability/pushgateway.md)
- Guide: [Pushgateway usage guide](../../guides/06-observability/pushgateway.md)

## When to Use

- 특정 batch or CI job metric이 갱신되지 않고 stale value를 유지할 때.
- Pushgateway metric group이 오염되었거나 high-cardinality label이 잘못 push되었을 때.
- Pushgateway ready endpoint, Traefik route, or internal service endpoint가 실패할 때.
- Prometheus target에서 Pushgateway scrape 상태를 확인해야 하지만 scrape job 존재 여부가 불명확할 때.
- Pushgateway memory usage가 비정상적으로 높고 stale group cleanup만으로 회복되지 않을 때.

## Procedure

### Checklist

- [ ] 영향받은 `job` and optional `instance` label을 확인한다.
- [ ] Pushgateway container 상태를 확인한다.
- [ ] 내부 ready endpoint와 protected external route 중 최소 하나의 도달성을 확인한다.
- [ ] Prometheus scrape job 존재 여부를 확인하고, 없으면 scrape failure가 아니라 integration gap으로 분류한다.
- [ ] 삭제 대상 metric group이 운영자가 승인한 stale or contaminated group인지 확인한다.

### Steps

1. 현재 상태와 로그를 캡처한다.

   ```bash
   docker compose -f infra/06-observability/docker-compose.yml --profile obs ps pushgateway
   docker logs --tail=100 pushgateway
   curl -I http://pushgateway:9091/-/ready
   ```

2. Prometheus scrape integration이 필요한 장애인지 확인한다.

   ```bash
   rg -n 'job_name: "pushgateway"|pushgateway:9091|honor_labels' infra/06-observability/prometheus/config/prometheus.yml
   ```

   Match가 없으면 Prometheus target failure로 처리하지 말고, Pushgateway scrape job 추가를 별도 runtime configuration task로 기록한다.

3. 현재 metric group을 조회한다.

   ```bash
   curl -s http://pushgateway:9091/metrics | grep -E 'push_time_seconds|<job_name>'
   ```

4. 메트릭이 오염되었거나 오래된 경우 특정 `job` 단위로 데이터를 삭제한다.

   ```bash
   curl -X DELETE http://pushgateway:9091/metrics/job/stale_batch_job
   curl -X DELETE http://pushgateway:9091/metrics/job/stale_batch_job/instance/worker-01
   ```

5. 상태가 매우 불안정하거나 메모리 임계치에 도달한 경우 Pushgateway를 재시작하여 in-memory buffer를 초기화한다. 현재 Compose는 persistence option을 선언하지 않으므로 restart는 보관 중인 metric을 잃을 수 있다.

   ```bash
   docker compose -f infra/06-observability/docker-compose.yml --profile obs restart pushgateway
   ```

6. 작업 노드와 external route에서 도달성을 다시 확인한다.

   ```bash
   curl -I http://pushgateway:9091/-/ready
   curl -I https://pushgateway.${DEFAULT_URL}/-/ready
   ```

### Verification Steps

- [ ] `curl -s http://pushgateway:9091/metrics` 출력에서 삭제 대상 `job` group이 사라졌는지 확인한다.
- [ ] `curl -I http://pushgateway:9091/-/ready`가 successful HTTP status를 반환한다.
- [ ] Prometheus scrape job이 존재하는 환경에서는 Prometheus UI `Targets`에서 `pushgateway` target이 `UP`인지 확인한다.
- [ ] Scrape job이 없는 환경에서는 관련 task or gap evidence에 `prometheus.yml` integration gap을 기록한다.

### Observability and Evidence Sources

- **Logs**: `docker logs --tail=100 pushgateway`
- **Metrics**: `pushgateway_http_requests_total`, `process_resident_memory_bytes`, `push_time_seconds` when scraped by Prometheus
- **Evidence to Capture**: status commands, deleted metric group path, before/after `/metrics` snippets, scrape-job check result

### Safe Rollback or Recovery Procedure

- 삭제한 metric group은 Git rollback으로 복원되지 않는다. metric이 필요하면 batch job을 재실행하거나 마지막으로 검증된 metric payload를 다시 push한다.
- Restart 후 Pushgateway가 올라오지 않으면 `docker compose -f infra/06-observability/docker-compose.yml --profile obs up -d pushgateway`를 실행하고 healthcheck를 재확인한다.
- Push 실패가 계속되면 batch job log와 network path를 확인하고, 추가 config 변경 전 escalation한다.

## Evidence

- 실행한 명령, timestamp, operator or agent action을 기록한다.
- 삭제한 metric group path와 삭제 전후 `/metrics` evidence를 기록한다.
- Prometheus scrape job check 결과를 기록한다.
- 실패한 check, 관찰된 증상, 최종 recovery or escalation 상태를 관련 task or incident evidence에 남긴다.

## Rollback or Recovery

이 런북에 명시된 cleanup, restart, repush 절차만 사용한다. 이 범위를 벗어난 persistence option, scrape job 추가, route 변경, image 변경은 별도 task와 approval이 필요한 runtime configuration change다. 관찰된 실패가 절차와 다르면 변경을 중단하고 evidence를 보존한 뒤 `## Escalation`으로 이동한다.

## Escalation

verification이 실패하거나, secret exposure risk가 보이거나, metric 삭제 범위가 불명확하거나, runtime config 변경이 필요하거나, 관찰된 상태가 예상 절차와 다르면 owning operator에게 escalation한다. 캡처한 evidence, 시도한 step, 현재 rollback/recovery 상태를 함께 제공한다.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/06-observability/pushgateway.md)
- [Operations policy](../../policies/06-observability/pushgateway.md)
