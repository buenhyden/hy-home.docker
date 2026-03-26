# Pushgateway Runbook

: Metrics Buffer Management

---

## Overview (KR)

이 런북은 Pushgateway 운영 중 발생할 수 있는 주요 문제(데이터 오염, 메모리 부하, 전송 실패)에 대한 복구 및 관리 절차를 정의한다.

## Purpose

Pushgateway의 안정적인 메트릭 버퍼 상태를 유지하고, 비정상적인 메트릭 데이터를 정제하여 가시성 품질을 확보한다.

## Canonical References

- ARD: `[../../02.ard/06-observability.md](../../02.ard/06-observability.md)`
- Infrastructure: `[infra/06-observability/pushgateway/README.md](../../../infra/06-observability/pushgateway/README.md)`
- Operation: `[../../08.operations/06-observability/pushgateway.md](../../08.operations/06-observability/pushgateway.md)`

## When to Use

- Prometheus에서 Pushgateway 스크랩 실패 발생 시.
- 특정 배치 작업의 메트릭이 업데이트되지 않고 예전 값을 유지할 때 (Stale metrics).
- Pushgateway의 메모리 사용량이 비정상적으로 높을 때.

## Procedure or Checklist

### Checklist

- [ ] Pushgateway 컨테이너 상태 (`docker ps | grep pushgateway`)
- [ ] Traefik 라우팅 및 SSL 상태 (`https://pushgateway.local/-/ready`)
- [ ] Prometheus Scrape Target 상태

### Procedure

#### 1. 비정상 메트릭 그룹 삭제
메트릭이 오염되었거나 오래된 경우 특정 `job` 단위로 데이터를 삭제한다.

```bash
# 특정 job 삭제
curl -X DELETE http://pushgateway.local/metrics/job/stale_batch_job

# 특정 job 및 instance 삭제
curl -X DELETE http://pushgateway.local/metrics/job/stale_batch_job/instance/worker-01
```

#### 2. 서비스 재시작 (In-memory 초기화)
상태가 매우 불안정하거나 메모리 임계치에 도달한 경우 서비스를 재시작하여 버퍼를 완전히 초기화한다. (영구 저장소 설정이 없는 경우 데이터가 소실됨에 주의)

```bash
docker compose -f infra/06-observability/docker-compose.yml restart pushgateway
```

#### 3. 연결 테스트
작업 노드에서 Pushgateway로의 도달 가능성을 확인한다.

```bash
curl -I https://pushgateway.${DEFAULT_URL}/-/ready
```

## Verification Steps

- [ ] `curl http://pushgateway.local/metrics` 명령으로 현재 보관 중인 메트릭 목록 확인.
- [ ] Prometheus UI (`Targets`)에서 `pushgateway` 스크랩 상태가 `UP`인지 확인.

## Observability and Evidence Sources

- **Signals**: `pushgateway_http_requests_total`, `process_resident_memory_bytes`
- **Evidence to Capture**: `curl -s http://localhost:9091/metrics | grep <job_name>`

## Safe Rollback or Recovery Procedure

- 배치 작업의 메트릭 유실이 크리티컬한 경우, 작업 재실행(Retry)을 통해 메트릭을 다시 Push한다.
- Push가 계속 실패할 경우, 배치 작업 로그를 직접 분석하여 작업을 완료한다.

---

Copyright (c) 2026. Licensed under the MIT License.
