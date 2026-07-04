---
status: active
---
<!-- Target: docs/05.operations/guides/06-observability/pushgateway.md -->

# Pushgateway Usage Guide

## Usage

### Overview

이 문서는 Pushgateway의 역할과 기본 사용법을 설명한다. Pushgateway는 Prometheus pull 모델이 직접 적용되기 어려운 short-lived or batch job metric을 일시적으로 받아 두는 버퍼이며, 장기 실행 서비스의 일반 metric 수집 경로로 쓰지 않는다.

### Usage Type

`system-guide`

### Target Audience

- Developer
- Operator
- Agent-tuner

### Purpose

Pushgateway의 역할과 동작 방식을 이해하고, 배치 작업에서 메트릭을 올바르게 전송하고 관리하는 방법을 익힌다.

### Prerequisites

- `pushgateway` service가 `obs` profile에서 실행 중이어야 한다.
- 작업이 `infra_net` 또는 Pushgateway에 도달할 수 있는 네트워크 경로에 있어야 한다.
- Prometheus에 의존하는 dashboard or alert를 만들기 전에는 `prometheus.yml`의 Pushgateway scrape job 존재를 확인해야 한다.

### Step-by-step Instructions

#### 1. 서비스 도달성 확인

작업 위치에서 Pushgateway ready endpoint에 도달할 수 있는지 확인한다.

```bash
curl -I http://pushgateway:9091/-/ready
```

#### 2. 메트릭 전송

배치 작업 종료 시 또는 주기적으로 HTTP POST/PUT을 사용하여 metric을 push한다. 모든 path에는 안정적인 `job` label을 포함한다.

```bash
echo "batch_job_duration_seconds 120" | curl --data-binary @- http://pushgateway:9091/metrics/job/my_batch_job
```

고유 worker를 구분해야 할 때만 bounded `instance` label을 사용한다.

```bash
cat <<EOF | curl --data-binary @- http://pushgateway:9091/metrics/job/my_batch_job/instance/worker-01
# HELP batch_process_items Total items processed by batch.
# TYPE batch_process_items counter
batch_process_items 1500
EOF
```

#### 3. Prometheus scrape 연동 확인

Prometheus dashboard or alert가 Pushgateway metric에 의존하기 전에는 `prometheus.yml`에 Pushgateway scrape job이 있는지 확인한다. 현재 문서 정리 범위는 runtime 설정 변경이 아니므로, scrape job이 없으면 gap으로 기록하고 별도 작업에서 추가한다.

```bash
rg -n 'job_name: "pushgateway"|pushgateway:9091|honor_labels' infra/06-observability/prometheus/config/prometheus.yml
```

#### 4. 메트릭 삭제

Pushgateway는 수신된 메트릭을 명시적으로 삭제하기 전까지 계속 보관한다. 작업이 완전히 종료되거나 더 이상 유효하지 않은 인스턴스의 메트릭은 삭제 API를 호출해야 한다.

```bash
curl -X DELETE http://pushgateway:9091/metrics/job/my_batch_job
```

### Common Pitfalls

- **Stale metrics**: Pushgateway는 마지막 값을 유지한다. 실패한 배치가 metric을 갱신하지 못하면 오래된 성공 값이 계속 보일 수 있다.
- **Label collision**: 여러 worker가 같은 `job`만 사용하면 metric group이 덮어써질 수 있다. worker 구분이 필요할 때만 안정적인 `instance` label을 추가한다.
- **High cardinality**: user ID, request ID, unbounded build ID를 label에 넣으면 cleanup이 어려워지고 메모리 사용량이 커진다.
- **Scrape assumption**: Pushgateway service가 떠 있어도 Prometheus scrape job이 없으면 Prometheus target이나 alert에서 해당 metric을 볼 수 없다.

## Common Checks

- `docker compose -f infra/06-observability/docker-compose.yml --profile obs ps pushgateway`
- `curl -I http://pushgateway:9091/-/ready`
- `rg -n 'job_name: "pushgateway"|pushgateway:9091|honor_labels' infra/06-observability/prometheus/config/prometheus.yml`

## Runbook Handoff

반복 실행 절차, 장애 대응, rollback 또는 escalation 기준은 [recovery runbook](../../runbooks/06-observability/pushgateway.md)을 따른다.

## Related Documents

- [Operations index](../../README.md)
- [Operations policy](../../policies/06-observability/pushgateway.md)
- [Recovery runbook](../../runbooks/06-observability/pushgateway.md)
