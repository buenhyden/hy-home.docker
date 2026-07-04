---
status: active
---
<!-- Target: docs/05.operations/runbooks/06-observability/loki.md -->

# Loki Readiness and Storage Recovery Runbook

## Loki Readiness and Storage Recovery Procedure

> Scope: Loki readiness checks, Alloy ingestion evidence, MinIO storage/retention verification, restart, and config rollback.

### Overview

이 런북은 Loki readiness failure, Grafana "no logs found", Alloy ingestion failure, MinIO storage/credential symptom, retention/compactor issue, label cardinality regression, and config regression을 다룬다. Guide와 policy의 설명을 반복하지 않고 실행 가능한 진단, 안전한 restart, evidence capture, escalation 기준을 제공한다.

### Purpose

운영자가 `infra-loki` 상태를 확인하고 Alloy -> Loki ingestion, MinIO S3 backend, retention/compactor config, custom image secret expansion, Grafana datasource를 검증하며, Secret 노출이나 retention/resource/runtime 변경 같은 위험 조치를 별도 승인으로 격리하도록 돕는다.

### Canonical References

- **Policy**: [Loki operations policy](../../policies/06-observability/loki.md)
- **Guide**: [Loki usage guide](../../guides/06-observability/loki.md)
- **Infrastructure**: [Loki infra README](../../../../infra/06-observability/loki/README.md)

## When to Use

- Loki UI route 또는 `ready` endpoint가 실패할 때.
- Grafana Explore에서 expected logs가 보이지 않을 때.
- Loki logs에 `S3`, `access denied`, `entry out of order`, `rate limit`, `compactor`, `retention`, or `OOM` symptom이 보일 때.
- `MINIO_APP_USERNAME`, `minio_app_user_password`, `loki-bucket`, retention, compactor, or label policy 변경 후 검증이 필요할 때.
- `loki-config.yaml`, `Dockerfile`, or `docker-entrypoint.sh` 변경 후 rollback 가능성을 확인해야 할 때.

## Procedure

### Checklist

- [ ] `loki` service, `infra-loki` container, `loki-data` volume, custom image, and Docker Secret ID 상태를 확인한다.
- [ ] 문제 유형을 readiness, Alloy ingestion, Grafana datasource/query, MinIO storage/credential, retention/compactor, label cardinality, config regression 중 하나로 분류한다.
- [ ] `MINIO_APP_USER_PASSWORD` value, MinIO credential value, rendered environment, or secret payload 원문은 기록하지 않는다.
- [ ] Retention, resource cap, MinIO bucket, route, or secret reference를 변경해야 해 보이면 중단하고 owning operator approval을 받는다.

### Steps

1. 현재 service 상태, 최근 로그, readiness를 캡처한다.

   ```bash
   docker compose -f infra/06-observability/docker-compose.yml --profile obs ps loki
   docker logs --tail=200 infra-loki
   docker exec infra-loki wget -qO- http://127.0.0.1:3100/ready
   ```

2. Compose service boundary가 policy와 일치하는지 확인한다.

   ```bash
   rg -n 'service: template-stateful-high|image: hy/loki:3.7.3-custom|container_name: infra-loki|loki-data|MINIO_APP_USERNAME|minio_app_user_password|LOKI_HOST_PORT|LOKI_PORT|/ready|gateway-standard-chain@file,sso-errors@file,sso-auth@file' infra/06-observability/docker-compose.yml
   ```

3. Custom image and secret expansion boundary를 확인한다.

   ```bash
   rg -n 'FROM grafana/loki:3.7.3|ENTRYPOINT \\[\"/docker-entrypoint.sh\"\\]|-config.expand-env=true|MINIO_APP_USER_PASSWORD|/run/secrets/minio_app_user_password|exec /usr/bin/loki' infra/06-observability/loki/Dockerfile infra/06-observability/loki/docker-entrypoint.sh
   ```

4. MinIO storage, retention, compactor, and ruler boundary를 확인한다.

   ```bash
   rg -n 'bucketnames: loki-bucket|access_key_id: \\$\\{MINIO_APP_USERNAME\\}|secret_access_key: \\$\\{MINIO_APP_USER_PASSWORD\\}|retention_enabled: true|retention_period: 168h|compaction_interval: 10m|retention_delete_delay: 2h|alertmanager_url: http://alertmanager:9093' infra/06-observability/loki/config/loki-config.yaml
   ```

5. Grafana "no logs found"가 문제이면 Alloy ingestion path와 Grafana datasource를 확인한다.

   ```bash
   rg -n 'loki.source.docker|loki.write|url = \"http://loki:3100/loki/api/v1/push\"|project_net\\|infra_net' infra/06-observability/alloy/config/config.alloy
   rg -n 'name: Loki|uid: Loki|url: http://loki:3100' infra/06-observability/grafana/provisioning/datasources/datasource.yml
   ```

