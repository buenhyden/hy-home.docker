---
status: active
---
<!-- Target: docs/05.operations/runbooks/06-observability/alloy.md -->

# Alloy Readiness and Pipeline Recovery Runbook

## Alloy Readiness and Pipeline Recovery Procedure

> Scope: Alloy readiness checks, Docker discovery evidence, OTLP ingress triage, downstream exporter verification, restart, and config rollback.

### Overview

이 런북은 Grafana Alloy의 service readiness failure, Docker discovery/log collection gap, OTLP trace ingress failure, downstream exporter failure, pipeline label drift, and config regression을 다룬다. Guide와 policy의 설명을 반복하지 않고 실행 가능한 진단, 안전한 restart, evidence capture, escalation 기준을 제공한다.

### Purpose

운영자가 `infra-alloy` 상태를 확인하고 Docker discovery, Loki/Prometheus/Tempo/Pyroscope exporter 경로, OTLP ports, route, config boundary를 검증하며, mount 권한이나 pipeline 구조 변경 같은 위험 조치를 별도 승인으로 격리하도록 돕는다.

### Canonical References

- **Policy**: [Alloy operations policy](../../policies/06-observability/alloy.md)
- **Guide**: [Alloy usage guide](../../guides/06-observability/alloy.md)
- **Infrastructure**: [Alloy infra README](../../../../infra/06-observability/alloy/README.md)

## When to Use

- Alloy UI or `/-/healthy` endpoint가 실패할 때.
- Docker logs, metrics, or traces가 backend에 도착하지 않을 때.
- OTLP clients가 `alloy:4317` or `alloy:4318`로 전송하지 못할 때.
- 특정 backend exporter에서 connection refused or timeout이 보일 때.
- `config.alloy` 변경 후 component graph, label, or exporter 상태 검증이 필요할 때.

## Procedure

### Checklist

- [ ] `alloy` service, `infra-alloy` container, `alloy-data` volume, and read-only Docker mounts 상태를 확인한다.
- [ ] 문제 유형을 readiness, Docker discovery/logs, OTLP ingress, downstream exporter, relabel/label drift, config regression 중 하나로 분류한다.
- [ ] Docker socket/container mounts를 read-write로 바꾸거나 exporter endpoint/port를 변경해야 해 보이면 중단하고 owning operator approval을 받는다.
- [ ] Secret-bearing labels or high-cardinality labels가 발견되면 원문 값을 기록하지 않는다.

### Steps

1. 현재 service 상태, 최근 로그, route/health signal을 캡처한다.

   ```bash
   docker compose -f infra/06-observability/docker-compose.yml --profile obs ps alloy
   docker logs --tail=200 infra-alloy
   docker exec infra-alloy bash -lc 'exec 3<>/dev/tcp/localhost/12345; printf "HEAD /-/healthy HTTP/1.1\r\nHost: localhost\r\n\r\n" >&3; timeout 2 head -1 <&3'
   ```

2. Compose service boundary가 policy와 일치하는지 확인한다.

   ```bash
   rg -n 'service: template-infra-med|image: grafana/alloy:v1.17.1|container_name: infra-alloy|ALLOY_OTLP_GRPC|ALLOY_OTLP_HTTP|/-/healthy|gateway-standard-chain@file,sso-errors@file,sso-auth@file' infra/06-observability/docker-compose.yml
   rg -n '/var/lib/docker/containers:/var/lib/docker/containers:ro|/var/run/docker.sock:/var/run/docker.sock:ro|alloy-data:/var/lib/alloy:rw' infra/06-observability/docker-compose.yml
   ```

3. Pipeline config boundary를 확인한다.

   ```bash
   rg -n 'discovery.docker|project_net\\|infra_net|loki.source.docker|loki.write|prometheus.remote_write|otelcol.receiver.otlp|otelcol.processor.batch|otelcol.exporter.otlp|pyroscope.write' infra/06-observability/alloy/config/config.alloy
   ```

4. Downstream exporter failure가 의심되면 backend readiness를 확인한다.

   ```bash
   docker exec infra-prometheus wget -qO- http://localhost:9090/-/healthy
   docker exec infra-loki wget -qO- http://127.0.0.1:3100/ready
   docker exec infra-tempo wget --no-verbose --tries=1 --spider http://localhost:3200/ready
   docker exec infra-pyroscope wget -q --spider http://localhost:4040/ready
   ```

