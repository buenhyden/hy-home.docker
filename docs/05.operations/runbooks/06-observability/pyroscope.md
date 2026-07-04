---
status: active
---
<!-- Target: docs/05.operations/runbooks/06-observability/pyroscope.md -->

# Pyroscope Readiness and Recovery Runbook

## Pyroscope Readiness and Recovery Procedure

> Scope: Pyroscope readiness checks, profile ingestion triage, local storage evidence, restart, and capacity escalation.

### Overview

이 런북은 Pyroscope profile ingestion gap, Grafana datasource failure, local filesystem storage pressure, high CPU overhead, and config regression을 다룬다. Guide와 policy의 설명을 반복하지 않고 실행 가능한 진단, 안전한 restart, evidence capture, escalation 기준을 제공한다.

### Purpose

운영자가 `infra-pyroscope` 상태를 확인하고 Alloy/Grafana 연결, ingestion limits, local storage boundary를 검증하며, 데이터 삭제나 retention/capacity 변경 같은 위험 조치를 별도 승인으로 격리하도록 돕는다.

### Canonical References

- **Policy**: [Pyroscope operations policy](../../policies/06-observability/pyroscope.md)
- **Guide**: [Pyroscope usage guide](../../guides/06-observability/pyroscope.md)
- **Infrastructure**: [Pyroscope infra README](../../../../infra/06-observability/pyroscope/README.md)

## When to Use

- Grafana Pyroscope datasource에서 최근 profile이 보이지 않을 때.
- Alloy `pyroscope.write` endpoint는 선언되어 있지만 profile ingestion gap이 의심될 때.
- `infra-pyroscope` 로그에 storage, ingestion limit, label cardinality, or ready failure 관련 오류가 보일 때.
- Profile ingestion으로 host or container CPU usage가 비정상적으로 높을 때.
- `pyroscope.yaml` 변경 후 readiness, storage, ingestion limit evidence가 필요할 때.

## Procedure

### Checklist

- [ ] `pyroscope` service, `infra-pyroscope` container, and `pyroscope-data` volume 상태를 확인한다.
- [ ] Profile labels에 high-cardinality or secret-bearing values가 들어갔는지 의심되면 ingestion source를 먼저 식별한다.
- [ ] 문제 유형을 readiness, ingestion, Grafana datasource, storage/capacity, CPU overhead, config regression 중 하나로 분류한다.
- [ ] Data deletion, retention change, storage backend change, or ingestion limit change가 필요해 보이면 중단하고 owning operator approval을 받는다.

### Steps

1. 현재 service 상태, ready endpoint, 최근 로그를 캡처한다.

   ```bash
   docker compose -f infra/06-observability/docker-compose.yml --profile obs ps pyroscope
   docker logs --tail=200 infra-pyroscope
   docker exec infra-pyroscope wget -q --spider http://localhost:4040/ready
   ```

2. Compose and config boundary가 policy와 일치하는지 확인한다.

   ```bash
   rg -n 'service: template-infra-med|image: grafana/pyroscope:2.1.0|container_name: infra-pyroscope|pyroscope-data|PYROSCOPE_PORT|/ready|pyroscope.middlewares' infra/06-observability/docker-compose.yml
   rg -n 'http_listen_port: 4040|reporting_enabled: false|data_dir: /var/lib/pyroscope/compactor|ingestion_rate_mb: 16|ingestion_burst_size_mb: 32|max_label_names_per_series: 30|multitenancy_enabled: false|backend: filesystem|dir: /var/lib/pyroscope|disable_push: true' infra/06-observability/pyroscope/config/pyroscope.yaml
   ```

3. Alloy writer와 Grafana datasource가 Pyroscope endpoint를 가리키는지 확인한다.

   ```bash
   rg -n 'pyroscope.write "local_pyroscope"|url = "http://pyroscope:4040"|type: grafana-pyroscope-datasource|url: http://pyroscope:4040' infra/06-observability/alloy/config/config.alloy infra/06-observability/grafana/provisioning/datasources/datasource.yml
   ```