6. Storage or retention symptom이 의심되면 Loki logs에서 관련 증상만 추출한다.

   ```bash
   docker logs --tail=500 infra-loki | grep -Ei 's3|bucket|loki-bucket|minio|access denied|secret|retention|compactor|rate limit|out of order|oom|error|warn'
   ```

   Secret value나 credential payload가 포함된 줄은 그대로 복사하지 말고 redaction summary로 기록한다.

7. Config와 Secret ID 경계가 정책과 일치하지만 runtime state가 회복되지 않으면 Loki를 재시작한다.

   ```bash
   docker compose -f infra/06-observability/docker-compose.yml --profile obs restart loki
   docker logs --tail=100 infra-loki
   docker exec infra-loki wget -qO- http://127.0.0.1:3100/ready
   ```

8. `loki-config.yaml`, custom image, or entrypoint 변경 후 장애가 발생했다면 Git-managed diff를 되돌리고 readiness를 재확인한다.

   ```bash
   git diff -- infra/06-observability/loki/config/loki-config.yaml infra/06-observability/loki/Dockerfile infra/06-observability/loki/docker-entrypoint.sh
   docker compose -f infra/06-observability/docker-compose.yml --profile obs restart loki
   docker exec infra-loki wget -qO- http://127.0.0.1:3100/ready
   ```

   이 런북은 retention change, MinIO bucket migration, resource cap increase, secret rotation, high-cardinality label expansion, or protected middleware change를 검증된 복구 절차로 제공하지 않는다. 해당 변경은 별도 approval과 rollback evidence가 필요하다.

### Verification Steps

- [ ] `docker compose -f infra/06-observability/docker-compose.yml --profile obs ps loki`에서 `loki` service가 running이다.
- [ ] `docker exec infra-loki wget -qO- http://127.0.0.1:3100/ready`가 ready response를 반환한다.
- [ ] Alloy `loki.write` endpoint가 `http://loki:3100/loki/api/v1/push`를 유지한다.
- [ ] Grafana datasource `Loki`가 `http://loki:3100`를 유지한다.
- [ ] `retention_enabled: true`, `retention_period: 168h`, and `bucketnames: loki-bucket`가 config에 남아 있다.
- [ ] 문서 또는 config만 바꾼 경우 관련 repository validation을 실행하고 evidence에 기록한다.

### Observability and Evidence Sources

- **Logs**: `docker logs --tail=200 infra-loki`, `docker logs --tail=200 infra-alloy`
- **Health**: Loki `/ready`, Grafana Explore query result, Alloy component graph
- **Config**: `loki-config.yaml`, Dockerfile, entrypoint, Alloy `loki.write`, Grafana datasource
- **Metrics**: `loki_request_duration_seconds_count`, `loki_panic_total`, compactor/retention log symptoms
- **Evidence to Capture**: failing query, affected labels, relevant redacted log excerpt, storage symptom, restart timestamp, final recovery or escalation state

### Safe Rollback or Recovery Procedure

- Git-managed `loki-config.yaml`, Dockerfile, entrypoint, Compose, Alloy endpoint, or Grafana datasource change가 원인이면 직전 Git diff 단위로 되돌리고 Loki를 재시작한다.
- Runtime restart는 `obs` profile compose 명령만 사용한다.
- Retention, MinIO bucket, resource cap, secret rotation, label cardinality policy, or protected route middleware change는 이 런북의 안전 롤백 범위를 벗어난다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

## Evidence

- 실행한 명령, timestamp, operator or agent action을 기록한다.
- Secret 값, rendered environment, MinIO credential 원문은 기록하지 않는다.
- Log ingestion 장애는 affected LogQL query, labels, Alloy component, Loki log excerpt, storage symptom을 함께 기록한다.
- Retention/resource/bucket/secret/middleware 변경 필요성이 보이면 approval state를 기록한다.

## Rollback or Recovery

이 런북에 명시된 validation, restart, and Git-managed config/image/entrypoint rollback만 사용한다. Retention, MinIO bucket, resource cap, secret rotation, high-cardinality label, protected middleware, or external storage 변경은 검증된 안전 복구 절차가 아니므로 `## Escalation`으로 이동한다.

## Escalation

verification이 실패하거나, secret exposure risk가 보이거나, retention/resource/bucket/secret/middleware 정책 변경이 필요하거나, 관찰된 상태가 예상 절차와 다르면 owning operator에게 escalation한다. 캡처한 evidence, 시도한 step, 현재 rollback/recovery 상태를 함께 제공한다.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/06-observability/loki.md)
- [Operations policy](../../policies/06-observability/loki.md)