5. OTLP ingress 장애가 의심되면 Compose port binding과 Alloy config를 확인한다.

   ```bash
   rg -n 'ALLOY_OTLP_GRPC_HOST_PORT|ALLOY_OTLP_HTTP_HOST_PORT|4317|4318' infra/06-observability/docker-compose.yml infra/06-observability/alloy/config/config.alloy
   ```

6. Label drift or discovery gap이 의심되면 relabel rules와 network filter를 확인한다.

   ```bash
   rg -n 'target_label  = "service_name"|target_label  = "container_name"|target_label = "scope"|regex         = "project_net\\|infra_net"|replacement   = "infra"' infra/06-observability/alloy/config/config.alloy
   ```

7. Config가 현재 정책과 일치하지만 runtime state가 회복되지 않으면 Alloy를 재시작한다.

   ```bash
   docker compose -f infra/06-observability/docker-compose.yml --profile obs restart alloy
   ```

8. `config.alloy` 변경 후 장애가 발생했다면 Git-managed config diff를 되돌리고 readiness를 재확인한다.

   ```bash
   git diff -- infra/06-observability/alloy/config/config.alloy
   docker compose -f infra/06-observability/docker-compose.yml --profile obs restart alloy
   docker logs --tail=100 infra-alloy
   ```

   이 런북은 mount permission relaxation, Docker socket read-write access, exporter endpoint change, OTLP port change, or high-cardinality relabel expansion을 검증된 복구 절차로 제공하지 않는다. 해당 변경은 별도 approval과 rollback evidence가 필요하다.

### Verification Steps

- [ ] `docker compose -f infra/06-observability/docker-compose.yml --profile obs ps alloy`에서 `alloy` service가 running이다.
- [ ] Alloy UI `https://alloy.${DEFAULT_URL}`에서 pipeline graph에 failed component가 없다.
- [ ] Logs appear in Loki, Alloy self metrics appear in Prometheus, and OTLP traces appear in Tempo for affected paths.
- [ ] Pyroscope writer endpoint remains configured, and profile ingestion is only claimed when a profile source is explicitly connected.
- [ ] 문서 또는 config만 바꾼 경우 관련 repository validation을 실행하고 evidence에 기록한다.

### Observability and Evidence Sources

- **Logs**: `docker logs --tail=200 infra-alloy`
- **Health**: Alloy `/-/healthy`, Alloy UI graph
- **Config**: `config.alloy`, Docker discovery/relabel rules, exporter endpoints
- **Backends**: Loki ready, Prometheus healthy, Tempo ready, Pyroscope ready
- **Evidence to Capture**: failing component, relevant log excerpt, affected telemetry signal, restart timestamp, final recovery or escalation state

### Safe Rollback or Recovery Procedure

- Git-managed `config.alloy`, Compose, or downstream endpoint change가 원인이면 직전 Git diff 단위로 되돌리고 Alloy를 재시작한다.
- Runtime restart는 `obs` profile compose 명령만 사용한다.
- Docker socket/container mount permission relaxation, exporter endpoint change, OTLP port change, relabel cardinality expansion은 이 런북의 안전 롤백 범위를 벗어난다.

### Agent Operations (If Applicable)

- **Prompt Rollback**: 적용하지 않음
- **Model Fallback**: 적용하지 않음
- **Tool Disable / Revoke**: secret 노출 위험이 있으면 파일 열람을 중단한다.
- **Eval Re-run**: 관련 validation과 문서 audit를 재실행한다.
- **Trace Capture**: 변경 파일, 명령, 결과를 task evidence에 기록한다.

## Evidence

- 실행한 명령, timestamp, operator or agent action을 기록한다.
- Secret-bearing label or payload가 의심되면 원문 값을 기록하지 않는다.
- Pipeline 장애는 component name, backend endpoint, log excerpt, affected telemetry signal을 함께 기록한다.
- Mount or endpoint change 필요성이 보이면 approval state를 기록한다.

## Rollback or Recovery

이 런북에 명시된 validation, restart, and Git-managed config rollback만 사용한다. Docker mount permission, exporter endpoint, OTLP port, high-cardinality relabel, or backend runtime 변경은 검증된 안전 복구 절차가 아니므로 `## Escalation`으로 이동한다.

## Escalation

verification이 실패하거나, secret exposure risk가 보이거나, Docker mount/endpoint/port 정책 변경이 필요하거나, 관찰된 상태가 예상 절차와 다르면 owning operator에게 escalation한다. 캡처한 evidence, 시도한 step, 현재 rollback/recovery 상태를 함께 제공한다.

## Related Documents

- [Operations index](../../README.md)
- [Usage guide](../../guides/06-observability/alloy.md)
- [Operations policy](../../policies/06-observability/alloy.md)