4. Storage or cardinality symptom은 로그와 capacity evidence를 캡처한다. Profile data를 삭제하지 않는다.

   ```bash
   docker logs --tail=500 infra-pyroscope | grep -Ei 'storage|filesystem|label|cardinality|ingestion|limit|error|warn'
   docker stats --no-stream infra-pyroscope
   docker compose -f infra/06-observability/docker-compose.yml config | grep -n 'pyroscope-data'
   ```

5. Readiness or ingestion state가 config와 맞지만 회복되지 않으면 Pyroscope를 재시작한다. Alloy writer state도 함께 의심될 때만 Alloy를 같이 재시작한다.

   ```bash
   docker compose -f infra/06-observability/docker-compose.yml --profile obs restart pyroscope
   docker compose -f infra/06-observability/docker-compose.yml --profile obs restart pyroscope alloy
   ```

6. `pyroscope.yaml` 변경 후 장애가 발생했다면 Git-managed config diff를 되돌리고 readiness를 재확인한다.

   ```bash
   git diff -- infra/06-observability/pyroscope/config/pyroscope.yaml
   docker compose -f infra/06-observability/docker-compose.yml --profile obs restart pyroscope
   docker exec infra-pyroscope wget -q --spider http://localhost:4040/ready
   ```

   이 런북은 profile data deletion, filesystem mutation, retention change, or ingestion limit change를 검증된 복구 절차로 제공하지 않는다. 데이터 손실 가능성이 있거나 운영 기준을 바꾸는 조치는 별도 incident/task approval과 rollback evidence가 필요하다.

### Verification Steps

- [ ] `docker exec infra-pyroscope wget -q --spider http://localhost:4040/ready`가 성공한다.
- [ ] Grafana Pyroscope datasource에서 최근 profile이 조회된다.
- [ ] `docker stats --no-stream infra-pyroscope`에서 CPU/memory 사용량이 정상 범위로 돌아온다.
- [ ] Storage symptom이면 `pyroscope-data`, `/var/lib/pyroscope`, and filesystem backend boundary가 policy와 일치한다.
- [ ] 문서 또는 config만 바꾼 경우 관련 repository validation을 실행하고 evidence에 기록한다.

### Observability and Evidence Sources

- **Logs**: `docker logs --tail=200 infra-pyroscope`, `docker logs --tail=200 infra-alloy`
- **Health**: Pyroscope `/ready`, Grafana Pyroscope datasource
- **Config**: `pyroscope.yaml`, Alloy `pyroscope.write`, Grafana datasource provisioning
- **Runtime**: `docker stats --no-stream infra-pyroscope`, `pyroscope-data` volume boundary
- **Evidence to Capture**: failing symptom, log excerpt, affected profile source or label, restart timestamp, final recovery or escalation state

### Safe Rollback or Recovery Procedure

- Git-managed `pyroscope.yaml`, Alloy writer, Grafana datasource, or Compose 변경이 원인이면 직전 Git diff 단위로 되돌리고 readiness를 다시 확인한다.
- Runtime restart는 `obs` profile compose 명령만 사용한다.
- Profile data deletion, filesystem mutation, retention change, storage backend change, and ingestion limit change는 이 런북의 안전 롤백 범위를 벗어난다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

## Evidence

- 실행한 명령, timestamp, operator or agent action을 기록한다.
- Profile label or payload에 secret-bearing value가 의심되면 원문 값을 기록하지 않는다.
- Ingestion 장애는 Alloy writer check, Pyroscope ready state, Grafana datasource result를 함께 기록한다.
- Storage/capacity symptom은 로그 발췌, `pyroscope-data` volume boundary, approval state를 기록한다.

## Rollback or Recovery

이 런북에 명시된 validation, restart, and Git-managed config rollback만 사용한다. 데이터 손실 가능성이 있는 profile data deletion, filesystem mutation, retention/storage/ingestion-limit change는 검증된 안전 복구 절차가 아니므로 `## Escalation`으로 이동한다.

## Escalation

verification이 실패하거나, secret exposure risk가 보이거나, destructive data change가 필요하거나, storage/capacity 정책 변경이 필요하거나, 관찰된 상태가 예상 절차와 다르면 owning operator에게 escalation한다. 캡처한 evidence, 시도한 step, 현재 rollback/recovery 상태를 함께 제공한다.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/06-observability/pyroscope.md)
- [Operations policy](../../policies/06-observability/pyroscope.md)
